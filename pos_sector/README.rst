=======================
Point of Sale - Sectors
=======================

.. 
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! source digest: sha256:a5af76e23d737427519c47730e768f07774f2b79f1170d247a4f2aea96141d74
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-grap%2Fgrap--odoo--incubator-lightgray.png?logo=github
    :target: https://github.com/grap/grap-odoo-incubator/tree/12.0/pos_sector
    :alt: grap/grap-odoo-incubator

|badge1| |badge2| |badge3|

This module extends the functionality of point of sale to support product
sectors restricting products display in the Point of Sale, depending of the
product sectors.

This module can be interesting if some cashiers have the right to sell
some products, and not other cashiers.

It can be also usefull if you have distinct point of sale that are saling
differents products, for exemple if your company has a restaurant part, and a
shop part, with two point of sale.

**Table of contents**

.. contents::
   :local:

Configuration
=============

To configure this module, you need to:

* Go to Point of Sale / Configuration / Sectors

* Create your PoS Sectors

.. figure:: https://raw.githubusercontent.com/grap/grap-odoo-incubator/12.0/pos_sector/static/description/pos_sector_tree.png

* Open your Point Of Sale configurations and set sectors

.. figure:: https://raw.githubusercontent.com/grap/grap-odoo-incubator/12.0/pos_sector/static/description/pos_config_form.png

* Finally, edit your products and set a sector

.. figure:: https://raw.githubusercontent.com/grap/grap-odoo-incubator/12.0/pos_sector/static/description/product_form.png

Usage
=====

To use this module, you need to

* open the point of sale

The products displayed will belong to the sectors of the current PoS config.
(Also the products without sectors will be displayed)

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/grap/grap-odoo-incubator/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us to smash it by providing a detailed and welcomed
`feedback <https://github.com/grap/grap-odoo-incubator/issues/new?body=module:%20pos_sector%0Aversion:%2012.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
~~~~~~~

* GRAP

Contributors
~~~~~~~~~~~~

* Sylvain LE GAL <https://twitter.com/legalsylvain>

Maintainers
~~~~~~~~~~~

This module is part of the `grap/grap-odoo-incubator <https://github.com/grap/grap-odoo-incubator/tree/12.0/pos_sector>`_ project on GitHub.

You are welcome to contribute.
