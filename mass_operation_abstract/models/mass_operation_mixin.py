# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import _, api, fields, models


class MassOperationMixin(models.AbstractModel):
    _name = 'mass.operation.mixin'

    # To Overload Section
    _action_pattern_name = False

    _wizard_model_name = False

    # Column Section
    name = fields.Char(string='Name', translate=True, required=True)

    model_id = fields.Many2one(
        comodel_name='ir.model', string='Model', required=True)

    action_id = fields.Many2one(
        comodel_name='ir.actions.act_window', string='Sidebar Action',
        readonly=True, copy=False)

    value_id = fields.Many2one(
        comodel_name='ir.values', string='Sidebar Button', readonly=True,
        copy=False)

    # Overload Section
    @api.multi
    def unlink(self):
        self.unlink_action()
        return super(MassOperationMixin, self).unlink()

    @api.multi
    def copy(self, default=None):
        default = default or {}
        default.update({
            'name': _('%s (copy)') % self.name})
        return super(MassOperationMixin, self).copy(default=default)

    # Custom Section
    @api.multi
    def create_action(self):
        action_obj = self.env['ir.actions.act_window']
        values_obj = self.env['ir.values']
        for mixin in self:
            button_name = _(self._action_pattern_name) % mixin.name
            mixin.action_id = action_obj.create({
                'name': button_name,
                'type': 'ir.actions.act_window',
                'res_model': self._wizard_model_name,
                'src_model': mixin.model_id.model,
                'view_type': 'form',
                'context': "{'mass_operation_mixin_id' : %d}" % (mixin.id),
                'view_mode': 'form,tree',
                'target': 'new',
            })
            mixin.value_id = values_obj.create({
                'name': button_name,
                'model': mixin.model_id.model,
                'key2': 'client_action_multi',
                'value': (
                    "ir.actions.act_window,%s" % mixin.action_id.id),
            })

    @api.multi
    def unlink_action(self):
        for mixin in self:
            if mixin.action_id:
                mixin.action_id.unlink()
            if mixin.value_id:
                mixin.value_id.unlink()
