# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID, api


def _hook_store_attachment_count_value(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env["ir.attachment"]._store_attachment_count_value(
        "account_invoice", "account.invoice"
    )
