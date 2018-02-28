.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

==========================================
Check if the session state is still opened
==========================================

Context
-------

In Point Of Sale module, the front-end works offline, so all datas are
loaded at the beginning.
At the end of the session, if user do not close the window, it will be
possible to create new pos order on a closed session, generating errors.

Functionality
-------------

* This module prevent the possility to create a pos order via the front
  end PoS UI, when session is closed.
* The session state is checked every minute by default. If the state of the
  session is not opened, a blocking pop up is displayed, and user has to
  reload the current page.

.. figure:: /pos_check_session_state/static/description/error_message.png
   :width: 800 px

Configuration
=============

* Go to Point of Sale / Configuration / Point of Sales
* Open a PoS Config and set a frequency for the check

.. figure:: /pos_check_session_state/static/description/pos_config_form.png
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
