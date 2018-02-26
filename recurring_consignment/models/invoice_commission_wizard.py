# coding: utf-8
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class InvoiceCommissionWizard(models.TransientModel):
    _name = 'invoice.commission.wizard'

    # Default values Section
    def _default_consignor_partner_id(self):
        return self.env.context.get('active_id', False)

    def _default_period_id(self):
        "return the last past accounting period"
        period_obj = self.env['account.period']
        period_ids = period_obj.search([
            ('date_stop', '<', datetime.now().strftime('%Y-%m-%d')),
            ('special', '=', False)],
            order='date_start desc', limit=1)
        return period_ids and period_ids[0] or False

    # Columns Section
    consignor_partner_id = fields.Many2one(
        comodel_name='res.partner', string='Consignor', required=True,
        domain="[('is_consignor', '=', True)]",
        default=_default_consignor_partner_id)

    period_id = fields.Many2one(
        comodel_name='account.period', string='Period', required=True,
        domain="[('special', '=', False), ('state', '=', 'draft')]")

    line_qty = fields.Integer(
        string='Move Lines Quantity', compute='_compute_line_qty')

    @api.depends('consignor_partner_id', 'period_id')
    def _compute_line_qty(self):
        for wizard in self:
            lines = wizard._get_line_ids()
            wizard.line_qty = len(lines)

    # Action Section
    @api.multi
    def invoice_commission(self):
        move_line_obj = self.env['account.move.line']
        invoice_obj = self.env['account.invoice']
        invoice_line_obj = self.env['account.invoice.line']
        invoice_ids = []
        grouped_data = {}
        done_line_ids = []

        for wizard in self:
            rate = wizard.consignor_partner_id.consignment_commission
            # Get lines to commission
            lines = self._get_line_ids()
            if not lines:
                raise UserError(_(
                    "There is no move lines to commission for this consignor"
                    " and this accounting period."))

            for line in lines:
                # If there is product commission on this line
                if line.tax_code_id.consignment_product_id:
                    key = self._get_line_key(line)
                    grouped_data.setdefault(key, [])
                    grouped_data[key].append(line)

            # Make Commission Invoice
            invoice_vals = {
                'partner_id': wizard.consignor_partner_id.id,
                'date_invoice': wizard.period_id.date_stop,
                'is_consignment_invoice': True,
                'type': 'out_invoice',
                'name': _('Commission Invoices (%s)') % wizard.period_id.code,
                'account_id':
                wizard.consignor_partner_id.consignment_account_id.id,
            }
            invoice = invoice_obj.create(invoice_vals)
            invoice_ids.append(invoice.id)

            # Create lines
            for key, value in grouped_data.iteritems():
                current_line_ids = [x.id for x in value]
                invoice_line_vals = self._prepare_invoice_line(
                    key, value, invoice)
                invoice_line_obj.create(invoice_line_vals)

                done_line_ids += current_line_ids

                # Mark Move lines as commisssioned
                current_lines = move_line_obj.browse(current_line_ids)
                current_lines.write({
                    'consignment_invoice_id': invoice.id,
                    'consignment_commission': rate,
                })

            # Mark leaving Move lines as no commisssioned
            leaving_line_ids = [x for x in lines.ids if x not in done_line_ids]
            leaving_lines = move_line_obj.browse(leaving_line_ids)
            leaving_lines.write({
                'consignment_invoice_id': invoice.id,
                'consignment_commission': 0,
            })

        # Recompute Taxes
        invoices = invoice_obj.browse(invoice_ids)
        invoices.button_reset_taxes()

        # Return action that displays new invoices
        result = self.env.ref('account.action_invoice_tree1').read()[0]
        result['domain'] =\
            "[('id', 'in', ["+','.join(map(str, invoice_ids))+"])]"
        return result

    @api.multi
    def _prepare_invoice_line(self, key, value, invoice):
        self.ensure_one()
        wizard = self[0]
        invoice_line_obj = self.env['account.invoice.line']
        rate = wizard.consignor_partner_id.consignment_commission
        total_credit = 0
        product = value[0].tax_code_id.consignment_product_id
        for line in value:
            total_credit += line.credit - line.debit
        res = invoice_line_obj.product_id_change(
            product.id, product.uom_id.id, qty=1,
            type='out_invoice', partner_id=wizard.consignor_partner_id.id,
            )['value']
        res.update({
            'product_id': product.id,
            'invoice_id': invoice.id,
            'price_unit': total_credit * rate / 100,
            'invoice_line_tax_id': [(6, False, res['invoice_line_tax_id'])],
            'name':  _(
                "Commission on Sale or Refunds\n"
                "(Rate : %s %%; Base : %.2f € ; Period %s)") % (
                rate, total_credit, value[0].period_id.code),

        })
        return res

    # Private Section
    @api.model
    def _get_line_key(self, move_line):
        return (
            move_line.period_id.id,
            move_line.tax_code_id.id)

    @api.multi
    def _get_line_ids(self):
        self.ensure_one()
        wizard = self[0]
        if not (wizard.consignor_partner_id and wizard.period_id):
            return []

        invoice_obj = self.env['account.invoice']
        journal_obj = self.env['account.journal']
        line_obj = self.env['account.move.line']

        # Get periods from the fiscal year, and previous to the selected one
        period_ids = []
        for period in wizard.period_id.fiscalyear_id.period_ids:
            if period.date_start <= wizard.period_id.date_start and\
                    not period.special:
                period_ids.append(period.id)

        # Get Lines to ignore
        ignore_invoices = invoice_obj.search([
            ('is_consignment_invoice', '=', True),
            ('period_id', 'in', period_ids),
            ('partner_id', '=', wizard.consignor_partner_id.id),
        ])
        ignore_move_line_ids = ignore_invoices.mapped('move_id.line_id').ids

        account_id = wizard.consignor_partner_id.consignment_account_id.id
        journals = journal_obj.search([
            ('type', 'in', ['sale', 'sale_refund'])])

        # Get lines to commission
        return line_obj.search([
            ('period_id', 'in', period_ids),
            ('account_id', '=', account_id),
            ('journal_id', 'in', journals.ids),
            ('consignment_invoice_id', '=', False),
            ('id', 'not in', ignore_move_line_ids),
        ], order='date, move_id, tax_code_id')
