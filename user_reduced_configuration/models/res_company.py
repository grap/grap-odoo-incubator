# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, models
from odoo.exceptions import AccessError


class ResCompany(models.Model):
    _inherit = "res.company"

    def write(self, vals):
        """company dependent fields are handled specificly:
        There are related fields.
        As a result, write is done automatically by ORM,
        and not by the set_values() of the res.config.settings
        models.
        """
        if self.env.context.get("create_in_reduced_configuration_context", False):
            self._check_write_access_reduced_configuration_context(vals.keys())
            return super(ResCompany, self.sudo()).write(vals)
        return super().write(vals)

    def _check_write_access_reduced_configuration_context(self, company_fields):
        ReducedSetting = self.env["res.reduced.config.settings"]
        allowed_company_related_fields = [
            y.related
            for x, y in ReducedSetting._fields.items()
            if x in ReducedSetting._get_allowed_fields()
        ]

        for company_field in company_fields:
            if f"company_id.{company_field}" not in allowed_company_related_fields:
                raise AccessError(
                    _(
                        "You have no right to write on the field '%(company_field)s'"
                        " of the model 'res.company'.",
                        company_field=company_field,
                    )
                )
