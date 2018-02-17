.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==========================================================
Allow the cash control on all cash registers for a session
==========================================================

It's now allowed to control all the payment method when user open or close
his session.

Functionnality
--------------

* Disable constrains on number of journals with cash control enabled,
  on pos config.


TODO : 
rename table pos.cash.controls -> pos_cash_control
dans pos_cash_control. 
pos_session_id -> session_id
cash_register_id -> statement_id


Contributors
------------

* Sylvain LE GAL (https://twitter.com/legalsylvain)

Funders
-------

The development of this module has been financially supported by:

* GRAP, Groupement Régional Alimentaire de Proximité (http://www.grap.coop)
