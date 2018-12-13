# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import _, api, fields, models


class MassMergingContent(models.Model):
    _name = 'mass.merging.content'
    _inherit = 'mass.operation.mixin'

    # Overwrite Section
    _wizard_model_name = 'mass.merging.content.wizard'

    one2many_field_id = fields.Many2one(
        comodel_name='ir.model.fields', string='Field to Sort', required=True,
        domain="[('model_id', '=', model_id),('ttype', '=', 'one2many')]")

    one2many_model = fields.Char(
        related='one2many_field_id.relation', readonly=True, store=True,
        help="Technical field, used in the model 'mass.merging.content.line'")

    line_ids = fields.One2many(
        comodel_name='mass.merging.content.line',
        inverse_name='merging_content_id', string='Sorting Criterias')

    @api.onchange('one2many_field_id')
    def onchange_one2many_field_id(self):
        self.ensure_one()
        IrModelFields = self.env['ir.model.fields']
        ContentLine = self.env['mass.merging.content.line']
        self.line_ids.unlink()
        if self.one2many_field_id:
            line_ids_vals = []
            fields = IrModelFields.search(
                [('model', '=', self.one2many_field_id.relation)])
            for field in fields:
                if ContentLine._is_technical_field(field):
                    continue
                print ">>>>>>>>>>>>>>>>>"
                print field.name
                vals = ContentLine._prepare_line(field)
                line_ids_vals.append((0, 0, vals))
            print line_ids_vals
            self.line_ids = line_ids_vals

    # Overwrite Section
    @api.multi
    def _get_action_name(self):
        self.ensure_one()
        return _("Merge Content (%s)" % (self.name))
