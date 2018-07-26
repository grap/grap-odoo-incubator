# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, models
from openerp.exceptions import Warning as UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Overload Section
    @api.model
    def create(self, vals):
        res = super(ProductTemplate, self).create(vals)
        res._check_access_fiscal_classification(vals)
        return res

    @api.multi
    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        self._check_access_fiscal_classification(vals)
        return res

    # Custom Section
    @api.multi
    def _check_access_fiscal_classification(self, vals):
        classification_obj = self.env['account.product.fiscal.classification']
        if vals.get('fiscal_classification_id', False):
            classification = classification_obj.browse(
                vals['fiscal_classification_id'])
            group = classification.usage_group_id
            if group and group.id not in self.env.user.groups_id.ids:
                raise UserError(_(
                    "You can not use the fiscal classification '%s' because"
                    " you're not member of the group '%s'.") % (
                        classification.name, group.name))
