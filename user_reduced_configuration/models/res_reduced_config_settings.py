# Part of Odoo. See LICENSE file for full copyright and licensing details.

from lxml import etree

from odoo import api, models


class ResReducedConfigSettings(models.TransientModel):
    _name = "res.reduced.config.settings"
    _inherit = "res.config.settings"
    _description = "Reduced Configuration Settings"

    @api.model_create_multi
    def create(self, vals_list):
        return super(
            ResReducedConfigSettings, self.with_context(reduced_configuration=True)
        ).create(vals_list)

    def _get_allowed_fields(self):
        return self.env.user.mapped(
            "groups_id.reduced_configuration_line_ids.field_id.name"
        )

    def execute(self):
        """
        OVERWRITE res.config.settings execute function.
        - remove all the 'module' part. Install / uninstall modules
          is prohibited in 'reduced configuration' mode.
        - call 'set_value()' with a context, to reduce the field that
          can be written.
        """
        self.ensure_one()
        self.with_context(execute_in_reduced_configuration_context=True).set_values()

        # force client-side reload because set_values could have ignored some
        # values
        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }

    def _get_classified_fields(self, fnames=None):
        """Overload the original function to reduce the list of field name.
        Return only fields that are allowed for the current user.
        Note that all the module name are removed anyway.

        This list is used by 'execute' function."""
        allowed_fields = self._get_allowed_fields()

        classified = super()._get_classified_fields(fnames=fnames)

        if not self.env.context.get("execute_in_reduced_configuration_context", False):
            return classified

        reduced_classified = {"default": [], "group": [], "config": [], "module": []}

        for name, model, field in classified["default"]:
            if name in allowed_fields:
                reduced_classified["default"].append((name, model, field))

        for name, groups, implied_group in classified["group"]:
            if name in allowed_fields:
                reduced_classified["group"].append((name, groups, implied_group))

        for name, icp in classified["config"]:
            if name in allowed_fields:
                reduced_classified["config"].append((name, icp))

        return reduced_classified

    @api.model
    def get_view(self, view_id=None, view_type="form", **kwargs):
        """Try to hide configuration that is forbidden for the current user.
        However, it's quite hard to display exactly only the field he has right
        to access.
        For the time being, this function:
        - hide all 'o_settings_container' that don't contain any allowed fields.
        - hide all 'o_setting_box' that don't contain any allowed fields.
        """

        allowed_fields = self._get_allowed_fields()
        res = super().get_view(view_id, view_type, **kwargs)
        if view_type != "form":
            return res

        arch = etree.XML(res["arch"])
        for container_div in arch.xpath('//div[hasclass("o_settings_container")]'):
            found = False
            for field_name in allowed_fields:
                for element in [x for x in container_div.iterdescendants()]:
                    if element.tag == "field" and element.get("name") == field_name:
                        found = True
                        break
            if not found:
                container_div.attrib["class"] = "d-none"

        for container_div in arch.xpath('//div[hasclass("o_setting_box")]'):
            found = False
            for field_name in allowed_fields:
                for element in [x for x in container_div.iterdescendants()]:
                    if element.tag == "field" and element.get("name") == field_name:
                        found = True
                        break
            if not found:
                container_div.attrib["class"] = "d-none"

        res["arch"] = etree.tostring(arch, encoding="unicode").replace("\t", "")

        return res
