This module is a module to analyze and provides tools to help purchasers
to change Odoo supplier invoices when they receives the invoice from the supplier.

It is helpull in the following Use Case:

- You create purchase orders with many lines in Odoo. (and send to your supplier)
- you receive products and changes quantities in some picking lines when you receive the goods.
- you generate a draft supplier invoice, based on the products you receiveds.

- Then you have to compare the draft theoritical invoice with the real supplier invoice
  and apply changes in the theoritical invoice to match with the real supplier invoice.

**Reflections regarding community work**

This module is an alternative to OCA modules, mainly ``account_invoice_import_invoice2data``.
The reasons of the development of a specific module are the following :

- To use the OCA solution, we need to install 9 modules for a total of 2500 lines of code.
  ``account_invoice_import``, ``account_invoice_import_invoice2data``, ``unece``, etc...
  while this module contains less than 300 lines of python code.

- The current invoice2data OCA modules doesn't handle line analysis. A Work In Progress
  is present since April 2022 here https://github.com/OCA/edi/ for the V14 version.
  It is unmerged, not available for GRAP branches (V12 / V16) and doesn't handle multiple
  discounts.

- The OCA wizard is very complex, because it handles a lot of use cases, while the
  wizard of this module is very simple and handles all the use cases of the workflow
  "Update the odoo invoice, based on supplier invoice".

+-----------------------+---------------------+-----------------------------------------+
| **Managed Suppliers**                                                                 |
+-----------------------+---------------------+-----------------------------------------+
| Supplier Name         |  VAT Number         |  Website                                |
+=======================+=====================+=========================================+
|  Relais Vert          |  FR 72 352 867 493  |  https://www.relais-vert.com/           |
|  Ekibio               |  FR 30 345 052 286  |  https://www.ekibio.fr/                 |
+-----------------------+---------------------+-----------------------------------------+


.. list-table:: **Managed Suppliers**
   * - Supplier Name
     - VAT Number
     - Website
   * - Relais Vert
     - FR 72 352 867 493
     - https://www.relais-vert.com/
   * - Ekibio
     - FR 30 345 052 286
     - https://www.ekibio.fr/
