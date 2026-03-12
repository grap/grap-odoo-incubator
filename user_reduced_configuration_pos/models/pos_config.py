from odoo import models


class PosConfig(models.Model):
    _inherit = "pos.config"

    def _search(self, *args, **kwargs):
        if self.env.context.get(
            "execute_in_reduced_configuration_context"
        ) and not self.env["pos.config"].check_access_rights(
            "read", raise_exception=False
        ):
            return self.env["pos.config"]

        return super()._search(*args, **kwargs)

    def _check_header_footer(self, values):
        return True
