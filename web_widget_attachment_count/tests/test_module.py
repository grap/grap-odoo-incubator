# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo_test_helper import FakeModelLoader

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestAttachmentCountMixin(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Load a test model using odoo_test_helper
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .fake_models import (
            ModelAttachmentCountMixin,
            ModelAttachmentCountMixinIrAttachment,
        )

        cls.loader.update_registry(
            (
                ModelAttachmentCountMixin,
                ModelAttachmentCountMixinIrAttachment,
            )
        )

        cls.ModelAttachmentCountMixin = cls.env["model.attachment.count.mixin"]
        cls.IrAttachment = cls.env["ir.attachment"]
        cls.item = cls.ModelAttachmentCountMixin.create({})

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        return super().tearDownClass()

    def test_computation(self):
        self.assertEqual(self.item.message_attachment_count, 0)

        # Check attachmentcreation
        attachment = self.IrAttachment.create(
            {
                "name": "Demo Name",
                "res_id": self.item.id,
                "res_model": "model.attachment.count.mixin",
            }
        )

        self.assertEqual(self.item.message_attachment_count, 1)

        attachment.write({"name": "Demo Name 2"})
        self.assertEqual(self.item.message_attachment_count, 1)

        attachment.unlink()
        self.assertEqual(self.item.message_attachment_count, 0)
