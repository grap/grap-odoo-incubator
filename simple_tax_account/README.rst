.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3


=================================================
Easy Switch between VAT Excluded and VAT Included
=================================================

Use case
--------

This module is useful in the following case:

* Odoo is implemented in a country with simple Taxes system, (Like in France)
  with generaly only one Tax type='percent'. (VAT)
* Users define allways product price with VAT included. (or allways excluded)
* Some customers / suppliers wants quotation / invoices with the other system

Technical Information
---------------------

* On account.tax, add a new field 'simple_tax_id' that is the according tax
  with or without tax included. Sample:
    * TAX A: VAT 10% included
    * TAX B : VAT 10% excluded
    * TAX A and TAX B will be linked together

.. image:: /simple_tax_account/static/description/tax_setting.png

* On res.partner, add a new field selection 'simple_tax_type' with
  the following values:
    * 'none' : (default) undefined, the Tax will be the tax of the product
    * 'excluded': All price will be recomputed with Tax excluded
    * 'included': All price will be recomputed with Tax inluded

.. image:: /simple_tax_account/static/description/partner_setting.png

* Possibility to switch between Price VAT Included and Price VAT Excluded
  when editing a Account Invoice

** Invoices with Mixed Taxes**

.. image:: /simple_tax_account/static/description/invoice_harmonized_taxes.png

** Invoices with Harmonized Taxes**

.. image:: /simple_tax_account/static/description/invoice_mixed_taxes.png

* on account.tax.template, add a new field 'simple_template_id' that is
  the according template with of without tax included.

.. image:: /simple_tax_account/static/description/tax_template_setting.png

Related Modules
---------------

* This following modules provide the same behouviour:
    * 'simple_tax_sale' for sale module;
    * 'simple_tax_purchase' for purchase module;

Credits
=======

Contributors
------------

* Sylvain LE GAL <https://twitter.com/legalsylvain>
