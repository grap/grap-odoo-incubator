# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.osv import expression


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _get_name_search_reset_fields(self):
        return ["name", "email"]

    @api.model
    def _name_search(
        self, name="", args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        # As the partner _name_search function doesn't call the _search function.
        # (see /odoo/addons/base/res_partner.py)
        # (it makes a hard sql request instead)
        # we OVERWRITE here the _name_search, function, writing the default
        # feature present in /odoo/models.py

        args = list(args or [])
        if not (name == "" and operator == "ilike"):
            name_args = []
            for field_name in self._get_name_search_reset_fields():
                name_args = expression.OR([name_args, [(field_name, operator, name)]])
            args = expression.AND([args, name_args])
        access_rights_uid = name_get_uid or self._uid
        ids = self._search(args, limit=limit, access_rights_uid=access_rights_uid)
        recs = self.browse(ids)
        return models.lazy_name_get(recs.sudo(access_rights_uid))
