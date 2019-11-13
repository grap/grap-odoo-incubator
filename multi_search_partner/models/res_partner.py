# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = ["res.partner", "multi.search.mixin"]

    # Overwrite Section
    @api.model
    def _multi_search_search_fields(self):
        return ["display_name", "email"]

    @api.model
    def _multi_search_write_fields(self):
        return ["name", "email"]

    @api.model
    def _multi_search_separator(self):
        # TODO FIX ME
        return ":"

    # Overload Section
    @api.multi
    def write(self, vals):
        """Overload in this part, because write function is not called
        in mixin model. TODO: Check if this weird behavior still occures
        in more recent Odoo versions.
        """
        if self._multi_search_separator():
            vals = self._multi_search_replace_dict(vals, True)
        return super(ResPartner, self).write(vals)
