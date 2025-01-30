from odoo import models


class ModelAttachmentCountMixin(models.Model):
    _name = "model.attachment.count.mixin"
    _description = "model.attachment.count.mixin"
    _inherit = ["attachment.count.mixin", "mail.thread"]


# pylint: disable=R8180
class ModelAttachmentCountMixinIrAttachment(models.Model):
    _inherit = "ir.attachment"

    def _get_attachment_count_models(self):
        res = super()._get_attachment_count_models()
        res += ["model.attachment.count.mixin"]
        return res
