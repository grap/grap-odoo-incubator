This module overload the regular process of Odoo, regarding the
setting `ẁeb.web.url`.

By default, the Odoo update the key, when the user admin is logging in,
with the value `request.httprequest.url_root.rstrip('/')`.
Cf. ./addons/base/res/res_users.py

With this module, this behaviour is skipped, and the value is forced,
when the database is loaded, regarding a key present in the odoo configuration
file.

Note :
this module remove the possibility to freeze this key, with the other
setting `web.base.url.freeze`.
