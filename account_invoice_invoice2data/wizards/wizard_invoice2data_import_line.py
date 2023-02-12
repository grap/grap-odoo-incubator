# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class WizardInvoice2dataImportLine(models.TransientModel):
    _name = "wizard.invoice2data.import.line"
    _description = "Wizard Line to import Bill invoices via invoice2data"

    wizard_id = fields.Many2one(comodel_name="wizard.invoice2data.import")

    product_id = fields.Many2one(comodel_name="product.product")

    invoice_line_id = fields.Many2one(comodel_name="account.invoice.line")

    pdf_product_code = fields.Char()

    pdf_product_name = fields.Char()

    pdf_product_qty = fields.Float()

    pdf_unit_price = fields.Float()

    @api.model
    def _prepare_from_pdf_line(self, wizard, line):
        return {
            "wizard_id": wizard.id,
            "pdf_product_code": line["product_code"],
            "pdf_product_name": line["product_name"],
            "pdf_product_qty": line["product_qty"],
            "pdf_unit_price": line["unit_price"],
        }
