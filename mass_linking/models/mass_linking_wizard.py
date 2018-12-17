# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import api, models


class MassLinkingWizard(models.TransientModel):
    _name = 'mass.linking.wizard'
    _inherit = 'mass.operation.wizard.mixin'

    @api.multi
    def _apply_operation(self, items):
        mass_linking = self._get_mass_operation()
        # Compute Domain
        ids = items.mapped(mass_linking.technical_relation).ids
        domain = "[('id','in',[" + ','.join(map(str, ids)) + "])]"

        # Use Defined action if defined
        if mass_linking.target_action_id:
            action = mass_linking.target_action_id
            result = action.read()[0]
            result['domain'] = domain
        else:
            # Otherwise, return a default action
            model_name = mass_linking.link_field_model_name
            view_mode = 'tree,form'  # TODO FIXME
            result = {
                'domain': domain,
                'res_model': model_name,
                'target': 'current',
                'type': 'ir.actions.act_window',
                'view_mode': view_mode,
            }

        return result
