# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

_NOT_COPIED_FIELDS = [
    "id",
    "__last_update",
    "create_uid",
    "create_date",
    "write_uid",
    "write_date",
]


class SynchronizationData(models.Model):
    _name = "synchronization.data"
    _order = "model"
    _inherit = ["synchronization.mixin"]
    _description = "Odoo Data Synchronisation"
    _rec_name = "model"

    model_id = fields.Many2one(comodel_name="ir.model", string="Model", required=True)

    mapping_ids = fields.One2many(
        comodel_name="synchronization.mapping", inverse_name="synchronization_data_id"
    )

    mapping_qty = fields.Integer(
        string="Mapping Quantity", compute="_compute_mapping_qty", store=True
    )

    model = fields.Char(related="model_id.model", string="Model Name", store=True)

    ignored_field_ids = fields.Many2many(
        comodel_name="ir.model.fields", string="Ignored Fields"
    )

    active = fields.Boolean(string="Active", default=True)

    _sql_constraints = [
        ("unique_model_id", "unique(model_id)", "Model should be unique"),
    ]

    @api.depends("mapping_ids")
    def _compute_mapping_qty(self):
        for data in self:
            data.mapping_qty = len(data.mapping_ids)

    @api.onchange("model_id")
    def _onchange_model_id(self):
        return {
            "domain": {
                "ignored_field_ids": [
                    ("model", "=", self.model_id.model),
                ],
            }
        }

    def action_synchronize(self):
        for synchronization in self:
            synchronization._synchronize()

    def action_full_synchronize(self):
        for synchronization in self:
            synchronization._synchronize(force_update=True)

    def _synchronize(self, force_update=False):
        self.ensure_one()
        right_now = fields.Datetime.now()

        SynchronisationMapping = self.env["synchronization.mapping"]
        TargetModel = self.env[self.model_id.model]

        # Get External access
        external_odoo = self._get_external_odoo()
        external_model = external_odoo.env[self.model_id.model]
        external_datas = external_model.with_context(active_test=False).search_read([])

        _tmp_data = external_odoo.env["ir.model.data"].search_read(
            [("model", "=", self.model_id.model)], ["complete_name", "res_id"]
        )
        external_xml_id_datas = {
            x["res_id"]: x["complete_name"]
            for x in _tmp_data
            if not x["complete_name"].startswith("__export__.")
        }

        _tmp_data = SynchronisationMapping.search_read(
            [("model_id", "=", self.model_id.id)],
            ["external_id", "internal_id", "write_date"],
        )
        mapping_external_2_local = {
            x["external_id"]: {
                "internal_id": x["internal_id"],
                "mapping_id": x["id"],
                "write_date": x["write_date"],
            }
            for x in _tmp_data
        }

        for external_data in external_datas:
            external_id = external_data["id"]
            if external_id not in mapping_external_2_local:
                # We create the mapping first
                if external_id in external_xml_id_datas:
                    # If we map for the first time,
                    # we should synchronize data
                    to_update = True

                    xml_id = external_xml_id_datas[external_id]
                    module, name = xml_id.split(".")
                    # This is an xml data we map with local existing data
                    local_datas = self.env["ir.model.data"].search(
                        [("module", "=", module), ("name", "=", name)]
                    )
                    if not local_datas:
                        raise UserError(_("xml id not found %s") % (xml_id))
                    else:
                        # we map with the local data
                        internal_id = local_datas[0]["res_id"]
                        _logger.info(
                            "Model : {model}. mapped external"
                            " #{external_id} with local #{internal_id}"
                            " based on the xml_id {xml_id}".format(
                                model=self.model_id.model,
                                external_id=external_id,
                                internal_id=internal_id,
                                xml_id=xml_id,
                            )
                        )

                else:
                    xml_id = False
                    to_update = False
                    _logger.info(
                        "Model : {model}. Create new item, based on the"
                        " external #{external_id}".format(
                            model=self.model_id.model,
                            external_id=external_id,
                        )
                    )
                    internal_id = TargetModel.create(
                        self._prepare_values(external_data)
                    ).id

                mapping = SynchronisationMapping.create(
                    {
                        "synchronization_data_id": self.id,
                        "external_id": external_id,
                        "internal_id": internal_id,
                        "xml_id": xml_id,
                    }
                )

            else:
                # The mapping has been done previously
                _local_info = mapping_external_2_local[external_data["id"]]
                internal_id = _local_info["internal_id"]
                local_write_date = _local_info["write_date"]
                external_write_date = datetime.strptime(
                    external_data["write_date"], "%Y-%m-%d %H:%M:%S"
                )
                to_update = force_update or (external_write_date > local_write_date)
                mapping = SynchronisationMapping.browse(_local_info["mapping_id"])

            if to_update:
                _logger.info(
                    "Updating %s#%d (External #%d)"
                    % (self.model, internal_id, external_data["id"])
                )
                # Update Target Item
                internal_item = TargetModel.browse(internal_id)
                internal_item.write(self._prepare_values(external_data))
                # Update mapping last update
                mapping.write({"write_date": right_now})

    def _prepare_values(self, external_data):
        SynchronisationMapping = self.env["synchronization.mapping"]

        self.ensure_one()
        res = {}
        for k, v in external_data.items():
            if k in _NOT_COPIED_FIELDS:
                continue

            if k in self.mapped("ignored_field_ids.name"):
                continue

            field = self.env["ir.model.fields"].search(
                [
                    ("model_id", "=", self.model_id.id),
                    ("name", "=", k),
                ],
                limit=1,
            )
            if not field:
                _logger.warning(
                    "Model {model}. the field {field}"
                    " doesn't exist in the local data model.".format(
                        model=self.model_id.name, field=k
                    )
                )
                continue

            if field.ttype == "many2one":
                mapping = SynchronisationMapping.search(
                    [
                        ("model", "=", field.relation),
                        ("external_id", "=", v),
                    ],
                    limit=1,
                )
                if mapping:
                    res[k] = mapping.internal_id
                else:
                    raise NotImplementedError("many2one: " + k)
            elif field.ttype == "many2many":
                raise NotImplementedError("many2many: " + k)
            else:
                res[k] = v

        return res
