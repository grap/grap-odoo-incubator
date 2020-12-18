# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import time

from odoo import _, api, fields, models
from odoo.exceptions import Warning as UserError


class InternalUse(models.Model):
    _name = 'internal.use'
    _description = 'Internal Uses'
    _order = 'date_done desc, name'

    _INTERNAL_USE_STATE = [
        ('draft', 'New'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
    ]

    # Columns section
    name = fields.Char(
        string='Name', required=True,
        default='Draft internal use')

    description = fields.Char(
        string='Description', states={
            'done': [('readonly', True)],
            'confirmed': [('readonly', True)]})

    date_done = fields.Date(
        string='Date', required=True,
        default=lambda *x: time.strftime('%Y-%m-%d'),
        states={
            'done': [('readonly', True)],
            'confirmed': [('readonly', True)]})

    internal_use_case_id = fields.Many2one(
        comodel_name='internal.use.case', string='Case', required=True,
        states={
            'done': [('readonly', True)],
            'confirmed': [('readonly', True)]})

    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', readonly=True,
        related='internal_use_case_id.company_id', store=True)

    state = fields.Selection(
        selection=_INTERNAL_USE_STATE, string='Status', readonly=True,
        default='draft')

    line_ids = fields.One2many(
        comodel_name='internal.use.line', inverse_name='internal_use_id',
        string='Lines', states={
            'done': [('readonly', True)],
            'confirmed': [('readonly', True)]})

    stock_move_ids = fields.One2many(
        comodel_name='stock.move', inverse_name='internal_use_id',
        string='Stock Moves', copy=False)

    stock_move_qty = fields.Integer(
        string='Stock Move Quantity', compute='_compute_stock_move_qty',
        store=True)

    account_move_id = fields.Many2one(
        comodel_name='account.move', string='Account Moves', readonly=True,
        copy=False)

    amount = fields.Float(
        string='Total Amount (Tax excluded)', compute='_compute_amount',
        store=True)

    # Compute Section
    @api.depends('state', 'line_ids', 'line_ids.amount')
    def _compute_amount(self):
        for use in self:
            use.amount = sum(use.mapped('line_ids.amount'))

    @api.depends('stock_move_ids.internal_use_id')
    def _compute_stock_move_qty(self):
        for use in self:
            use.stock_move_qty = len(use.stock_move_ids)

    # Overload Section
    @api.multi
    def unlink(self):
        if self.filtered(lambda x: x.state != 'draft'):
            raise UserError(_('You can only delete draft uses.'))
        return super().unlink()

    # Action Section
    @api.multi
    def action_view_stock_lines(self):
        self.ensure_one()
        action = self.env.ref('stock.stock_move_line_action')
        action_data = action.read()[0]
        moves = self.stock_move_ids.ids
        moves_str = ','.join(str(e) for e in moves)
        action_data['domain'] = "[('move_id','in', [" + moves_str + "])]"
        return action_data

    @api.multi
    def action_confirm(self):
        StockMove = self.env['stock.move']
        for use in self.filtered(lambda x: x.state == 'draft'):
            if len(use.line_ids) == 0:
                raise UserError(_(
                    "You can not confirm an empty Internal Use."))

            # Retrieve lines and create one stock move
            vals_list = []
            for line in use.line_ids:
                vals = line._get_move_values(
                    line.product_qty,
                    line.internal_use_id.internal_use_case_id.
                    default_location_src_id.id,
                    line.internal_use_id.internal_use_case_id.
                    default_location_dest_id.id, True)
                vals_list.append(vals)
            sm = StockMove.create(vals_list)
            sm._action_done()

            # Name internal use
            sq_internal_use =\
                self.env['ir.sequence'].next_by_code('internal.use')
            use.write({'name': sq_internal_use})

            # Mark the use as 'confirmed' or 'done'
            if use.internal_use_case_id.journal_id:
                use.write({'state': 'confirmed'})
            else:
                use.write({'state': 'done'})

        return True

    @api.multi
    def action_done(self):
        """ Set the internal use to 'done' and create account moves"""
        AccountMove = self.env['account.move']
        InternalUseLine = self.env['internal.use.line']

        use_data = {}

        # Handle confirmed internal use that have to generate accounting
        # entries
        for use in self.filtered(
                lambda x: (
                    x.state == 'confirmed' and
                    x.internal_use_case_id.journal_id)):

            key = use._get_expense_entry_key()
            if key in use_data.keys():
                use_data[key].append(use.id)
            else:
                use_data[key] = [use.id]

        for key, use_ids in use_data.items():
            uses = self.browse(use_ids)
            # prepare Account Move
            account_move_vals = uses._prepare_account_move()
            all_account_move_line_vals = []

            # Create Counterpart Account Move Line(s)
            charge_use_line_data = {}
            uncharge_use_line_data = {}

            for line in uses.mapped('line_ids'):
                # Get Charge line data
                charge_line_key = line._get_expense_entry_key_charge()

                if charge_line_key in charge_use_line_data:
                    charge_use_line_data[charge_line_key].append(line.id)
                else:
                    charge_use_line_data[charge_line_key] = [line.id]

                # Get Unharge line data
                uncharge_line_key = line._get_expense_entry_key_uncharge()

                if uncharge_line_key in uncharge_use_line_data:
                    uncharge_use_line_data[uncharge_line_key].append(line.id)
                else:
                    uncharge_use_line_data[uncharge_line_key] = [line.id]

            # Create uncharge Lines
            for key, line_ids in uncharge_use_line_data.items():
                lines = InternalUseLine.browse(line_ids)
                account_move_line_vals =\
                    lines._prepare_account_move_line_uncharge(
                        account_move_vals)
                all_account_move_line_vals.append(
                    (0, 0, account_move_line_vals))

            # Create charge Lines
            for key, line_ids in charge_use_line_data.items():
                lines = InternalUseLine.browse(line_ids)
                account_move_line_vals =\
                    lines._prepare_account_move_line_charge(
                        account_move_vals)
                all_account_move_line_vals.append(
                    (0, 0, account_move_line_vals))

            # Create Account move and validate it
            account_move_vals['line_ids'] = all_account_move_line_vals
            account_move = AccountMove.create(account_move_vals)

            # Validate Account Move
            account_move.post()

            # Associate internal uses to account move and set to 'done'
            uses.write({
                'state': 'done',
                'account_move_id': account_move.id,
            })

        # Handle confirmed internal use that don't have to generate accounting
        # entries. (fix incorrect state)
        uses = self.filtered(
            lambda x: (
                x.state == 'confirmed' and
                not x.internal_use_case_id.journal_id))
        uses.write({
            'state': 'done',
        })

        return True

    # Custom Section
    @api.multi
    def _get_expense_entry_key(self):
        """
            define how to group by uses to generate a unique Journal Entry.
            By default, an entry is generated by use case and by month.
            Overwrite this function to change the behaviour.
            Note that internal_use_case_id is mandatory.
        """
        self.ensure_one()
        dt = fields.Date.from_string(self.date_done)
        return (
            self.internal_use_case_id.id,
            '%d-%d' % (dt.year, dt.month),
        )

    @api.multi
    def _prepare_account_move(self):
        use_case = self[0].internal_use_case_id
        return {
            'journal_id': use_case.journal_id.id,
            'company_id': use_case.company_id.id,
            'ref': _('Expense Transfert (%s)') % (use_case.name),
        }
