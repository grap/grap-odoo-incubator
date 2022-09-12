# Copyright (C) 2022-Today: La Louve (<http://www.lalouve.net/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductPrintCategoryMixin(models.AbstractModel):
    _name = "product.print.category.mixin"
    _description = "Abstract Model for Product Print Categories"

    @api.multi
    def _update_to_print_values(self, vals):
        # This function work for item that are product.product and product.template
        to_update_item_ids = []
        # Set 'To print' if we change one field choosen in print_category
        for item in self.filtered(lambda x: x.print_category_id):
            triggering_fields = item.print_category_id.field_ids.mapped("name") + [
                "print_category_id"
            ]
            if len(list(set(vals.keys()) & set(triggering_fields))):
                to_update_item_ids.append(item.id)
        to_update_items = self.browse(to_update_item_ids)
        # This function is called from the write of the current RecordSet :
        # prevent an infinite loop by calling the function super
        super(ProductPrintCategoryMixin, to_update_items).write({"to_print": True})
