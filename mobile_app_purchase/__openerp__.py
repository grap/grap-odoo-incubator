# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Scan To Purchase',
    'version': '1.0',
    'category': 'Purchase',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'purchase',
        'stock',
    ],
    'data': [
        'views/view_res_company.xml',
    ],
    'demo': [
        'demo/res_groups.yml',
        'demo/product_product.yml',
    ],
    'installable': True,
}
