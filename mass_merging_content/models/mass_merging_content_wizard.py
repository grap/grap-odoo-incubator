# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import api, models


class MassMergingContentWizard(models.TransientModel):
    _name = 'mass.merging.content.wizard'
    _inherit = 'mass.operation.wizard.mixin'

    @api.model
    def _prepare_key(self, group_fields, line):
        res = []
        for field in group_fields:
            if field.ttype == 'many2one':
                res.append(getattr(line, field.name).id)
            elif field.ttype == 'many2many':
                res.append(str(sorted(getattr(line, field.name).ids)))
            else:
                res.append(getattr(line, field.name))
        return str(res)

    @api.multi
    def _apply_operation(self, items):
        merging_content = self._get_mass_operation()
        group_fields = merging_content._get_group_fields()
        sum_field_names = merging_content._get_sum_field_names()
        read_field_names = sum_field_names
        for item in items:
            lines = getattr(item, merging_content.one2many_field_id.name)
            grouped_data = {}
            for line in lines:
                key = self._prepare_key(group_fields, line)
                if key not in grouped_data.keys():
                    print key
                    grouped_data[key] = {
                        'first_item': line,
                        'delete_line_ids': [],
                        'vals': {x: False for x in read_field_names},
                    }
                else:
                    grouped_data[key]['delete_line_ids'].append(line.id)
                for sum_field_name in sum_field_names:
                    grouped_data[key]['vals'][sum_field_name] +=\
                        getattr(line, sum_field_name)

            for key, data in grouped_data.iteritems():
                # Update the first item
                data['first_item'].write(data['vals'])
                delete_ids = grouped_data[key]['delete_line_ids']

                # Drop obsolete lines
                if delete_ids:
                    lines.filtered(lambda x: x.id in delete_ids).unlink()
