# Copyright (C) 2026 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    env.cr.execute("select distinct(group_id) from reduced_configuration_line")
    for group_id in [x[0] for x in env.cr.fetchall()]:
        env.cr.execute(
            "select field_id from reduced_configuration_line where group_id = %s",
            (group_id,),
        )
        # res = env.cr.fetchall()
        field_ids = [x[0] for x in env.cr.fetchall()]

        env["reduced.configuration"].create(
            {"group_id": group_id, "field_ids": field_ids}
        )
