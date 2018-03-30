.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

===============================================
Point of Sale - Limit 'Unknown Barcode' message
===============================================

This module extends the functionality of point of sale to limit the
display of 'Unknown barcode'.

In Odoo, by default, when the user tip text with the keyboard a check is
processed if the speed is quick, to check if it is a barcode.

That's not very predictive and some undesired warning occured if:

* the user remove a text in a field (for exemple in the field to search customer)
* the user tip with the keyboard quickly.

The first case occures very often if the user leaves the key 'backspace' pressed.

.. figure:: /pos_limit_unknown_barcode/static/description/pos_error.png
   :width: 800 px

This module will display a message only if the text matches exactly a given
pattern.

Configuration
=============

To configure this module, you need to:

* Go to Point of Sale / Configuration / Point of Sales

* Tip a regex in the new field 'Regular Expresssion for Barcode Warnings'

by default the pattern matches with text from 8 to 13 digits.

.. figure:: /pos_limit_unknown_barcode/static/description/pos_config_form.png
   :width: 800 px

Credits
=======

Contributors
------------

* Sylvain LE GAL (https://www.twitter.com/legalsylvain)

Funders
-------

The development of this module has been financially supported by:

* GRAP, Groupement Régional Alimentaire de Proximité (http://www.grap.coop)
