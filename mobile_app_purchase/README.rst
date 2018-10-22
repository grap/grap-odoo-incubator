.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3


===========================================================================
Provide light Web app to scan products Barcode and generate Purchase Orders
===========================================================================

This module was written to extend the functionality of odoo Purchase module.

This module provides a web app designed to work on a Mobile. The app allows
user to scan products and select a quantity to purchase. A draft purchase order
is automatically created and updated.

Interface
=========

Authentication
--------------

The first screen asks Odoo credentials. The user should be member of the Odoo
'Purchase User' group.

.. image:: /mobile_app_purchase/static/src/img/phone_authentication.png

Data Loading
------------

Once authenticated, some datas are cached : Active Products, partners flagged
as supplier, and draft Purchase Orders.

.. image:: /mobile_app_purchase/static/src/img/phone_data_loading.png

Purchase Order Selection
------------------------

Once datas are loaded, user can select an existing draft purchase order he
want to complete.

.. image:: /mobile_app_purchase/static/src/img/phone_select_purchase_order.png


Alternatively, user can create a new purchase order, selecting a supplier.

.. image:: /mobile_app_purchase/static/src/img/phone_select_supplier.png


Product Selection and Quantity Selection
----------------------------------------

Once the purchase order created or selected, the user can select a product,
scanning a barcode.

.. image:: /mobile_app_purchase/static/src/img/phone_select_product.png

If the EAN13 barcode is recognized, some informations are displayed to be
sure that the product is the good one (name, internal code) and other
informations related to stock (quantity on hand and forecasted quantity)
User has to set a quantity to purchase and then validate.

.. image:: /mobile_app_purchase/static/src/img/phone_select_quantity.png


Menu
----

A menu is available in each screen that allows user to navigates between
screens.

.. image:: /mobile_app_purchase/static/src/img/phone_menu.png


Technical Informations
======================

Hardware
--------

This module is designed to work with

* a Browser running on a Mobile (Firefox Mobile / Chrome / ...)
* a Scan reader communicating with the mobile via Bluetooth (SPP settings)

**Implementation Sample**

* Mobile : `Samsung Galaxy Xcover 3 <http://www.samsung.com/fr/consumer/mobile-devices/smartphones/others/SM-G388FDSAXEF>`_
* Browser : `Firefox 46+ <https://www.mozilla.org/en-US/firefox/os/>`_
* Scan Reader : `KDC 400 <https://koamtac.com/kdc400-bluetooth-barcode-scanner/>`_


Used Technologies
-----------------

This module uses extra JS / CSS components.

* `Angular JS v1.x <https://angularjs.org/>`_ 
* `Angular Translate <https://angular-translate.github.io/>`_
* `Ionic Framework <http://ionicframework.com/>`_
* `Ionic Icons <http://ionicons.com/>`_ (MIT Licensed)

* `Angular Odoo <https://github.com/hparfr/angular-odoo>`_, light Javascript
  library developped by `Akretion <http://www.akretion.com/>`_
  and `Camp To Camp <http://www.camptocamp.org/>`_

Available languages
-------------------

* English
* French

Similar Projects
----------------

* You could be interested by another implementation of similar features
  `'stock_scanner' on Github <https://github.com/syleam/stock_scanner>`_
  developped by `Syleam <https://www.syleam.fr/>`_
  and `Acsone <https://www.acsone.eu/>`_.

Installation
============

Normal installation.

Once installed, assuming that your Odoo instance is accessible by the URL
http//localhost:8069/, the web app can be reached at the URL
http//localhost:8069/mobile_app_purchase/static/www/index.html

Configuration
=============

* No extra configuration is needed.

Credits
=======

Contributors
------------

* Sylvain LE GAL <https://twitter.com/legalsylvain>

Roadmap / Current Limits
------------------------

* Currency symbol is hard coded. (€ for the time being);

* Dates and Prices displays do NOT change depending of the localization of
  the user;

* JS and CSS lib are hard included. So if many apps are developped, it could
  be great to have a generic 'web_ionic' module that have all tools to avoid
  to duplicate files;

Known Issues
------------

* **Firefox Ionic Bug** : The first screen allow user to select database,
  in a multi database context. This module use ionic select component, that
  doesn't not works On Firefox Mobile.
  `See the bug on Ionic Github <https://github.com/driftyco/ionic/issues/4767>`_
  
* **Chrome Mobile limitation** : This module plays mp3 sounds when app is,
  or . This feature is not available for Chrome Mobile for the time being,
  cause Chrome consider that allowing to play a sound without explicit action
  of the user raises security issues.
  `See the bug on Chromium website <https://bugs.chromium.org/p/chromium/issues/detail?id=178297>`_

