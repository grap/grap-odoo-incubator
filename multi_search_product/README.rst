.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=======================
Multi Search - Products
=======================

This module slighly changes the product search function to allow multi words
search, usefull when you have a lot of products.

The order of the words you type doesn't matter.

Configuration
=============

* Go to 'Settings / Configuration / General Settings'

* Choose the character that will be used to allow a search with multiple words

.. figure:: https://raw.githubusercontent.com/grap/odoo-addons-misc/8.0/multi_search_product/static/description/setting_form.png
   :width: 80 %
   :align: center

Important Note
--------------

When you do this settings, a process will remove this char from all your
products in the field ```name``` and ```default_code```.

Usage
=====

If a user make a search with the following entry ```dis*ret```, it will
find products named "Ipad **Ret** ina **Dis** play"

.. figure:: https://raw.githubusercontent.com/grap/odoo-addons-misc/8.0/multi_search_product/static/description/product_search.png
   :width: 80 %
   :align: center

Credits
=======

Contributors
------------

* Sylvain LE GAL <https://twitter.com/legalsylvain>
* Julien WESTE

Funders
-------

The development of this module has been financially supported by:

* GRAP, Groupement Régional Alimentaire de Proximité (http://www.grap.coop)
