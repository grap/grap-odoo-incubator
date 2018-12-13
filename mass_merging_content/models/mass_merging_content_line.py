# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import _, api, fields, models
from openerp.exceptions import ValidationError


class MassMergingContentLine(models.Model):
    _name = 'mass.merging.content.line'

    _OPERATION_TYPE_SELECTION = [
        ('ignored', 'Ignored'),
        ('sum', 'Sum Values'),
        ('group_by', 'Group'),
    ]

    merging_content_id = fields.Many2one(
        comodel_name='mass.merging.content', ondelete='cascade')

    field_id = fields.Many2one(
        comodel_name='ir.model.fields', string='Field', required=True,
        domain="[('model', '=', parent.one2many_model)]")

    field_type = fields.Char(
        compute='_compute_field_type', string='Field type')

    operation_type = fields.Selection(
        string='Operation Type', required=True,
        selection=_OPERATION_TYPE_SELECTION)

    @api.multi
    @api.depends('field_id')
    def _compute_field_type(self):
        for line in self:
            line.field_type = line.field_id.ttype

    # Constraint Section
    @api.constrains('field_id', 'merging_content_id')
    def _check_field_id(self):
        for line in self:
            if line.field_id.model != line.merging_content_id.one2many_model:
                raise ValidationError(_(
                    "The selected field '%s' must belong to the model of"
                    " the Field to Sort.") % (line.field_id.field_description))

    @api.model
    def _is_technical_field(self, field):
        return field.name in [
            'create_date', 'create_uid', 'display_name', 'id',
            '__last_update', 'write_date', 'write_uid']

    @api.model
    def _prepare_line(self, field):
        if field.ttype in ('many2one', 'many2many'):
            operation_type = 'group_by'
        else:
            operation_type = 'ignored'
        return {
            'field_id': field.id,
            'operation_type': operation_type,
        }
