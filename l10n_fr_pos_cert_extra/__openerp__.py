# -*- coding: utf-8 -*-
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# Copyright (C) 2017 - Today: Akretion (http://www.akretion.com)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Extra - French Certification (Point of Sale)",
    "summary": "Certification for Point of Sale Module",
    "version": "8.0.1.0.0",
    "category": "Point Of sale",
    "author": "GRAP",
    "license": "AGPL-3",
    "depends": [
        "l10n_fr_pos_cert",
    ],
    "data": [
        "views/view_pos_order.xml",
        "views/view_pos_config.xml",
        "views/templates.xml",
    ],
    'qweb': [
        'static/src/xml/l10n_fr_pos_cert_extra.xml',
    ],
    "demo": [
    ],
    'installable': False,
}
