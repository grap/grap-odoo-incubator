# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import _, api, fields, models


class MassLinking(models.Model):
    _name = 'mass.linking'
    _inherit = 'mass.operation.mixin'

    # Overwrite Section
    _wizard_model_name = 'mass.linking.wizard'

    @api.multi
    def _prepare_action_name(self):
        self.ensure_one()
        return _("See (%s)" % (self.name))

    # Column Section
    link_field_1_id = fields.Many2one(
        comodel_name='ir.model.fields', string='Field #1', required=True,
        domain="[('model_id', '=', model_id), ('relation', '!=', '')]")

    link_field_1_model_id = fields.Many2one(
        string='Field #1 Model', comodel_name='ir.model',
        compute='_compute_link_field_1_model_id', store=True)

    link_field_2_id = fields.Many2one(
        comodel_name='ir.model.fields', string='Field 2',
        domain="[('model_id', '=', link_field_1_model_id),"
        " ('relation', '!=', '')]")

    link_field_2_model_id = fields.Many2one(
        string='Field #2 Model', comodel_name='ir.model',
        compute='_compute_link_field_2_model_id', store=True)

    link_field_3_id = fields.Many2one(
        comodel_name='ir.model.fields', string='Field 3',
        domain="[('model_id', '=', link_field_2_model_id),"
        " ('relation', '!=', '')]")

    link_field_3_model_id = fields.Many2one(
        string='Field #3 Model', comodel_name='ir.model',
        compute='_compute_link_field_3_model_id', store=True)

    link_field_id = fields.Many2one(
        comodel_name='ir.model.fields', string='Final Target Field',
        compute='_compute_link', store=True)

    technical_relation = fields.Char(
        string='Technical Relation', compute='_compute_link', store=True)

    link_field_model_name = fields.Char(
        related='link_field_id.relation', readonly=True)

    target_action_id = fields.Many2one(
        comodel_name='ir.actions.act_window', string='Target Action',
        domain="[('res_model', '=', link_field_model_name)]")

    # compute Section
    @api.multi
    @api.depends('link_field_1_id')
    def _compute_link_field_1_model_id(self):
        IrModel = self.env['ir.model']
        for mass_linking in self:
            models = IrModel.search(
                [('model', '=', mass_linking.link_field_1_id.relation)])
            mass_linking.link_field_1_model_id = models and models[0].id

    @api.multi
    @api.depends('link_field_2_id')
    def _compute_link_field_2_model_id(self):
        IrModel = self.env['ir.model']
        for mass_linking in self:
            models = IrModel.search(
                [('model', '=', mass_linking.link_field_2_id.relation)])
            mass_linking.link_field_2_model_id = models and models[0].id

    @api.multi
    @api.depends('link_field_3_id')
    def _compute_link_field_3_model_id(self):
        IrModel = self.env['ir.model']
        for mass_linking in self:
            models = IrModel.search(
                [('model', '=', mass_linking.link_field_3_id.relation)])
            mass_linking.link_field_3_model_id = models and models[0].id

    @api.multi
    @api.depends('link_field_1_id', 'link_field_2_id', 'link_field_3_id')
    def _compute_link(self):
        for mass_linking in self:
            if mass_linking.link_field_1_id:
                links = [mass_linking.link_field_1_id.name]
                field = mass_linking.link_field_1_id
                if mass_linking.link_field_2_id:
                    links.append(mass_linking.link_field_2_id.name)
                    field = mass_linking.link_field_2_id
                    if mass_linking.link_field_3_id:
                        links.append(mass_linking.link_field_3_id.name)
                        field = mass_linking.link_field_3_id
                mass_linking.technical_relation = '.'.join(links)
                mass_linking.link_field_id = field
