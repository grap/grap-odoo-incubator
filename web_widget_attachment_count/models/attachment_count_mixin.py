# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AttachmentCountMixin(models.AbstractModel):
    _name = "attachment.count.mixin"
    _description = "Attachment Count Mixin Model"

    message_attachment_count = fields.Integer(
        store=True,
    )
