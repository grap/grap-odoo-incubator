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

* Go to ...

.. figure:: path/to/local/image.png
   :alt: alternative description
   :width: 600 px

Usage
=====

To use this module, you need to:

* Go to ...


Known issues / Roadmap
======================

* ...

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


.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3
















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


Credits
=======

Icon
----

Icon is a merge of the Odoo Point of Sale icon and a checklist icon
available here : https://www.iconfinder.com/icons/379508/checklist_icon

Contributors
------------

* Sylvain LE GAL (https://twitter.com/legalsylvain)

Funders
-------

The development of this module has been financially supported by:

* GRAP, Groupement Régional Alimentaire de Proximité (http://www.grap.coop)
