# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# Part of the code comes from
# OCA/edi/account_invoice_import_invoice2data Module.
# Copyright 2015 - Today Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64
import mimetypes
import os
import tempfile
from datetime import datetime

import invoice2data

from odoo import _, fields, models, tools
from odoo.exceptions import UserError


class WizardInvoice2dataImport(models.TransientModel):
    _name = "wizard.invoice2data.import"
    _description = "Wizard to import Bill invoices via invoice2data"

    invoice_file = fields.Binary(string="PDF Invoice", required=True)

    invoice_filename = fields.Char(string="Filename", readonly=True)

    state = fields.Selection(
        selection=[
            ("import", "Import"),
            ("product_mapping", "Products Mapping"),
            ("line_differences", "Invoice Lines Differences"),
        ],
        default="import",
        required=True,
        readonly=True,
    )

    invoice_id = fields.Many2one(
        comodel_name="account.invoice",
        string="Supplier Invoice",
        required=True,
        readonly=True,
        ondelete="cascade",
    )

    partner_id = fields.Many2one(
        string="Supplier",
        comodel_name="res.partner",
        related="invoice_id.partner_id",
        readonly=True,
    )

    line_ids = fields.One2many(
        comodel_name="wizard.invoice2data.import.line", inverse_name="wizard_id"
    )

    product_mapping_line_ids = fields.One2many(
        comodel_name="wizard.invoice2data.import.line",
        inverse_name="wizard_id",
        string="Product Mapping",
        domain=[("is_product_mapped", "=", False)],
    )

    invoice_difference_line_ids = fields.One2many(
        comodel_name="wizard.invoice2data.import.line",
        inverse_name="wizard_id",
        string="Invoice Lines Differences",
        domain=[("changes_description", "!=", False)],
    )

    to_delete_invoice_line_ids = fields.Many2many(
        comodel_name="account.invoice.line",
        string="Invoice Lines to delete",
        readonly=True,
    )

    pdf_invoice_number = fields.Char(readonly=True)

    pdf_amount = fields.Float(readonly=True)

    pdf_date = fields.Date(readonly=True)

    pdf_date_due = fields.Date(readonly=True)

    def _get_action_from_state(self, state):
        action = self.env["ir.actions.act_window"].for_xml_id(
            "account_invoice_invoice2data", "action_wizard_invoice2data_import"
        )
        self.state = state
        action["res_id"] = self.id
        return action

    def import_invoice(self):
        self.ensure_one()
        result = self._extract_json_from_pdf()
        self._initialize_wizard_invoice(result)
        self._initialize_wizard_lines(result)
        if not all(self.mapped("line_ids.is_product_mapped")):
            return self._get_action_from_state("product_mapping")
        else:
            self._analyze_invoice_lines()
            return self._get_action_from_state("line_differences")

    def _initialize_wizard_invoice(self, result):
        for invoice_field in ["amount", "invoice_number", "date", "date_due"]:
            if invoice_field in result:
                value = result[invoice_field]
                if "date" in invoice_field:
                    value = datetime.strptime(
                        result[invoice_field], result["date_format"]
                    ).date()
                setattr(self, "pdf_%s" % invoice_field, value)

    def map_products(self):
        self.line_ids._create_supplierinfo()
        if not all(self.mapped("line_ids.is_product_mapped")):
            return self._get_action_from_state("product_mapping")
        else:
            self._analyze_invoice_lines()
            return self._get_action_from_state("line_differences")

    def _analyze_invoice_lines(self):
        self.line_ids._analyze_invoice_lines()
        self.to_delete_invoice_line_ids = self.mapped(
            "invoice_id.invoice_line_ids"
        ).filtered(lambda x: x.id not in self.mapped("line_ids.invoice_line_id").ids)

    def _initialize_wizard_lines(self, pdf_data):
        self.line_ids.unlink()
        WizardLine = self.env["wizard.invoice2data.import.line"]
        WizardLine.create(WizardLine._prepare_from_pdf_data(self, pdf_data))

    def _extract_json_from_pdf(self):
        self.ensure_one()

        # Load Templates
        local_templates_dir = tools.config.get("invoice2data_templates_dir", False)
        if not local_templates_dir:
            raise UserError(
                _("'invoice2data_templates_dir' not set in the odoo Config File")
            )
        if not os.path.isdir(local_templates_dir):
            raise UserError(_("%s not available.") % str(local_templates_dir))
        templates = invoice2data.extract.loader.read_templates(local_templates_dir)
        if not len(templates):
            raise UserError(_("No Template found to for bill invoices analyze."))

        # Get data, and check filetype
        file_data = base64.b64decode(self.invoice_file)
        filetype = mimetypes.guess_type(self.invoice_filename)
        if not filetype or filetype[0] != "application/pdf":
            raise UserError(_("Unimplemented file type : '%s'") % str(filetype))

        # Write data in a temporary file
        fd, tmp_file_name = tempfile.mkstemp()
        try:
            os.write(fd, file_data)
        finally:
            os.close(fd)

        try:
            result = invoice2data.main.extract_data(tmp_file_name, templates=templates)
        except Exception as e:
            raise UserError(_("PDF Invoice parsing failed. Error message: %s") % e)
        if not result:
            raise UserError(_("This PDF invoice doesn't match a known templates"))

        return result

    def apply_changes(self):
        self.ensure_one()
        lines_vals = [x._prepare_invoice_line_vals() for x in self.line_ids]

        sequence = len(lines_vals)
        for line in self.to_delete_invoice_line_ids:
            sequence += 1
            line_vals = {
                "sequence": sequence,
                "price_unit": 0,
                "name": _(
                    "%s\n"
                    "[PDF analysis] Unit Price %s set to 0,"
                    " because the line is not present in the PDF."
                )
                % (line.name, line.quantity),
            }
            lines_vals.append((1, line.id, line_vals))

        vals = {
            "invoice_line_ids": lines_vals,
        }
        if self.pdf_date:
            vals.update(
                {
                    "date_invoice": self.pdf_date,
                }
            )
        if self.pdf_date_due:
            vals.update(
                {
                    "date_due": self.pdf_date_due,
                }
            )
        if self.pdf_invoice_number:
            vals.update(
                {
                    "reference": self.pdf_invoice_number,
                }
            )

        self.invoice_id.write(vals)