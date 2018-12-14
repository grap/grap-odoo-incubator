# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import _, api, fields, models


class MassLinkingContent(models.Model):
    _name = 'mass.linking'
    _inherit = 'mass.operation.mixin'

    # Overwrite Section
    _wizard_model_name = 'mass.linking.wizard'

    many2one_field_id = fields.Many2one(
        comodel_name='ir.model.fields', string='Target Field', required=True,
        domain="[('model_id', '=', model_id), ('ttype', '=', 'many2one')]")

    many2one_field_model_name = fields.Char(
        related='many2one_field_id.relation')

    target_action_id = fields.Many2one(
        comodel_name='ir.actions.act_window', string='Target Action',
        domain="[('res_model', '=', many2one_field_model_name)]")

    # Overwrite Section
    @api.multi
    def _get_action_name(self):
        self.ensure_one()
        return _("See (%s)" % (self.name))

    @api.model
    def create(self, vals):
        print "------------------------"
        print vals
        vals.pop('many2one_field_model_name', False)
        return super(MassLinkingContent, self).create(vals)
