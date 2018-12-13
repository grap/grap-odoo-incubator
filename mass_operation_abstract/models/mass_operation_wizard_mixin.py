# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError
from openerp.osv import expression
from openerp.tools.safe_eval import safe_eval


class MassOperationWizardMixin(models.AbstractModel):
    _name = 'mass.operation.wizard.mixin'

    # To Overwrite Section
    @api.multi
    def _apply_operation(self, items):
        pass

    # Column Section
    selected_item_qty = fields.Integer(readonly=True)

    removed_item_qty = fields.Integer(readonly=True)

    remaining_item_qty = fields.Integer(readonly=True)

    src_model_id = fields.Many2one(comodel_name='ir.model')

    @api.model
    def default_get(self, fields):
        res = super(MassOperationWizardMixin, self).default_get(fields)

        # Compute items quantity
        active_ids = self.env.context.get('active_ids')
        remaining_items = self._get_remaining_items()

        res.update({
            'selected_item_qty': len(active_ids),
            'remaining_item_qty': len(remaining_items),
            'removed_item_qty': len(active_ids) - len(remaining_items),
            'src_model_id': self._get_src_model().id,
        })
        return res

    @api.multi
    def button_apply(self):
        items = self._get_remaining_items()
        if not len(items):
            raise UserError(_(
                "there is no more element that corresponds to the rules of"
                " the domain.\n Please refresh your list and try to"
                " select again the items."))
        self._apply_operation(items)

    # Private Section
    @api.model
    def _get_mass_operation(self):
        IrModel = self.env['ir.model']
        mass_operation_models = IrModel.search([
            ('model', '=',
                self.env.context.get('mass_operation_mixin_name', False))])
        if len(mass_operation_models) != 1:
            return False
        MassOperationModel = self.env[mass_operation_models[0].model]
        return MassOperationModel.search([
            ('id', '=', self.env.context.get('mass_operation_mixin_id', 0))])

    @api.model
    def _get_src_model(self):
        IrModel = self.env['ir.model']
        models = IrModel.search([
            ('model', '=', self.env.context.get('active_model', False))])
        return models[0]

    @api.model
    def _get_remaining_items(self):
        print ">>>>>>>>>>>>>>>>>>>>>><"
        print self.env.context
        active_ids = self.env.context.get('active_ids')
        mass_operation = self._get_mass_operation()
        if mass_operation.domain != '[]':
            SrcModel = self.env[self._get_src_model().model]
            domain = expression.AND([
                safe_eval(mass_operation.domain),
                [('id', 'in', active_ids)]])
            remaining_items = SrcModel.search(domain)
        else:
            remaining_items = active_ids
        print remaining_items
        print ">>>>>>>>>>>>>>>>>>>>>><"
        return remaining_items
