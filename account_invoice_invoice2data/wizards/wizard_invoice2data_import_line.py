# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class WizardInvoice2dataImportLine(models.TransientModel):
    _name = "wizard.invoice2data.import.line"
    _description = "Wizard Line to import Bill invoices via invoice2data"

    wizard_id = fields.Many2one(comodel_name="wizard.invoice2data.import")

    product_id = fields.Many2one(comodel_name="product.product")

    invoice_line_id = fields.Many2one(comodel_name="account.invoice.line")

    is_product_mapped = fields.Boolean(readonly=True)

    pdf_product_code = fields.Char(readonly=True)

    pdf_product_name = fields.Char(readonly=True)

    pdf_product_qty = fields.Float(readonly=True)

    pdf_unit_price = fields.Float(readonly=True)

    data = fields.Text(readonly=True)

    @api.model
    def _get_product_id_from_product_code(self, partner, product_code):
        products = self.env["product.product"]
        # Search for product
        supplierinfos = self.env["product.supplierinfo"].search(
            [
                ("name", "=", partner.id),
                ("product_code", "=", product_code),
            ]
        )
        products = supplierinfos.filtered(lambda x: x.product_id).mapped("product_id")

        products |= supplierinfos.filtered(lambda x: not x.product_id).mapped(
            "product_tmpl_id.product_variant_ids"
        )

        if len(products) > 1:
            raise UserError(
                _("Many products found for the supplier %s and the code %s")
                % (partner.complete_name, product_code)
            )
        return products and products[0].id

    @api.model
    def _prepare_from_pdf_line(self, wizard, line_data):
        product_id = self._get_product_id_from_product_code(
            wizard.partner_id, line_data["product_code"]
        )
        return {
            "wizard_id": wizard.id,
            "is_product_mapped": bool(product_id),
            "product_id": product_id,
            "pdf_product_code": line_data["product_code"],
            "pdf_product_name": line_data["product_name"],
            "pdf_product_qty": line_data["product_qty"],
            "pdf_unit_price": line_data["unit_price"],
            "data": str(line_data),
        }

    def _create_supplierinfo(self):
        for line in self.filtered(lambda x: not x.is_product_mapped and x.product_id):
            self.env["product.supplierinfo"].create(
                {
                    "name": line.wizard_id.partner_id.id,
                    "product_tmpl_id": line.product_id.product_tmpl_id.id,
                    "product_id": (
                        line.product_id.product_tmpl_id.product_variant_count > 1
                    )
                    and line.product_id.id,
                    "product_code": line.pdf_product_code,
                    "product_name": line.pdf_product_name,
                    "price": line.pdf_unit_price,
                }
            )
            line.is_product_mapped = True
