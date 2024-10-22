# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo.tests.common import SavepointCase


class TestProductTemplate(SavepointCase):
    def test_product_variant_id(self):
        """Test that product_variant_id is correctly populated for cloned
        archived products.

        This test is needed because we now store the product_variant_id computed
        field, instead of recomputing it every time.
        """
        product = self.env["product.template"].create({"name": "Test"})
        product.active = False
        new_product = product.copy()
        new_variants = new_product.with_context(active_test=False).product_variant_ids
        self.assertFalse(new_product.active)
        # This one is weird. The default Odoo upstream behaviour is that this
        # field is False when the template is inactive. We replicate that.
        self.assertFalse(new_product.product_variant_id)
        new_product.active = True
        self.assertEqual(new_product.product_variant_id, new_variants[0])
