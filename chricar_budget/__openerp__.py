# -*- coding: utf-8 -*-
{ "name"         : "Budget Products"
, "version"      : "1.0"
, "author"       : "ChriCar Beteiligungs- und Beratungs- GmbH,Odoo Community Association (OCA)"
, "website"      : "http://www.chricar.at/ChriCar"
, "description"  : """Allows to plan production and sales quantities for products sales prices
generated 2009-08-18 23:44:30+02"""
, "category"     : "Client Modules/ChriCar Addons"
, "depends"      : 
    [ "product"
    , "picking_invoice_rel"
    , "c2c_budget_chricar"
    , "c2c_product_price_unit"
    , "one2many_sorted"
    , "chricar_stocklocation_moves"
    ]
, "init_xml"     : ["mig_budget_init.xml"]
, "demo"         : []
, "update_xml"   : ["budget_view.xml","security/ir.model.access.csv"]
, "auto_install" : False
, "installable"  : True
, 'application'  : False
}
