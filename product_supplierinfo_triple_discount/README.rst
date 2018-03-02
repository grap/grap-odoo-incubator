.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

=========================================
Triple Discounts in product supplier info
=========================================

This module allows to put three discounts in the supplier info form, and
propagate it to purchase orders, having two advantages over pricelists:

* The discount is directly put on purchase orders instead of reducing the
  unit price.
* You can set prices and discounts on the same screen.

Configuration
=============

To see prices and discounts on supplier info view, you have to enable the
option "Manage pricelist per supplier" inside *Configuration > Purchases*

Usage
=====

Go to Purchase > Products, open one product, and edit or add a record on the
*Suppliers* section of the *Procurements*. You will see in the prices section
in the down part three columns *Discount (%)*. You can enter here
the desired discounts for that quantity.

When you make a purchase order for that supplier and that product, discounts
will be put automatically.

Known issues / Roadmap
======================

* The discount is always applied, independently if you have based
  your pricelist on other value than "Supplier Prices on the product form".

Credits
=======

Contributors
------------

* Sylvain LE GAL (https://www.twitter.com/legalsylvain)
* Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>

Do not contact contributors directly about support or help with technical issues.

Funders
-------

The development of this module has been financially supported by:

* GRAP, Groupement Régional Alimentaire de Proximité (http://www.grap.coop)
