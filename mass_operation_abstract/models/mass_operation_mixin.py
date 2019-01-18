# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import _, api, fields, models


class MassOperationMixin(models.AbstractModel):
    _name = 'mass.operation.mixin'

    # To Overwrite Section (Mandatory)
    _wizard_model_name = False

    # To Overwrite Section (Optional)
    @api.multi
    def _prepare_action_name(self):
        return _("Mass Operation (%s)" % (self.name))

    @api.multi
    def _get_model_domain(self):
        return [('osv_memory', '=', False)]

    # Column Section
    name = fields.Char(string='Name', required=True)

    action_name = fields.Char(
        string='Action Name', required=True)

    model_id = fields.Many2one(
        comodel_name='ir.model', string='Model', required=True,
        domain=lambda s: s._get_model_domain())

    action_id = fields.Many2one(
        comodel_name='ir.actions.act_window', string='Sidebar Action',
        readonly=True, copy=False)

    value_id = fields.Many2one(
        comodel_name='ir.values', string='Sidebar Button', readonly=True,
        copy=False)

    groups_id = fields.Many2one(
        comodel_name='res.groups', string='Allowed Groups')

    domain = fields.Char(string='Domain', required=True, default="[]")

    # Onchange Section
    @api.onchange('name')
    def onchange_name(self):
        if self.name and not self.action_name:
            self.action_name = self._prepare_action_name()

    # Action Section
    @api.multi
    def enable_mass_operation(self):
        action_obj = self.env['ir.actions.act_window']
        values_obj = self.env['ir.values']
        for mixin in self:
            if not mixin.action_id:
                mixin.action_id = action_obj.create(mixin._prepare_action())
            if not mixin.value_id:
                mixin.value_id = values_obj.create(mixin._prepare_value())

    @api.multi
    def disable_mass_operation(self):
        for mixin in self:
            if mixin.action_id:
                mixin.action_id.unlink()
            if mixin.value_id:
                mixin.value_id.unlink()

    # Overload Section
    @api.multi
    def unlink(self):
        self.disable_mass_operation()
        return super(MassOperationMixin, self).unlink()

    @api.multi
    def copy(self, default=None):
        default = default or {}
        default.update({'name': _('%s (copy)') % self.name})
        return super(MassOperationMixin, self).copy(default=default)

    # Private Section
    @api.multi
    def _prepare_action(self):
        self.ensure_one()
        return {
            'name': self.action_name,
            'type': 'ir.actions.act_window',
            'res_model': self._wizard_model_name,
            'src_model': self.model_id.model,
            'groups_id': self.groups_id.ids,
            'view_type': 'form',
            'context': """{
                'mass_operation_mixin_id' : %d,
                'mass_operation_mixin_name' : '%s',
            }""" % (self.id, self._name),
            'view_mode': 'form,tree',
            'target': 'new',
        }

    @api.multi
    def _prepare_value(self):
        self.ensure_one()
        return {
            'name': self.action_name,
            'model': self.model_id.model,
            'key2': 'client_action_multi',
            'value': ("ir.actions.act_window,%s" % self.action_id.id),
        }
