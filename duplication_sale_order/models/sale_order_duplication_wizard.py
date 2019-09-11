# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Quentin DUPONT (https://twitter.com/pondupont)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class SaleOrderDuplicationWizard(models.TransientModel):
    _name = 'sale.order.duplication.wizard'

    _DUPLICATION_TYPE_KEYS = [
        ('week', 'Weekly'),
        ('month', 'Monthly'),
    ]

    # Column Section
    order_id = fields.Many2one(
        comodel_name='sale.order', string='Sale Order', readonly=True,
        default=lambda s: s._default_order_id())

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
        default='week', required=True)

    duplication_duration = fields.Integer(
        string='Duplication Duration', required=True, default=0)

    date_line_ids = fields.One2many(
        comodel_name='sale.order.duplication.wizard.date.line',
        inverse_name='wizard_id', string='New Dates')

    # Default Section
    @api.model
    def _default_order_id(self):
        return self.env.context.get('active_id', False)

    @api.model
    def _default_partner_id(self):
        order_obj = self.env['sale.order']
        order_id = self.env.context.get('active_id', False)
        if not order_id:
            return False
        else:
            return order_obj.browse(order_id).partner_id

    @api.model
    def _default_begin_date(self):
        order_obj = self.env['sale.order']
        order_id = self.env.context.get('active_id', False)
        if not order_id:
            return False
        else:
            return order_obj.browse(order_id).date_order.strftime('%Y-%m-%d')

    # View Section
    @api.onchange(
        'begin_date', 'duplication_type', 'duplication_duration',
        'include_current_date')
    def onchange_duplication_settings(self):
        self.ensure_one()
        self.date_line_ids = []

        if (self.begin_date and self.duplication_type and
                self.duplication_duration):
            date_line_ids = []
            date_line_ids.append((5, 0, 0))
            begin_index = 0
            end_index = self.duplication_duration
            if not self.include_current_date:
                begin_index += 1
                end_index += 1
            for i in range(begin_index, end_index):
                if self.duplication_type == 'week':
                    current_date =\
                        self.begin_date + datetime.timedelta(weeks=i)
                else:
                    current_date =\
                        self.begin_date + relativedelta(months=i)
                date_line_ids.append((0, 0, {
                    'date': current_date.strftime('%Y-%m-%d'),
                }))
            self.date_line_ids = date_line_ids

    @api.multi
    def duplicate_button(self):
        self._duplicate()
        return True

    @api.multi
    def duplicate_open_button(self):
        order_ids = self._duplicate()
        result = self.env.ref('sale.action_quotations').read()[0]
        result['domain'] =\
            "[('id', 'in', [" + ','.join(map(str, order_ids)) + "])]"
        return result

    @api.multi
    def _duplicate(self):
        self.ensure_one()
        order_ids = []
        for date_line in self.date_line_ids:
            order_ids.append(self.order_id.copy(
                default={'date_order': date_line.date}).id)
        return order_ids
