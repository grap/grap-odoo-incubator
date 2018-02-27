.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

====================================================
Duplication Tool for Invoices with a given frequency
====================================================

This module extends the functionality of Account Module to provide a wizard to
duplicate a given Account Invoite.

User can define:

* a begin date
* a frequency (week, ...)
* a recurring quantity
* a duration for the due date

Usage
=====

To use this module, you need to

* go to Invoices / (Customer / Supplier ) Invoices

* Select any invoice and click on 'More' / 'Duplication Wizard'

.. figure:: /duplication_sale_order/static/description/account_invoice_duplication_wizard_form.png
   :width: 800 px

Known issues / Roadmap
======================

Change the field due_date_duration in the wizard by the selection of a
``account.payment.term``

Credits
=======

Contributors
------------

* Sylvain LE GAL (https://www.twitter.com/legalsylvain)

Funders
-------

The development of this module has been financially supported by:

* GRAP, Groupement Régional Alimentaire de Proximité (http://www.grap.coop)
