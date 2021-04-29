This module is a technical module that adds several fields on ``product.template`` model:

* ``uom_package_id`` that is a new optional unit of measure, that is the
  package quantity used for sale the product.

- ``uom_package_qty``. if defined, the sale should be a multiple of the field ``uom_package_qty`` (if defined)
  or a multiple of the ``uom_id`` otherwise.
