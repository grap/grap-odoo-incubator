.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

===================================
Sale - Handle Recurring Consignment
===================================

For more information about consigment see:
https://en.wikipedia.org/wiki/Consignment

This module manage recurring consignment: A product will allways be provided
by the same consignor and can not be provided by another way.

For other implementation of consigment you could see:

* (vendor_consignment_stock)[https://github.com/OCA/purchase-workflow];


Functionality
-------------

TODO :
- basic user can only change location and email.
Partner Model

* Add a 'is_consignor' field on Partner;

Product Model

* Add a consignor_partner_id field (res.partner), indicating which partner
  provide the product;
* if consignor_partner_id is defined:
    * The product can not have seller_ids defined;
    * The product has a special VAT defined;

TODO :

- Ajouter le justificatif de commission dans le mail à envoyer.
  (surcharger account.invoice ?)

- Ajouter blocage dans product. Interdire le changement de consignor, si
  il y a un stock move associé au produit.
  
- Créer nouveau module:
    * recurring_consignment_sale_margin
    * recurring_consignment_invoice_margin
    * recurring_consignment_pos_margin

--> Surcharger le get du standard_price, pour avoir 



This module extends the functionality of ... to support ...
and to allow you to ...

Installation
============

To install this module, you need to:

#. Do this ...

Configuration
=============

To configure this module, you need to:

* Go to ...

.. figure:: /path/to/local/image.png
   :width: 800 px

Usage
=====

To use this module, you need to:

* Go to ...

Known issues / Roadmap
======================

* OK : Make impossible to unset / set **is_consignor** to a partner if it has been set.
* Make impossible to unset / set **consignor_partner_id** to a product if sale / purchase is done.
* Add a boolean an product to mention that the product is used for commission
* forbid that invoices have commission and non commission in lines
  in the same times.


* Try to fix account_invoice.py (french sentences)
* Check if account_voucher.py is still required
* Add test
* To fix noupdate = 0/1.
* 

* General Check

V10 Roadmap
===========

* Full new API should let possible to remove duplicated code in
  product_product.py and product_template.py files. (on change system)

Credits
=======

Contributors
------------

* Sylvain LE GAL <https://twitter.com/legalsylvain>

Funders
-------

* GRAP, Groupement Régional Alimentaire de Proximité <http://www.grap.coop>
