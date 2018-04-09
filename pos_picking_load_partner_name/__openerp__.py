# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Point of Sale - Load Picking by Partner Name improvment',
    'summary': "Improve load of picking in PoS by partner name",
    'version': '8.0.2.0.0',
    'category': 'Point of Sale',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'pos_picking_load',
    ],
    'pre_init_hook': 'pre_init_hook',
}
