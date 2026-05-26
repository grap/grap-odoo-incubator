# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class CreateRecursiveMixin(models.AbstractModel):
    _name = "create.recursive.mixin"
    _description = "Mixin providing recurring creation of parents"

    def _create_recursive_get_or_create_parent_id(self, item_name):
        data = self.name_search(name=item_name, operator="=")
        if data:
            return data[0][0]
        else:
            parent_id, _parent_name = self.name_create(item_name)
            return parent_id

    # Workaround.
    # If a model, like (product.category), overwrite the name_create
    # function, it will fail, so we add that workaround.
    @api.model
    def name_create(self, name):
        return self._name_create(name)

    @api.model
    def _name_create(self, name):
        """Natively, this function is called if a search of 'name' fails
        to create simply an item, with {'name': name} value.
        This overload will alter the function if the name contains a '/'.
        For exemple, if the name is 'Parent / Child', it will not create
        an item with such name. It will:
        - search an item named 'Parent' (or create it if it doesn't exist)
        - then, create an item named 'Child' with the parent found as parent_id.
        """
        vals = {}
        self._create_recursive_alter_vals(vals, name)

        item = self.create(vals)
        return item.name_get()[0]

    @api.model
    def _create_recursive_alter_vals(self, vals, name=False):
        name = name and name or vals.get("name", "")
        if "/" in name:
            splitted_name = name.split("/")
            parent_name = (" / ".join([x.strip() for x in splitted_name[:-1]])).strip()
            item_name = splitted_name[-1:][0].strip()
            parent_id = self._create_recursive_get_or_create_parent_id(parent_name)
            vals.update({"name": item_name, "parent_id": parent_id})
        else:
            vals.update({"name": name})

    @api.model_create_multi
    def create(self, vals_list):
        if self.env.context.get("imported_model") == self._name:
            result = self
            # Creation from import of model
            # create parents if doesn't exist
            # Note: we explicitely break the create_multi
            # because other it generates duplicates
            for vals in vals_list:
                self._create_recursive_alter_vals(vals)
                result |= super().create(vals)
            return result
        else:
            # Regular creation, removing bad "/"
            for vals in vals_list:
                if "name" in vals:
                    vals["name"] = vals["name"].replace("/", "-").strip()
            return super().create(vals_list)

    def write(self, vals):
        if "name" in vals:
            vals["name"] = vals["name"].replace("/", "-").strip()
        return super().write(vals)
