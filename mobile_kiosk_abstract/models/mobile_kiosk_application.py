# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import fields, models


class MobileKioskApplication(models.Model):
    _name = 'mobile.kiosk.application'
    _description = 'Mobile Kiosk Applications'

    _TARGET_SELECTION = [
        ('current', 'Current Window'),
        ('new', 'New Window'),
        ('fullscreen', 'Full Screen'),
        ('main', 'Main action of Current Window'),
    ]

    name = fields.Char(string="Name", required=True)

    action_tag = fields.Char(string="Action Tag", required=True)

    target = fields.Selection(selection=_TARGET_SELECTION, required=True)

    summary = fields.Char(string="Summary")

    icon = fields.Char(string="Icon URL")

    def button_launch(self):
        self.ensure_one()
        return {
            "type": "ir.actions.client",
            "name": self.name,
            "tag": self.action_tag,
            "target": "main",
        }
