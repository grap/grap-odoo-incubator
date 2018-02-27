# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import datetime
from dateutil.relativedelta import relativedelta

from openerp import api, fields, models


class AccountInvoiceDuplicationWizard(models.TransientModel):
    _name = 'account.invoice.duplication.wizard'

    _DUPLICATION_TYPE_KEYS = [
        ('week', 'Weekly'),
        ('month', 'Monthly'),
    ]

    invoice_id = fields.Many2one(
        comodel_name='account.invoice', string='Invoice', readonly=True,
        default=lambda s: s._default_invoice_id())

    partner_id = fields.Many2one(
        comodel_name='res.partner', string='Partner', readonly=True,
        default=lambda s: s._default_partner_id())

    begin_date = fields.Date(
        string='Begin Date', required=True,
        default=lambda s: s._default_begin_date())

    include_current_date = fields.Boolean(
        string='Include Current Date', default=False)

    duplication_type = fields.Selection(
        selection=_DUPLICATION_TYPE_KEYS, string='Duplication Type',
        default='month', required=True)

    duplication_duration = fields.Integer(
        string='Duplication Duration', required=True, default=0)

    date_line_ids = fields.One2many(
        comodel_name='account.invoice.duplication.wizard.date.line',
        inverse_name='wizard_id', string='New Dates')

    date_due_duration = fields.Integer(
        string='Due Date Duration', required=True,
        default=lambda s: s._default_date_due_duration())

    # Default Section
    @api.model
    def _default_invoice_id(self):
        return self.env.context.get('active_id', False)

    @api.model
    def _default_partner_id(self):
        invoice_obj = self.env['account.invoice']
        invoice_id = self.env.context.get('active_id', False)
        if not invoice_id:
            return False
        else:
            return invoice_obj.browse(invoice_id).partner_id

    @api.model
    def _default_begin_date(self):
        invoice_obj = self.env['account.invoice']
        invoice_id = self.env.context.get('active_id', False)
        if not invoice_id:
            return False
        else:
            return invoice_obj.browse(invoice_id).date_invoice

    @api.model
    def _default_date_due_duration(self):
        invoice_obj = self.env['account.invoice']
        invoice_id = self.env.context.get('active_id', False)
        if invoice_id:
            invoice = invoice_obj.browse(invoice_id)
            if invoice.date_due and invoice.date_invoice:
                date_invoice = datetime.datetime.strptime(
                    invoice.date_invoice, '%Y-%m-%d')
                due_date = datetime.datetime.strptime(
                    invoice.date_due, '%Y-%m-%d')
                return (due_date - date_invoice).days
        return 0

    # View Section
    @api.onchange(
        'begin_date', 'duplication_type', 'duplication_duration',
        'include_current_date', 'date_due_duration')
    def onchange_duplication_settings(self):
        self.ensure_one()
        self.date_line_ids = []
        if (self.begin_date and self.duplication_type and
                self.duplication_duration):
            date_line_ids = []
            begin_date = datetime.datetime.strptime(
                self.begin_date, '%Y-%m-%d')
            begin_index = 0
            end_index = self.duplication_duration
            if not self.include_current_date:
                begin_index += 1
                end_index += 1
            for i in range(begin_index, end_index):
                if self.duplication_type == 'week':
                    date_invoice =\
                        begin_date + datetime.timedelta(weeks=i)
                else:
                    date_invoice =\
                        begin_date + relativedelta(months=i)
                date_due =\
                    date_invoice + datetime.timedelta(
                        days=self.date_due_duration)
                date_line_ids.append((0, 0, {
                    'date_invoice': date_invoice.strftime('%Y-%m-%d'),
                    'date_due': date_due.strftime('%Y-%m-%d'),
                }))
            self.date_line_ids = date_line_ids

    @api.multi
    def duplicate_button(self):
        self._duplicate()
        return True

    @api.multi
    def duplicate_open_button(self):
        invoice_ids = self._duplicate()
        if self.invoice_id.type == 'out_invoice':
            result = self.env.ref('account.action_invoice_tree1').read()[0]
        elif self.invoice_id.type == 'out_refund':
            result = self.env.ref('account.action_invoice_tree3').read()[0]
        elif self.invoice_id.type == 'in_invoice':
            result = self.env.ref('account.action_invoice_tree2').read()[0]
        elif self.invoice_id.type == 'in_refund':
            result = self.env.ref('account.action_invoice_tree4').read()[0]
        result['domain'] =\
            "[('id', 'in', ["+','.join(map(str, invoice_ids))+"])]"
        return result

    @api.multi
    def _duplicate(self):
        self.ensure_one()
        invoice_ids = []
        for date_line in self.date_line_ids:
            invoice_ids.append(self.invoice_id.copy(default={
                'date_invoice': date_line.date_invoice,
                'date_due': date_line.date_due,
                }).id)
        return invoice_ids
