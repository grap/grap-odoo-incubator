This module define a new mixin ``create.recursive.mixin`` that can be used
on any model that contains the following code.

.. code:: python

    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = "complete_name"

(See example in the ``product.category`` model in the odoo ``product`` module)
