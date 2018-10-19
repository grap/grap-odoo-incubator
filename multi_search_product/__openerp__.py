# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Multi Search - Products',
    'version': '8.0.1.0.0',
    'category': 'Product',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'multi_search_abstract',
        'product',
    ],
    'data': [
        'views/view_base_config_settings.xml',
    ],
    'images': [
        'static/description/product_search.png',
        'static/description/setting_form.png',
    ],
    'installable': True,
}
