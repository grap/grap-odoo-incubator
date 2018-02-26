# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Columns Section
    consignor_partner_id = fields.Many2one(
        string='Consignor', comodel_name='res.partner',
        domain="[('is_consignor', '=', True)]")

    is_consignment = fields.Boolean(
        string='Is Consignment Product', store=True,
        compute='_compute_is_consignment')

    is_consignment_commission = fields.Boolean(
        string='Is Consignment Commission')

    tax_group_id = fields.Many2one(  # Overload to update domain
        domain="[('company_id', '=', company_id),"
        "('consignor_partner_id', '=', consignor_partner_id)]")

    # Compute Section
    @api.depends('consignor_partner_id')
    def _compute_is_consignment(self):
        for template in self:
            template.is_consignment =\
                (template.consignor_partner_id.id is not False)

    # Onchange Section
    @api.onchange('consignor_partner_id')
    def onchange_consignor_partner_id(self):
        if not self.consignor_partner_id:
            return
        else:
            self.standard_price = 0
            self.seller_ids = False
            if len(self.consignor_partner_id.consignor_tax_group_ids):
                self.tax_group_id =\
                    self.consignor_partner_id.consignor_tax_group_ids[0]
            else:
                self.tax_group_id = False

    # Constrains Section
    @api.constrains('standard_price', 'consignor_partner_id', 'seller_ids')
    def _check_consignor_partner_id_fields(self):
        for template in self:
            if template.consignor_partner_id:
                if template.standard_price:
                    raise UserError(_(
                        "A consigned product must have null Cost Price"))
                if len(template.seller_ids):
                    raise UserError(_(
                        "A consigned product must not have suppliers defined"))

    # Overload Section
    @api.model
    def create(self, vals):
        vals = self._update_vals_consignor(vals)
        return super(ProductTemplate, self).create(vals)

    @api.multi
    def write(self, vals):
        self._check_consignor_changes(vals)
        vals = self._update_vals_consignor(vals)
        if vals.get('is_consignment_commission', False):
            raise UserError(_(
                "You can not change the value of the field"
                " 'Is Consignment Commission'. You can disable this product"
                " and create a new one properly."))
        return super(ProductTemplate, self).write(vals)

    # Custom Section
    @api.multi
    def _check_consignor_changes(self, vals):
        stock_move_obj = self.env['stock.move']
        invoice_line_obj = self.env['account.invoice.line']
        if vals.get('consignor_partner_id', False):
            for template in self:
                product_ids = template.product_variant_ids.ids
                if template.consignor_partner_id.id !=\
                        vals.get('consignor_partner_id', False):
                    moves = stock_move_obj.search([
                        ('product_id', 'in', product_ids)])
                    if len(moves):
                        raise UserError(_(
                            "You can not change the value of the field"
                            " 'Consignor' because the product is associated"
                            " to one or more stock Moves. You should"
                            " disable the product and create a new one."))
                    invoice_lines = invoice_line_obj.search([
                        ('product_id', 'in', product_ids)])
                    if len(invoice_lines):
                        raise UserError(_(
                            "You can not change the value of the field"
                            " 'Consignor' because the product is associated"
                            " to one or more Account Invoice Lines. You should"
                            " disable the product and create a new one."))

    @api.model
    def _update_vals_consignor(self, vals):
        partner_obj = self.env['res.partner']
        if vals.get('consignor_partner_id', False):
            partner = partner_obj.browse(vals.get('consignor_partner_id'))
            vals['purchase_ok'] = True
            vals['property_account_income'] =\
                partner.consignment_account_id.id
            vals['property_account_expense'] =\
                partner.consignment_account_id.id
        return vals
