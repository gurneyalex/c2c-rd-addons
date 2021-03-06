# -*- coding: utf-8 -*-
##############################################
#
# Swing Entwicklung betrieblicher Informationssysteme GmbH
# (<http://www.swing-system.com>)
# Copyright (C) ChriCar Beteiligungs- und Beratungs- GmbH
# all rights reserved
#    08-JUN-2012 (GK) created
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs.
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contract a Free Software
# Service Company.
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/> or
# write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA  02111-1.17, USA.
#
###############################################
from osv import osv, fields
import logging
from tools.translate import _


class payment_order_create(osv.osv_memory):
    _inherit     = 'payment.order.create'

    _columns     = \
        { 'balance_filter' : fields.boolean
            ( 'Only partners with total liability'
            , help='Will select only partners with a debit-credit < 0 regardless of due date.'
            )
        , 'min_balance'    : fields.float 
            ( 'Minimum Total Amount Due'
            , help="Will select only partners with total payment balance greater than this amount."
            )
        }

    def _get_min_balance_default(self, cr, uid, context=None):
        _logger = logging.getLogger(__name__)
        _logger.info('FGF pay min_balance context %s' % (context))
        min_balance = 0
        order_obj = self.pool.get('payment.order')
        for order in order_obj.browse(cr, uid, [ context['active_id'] ]):
            min_balance = order.mode.amount_partner_min
        return min_balance


    _defaults    = \
        { 'balance_filter' : lambda *a: True
        , 'min_balance'    : _get_min_balance_default
        }

    def search_entries(self, cr, uid, ids, context=None):
        _logger = logging.getLogger(__name__)
        if context is None : context = {}
        order_obj = self.pool.get('payment.order')
        line_obj  = self.pool.get('account.move.line')
        invoice_obj  = self.pool.get('account.invoice')
        mod_obj   = self.pool.get('ir.model.data')
        obj       = self.browse(cr, uid, ids, context=context)[0]
        payment   = order_obj.browse(cr, uid, context['active_id'], context=context)
        company_id = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.id
        domain    = \
            [ ('reconcile_id', '=', False)
            , ('account_id.type', '=', 'payable')
            , ('company_id', '=', company_id)
            , ('partner_id', '!=', False) # must be there in case there are imported lines without partner_id (Deloitte)
            , ('state', '=', 'valid')
            # , ('amount_to_pay', '>', 0) # see later in if statements
            ]
        domain   += \
            [ '|'
            , ('date_maturity', '<=', obj.duedate)
            , ('date_maturity', '=', False)
            ]
        _logger.info('FGF pay line domain %s' % (domain))
        _logger.info('FGF pay line context %s' % (context))
        ids = line_obj.search(cr, uid, domain, context=context)
        ids2 = ','.join(map(str,ids))
        sql = """select partner_id, round(sum(debit-credit),2) as balance
                   from account_move_line
                  where id in (%s)
                  group by partner_id""" % (ids2)
        cr.execute(sql)
        partner_balances = dict(cr.fetchall())
        precision = self.pool.get('decimal.precision').precision_get(cr, uid, 'Account')
        _logger.info('FGF partner_balance %s' % (partner_balances))

        _logger.info('FGF pay line ids %s' % (ids))
        line_ids = []
        for line in line_obj.browse(cr, uid, ids) :
            _logger.info('FGF line %s %s ' % (line.id, line.partner_id.name))
            _logger.info('FGF pay block %s' % (line.invoice.payment_block))
            if line.invoice.payment_block : continue
            _logger.info('FGF pay partner block %s' % (line.partner_id.payment_block))
            if line.partner_id.payment_block : continue
            # FGF its crazy : 
            #  partner_id.credit always returns 0
            #  partner_id.debit :
            #     positive: credit
            #     negative: debit 
            # https://bugs.launchpad.net/openobject-addons/+bug/1066066
            partner_balance = -line.partner_id.debit

            # check  balance  of records due for this payment order
            #sql = """select sum(debit-credit)
            #           from account_move_line
            #          where partner_id = %s
            #            and id in (%s)""" % (line.partner_id.id, ids2)
            #cr.execute(sql)
            #res = cr.fetchone()
            #balance_to_pay = res and -res[0] or 0
            balance_to_pay = -round(partner_balances[line.partner_id.id],precision)

            _logger.info('FGF pay partner balance %s amount to pay %s balance_to_pay %s Obey %s' % (partner_balance, line.amount_to_pay, balance_to_pay, line.partner_id.payment_obey_balance ))
            if (line.partner_id.payment_obey_balance 
                and obj.balance_filter 
                and (-partner_balance < obj.min_balance 
                or balance_to_pay < obj.min_balance) ) : continue 
            elif not line.amount_to_pay > 0: continue
                
            _logger.info('FGF pay bank invoice %s, partner %s' % (line.invoice.partner_bank_id, line.invoice and line.invoice.partner_id.bank_ids ))
            if (line.invoice and not line.invoice.partner_bank_id):
                if not line.invoice.partner_id.bank_ids and payment.mode.require_bank_account : 
                    continue
                else:
                    if line.invoice.partner_id.bank_ids :
                        vals = {'partner_bank_id' : line.invoice.partner_id.bank_ids[0].id}
                        invoice_obj.write(cr, uid, line.invoice.id, vals)
                    else :
                        raise osv.except_osv \
                            ( _('Data model error ! !')
                            , _('Partner %s has no bank account information') % line.invoice.partner_id.name
                            )
            _logger.info('FGF ACCEPTED %s' % (line.id))
            line_ids.append(line.id)
        _logger.info('FGF line_ids %s' % (line_ids))
# End search modification

# 

        context.update({'line_ids': line_ids})
        model_data_ids = mod_obj.search(cr, uid,[('model', '=', 'ir.ui.view'), ('name', '=', 'view_create_payment_order_lines')], context=context)
        resource_id = mod_obj.read(cr, uid, model_data_ids, fields=['res_id'], context=context)[0]['res_id']
        return {'name': ('Entry Lines'),
                'context': context,
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'payment.order.create',
                'views': [(resource_id,'form')],
                'type': 'ir.actions.act_window',
                'target': 'new',
        }

payment_order_create()
