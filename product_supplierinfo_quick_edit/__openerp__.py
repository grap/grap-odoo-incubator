# -*- encoding: utf-8 -*-
##############################################################################
#
#    Product - Supplier Info Quick Edit module for Odoo
#    Copyright (C) 2015-Today GRAP (http://www.grap.coop)
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
    'name': 'Product - Supplier Info Quick Edit',
    'summary': 'Provides Wizard to manage easily Supplierinfo',
    'version': '8.0.3.0.0',
    'category': 'Product',
    'description': """
Provides Wizard to manage easily Supplierinfo
=============================================

* Display a tree and editable view to edit quickly supplier info;
    * possibility to update very quickly if there is only one line in
      pricelist_ids;
    * Possibility to see and update lines if there are many pricelist_ids;

* Display on partner form and kanban view, the quantity of products supplied
  by the partner and a link to see the products;

* Possibility to select various products to create quickly a new draft purchase
  order;

TODO : add edition in line on template view. disable possibility to have
many pricelist_ids. (that will could be reintroduced in V10.)

Copyright, Authors and Licence:
-------------------------------
    * Copyright: 2015, GRAP: Groupement Régional Alimentaire de Proximité;
    * Author:
        * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence: AGPL-3 (http://www.gnu.org/licenses/);""",
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'product',
        'purchase',
        'product_supplierinfo_discount',
        'product_supplierinfo_triple_discount',
    ],
    'data': [
        'view/view_product_supplierinfo_create_purchase_order.xml',
        'view/view_product_supplierinfo.xml',
        'view/action.xml',
        'view/view_res_partner.xml',
        'view/menu.xml',
    ],
    'demo': [
        'demo/res_groups.yml',
    ],
    'installable': True,
}
