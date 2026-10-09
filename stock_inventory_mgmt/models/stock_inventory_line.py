# Part of Odoo CE V12. LGPL.

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_utils


class StockInventoryLine(models.Model):
    _name = "stock.inventory.line"
    _description = "Inventory Line"
    _order = "product_id, inventory_id, location_id, prod_lot_id"

    # Inventory fields
    inventory_id = fields.Many2one(
        "stock.inventory", string="Inventory", index=True, ondelete="cascade"
    )
    state = fields.Selection(related="inventory_id.state", readonly=True)
    inventory_location_id = fields.Many2one(
        comodel_name="stock.location",
        string="Inventory Location",
        related="inventory_id.location_id",
        related_sudo=False,
        readonly=False,
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        related="inventory_id.company_id",
        index=True,
        readonly=True,
        store=True,
    )

    # Product Fields
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        domain=[("type", "=", "product")],
        index=True,
        required=True,
    )
    product_tracking = fields.Selection(related="product_id.tracking", readonly=True)

    product_active = fields.Boolean(compute="_compute_product_active", store=True)

    # Inventory line fields
    partner_id = fields.Many2one(string="Owner", comodel_name="res.partner")
    product_uom_id = fields.Many2one(
        string="Product Unit of Measure", comodel_name="uom.uom", required=True
    )
    product_uom_category_id = fields.Many2one(
        string="Uom category", related="product_uom_id.category_id", readonly=True
    )
    location_id = fields.Many2one(
        string="Location", comodel_name="stock.location", index=True, required=True
    )
    package_id = fields.Many2one("stock.quant.package", "Pack", index=True)
    prod_lot_id = fields.Many2one(
        string="Lot/Serial Number",
        comodel_name="stock.lot",
        domain="[('product_id','=',product_id)]",
    )

    theoretical_qty = fields.Float(
        string="Theoretical Quantity",
        compute="_compute_theoretical_qty",
        digits="Product Unit of Measure",
        readonly=True,
        store=True,
    )
    product_qty = fields.Float(
        string="Real Quantity",
        digits="Product Unit of Measure",
        default=0,
    )

    @api.depends(
        "location_id",
        "product_id",
        "package_id",
        "product_uom_id",
        "company_id",
        "prod_lot_id",
        "partner_id",
    )
    def _compute_theoretical_qty(self):
        for line in self:
            if not line.product_id:
                line.theoretical_qty = 0
            else:
                quantity = line.product_id.with_context(
                    location=line.location_id.ids
                )._compute_quantities_dict(
                    line.prod_lot_id.id,
                    line.partner_id.id,
                    line.package_id.id,
                )[line.product_id.id]["qty_available"]

                line.theoretical_qty = line.product_id.uom_id._compute_quantity(
                    quantity, line.product_uom_id
                )

    @api.onchange("product_id")
    def _onchange_product(self):
        res = {}
        # If no UoM or incorrect UoM put default one from product
        if self.product_id:
            self.product_uom_id = self.product_id.uom_id
            res["domain"] = {
                "product_uom_id": [
                    ("category_id", "=", self.product_id.uom_id.category_id.id)
                ]
            }
        return res

    @api.onchange(
        "product_id",
        "location_id",
        "product_uom_id",
        "prod_lot_id",
        "partner_id",
        "package_id",
    )
    def _onchange_quantity_context(self):
        if (
            self.product_id
            and self.location_id
            and self.product_id.uom_id.category_id == self.product_uom_id.category_id
        ):  # TDE FIXME: last part added because crash
            self._compute_theoretical_qty()
            self.product_qty = self.theoretical_qty

    @api.depends("product_id")
    def _compute_product_active(self):
        for line in self:
            line.product_active = line.product_id.active

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if "product_id" in values and "product_uom_id" not in values:
                values["product_uom_id"] = (
                    self.env["product.product"].browse(values["product_id"]).uom_id.id
                )
        res = super().create(vals_list)
        res._check_no_duplicate_line()
        return res

    def write(self, vals):
        res = super().write(vals)
        self._check_no_duplicate_line()
        return res

    def _check_no_duplicate_line(self):
        for line in self:
            existings = self.search(
                [
                    ("id", "!=", line.id),
                    ("product_id", "=", line.product_id.id),
                    ("inventory_id.state", "=", "confirm"),
                    ("location_id", "=", line.location_id.id),
                    ("partner_id", "=", line.partner_id.id),
                    ("package_id", "=", line.package_id.id),
                    ("prod_lot_id", "=", line.prod_lot_id.id),
                ]
            )
            if existings:
                raise UserError(
                    _(
                        "You cannot have two inventory adjustments"
                        " in state 'In Progress'"
                        " with the same product (%(product_name)s),"
                        " same location, same package, same owner and same lot."
                        " Please first validate the first inventory adjustment"
                        " before creating another one.",
                        product_name=line.product_id.display_name,
                    )
                )

    @api.constrains("product_id")
    def _check_product_id(self):
        """As no quants are created for consumable products,
        it should not be possible do adjust their quantity.
        """
        for line in self:
            if line.product_id.type != "product":
                raise ValidationError(
                    _(
                        "You can only adjust storable products."
                        "\n\n%(product_name)s -> %(product_type)s",
                        product_name=line.product_id.display_name,
                        product_type=line.product_id.type,
                    )
                )

    def _get_move_values(self, qty, location_id, location_dest_id, out):
        self.ensure_one()
        return {
            "name": _("INV:") + (self.inventory_id.name or ""),
            "product_id": self.product_id.id,
            "product_uom": self.product_uom_id.id,
            "product_uom_qty": qty,
            "date": self.inventory_id.date,
            "company_id": self.inventory_id.company_id.id,
            "inventory_id": self.inventory_id.id,
            "state": "confirmed",
            "restrict_partner_id": self.partner_id.id,
            "location_id": location_id,
            "location_dest_id": location_dest_id,
            "move_line_ids": [
                (
                    0,
                    0,
                    {
                        "product_id": self.product_id.id,
                        "lot_id": self.prod_lot_id.id,
                        "reserved_uom_qty": 0,  # bypass reservation here
                        "product_uom_id": self.product_uom_id.id,
                        "qty_done": qty,
                        "package_id": out and self.package_id.id or False,
                        "result_package_id": (not out) and self.package_id.id or False,
                        "location_id": location_id,
                        "location_dest_id": location_dest_id,
                        "owner_id": self.partner_id.id,
                    },
                )
            ],
        }

    def _generate_moves(self):
        vals_list = []
        for line in self:
            if (
                float_utils.float_compare(
                    line.theoretical_qty,
                    line.product_qty,
                    precision_rounding=line.product_id.uom_id.rounding,
                )
                == 0
            ):
                continue
            diff = line.theoretical_qty - line.product_qty
            if diff < 0:  # found more than expected
                vals = line._get_move_values(
                    abs(diff),
                    line.product_id.property_stock_inventory.id,
                    line.location_id.id,
                    False,
                )
            else:
                vals = line._get_move_values(
                    abs(diff),
                    line.location_id.id,
                    line.product_id.property_stock_inventory.id,
                    True,
                )
            vals_list.append(vals)
        return self.env["stock.move"].create(vals_list)
