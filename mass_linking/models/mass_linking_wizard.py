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
        ids = items.mapped(mass_linking.many2one_field_id.name).ids
        model_name = mass_linking.model_id.model
        domain = "[('id','in',[" + ','.join(map(str, ids)) + "])]"
        action = {
            'name': 'FROMAGE',
            'type': 'ir.actions.act_window',
            'res_model': model_name,
            'view_type': 'form',
            'view_mode': 'tree,form',
            'target': 'self',
            'domain': domain,
        }

        # action.pop('views')
        # action.pop('view_id')
        # action.pop('view_ids')
        for k in sorted(action.keys()):
            print "===== %s" % k
            print action[k]
        print ">>>>>>>>>>>>>>>>>>>><"
        print ">>>>>>>>>>>>>>>>>>>><"
        import pdb; pdb.set_trace()
        return action

        # action = mass_linking.target_action_id
        # result = action.read()[0]
        # import pdb; pdb.set_trace()
        # result['domain'] = domain
        # print result
        # import pdb; pdb.set_trace()
        # return result
        # result = self.pool['ir.model.data']
        # .xmlid_to_res_id(cr, uid, 'sale.action_order_line_product_tree',
        # raise_if_not_found=True)
        # result = self.pool['ir.actions.act_window'].read
        # (cr, uid, [result], context=context)[0]
        # return result
