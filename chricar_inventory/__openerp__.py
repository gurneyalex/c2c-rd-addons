{ "name"         : "Inventory"
, "version"      : "0.1"
, "author"       : "Camptocamp"
, "website"      : "http://www.camptocamp.com"
, "description"  : """Easy first time import of office/home Inventory from Spreadsheet (CSV)
generated 2009-02-11 16:03:53+01"""
, "category"     : "Client Modules"
, "depends"      : ["stock","chricar_top"]
, "init_xml"     : []
, "demo_xml"     : []
, "update_xml"   : 
    [ "inventory_view.xml"
    , "security/group.xml"
    , "security/ir.model.access.csv"
    ]
, "auto_install" : False
, "installable"  : True
}
