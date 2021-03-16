This module is a technical module, that remove a bad implementation of ``_name_search`` function
for the model ``res.partner``.

In odoo, the ``_name_search`` function has a bad behaviour :
- if name field is not set, a super of ``_search`` function is called
- but if name field is set, an hardcoded SQL request function is done.

This implementation prevent to overload properly the ``_search`` function, and breaks ACL restrictions.

This module restore the default ``_name_search`` function for the model ``res.partner``,
writen in the ``models.py`` file.
