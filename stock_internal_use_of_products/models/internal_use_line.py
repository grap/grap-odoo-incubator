# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError

from .internal_use import _INTERNAL_USE_STATE

import openerp.addons.decimal_precision as dp


class InternalUseLine(models.Model):
    _name = 'internal.use.line'

    # Column Section
    internal_use_id = fields.Many2one(
        comodel_name='internal.use', string='Internal Uses', select=True,
        readonly=True, ondelete='cascade', oldname='internal_use')

    product_id = fields.Many2one(
        comodel_name='product.product', string='Product', required=True,
        domain="[('type', '!=', 'service')]", select=True)

    product_qty = fields.Float(
        string='Quantity', digits_compute=dp.get_precision('Product UoM'),
        required=True, default=1)

    # TODO ADD CONSTRAINT
    product_uom_id = fields.Many2one(
        comodel_name='product.uom', string='Unit of Measure', required=True)

    price_unit = fields.Float(
        string='Unit Price (Tax Excluded)',
        digits_compute=dp.get_precision('Product Price'))

    amount = fields.Float(
        string='Amount (Tax Excluded)', store=True,
        compute='_compute_amount',
        digits_compute=dp.get_precision('Product Price'), oldname='subtotal')

    # Related Fields
    name = fields.Char(
        related='internal_use_id.name', string='Name')

    internal_use_case_id = fields.Many2one(
        commodel_name='internal.use.case', string='Internal Use Case',
        related='internal_use_id.internal_use_case_id',
        select=True, store=True,
        oldname='internal_use_case')

    date_done = fields.Date(
        related='internal_use_id.date_done', string='Date',
        select=True, store=True)

    company_id = fields.Many2one(
        comodel_name='res.company', related='internal_use_id.company_id',
        string='Company', select=True, store=True)

    state = fields.Selection(
        string='State', related='internal_use_id.state',
        selection=_INTERNAL_USE_STATE,
        readonly=True, store=True, select=True)

    # Compute section
    @api.depends('product_qty', 'price_unit', 'product_id', 'product_uom_id')
    def _compute_amount(self):
        uom_obj = self.env['product.uom']
        for line in self:
            if not (line.product_id and line.product_uom_id):
                continue
            line.amount = line.price_unit * uom_obj._compute_qty_obj(
                line.product_uom_id, line.product_qty, line.product_id.uom_id)

    # Views section
    @api.onchange('product_id')
    def _on_change_product_id(self):
        self.ensure_one()
        line = self
        if not line.product_id:
            return
        line.product_uom_id = line.product_id.uom_id.id
        line.price_unit = line.product_id.standard_price
        line.price_unit = line.product_id.supplier_taxes_id.compute_all(
            line.price_unit, line.product_qty, line.product_id.id)['total']

    # Constrains Section
    @api.constrains('product_qty')
    def _constrains_product_qty(self):
        for line in self:
            if not line.product_qty:
                raise UserError(_("Line quantity can not be null"))

    # Constrains Section
    @api.constrains('product_uom_id', 'product_id')
    def _constrains_product_qty(self):
        for line in self:
            if not (line.product_id and line.product_uom_id):
                continue
            if line.product_id.uom_id.category_id !=\
                    line.product_uom_id.category_id:
                raise UserError(_(
                    "The current unit of measure '%s' of the line %s (quantity"
                    "  %s) is not compatible with the unit of measure '%s'"
                    " of the product") % (
                        line.product_uom_id.name, line.product_id.name,
                        line.product_qty, line.product_id.uom_id.name))

    @api.multi
    def _prepare_stock_move(self):
        self.ensure_one()
        return {
            'name': 'Internal Use Line/' + str(self.id),
            'product_id': self.product_id.id,
            'internal_use_id': self.internal_use_id.id,
            'product_uom': self.product_uom_id.id,
            'date': self.date_done,
            'product_uom_qty': (
                self.product_qty > 0 and
                self.product_qty or -self.product_qty),
            'location_id': (
                self.product_qty > 0 and
                self.internal_use_case_id.default_location_src_id.id or
                self.internal_use_case_id.default_location_dest_id.id),
            'location_dest_id': (
                self.product_qty > 0 and
                self.internal_use_case_id.default_location_dest_id.id or
                self.internal_use_case_id.default_location_src_id.id),
        }

    @api.multi
    def _get_expense_entry_key(self):
        """
            define how to group by use lines to generate a unique account move
            line.
            Overwrite this function to change the behaviour.
        """
        self.ensure_one()
        return (
            self.product_id.get_income_expense_accounts()['account_expense'],
            self.product_id.supplier_taxes_id.ids,
        )

    @api.multi
    def _prepare_account_move_line(self, account_move_vals):
        use_case = self[0].internal_use_case_id
        total = sum(self.mapped('amount'))
        tax_code_id = self[0].product_id.supplier_taxes_id and\
            self[0].product_id.supplier_taxes_id[0].base_code_id or False
        return {
            'name': _('Expense Transfert (%s)') % (use_case.name),
            'date': account_move_vals['date'],
            'period_id': account_move_vals['period_id'],
            'product_id': False,
            'product_uom_id': False,
            'quantity': 0,
            'account_id': self[0].product_id.get_income_expense_accounts()[
                'account_expense'].id,
            'credit': (total > 0) and total or 0,
            'debit': (total < 0) and -total or 0,
            'tax_code_id': tax_code_id,
            'tax_amount': tax_code_id and max(total, -total) or 0,
        }
