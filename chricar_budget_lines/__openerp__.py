# -*- coding: utf-8 -*-
{ "name"         : "Budget Products Lines"
, "version"      : "1.0"
, "author"       : "Camptocamp"
, "website"      : "http://www.camptocamp.com"
, "description"  : """Allows to plan details for product budgets
generated 2009-08-21 15:12:07+02"""
, "category"     : "Client Modules/ChriCar Addons"
, "depends"      : 
    [ "chricar_budget"
    , "mrp"
    , "stock"
    , "account"
    , "chricar_view_id"
    , "chricar_partner_parent_companies"
    , "c2c_product_price_unit"
    ]
, "init_xml"     : []
, "demo_xml"     : []
, "update_xml"   : ["budget_lines_view.xml"]
, "auto_install" : False
, "installable"  : True
}
