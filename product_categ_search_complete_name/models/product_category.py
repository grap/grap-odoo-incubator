# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import api, fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'
    _rec_name = 'stored_complete_name'

    # Columns section
    stored_complete_name = fields.Char(
        string='Stored Complete Name', store=True,
        compute='_compute_stored_complete_name')

    # compute Section
    @api.multi
    @api.depends('name', 'parent_id.stored_complete_name')
    def _compute_stored_complete_name(self):
        for category in self:
            if not category.parent_id:
                category.stored_complete_name = category.name
            else:
                category.stored_complete_name = "%s / %s" % (
                    category.parent_id.stored_complete_name, category.name)

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        res = self.search(
            [('stored_complete_name', operator, name)] + (args or []),
            limit=limit)
        return res.name_get()
