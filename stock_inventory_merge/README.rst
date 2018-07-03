.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=========================
Stock - Merge Inventories
=========================


This module extends the functionality of Stock Module to support the
possibility to create many little inventories to merge, to have the possibility
to make complete inventory in Odoo.

This module is usefull in a context when you have a lot of products, and you
will physicaly organize your inventory process, making a lot of partial
inventory.

In that case, with this module, the classical process is :

* Make a lot of partial inventories;
* Merge all the partial inventories into a single one;
* Check if there are duplicates and fix the situation. (change a line, or sum
  the lines because a product can be in many places.)
* Fill your inventory with all the products you didn't inventoried with
  a zero quantity.

Main Features
=============

* Disable the constrains that makes impossible to have two pending inventories
  with the same product.

.. figure:: https://raw.githubusercontent.com/grap/grap-odoo-incubator/8.0/stock_inventory_merge/static/description/stock_inventory_disabled_warning.png

* So, a new smart button is available to see the duplicates, into an pending
  inventory, and a button allow users to merge duplicates. In that case,
  the quantities will be sumed.

.. figure:: https://raw.githubusercontent.com/grap/grap-odoo-incubator/8.0/stock_inventory_merge/static/description/stock_inventory_form_duplicate.png
   :width: 1024 px

* Add an action to have the possibility to merge many inventories.
  that wizard will create a new inventories, based on the little ones.

.. figure:: https://raw.githubusercontent.com/grap/grap-odoo-incubator/8.0/stock_inventory_merge/static/description/stock_inventory_tree_merge.png

* An option is available to fill an inventory with the missing products that
  are not listed in the inventory lines.

.. figure:: https://raw.githubusercontent.com/grap/grap-odoo-incubator/8.0/stock_inventory_merge/static/description/stock_inventory_form_complete_zero.png

Credits
=======

Contributors
------------

* Sylvain LE GAL <https://twitter.com/legalsylvain>

Funders
-------

* GRAP, Groupement Régional Alimentaire de Proximité <http://www.grap.coop>
