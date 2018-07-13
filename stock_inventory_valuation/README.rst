.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===========================
Stock Inventory - Valuation
===========================

This module add simple valuation on stock inventories, based on standard_price
of each product.

A new computed field 'valuation' is added on stock.inventory and
stock.iventory.line models so as to be able to calculate the total valuation
of one inventory.

This module can be usefull when you don't use valuation by quants.

.. figure:: ./stock_inventory_valuation/static/description/stock_inventory_form.png
   :width: 800px

Known issues / Roadmap
======================

* the field ```valuation``` on ```stock.inventory.line``` is not designed
  correctly for the time being : It is a computed field, and should be a
  classical field with onchange. It is due to the dual API in odoo 8.0.
  When porting this module in version 10.0, should be refactored in normal
  field.

Contributors
------------

* Sylvain LE GAL (https://twitter.com/legalsylvain)

Funders
-------

The development of this module has been financially supported by:

* GRAP, Groupement Régional Alimentaire de Proximité (http://www.grap.coop)
