.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

================================
Stock - Internal Use of products
================================

This module extends the functionality of stock and account module
to allow non accountant user to declare the use of stockable products for
specific uses (eg: gifts, tastings, etc.)

.. figure:: ./stock_internal_use_of_products/static/description/internal_use_form.png
   :width: 800 px


Configuration
=============

To configure this module, you need to:

* Go to Warehouse / Configuration / Internal Use Cases

.. figure:: ./stock_internal_use_of_products/static/description/internal_use_case_form.png
   :width: 800 px


Technical informations
----------------------

Confirming an internal_use will create:

* One stock.move for each internal_use.line between the 2 locations
  defined in the internal_use_case
* (One account.move per products defined in ```real_time``` inventory)
* One account.move to transfer the expense if accounting settings are
  defined in your internal use case.

Known issues / Roadmap
======================

This module is designed like inventory concept. (New module inventory and
inventory lines). We could consider replacing by native concept like replacing:

* ```internal.use.case``` by ```stock.picking.type```
* ```internal.use``` by ```stock.picking```
* ```internal.use.line``` by ```stock.move```

Credits
=======

Contributors
------------

* Julien WESTE
* Sylvain LE GAL (https://www.twitter.com/legalsylvain)

Do not contact contributors directly about support or help with technical issues.

Funders
-------

The development of this module has been financially supported by:

* GRAP, Groupement Régional Alimentaire de Proximité (http://www.grap.coop)
