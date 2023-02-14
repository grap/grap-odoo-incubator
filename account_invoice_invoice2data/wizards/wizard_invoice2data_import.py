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
        self._initialize_wizard_lines(result)
        return self._get_action_from_state("import")

        if not all(self.mapped("line_ids.is_product_mapped")):
            return self._get_action_from_state("product_mapping")
        else:
            self._analyze_invoice_lines()
            return self._get_action_from_state("line_differences")

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
        vals = {
            "invoice_line_ids": [x._prepare_invoice_line_vals() for x in self.line_ids]
        }
        self.invoice_id.write(vals)
        self.to_delete_invoice_line_ids.unlink()
        self.invoice_id.message_post(body=str(vals))


# bob = {
#     "issuer": "Ekibio",
#     "amount": 671.37,
#     "invoice_number": "792437",
#     "date": "06/02/2023",
#     "currency": "EUR",
#     "lines": [
#         {
#             "product_code": "001053",
#             "product_name": "COQUILLETTES 1/2 CPLETES fil France 5KG",
#             "certification": "001",
#             "referential": "001",
#             "package_number": "3",
#             "quantity": "15.000",
#             "unit_price": "2.350",
#             "total_vat_excl": "35.25",
#         },
#         {
#             "product_code": "005850",
#             "product_name": "TAMPON SUPER SS APPLIC. 16u",
#             "certification": "021",
#             "referential": "007",
#             "package_number": "1",
#             "quantity": "12.000",
#             "unit_price": "3.120",
#             "total_vat_excl": "37.44",
#         },
#         {
#             "product_code": "007167",
#             "product_name": "BOUILLON DE POULE BIO 80G",
#             "certification": "001",
#             "referential": "001",
#             "package_number": "1",
#             "quantity": "12.000",
#             "unit_price": "1.540",
#             "total_vat_excl": "18.48",
#         },
#         {
#             "product_code": "010117",
#             "product_name": "COUSCOUS BLANC FILIERE FRANCE 5KG",
#             "certification": "001",
#             "referential": "001",
#             "package_number": "3",
#             "quantity": "15.000",
#             "unit_price": "2.560",
#             "total_vat_excl": "38.40",
#         },
#         {
#             "product_code": "005856",
#             "product_name": "FLEUR DE SHAMPOOING CHEVEUX NORMAUX 85G",
#             "certification": "021",
#             "referential": "006",
#             "package_number": "2",
#             "quantity": "12.000",
#             "unit_price": "3.550",
#             "total_vat_excl": "42.60",
#         },
#         {
#             "product_code": "007508",
#             "product_name": "PENNE BLANCHES FIL FR 5KG",
#             "certification": "001",
#             "referential": "001",
#             "package_number": "3",
#             "quantity": "15.000",
#             "unit_price": "2.340",
#             "total_vat_excl": "35.10",
#         },
#         {
#             "product_code": "007049",
#             "product_name": "PSYLLIUM BLOND TEGUMENTS 150G",
#             "certification": "001",
#             "referential": "001",
#             "package_number": "2",
#             "quantity": "12.000",
#             "unit_price": "5.560",
#             "total_vat_excl": "66.72",
#         },
#         {
#             "product_code": "006279",
#             "product_name": "SPIRALES 1/2 COMPLETES fil France 5KG",
#             "certification": "001",
#             "referential": "001",
#             "package_number": "3",
#             "quantity": "15.000",
#             "unit_price": "2.350",
#             "total_vat_excl": "35.25",
#         },
#         {
#             "product_code": "008744",
#             "product_name": "TARTELETTE CHOCO NOISETTE 150G",
#             "certification": "001",
#             "referential": "035",
#             "package_number": "1",
#             "quantity": "6.000",
#             "unit_price": "2.030",
#             "total_vat_excl": "12.18",
#         },
#         {
#             "product_code": "005278",
#             "product_name": "RICE DRINK NATURE 1L",
#             "certification": "001",
#             "referential": "001",
#             "package_number": "2",
#             "quantity": "12.000",
#             "unit_price": "1.580",
#             "total_vat_excl": "18.96",
#         },
#         {
#             "product_code": "001420",
#             "product_name": "CHOUCROUTE DEMETER 720ml",
#             "certification": "001",
#             "referential": "004",
#             "package_number": "2",
#             "quantity": "12.000",
#             "unit_price": "2.100",
#             "total_vat_excl": "25.20",
#         },
#         {
#             "product_code": "000115",
#             "product_name": "COQUILLETTES BLANCHES BIO FIL FRANCE 5KG",
#             "certification": "001",
#             "referential": "001",
#             "package_number": "2",
#             "quantity": "10.000",
#             "unit_price": "2.340",
#             "total_vat_excl": "23.40",
#         },
#         {
#             "product_code": "007389",
#             "product_name": "VRAC PALETS NOIR 70% 5KG",
#             "certification": "002",
#             "referential": "003",
#             "package_number": "1",
#             "quantity": "1.000",
#             "unit_price": "62.830",
#             "total_vat_excl": "62.83",
#         },
#         {
#             "product_code": "005522",
#             "product_name": "RIZ RD BLANC CAMARGUE 25KG IGP",
#             "certification": "001",
#             "referential": "018",
#             "package_number": "1",
#             "quantity": "25.000",
#             "unit_price": "3.180",
#             "total_vat_excl": "79.50",
#         },
#         {
#             "product_code": "009989",
#             "product_name": "LESSIVE PECHE 2L",
#             "certification": "021",
#             "referential": "005",
#             "package_number": "1",
#             "quantity": "6.000",
#             "unit_price": "6.020",
#             "total_vat_excl": "36.12",
#         },
#         {
#             "product_code": "008036",
#             "product_name": "HARICOTS VERTS EXTRA FINS FRANCE 720ML",
#             "certification": "001",
#             "referential": "035",
#             "package_number": "1",
#             "quantity": "6.000",
#             "unit_price": "2.340",
#             "total_vat_excl": "14.04",
#         },
#         {
#             "product_code": "005766",
#             "product_name": "MIX PATISSERIE MVSG 500G",
#             "certification": "001",
#             "referential": "021",
#             "package_number": "1",
#             "quantity": "6.000",
#             "unit_price": "3.080",
#             "total_vat_excl": "18.48",
#         },
#         {
#             "product_code": "010118",
#             "product_name": "COUSCOUS DEMI COMPLET FILIERE FRANCE 5KG",
#             "certification": "001",
#             "referential": "001",
#             "package_number": "2",
#             "quantity": "10.000",
#             "unit_price": "2.560",
#             "total_vat_excl": "25.60",
#         },
#     ],
#     "desc": "Invoice from Ekibio",
# }
