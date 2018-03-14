# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: GRAP (<http://www.grap.coop>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'GRAP - Print Product',
    'summary': 'Possibility to print EAN13 product',
    'version': '0.1',
    'category': 'Custom',
    'description': """
Possibility to print product information
========================================

Functionality
-------------

* Possibility to generate EAN13 code;
* Possibility to print ean13 codes;

Limits / Roadmap
----------------

* create differente model;
    * create model product.print.type:
        * margin_top;
        * margin_left;
        * inner_margin_top;
        * inner_margin_left;
        * row_qty;
        * column_qty;
        * width;
        * height;


* after V8 migration and CRB integration,
  merge odoo-addons-misc/grap_print_product
  and odoo-addons-grap/grap_change_print

Copyright, Authors and Licence
------------------------------

* Copyright: 2015, GRAP: Groupement Régional Alimentaire de Proximité;
* Author:
    * Sylvain LE GAL (https://twitter.com/legalsylvain);
* Licence: AGPL-3 (http://www.gnu.org/licenses/);""",
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'product',
        'report_webkit',
    ],
    'data': [
        'security/res_groups.yml',
        'security/ir_model_access.yml',
        'security/ir_rule.xml',
        'report/print_product_1_report.xml',
        'views/print_product_type_view.xml',
        'views/print_product_wizard_view.xml',
        'views/action.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/res_groups.yml',
    ],
    'external_dependencies': {
        'python': ['cairosvg', 'barcode'],
        'bin': ['wkhtmltopdf'],
    },
}
