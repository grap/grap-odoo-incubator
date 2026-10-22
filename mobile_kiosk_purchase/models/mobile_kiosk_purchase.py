# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from math import ceil

from odoo import _, api, models


class MobileKioskPurchase(models.TransientModel):
    _name = "mobile.kiosk.purchase"
    _inherit = "mobile.kiosk.abstract"
    _description = "Mobile Kiosk Purchase Proxy"

    # ################################
    # Public API
    # ################################
    @api.model
    def scan_barcode(self, barcode, partner_id):
        result = self._result_prepare()

        # Search for product
        product = self.env["product.product"].search(
            [("barcode", "=", barcode)], limit=1
        )

        # raise an error if no product was found
        if not product:
            return self._result_add_notification(
                result,
                level="danger",
                title=_("Barcode not found"),
                message=_(
                    "No product has been found for barcode '%(barcode)s'.",
                    barcode=barcode,
                ),
            )

        result["action"] = self._hook_after_product_product_selection(
            product, partner_id
        )
        return result

    @api.model
    def add_quantity(self, partner_id, product_id, product_qty):
        result = self._result_prepare()

        # Search for partner
        partner = self.env["res.partner"].browse(partner_id)

        # raise an error if no partner was found
        if not partner or not partner.active:
            return self._result_add_notification(
                result,
                level="danger",
                title=_("Supplier not found"),
                message=_(
                    "No active supplier has been found for ID #%(partner_id)s.",
                    partner_id=partner_id,
                ),
            )

        # Search for product
        product = self.env["product.product"].browse(product_id)

        # raise an error if no product was found
        if not product or not product.active:
            return self._result_add_notification(
                result,
                level="danger",
                title=_("Product not found"),
                message=_(
                    "No active product has been found for ID #%(product_id)s.",
                    product_id=product_id,
                ),
            )

        if product_qty is None:
            return self._result_add_notification(
                result,
                level="danger",
                title=_("Missing Quantity"),
            )

        if not (isinstance(product_qty, int) or isinstance(product_qty, float)):
            return self._result_add_notification(
                result,
                level="danger",
                title=_("Incorrect Quantity"),
                message=_(
                    "'%(product_qty)s' is not a correct value for a quantity.",
                    product_qty=product_qty,
                ),
            )

        order = self._get_purchase_order(partner_id, force_create=True)

        seller = product._select_seller(
            partner_id=partner,
            quantity=product_qty,
            date=order.date_order and order.date_order.date(),
            uom_id=product.uom_po_id,
        )

        # First, Check minimum quantity
        if not seller:
            supplierinfos = self.env["product.supplierinfo"].search(
                [
                    ("partner_id", "=", partner.id),
                    ("product_tmpl_id", "=", product.product_tmpl_id.id),
                ]
            )
            if supplierinfos:
                min_qty = min(supplierinfos.mapped("min_qty"))
                if min_qty > product_qty:
                    self._result_add_notification(
                        result,
                        title=_("Quantity increased"),
                        message=_(
                            "The quantity has been increased to the minimum"
                            " quantity (from %(product_qty)s to %(min_qty)s).",
                            product_qty=product_qty,
                            min_qty=min_qty,
                        ),
                    )
                    product_qty = min_qty
                    seller = product._select_seller(
                        partner_id=partner,
                        quantity=product_qty,
                        date=order.date_order and order.date_order.date(),
                        uom_id=product.uom_po_id,
                    )

        # Then, Check multiplier quantity
        if seller:
            if seller.multiplier_qty and product_qty % seller.multiplier_qty:
                rounded_qty = (
                    ceil(product_qty / seller.multiplier_qty) * seller.multiplier_qty
                )
                self._result_add_notification(
                    result,
                    title=_("Quantity rounded"),
                    message=_(
                        "The quantity has been rounded due to multiplier"
                        " quantity (from %(product_qty)s to %(rounded_qty)s).",
                        product_qty=product_qty,
                        rounded_qty=rounded_qty,
                    ),
                )
                product_qty = rounded_qty

        self.env["purchase.order.line"].create(
            {
                "order_id": order.id,
                "product_id": product.id,
                "product_qty": product_qty,
            }
        )

        result["action"] = self._hook_after_res_partner_selection(order.partner_id)
        return result

    # ################################
    # Private Function
    # ################################
    @api.model
    def _get_purchase_order(self, partner_id, force_create=False):
        order = self.env["purchase.order"].search(
            [
                ("partner_id", "=", partner_id),
                ("state", "in", ["draft", "sent"]),
            ],
            order="date_order desc",
            limit=1,
        )
        if order:
            return order
        if not force_create:
            return False

        return self.env["purchase.order"].create(
            {
                "partner_id": partner_id,
                "origin": _("Mobile Application"),
            }
        )

    @api.model
    def _hook_after_res_partner_selection(self, partner):
        context = {}
        self._prepare_supplier_context(context, partner)

        return {
            "type": "ir.actions.client",
            "name": _("Purchase"),
            "tag": "mobile_kiosk_purchase_action_set_product",
            "target": "fullscreen",
            "context": context,
        }

    @api.model
    def _hook_after_product_product_selection(self, product, partner_id):
        partner = self.env["res.partner"].browse(partner_id)

        context = {}
        if partner:
            self._prepare_supplier_context(context, partner)
            self._prepare_product_context(context, partner, product)

        return {
            "type": "ir.actions.client",
            "name": _("Purchase"),
            "tag": "mobile_kiosk_purchase_action_set_quantity",
            "target": "fullscreen",
            "context": context,
        }

    @api.model
    def _prepare_supplier_context(self, current_context, partner):
        current_context.update(
            {
                "mk_purchase_supplier_id": partner.id,
                "mk_purchase_supplier_name": partner.name,
            }
        )

        order = self._get_purchase_order(partner.id)
        if order:
            description = _(
                "%(line_qty)s lines -"
                " %(amount_untaxed)s € Vat Excl -"
                " %(amount_total)s € Vat Incl",
                line_qty=len(order.order_line),
                amount_untaxed=order.amount_untaxed,
                amount_total=order.amount_total,
            )
            current_context.update(
                {
                    "mk_purchase_order_id": order.id,
                    "mk_purchase_order_name": order.name,
                    "mk_purchase_order_description": description,
                }
            )
        else:
            current_context.update(
                {
                    "mk_purchase_order_id": False,
                    "mk_purchase_order_name": _("Order to be created"),
                    "mk_purchase_order_description": False,
                }
            )

    @api.model
    def _prepare_product_context(self, current_context, partner, product):
        current_context.update(
            {
                "mk_purchase_product_id": product.id,
                "mk_purchase_product_name": product.name,
                "mk_purchase_supplierinfo_multiplier_qty": False,
            }
        )

        seller = product._select_seller(partner_id=partner)

        if seller:
            current_context.update(
                {
                    "mk_purchase_supplierinfo_multiplier_qty": seller.multiplier_qty,
                }
            )
