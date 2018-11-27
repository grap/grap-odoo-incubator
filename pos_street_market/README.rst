.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=============================
Point of Sale - Street Market
=============================

This module extends the functionality of point of sale to support saling
in the street using the point of sale and to allow you to mention on the
pos order, the place where the seller is for the time being.

Configuration
=============

To configure this module, you need to:

* Add your users to the new group 'Street Market Manager'

* Go to Point of Sale / Configuration / Point of Sales

* Check the box 'Market Place'

.. figure:: ../static/description/pos_config_form.png

Usage
=====

To use this module, you need to

* open the point of sale

* Click on 'Market Place' Button and select the place where you are

.. figure:: ../static/description/pos_front_end_ui.png

You can later make some statistics, filtering your sale by market places.


.. figure:: ../static/description/pos_order_search.png

Note
----

This module Add the possibility to change the date of a pos order, for
Street Market Manager members, because in some case, user will not have an
odoo instance during the sale, and will tip the PoS orders a few hours later or
a a few days later.

Credits
=======

Contributors
------------

* Sylvain LE GAL (https://www.twitter.com/legalsylvain)

Funders
-------

The development of this module has been financially supported by:

* GRAP, Groupement Régional Alimentaire de Proximité (http://www.grap.coop)
