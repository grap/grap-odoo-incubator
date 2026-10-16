# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class MobileKioskApplication(models.Model):
    _name = "mobile.kiosk.application"
    _description = "Mobile Kiosk Applications"

    name = fields.Char(required=True, translate=True)

    action_tag = fields.Char(required=True)

    summary = fields.Char(translate=True)

    icon = fields.Char(string="Icon URL")

    def button_launch(self):
        self.ensure_one()
        return {
            "type": "ir.actions.client",
            "name": self.name,
            "tag": self.action_tag,
            "target": "fullscreen",
        }
