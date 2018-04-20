# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class SaleOrderMassActionWizard(models.TransientModel):
    _name = 'sale.order.mass.action.wizard'

    # Column Section
    confirmable_order_qty = fields.Integer(
        string='Confirmable Order Quantity', readonly=True,
        default=lambda s: s._default_confirmable_order_qty())

    confirm = fields.Boolean(
        string='Confirm', default=True, help="check this box if you want to"
        " confirm all the selected quotations.")

    finishable_order_qty = fields.Integer(
        string='Finishable Order Quantity', readonly=True,
        default=lambda s: s._default_finishable_order_qty())

    finish = fields.Boolean(
        'Manually Set To Done', default=True, help="check this box if you"
        "manually set to done selected orders.")

    # compute Section
    @api.model
    def _get_confirmable_order_ids(self):
        so_obj = self.env['sale.order']
        return so_obj.search([
            ('id', 'in', self.env.context.get('active_ids', [])),
            ('state', '=', 'draft')])

    @api.model
    def _get_finishable_order_ids(self):
        so_obj = self.env['sale.order']
        return so_obj.search([
            ('id', 'in', self.env.context.get('active_ids', [])),
            ('state', '=', 'progress')])

    @api.model
    def _default_confirmable_order_qty(self):
        return len(self._get_confirmable_order_ids())

    @api.model
    def _default_finishable_order_qty(self):
        return len(self._get_finishable_order_ids())

    @api.multi
    def apply_button(self):
        self.ensure_one()
        if self.confirm:
            orders = self._get_confirmable_order_ids()
            for order in orders:
                order.action_button_confirm()
        if self.finish:
            orders = self._get_finishable_order_ids()
            orders.write({'state': 'done'})
