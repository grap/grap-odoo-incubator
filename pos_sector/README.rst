.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=======================
Point of Sale - Sectors
=======================

This module extends the functionality of point of sale to support product
sectors restricting products display in the Point of Sale, depending of the
product sectors.

This module can be interesting if some cashiers have the right to sell
some products, and not other cashiers.


Configuration
=============

To configure this module, you need to:

* Go to Point of Sale / Configuration / Sectors

* Create your PoS Sectors

.. figure:: /pos_sector/static/description/pos_sector_tree.png
   :width: 800 px

* Open your Point Of Sale configurations and set sectors

.. figure:: /pos_sector/static/description/pos_config_form.png
   :width: 800 px

* Finally, edit your products and set a sector

.. figure:: /pos_sector/static/description/product_form.png
   :width: 800 px

Usage
=====

To use this module, you need to

* open the point of sale

the products displayed will belong to the sectors of the current PoS config.
(Also the products without sectors will be displayed)

Credits
=======

Contributors
------------

* Sylvain LE GAL (https://www.twitter.com/legalsylvain)

Funders
-------

The development of this module has been financially supported by:

* GRAP, Groupement Régional Alimentaire de Proximité (http://www.grap.coop)
