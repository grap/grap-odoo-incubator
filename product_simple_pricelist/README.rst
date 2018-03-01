.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

==========================
Product - Simple Pricelist
==========================

This module extends the functionality of Pricelist Module to provide an
interface to easily change price per product, creating pricelist item for
each product.

It so add a boolean on pricelist "Is Simple". A wizard is available to edit
the "simple pricelist", that allow users, in an editable tree view, to set
price by product.

A "simple pricelist" has one and only one version.

Configuration
=============

To use this module, you need to go to Sale / Configuration / Pricelists

* Check the box simple pricelist on your desired pricelist

* click then on the edit button, available on the tree or the form view

.. figure:: /product_simple_pricelist/static/description/product_pricelist_tree.png
   :width: 800 px

* you can then edit easily change the price for a given product with the
  buttons in the end of each lines.

.. figure:: /product_simple_pricelist/static/description/simple_price_list_item.png
   :width: 800 px

* In the wizard, mention the new price you want to apply for this pricelist

.. figure:: /product_simple_pricelist/static/description/wizard_form.png
   :width: 800 px

* The according pricelist item will be created

.. figure:: /product_simple_pricelist/static/description/pricelist_item_form.png
   :width: 800 px

Roadmad / Issue
---------------

Create a simple pricelist without creating a version will fail.

Credits
=======

Contributors
------------

* Sylvain LE GAL (https://www.twitter.com/legalsylvain)

Funders
-------

The development of this module has been financially supported by:

* GRAP, Groupement Régional Alimentaire de Proximité (http://www.grap.coop)
