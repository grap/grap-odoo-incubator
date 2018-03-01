# -*- encoding: utf-8 -*-
##############################################################################
#
#    Product - Simple Pricelist module for Odoo
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
    'name': 'Product - Simple Pricelist',
    'summary': 'Provides Wizard to manage easily Pricelist By Products',
    'version': '0.1',
    'category': 'Product',
    'description': """
Provides Wizard to manage easily Pricelist By Products
======================================================

Functionality:
--------------
    * A pricelist has now a new boolean field : simple_pricelist, that indicate
      that user can use a wizard to edit the pricelist by product;
      An "simple pricelist" has one and only one version;
    * An "simple pricelist" has one item based on product;
    * A wizard is available to edit the "simple pricelist", that allow users,
      in an editable tree view, to set price by product;

Roadmad / Issue
---------------

create a simple pricelist should be more intuitive or more documented.
Create a simple pricelist without creating a version will fail)

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
    ],
    'data': [
        'security/ir_rule.yml',
        'security/ir_model_access.yml',
        'view/view.xml',
        'view/action.xml',
    ],
    'installable': True,
}
