# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import functools
import logging

from lxml import etree

from odoo import _, api, models

_logger = logging.getLogger(__name__)

fields_view_get_origin = models.BaseModel.fields_view_get


@api.model
def fields_view_get(self, view_id=None, view_type="form", toolbar=False, submenu=False):
    res = fields_view_get_origin(
        self, view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
    )

    # We make an optional load of the model because this code can be executed
    # on database that have the module database_synchronization installed.
    # see : https://github.com/OCA/OpenUpgrade/issues/2440#issuecomment-800903396
    if "synchronization.data" not in self.env:
        return res

    SynchronizationData = self.env["synchronization.data"]
    synchronizations = SynchronizationData.search([("model", "=", self._name)])
    if synchronizations and view_type == "form":
        doc = etree.XML(res["arch"])
        nodes = doc.xpath("//%s" % (view_type))
        has_access_func = functools.partial(
            self.check_access_rights, raise_exception=False
        )
        has_access = (
            has_access_func("write")
            or has_access_func("create")
            or has_access_func("unlink")
        )
        if has_access and nodes:
            node = nodes[0]
            title = _("Readonly Table")
            message = _(
                "Do not create, update or unlink items of this model, as the table is"
                " synchronized with another Odoo Master instance. Instead, you can log"
                " on the Odoo Master instance and make the required changes."
            )
            element = etree.fromstring(
                "<div class='alert-danger'><h1>{title}</h1>{message}</div>".format(
                    title=title, message=message
                )
            )
            node.insert(0, element)
            res["arch"] = etree.tostring(doc, encoding="unicode")
    return res


models.BaseModel.fields_view_get = fields_view_get
