# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
import odoorpc

from odoo import api, fields, models

from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

_NOT_COPIED_FIELDS = [
    "id", "__last_update",
    "create_uid", "create_date",
    "write_uid", "write_date",
]


class SynchronizationData(models.Model):
    _name = "synchronization.data"
    _description = "Odoo Data Synchronisation"

    model_id = fields.Many2one(
        comodel_name="ir.model", string="Model")

    model = fields.Char(
        related="model_id.model", string="Model Name", store=True)

    ignored_field_ids = fields.Many2many(
        comodel_name="ir.model.fields", string="Ignored Fields")

    active = fields.Boolean(string="Active", default="True")

    @api.onchange('model_id')
    def _onchange_model_id(self):
        return {
            'domain': {
                'ignored_field_ids': [
                    ('model', '=', self.model_id.model),
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
        IrConfigParameter = self.env['ir.config_parameter'].sudo()
        port = IrConfigParameter.get_param("database_synchronization.port")
        host = IrConfigParameter.get_param("database_synchronization.host")
        database = IrConfigParameter.get_param(
            "database_synchronization.database")
        login = IrConfigParameter.get_param("database_synchronization.login")
        password = IrConfigParameter.get_param(
            "database_synchronization.password")

        SynchronisationMapping = self.env["synchronization.mapping"]
        TargetModel = self.env[self.model_id.model]

        if port == 443:
            protocol = "jsonrpc+ssl"
        else:
            protocol = "jsonrpc"
        external_odoo = odoorpc.ODOO(host, protocol, port=port)
        external_odoo.login(database, login, password)

        external_model = external_odoo.env[self.model_id.model]

        external_datas = external_model.with_context(
            active_test=False).search_read([])

        _tmp_data =\
            external_odoo.env["ir.model.data"].search_read(
                [("model", "=", self.model_id.model)],
                ["complete_name", "res_id"]
            )
        external_xml_id_datas = {
            x["res_id"]: x["complete_name"]
            for x in _tmp_data
            if not x["complete_name"].startswith("__export__.")
        }

        _tmp_data = SynchronisationMapping.search_read(
            [("model_id", "=", self.model_id.id)],
            ["external_id", "internal_id"],
        )
        mapping = {x["external_id"]: x["internal_id"] for x in _tmp_data}

        for external_data in external_datas:
            check_update = True
            external_id = external_data["id"]
            if external_id not in mapping:
                # We should create the mapping first

                if external_id in external_xml_id_datas:
                    xml_id = external_xml_id_datas[external_id]
                    module, name = xml_id.split(".")
                    # This is an xml data we map with local exsiting data
                    local_datas = self.env["ir.model.data"].search(
                        [("module", "=", module), ("name", "=", name)]
                    )
                    if not local_datas:
                        raise UserError("xml id not found %s" % (xml_id))
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
                                xml_id=xml_id))

                else:
                    _logger.info(
                        "Model : {model}. Create new item, based on the"
                        " external #{external_id}".format(
                            model=self.model_id.model,
                            external_id=external_id,
                        ))
                    check_update = False
                    internal_id = TargetModel.create(self._prepare_values(
                        external_data)).id

                SynchronisationMapping.create({
                    "model_id": self.model_id.id,
                    "external_id": external_id,
                    "internal_id": internal_id,
                    })

            else:
                internal_id = mapping[external_data["id"]]

            if check_update or force_update:
                print("todo, check update")

    def _prepare_values(self, external_data):
        SynchronisationMapping = self.env["synchronization.mapping"]

        self.ensure_one()
        res = {}
        for k, v in external_data.items():
            if k in _NOT_COPIED_FIELDS:
                continue

            if k in self.mapped("ignored_field_ids.name"):
                continue

            field = self.env["ir.model.fields"].search([
                ("model_id", "=", self.model_id.id),
                ("name", "=", k),
            ], limit=1)
            if not field:
                _logger.warning(
                    "Model {model}. the field {field}"
                    " doesn't exist in the local data model.".format(
                        model=self.model_id.name,
                        field=k))
                continue

            if field.ttype == "many2one":
                mapping = SynchronisationMapping.search([
                    ("model", "=", field.relation),
                    ("external_id", "=", v),
                ], limit=1)
                if mapping:
                    res[k] = mapping.internal_id
                else:
                    raise NotImplementedError("many2one: " + k)
            elif field.ttype == "many2many":
                raise NotImplementedError("many2many: " + k)
            else:
                res[k] = v

        return res
