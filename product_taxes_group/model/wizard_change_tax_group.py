# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields
from openerp.osv.orm import TransientModel


class WizardChangeTaxGroup(TransientModel):
    """Wizard to allow to change the Tax Group of products."""
    _name = "wizard.change.tax.group"

    def change_tax_group(self, cr, uid, ids, context=None):
        pt_obj = self.pool['product.template']
        for wctg in self.browse(cr, uid, ids, context=context):
            pt_ids = [
                x.product_tmpl_id.id
                for x in wctg.old_tax_group_id.product_ids]
            pt_obj.write(cr, uid, pt_ids, {
                'tax_group_id': wctg.new_tax_group_id.id}, context=context)
        return {}

    _columns = {
        'old_tax_group_id': fields.many2one(
            'tax.group', 'Old Tax Group', required=True, readonly=True),
        'new_tax_group_id': fields.many2one(
            'tax.group', 'New Tax Group', required=True,
            domain="""[('id', '!=', old_tax_group_id)]"""),
    }

    _defaults = {
        'old_tax_group_id': lambda self, cr, uid, ctx: ctx and ctx.get(
            'active_id', False) or False
    }
