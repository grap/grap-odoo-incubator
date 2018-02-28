.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
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

.. image:: /pos_check_session_state/static/description/error_message.png

Installation
============

Normal installation.

Configuration
=============

* Go to "Settings" / "Technicals" / "Parameters" / "System Parameters"
* Edit the key pos_check_session_state.frequency
* Set a value (in Second)

Credits
=======

Contributors
------------

* Sylvain LE GAL <https://twitter.com/legalsylvain>
