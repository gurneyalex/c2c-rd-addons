# -*- coding: utf-8 -*-
{ "name"         : "Account Moves Igel"
, "version"      : "1.0"
, "author"       : "Camptocamp"
, "website"      : "http://www.camptocamp.com"
, "description"  : """Import table for account move lines of Igel"""
, "category"     : "Client Modules/ChriCar Addons"
, "depends"      : ["account"]
, "init_xml"     : []
, "demo_xml"     : []
, "update_xml"   : 
    [ "account_move_line_igel_view.xml"
    , "wizard/moves_igel_view.xml"
    , "security/rule.xml","security/ir.model.access.csv"
    ]
, "auto_install" : False
, "installable"  : True
}

