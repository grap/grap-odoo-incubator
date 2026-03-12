from odoo import models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    def _default_pos_config(self):
        return super(ResConfigSettings, self.sudo())._default_pos_config()
