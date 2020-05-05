# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Mobile App Purchase R&D',
    'version': "12.0.1.0.0",
    'author': 'GRAP',
    'summary': "Mobile App Purchase R&D",
    'category': 'Tools',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'purchase',
    ],
    'data': [
        "views/menu.xml",
        "views/templates.xml",
        "views/view_product_product.xml",
    ],
    'qweb': [
        "static/src/xml/kiosk_mode.xml",
    ],
    'installable': True,
}
