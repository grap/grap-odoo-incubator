# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Street Market module for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Point of Sale - Street Market',
    'version': '8.0.1.1.0',
    'category': 'Point of Sale',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'point_of_sale',
    ],
    'data': [
        'security/ir_rule.xml',
        'security/res_groups.yml',
        'security/ir_model_access.yml',
        'view/include.xml',
        'view/view.xml',
        'view/action.xml',
        'view/menu.xml',
    ],
    'qweb': [
        'static/src/xml/pos_street_market.xml',
    ],
    'demo': [
        'demo/res_groups.yml',
        'demo/market_place.yml',
    ],
}
