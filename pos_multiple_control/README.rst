.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=====================================
Point Of Sale - Multiple Cash Control
=====================================

This module extends the functionality of point of sale and to support
improved control during the close of the session.

* Allow user to control each statement. (not only the cash statement,
  by default)

.. figure:: pos_multiple_control/static/description/pos_session_closing_form.png
   :width: 800 px

* User should set the closing balance for all the statements

.. figure:: pos_multiple_control/static/description/account_bank_statement_piece_form.png
   :width: 800 px

* User can access to the summary by payment methods for each statement

.. figure:: pos_multiple_control/static/description/account_bank_statement_summary_form.png
   :width: 800 px

* So that, force user to have correct balance on each statement. If not,
  user should have to set Profit or Loss reason, using the OCA module
  ``pos_cash_move_reason``

* As the check is more complete, allow user to reopen a new session, if the
  first one is in a closing state.

Extra checks are done, to prevent user errors:

* It is not possible to click on the button 'Close Session' if there are some
  draft orders.

Configuration
=============

To configure this module, you need to:

* Go to Invoicing / Configuration / Journals / Journals

* Check the box 'Bank and Checks Control' if you want to enable this feature
  for this journal
  
.. figure:: pos_multiple_control/static/description/account_journal_bank_setting.png
   :width: 800 px

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
