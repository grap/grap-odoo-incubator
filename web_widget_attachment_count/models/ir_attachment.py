# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from openupgradelib import openupgrade
from psycopg2.extensions import AsIs

from odoo import api, models

logger = logging.getLogger(__name__)


class IrAttachment(models.AbstractModel):
    _inherit = "ir.attachment"

    def _get_attachment_count_models(self):
        return []

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        res._recompute_attachment_count_for_related_items()
        return res

    def write(self, vals):
        res = super().write(vals)
        if "res_id" in vals:
            self._recompute_attachment_count_for_related_items()
        return res

    @api.multi
    def unlink(self):
        to_update = {}
        for model in self._get_attachment_count_models():
            to_update[model] = self.filtered(lambda x: x.res_model == model).mapped(
                "res_id"
            )
        res = super().unlink()
        for model, item_ids in to_update.items():
            self.env[model].browse(item_ids)._compute_message_attachment_count()
        return res

    @api.multi
    def _recompute_attachment_count_for_related_items(self):
        for attachment in self:
            for model in self._get_attachment_count_models():
                item_ids = attachment.filtered(lambda x: x.res_model == model).mapped(
                    "res_id"
                )
                self.env[model].browse(item_ids)._compute_message_attachment_count()

    @api.model
    def _store_attachment_count_value(self, table_name, model_name):
        logger.info(
            "Storing 'message_attachment_count' in the table %s ..." % (table_name)
        )
        if not openupgrade.column_exists(
            self.env.cr, table_name, "message_attachment_count"
        ):
            self.env.cr.execute(
                """
                ALTER TABLE %s ADD COLUMN message_attachment_count integer;""",
                (AsIs(table_name),),
            )
        self.env.cr.execute(
            """
            UPDATE %s ai
            SET message_attachment_count = temporary_table.qty
            FROM (
                SELECT
                    res_id,
                    count(*) as qty
                FROM ir_attachment ia
                WHERE ia.res_model = %s
                GROUP BY res_id
            ) as temporary_table
            WHERE temporary_table.res_id = ai.id;

;""",
            (AsIs(table_name), model_name),
        )
