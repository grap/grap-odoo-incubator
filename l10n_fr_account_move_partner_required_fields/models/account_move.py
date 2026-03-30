# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)wallet_payments
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    _PARTNER_REQUIRED_ADDRESS = ["street", "zip", "city"]

    partner_has_siren = fields.Boolean(compute="_compute_partner_has_required_fields")
    partner_has_address = fields.Boolean(compute="_compute_partner_has_required_fields")
    partner_is_company = fields.Boolean(compute="_compute_partner_has_required_fields")

    @api.depends(
        "commercial_partner_id",
        "commercial_partner_id.street",
        "commercial_partner_id.zip",
        "commercial_partner_id.city",
        "commercial_partner_id.siren",
    )
    def _compute_partner_has_required_fields(self):
        for move in self:
            partner = move.commercial_partner_id
            move.partner_is_company = partner.is_company

            # Check address
            move.partner_has_address = True
            for field in self._PARTNER_REQUIRED_ADDRESS:
                value = getattr(partner, field, False)
                if not value:
                    move.partner_has_address = False
                    break

            # Check SIREN
            move.partner_has_siren = bool(partner.siren)

    def _post(self, *args, **kwargs):
        # Override posting if it lacks some required informations
        for move in self:
            partner = move.commercial_partner_id
            if not move.partner_is_company:
                continue

            missing_parts = []

            if not move.partner_has_siren:
                missing_parts.append(_("the SIREN"))
            if not move.partner_has_address:
                missing_parts.append(_("address informations (street, ZIP code, city)"))

            if missing_parts:
                raise UserError(
                    _(
                        "In order to invoice the company %(customer_name)s, "
                        "you need to complete %(_missing_parts)s.",
                        customer_name=partner.display_name,
                        _missing_parts=" and ".join(missing_parts),
                    )
                )

        return super()._post(*args, **kwargs)
