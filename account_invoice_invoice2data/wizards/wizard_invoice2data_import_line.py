# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class WizardInvoice2dataImportLine(models.TransientModel):
    _name = "wizard.invoice2data.import.line"
    _description = "Wizard Line to import Bill invoices via invoice2data"

    sequence = fields.Integer(readonly=True)

    wizard_id = fields.Many2one(comodel_name="wizard.invoice2data.import")

    product_id = fields.Many2one(comodel_name="product.product")

    invoice_line_id = fields.Many2one(
        comodel_name="account.invoice.line", readonly=True
    )

    is_product_mapped = fields.Boolean(readonly=True)

    pdf_product_code = fields.Char(readonly=True)

    pdf_product_name = fields.Char(readonly=True)

    pdf_product_qty = fields.Float(readonly=True)

    pdf_unit_price = fields.Float(readonly=True)

    data = fields.Text(readonly=True)

    changes_description = fields.Char(readonly=True)

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
    def _get_extra_products(self):
        return {
            "amount_parafiscal_tax_interfel": {
                "product_code": "TPF",
                "product_name": _("Taxe Interfel TPF"),
            },
        }

    @api.model
    def _prepare_from_pdf_data(self, wizard, pdf_data):
        result = []
        sequence = 0
        # Create regular product lines
        for line_data in pdf_data["lines"]:
            sequence += 1
            product_id = self._get_product_id_from_product_code(
                wizard.partner_id, line_data["product_code"]
            )
            result.append(
                {
                    "sequence": sequence,
                    "wizard_id": wizard.id,
                    "is_product_mapped": bool(product_id),
                    "product_id": product_id,
                    "pdf_product_code": line_data["product_code"],
                    "pdf_product_name": line_data["product_name"],
                    "pdf_product_qty": line_data["product_qty"],
                    "pdf_unit_price": line_data["unit_price"],
                    "data": str(line_data),
                }
            )
        for key, value in self._get_extra_products().items():
            if key in pdf_data.keys():
                sequence += 1
                product_id = self._get_product_id_from_product_code(
                    wizard.partner_id, value["product_code"]
                )
                result.append(
                    {
                        "sequence": sequence,
                        "wizard_id": wizard.id,
                        "is_product_mapped": bool(product_id),
                        "product_id": product_id,
                        "pdf_product_code": value["product_code"],
                        "pdf_product_name": value["product_name"],
                        "pdf_product_qty": 1,
                        "pdf_unit_price": pdf_data[key],
                        "data": str(pdf_data[key]),
                    }
                )
        return result

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

    def _analyze_invoice_lines(self):
        for wizard_line in self:
            invoice_lines = wizard_line.wizard_id.invoice_id.invoice_line_ids.filtered(
                lambda x: x.product_id == wizard_line.product_id
            )
            # Case 1 : Many lines. Unimplemented feature
            if len(invoice_lines) > 1:
                raise UserError(
                    _(
                        "Unimplemented feature : Many invoice lines for the same product '%s'"
                    )
                    % wizard_line.product_id.complete_name
                )

            # Case 2: No lines. -> Creation
            if not invoice_lines:
                wizard_line.write(
                    {
                        "changes_description": _("New Line Creation"),
                        "invoice_line_id": False,
                    }
                )
                continue

            # Case 3 : Check if data changed
            changes = []
            if invoice_lines[0].quantity != wizard_line.pdf_product_qty:
                changes.append(
                    _(
                        "Quantity : %s -> %s"
                        % (invoice_lines[0].quantity, wizard_line.pdf_product_qty)
                    )
                )
            if invoice_lines[0].price_unit != wizard_line.pdf_unit_price:
                changes.append(
                    _(
                        "Unit Price : %s -> %s"
                        % (invoice_lines[0].price_unit, wizard_line.pdf_unit_price)
                    )
                )
            wizard_line.write(
                {
                    "invoice_line_id": invoice_lines[0].id,
                    "changes_description": changes and "\n".join(changes) or False,
                }
            )

    def _prepare_invoice_line_vals(self):
        self.ensure_one()
        if not self.invoice_line_id:

            # prepare creation of a new line
            fiscal_position = self.wizard_id.invoice_id.fiscal_position_id
            account = self.env["account.invoice.line"].get_invoice_line_account(
                "in_invoice", self.product_id, fiscal_position, self.env.user.company_id
            )
            taxes = fiscal_position.map_tax(
                self.product_id.supplier_taxes_id,
                self.product_id,
                self.wizard_id.invoice_id.partner_id,
            )
            name = self.product_id.with_context(
                partner_id=self.wizard_id.partner_id.id
            ).partner_ref
            if self.product_id.description_purchase:
                name += "\n" + self.product_id.description_purchase
            return (
                0,
                0,
                {
                    "sequence": self.sequence,
                    "product_id": self.product_id.id,
                    "name": name,
                    "origin": _("PDF Analysis"),
                    "account_id": account.id,
                    "quantity": self.pdf_product_qty,
                    "price_unit": self.pdf_unit_price,
                    "invoice_line_tax_ids": taxes.ids,
                },
            )
        else:
            vals = {"sequence": self.sequence}
            if self.invoice_line_id.price_unit != self.pdf_unit_price:
                vals.update({"price_unit": self.pdf_unit_price})
            if self.invoice_line_id.quantity != self.pdf_product_qty:
                vals.update({"quantity": self.pdf_product_qty})
            return (1, self.invoice_line_id.id, vals)
