.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3


====================
POS Load Done Orders
====================


This module extends the functionality of point of sale to allow you to
load again a done PoS Order in the point of sale to make extra operation on it.

For the time being, only the reprint of the bill is allowed.

Configuration
=============

To configure this module, you need to:

* Go to Point of Sale / Configuration / Point of Sale
* check the box Load Done Orders
* Optionnaly, change the value of the max done orders to load field.

.. figure:: /pos_done_order_load/static/description/pos_config_form.png

Usage
=====

To use this module, you need to:

* Launch the point of sale

* Click on the new button 'Load Done Orders'

.. figure:: /pos_done_order_load/static/description/pos_load_done_order_button.png

* the list of the last previous done orders are displayed.

* You can perform a research by name or PoS Reference field in the search box

* At the end of the line, buttons are available to make extra actions

.. figure:: /pos_done_order_load/static/description/pos_done_order_list.png
   :width: 800 px


Known issues / Roadmap
======================

* For a reason of cached data, it is only possible to reprint an order of
  the current session. Printing older orders could be possible if we load
  previous statements.

* It could be great to add an other button 'Refund' to create an refund order
  directly in the Point of Sale.

* It could be great to add an other button 'Invoice' to create have the
  possibility to reedit the invoice.

Credits
=======

Contributors
------------

* Sylvain LE GAL (https://www.twitter.com/legalsylvain)

Funders
-------

The development of this module has been financially supported by:

* GRAP, Groupement Régional Alimentaire de Proximité (http://www.grap.coop)
