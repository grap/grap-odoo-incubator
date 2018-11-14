.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=========================
Point Of Sale - Invoicing
=========================

When you pay a pos_order, and then create an invoice :

* you mustn't register a payment against the invoice as the payment
  already exists in POS;
* The POS payment will be reconciled with the invoice when the session
  is closed.
* You mustn't modify the invoice because the amount could become
  different from the one registered in POS. Thus we have to
  automatically validate the created invoice.

Functionality
-------------
About the invoices created from POS after payment:
* automatically validate them and don't allow modifications;
* Disable the Pay Button;
* Don't display them in the Customer Payment tool;

Technically
-----------

add a ```pos_pending_payment``` field on the ```account.invoice``` to mark the
items that shouldn't be paid.

.. figure:: /pos_invoicing/static/description/account_invoice_form.png

Roadmap / Known Issues
======================

* This module reconcile invoiced orders only if a customer has one invoice per
  session.

* It should be great to use the OCA module ```pos_autoreconcile```.

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
