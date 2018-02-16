.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

================================
Stock - Internal Use of products
================================

This module extends the functionality of stock and account module
to allow non accountant user to declare the use of stockable products for
specific uses (eg: gifts, tastings, etc.)

Features
--------

* add a 'Internal Use' menu to register such uses
* add a 'Internal Use Line' menu mostly for reporting purposes

Technical informations
----------------------

* add a 'Internal Use Case' menu to configure the internal use
  possibilities
* for each internal_use_case, you need to define an inventory-type
  stock_location

* Confirming an internal_use will create
    * 1 stock.picking
    * 1 stock.move for each internal_use.line between the 2 locations
      defined in the internal_use_case
    * (1 account.move if your products are defined in real_time inventory)
    * 1 account.move to transfer the expense


Installation
============

To install this module, you need to:

* Do this ...

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
