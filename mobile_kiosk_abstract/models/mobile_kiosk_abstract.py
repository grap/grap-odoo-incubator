# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class MobileKioskAbstract(models.TransientModel):
    _name = "mobile.kiosk.abstract"
    _description = "Mobile Kiosk Abstract Proxy"

    @api.model
    def _result_prepare(self):
        return {
            "notifications": [],
            "action": False,
        }

    def _result_add_notification(
        self, result, title=False, message="", level="info", **kwargs
    ):
        assert level in ["info", "success", "warning", "danger"]
        kwargs.update({"title": title, "message": message, "type": level})
        result["notifications"].append(kwargs)
        return result
