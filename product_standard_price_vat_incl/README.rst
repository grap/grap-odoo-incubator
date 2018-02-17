.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=====================================
Product - Standard Price VAT Included
=====================================

This module brings a standard Price with VAT Included.

This module is interesting in the following case:
    * You use VAT With Price Included;
    * You want to create price list based on standard Price;

Without this module, the sale price (with a price list based on standard price)
will be bad, because the VAT will be not correctly computed.

This module so add a new field ```standard_price_vat_incl``` on product
model.

.. figure:: /product_standard_price_vat_incl/static/description/product_form.png
   :width: 800 px

It is possible to base a pricelist on this new field.

.. figure:: /product_standard_price_vat_incl/static/description/pricelist_version_form.png
   :width: 800 px


Credits
=======

Contributors
------------

* Sylvain LE GAL (https://www.twitter.com/legalsylvain)

Funders
-------

The development of this module has been financially supported by:

* GRAP, Groupement Régional Alimentaire de Proximité (http://www.grap.coop)
