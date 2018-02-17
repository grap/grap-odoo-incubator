.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=====================================
Point of Sale - Multi Company Context
=====================================

This module extends the functionality of point of sale to fully support
multi companies implementation and to allow you to separate PoS Categories
and PoS Sessions by companies.

Technical information
---------------------

* ``pos.session`` : Add new related ``company_id`` field and restrict
  access right
* ``pos.category`` : Add new  ``company_id`` field and restrict access
  right
* Add the ``company_id`` field in all the search / tree / form views of the
  Point of Sale.

.. figure:: /pos_multicompany/static/description/pos_category_tree.png
   :width: 800 px

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
