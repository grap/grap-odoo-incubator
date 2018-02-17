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

.. figure:: pos_street_market/static/description/pos_config_form.png
   :width: 800 px

Usage
=====

To use this module, you need to

* open the point of sale

* Click on 'Market Place' Button and select the place where you are

.. figure:: pos_street_market/static/description/pos_front_end_ui.png
   :width: 800 px

You can later make some statistics, filtering your sale by market places.


.. figure:: pos_street_market/static/description/pos_order_search.png
   :width: 800 px

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













.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

Add some feature for users who sale in street
=============================================

Features
--------
* Add a market place object;
    * a PoS has now an extra field 'market_place_id' that mentions where the
      sale has been done;
    * Possibility to select a Market place in Front Office or in Back Office;


Screenshots
-----------
* New popUp to select Market Place In PoS Front End

.. image:: /pos_street_market/static/description/screenshot_front_end_ui.png

* Possibility to search or filter by market place

.. image:: /pos_street_market/static/description/screenshot_back_office_search.png

Roadmap / Limits
----------------
* Could be great to have some graphical reporting like evolution of PoS sale
  depending of market places;

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/grap/odoo-addons-misc/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/grap/odoo-addons-misc/issues/new?body=module:%20pos_street_market%0Aversion:%208.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


Credits
=======

Contributors
------------

* Sylvain LE GAL (https://twitter.com/legalsylvain);
