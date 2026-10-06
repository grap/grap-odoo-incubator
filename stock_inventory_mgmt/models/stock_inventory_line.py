# Part of Odoo CE V12. LGPL.

from odoo import Command, _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import float_utils


class StockInventoryLine(models.Model):
    _name = "stock.inventory.line"
    _description = "Inventory Line"
    _order = "create_date, product_id, location_id, prod_lot_id"

    _KEY_FIELDS = [
        "product_id",
        "location_id",
        "partner_id",
        "package_id",
        "prod_lot_id",
    ]

    # Inventory fields
    inventory_id = fields.Many2one(
        comodel_name="stock.inventory",
        string="Inventory",
        index=True,
        ondelete="cascade",
        readonly=True,
    )
    state = fields.Selection(related="inventory_id.state", readonly=True, store=True)
    inventory_location_id = fields.Many2one(
        comodel_name="stock.location",
        string="Inventory Location",
        related="inventory_id.location_id",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        related="inventory_id.company_id",
        index=True,
        readonly=True,
        store=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="inventory_id.currency_id",
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
        readonly=True,
        states={"in_progress": [("readonly", False)]},
    )
    product_tracking = fields.Selection(related="product_id.tracking", readonly=True)

    product_active = fields.Boolean(
        # Default=True avoid to have italic line, before the product selection
        # We don't want a related field here, because we want to state the active
        # value of the product, at the date of the inventory.
        compute="_compute_product_active",
        store=True,
        default=True,
    )
    product_category_id = fields.Many2one(
        string="Product Category",
        comodel_name="product.category",
        related="product_id.categ_id",
        readonly=True,
    )
    product_uom_category_id = fields.Many2one(
        string="UoM Category", related="product_id.uom_id.category_id", readonly=True
    )

    # Inventory line fields
    partner_id = fields.Many2one(
        string="Owner",
        comodel_name="res.partner",
        readonly=True,
        states={"in_progress": [("readonly", False)]},
    )
    product_uom_id = fields.Many2one(
        string="Product Unit of Measure",
        comodel_name="uom.uom",
        required=True,
        readonly=True,
        states={"in_progress": [("readonly", False)]},
    )

    location_id = fields.Many2one(
        string="Location",
        comodel_name="stock.location",
        index=True,
        required=True,
        readonly=True,
        states={"in_progress": [("readonly", False)]},
    )
    package_id = fields.Many2one(
        string="Pack",
        comodel_name="stock.quant.package",
        index=True,
        readonly=True,
        states={"in_progress": [("readonly", False)]},
    )
    prod_lot_id = fields.Many2one(
        string="Lot/Serial Number",
        comodel_name="stock.lot",
        domain="[('product_id','=',product_id)]",
        readonly=True,
        states={"in_progress": [("readonly", False)]},
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
        readonly=True,
        states={"in_progress": [("readonly", False)]},
    )

    variation_qty = fields.Float(
        string="Quantity Variation",
        digits="Product Unit of Measure",
        compute="_compute_variation",
        store=True,
    )
    variation_valuation = fields.Monetary(
        compute="_compute_variation",
        store=True,
    )
    price_unit = fields.Monetary(
        string="Unit Price",
        compute="_compute_price_unit",
        store=True,
        help="Technical field used to record the product cost at"
        " the time of the inventory",
    )

    valuation = fields.Monetary(
        compute="_compute_valuation",
        store=True,
    )

    merged_inventory_line_id = fields.Many2one(
        comodel_name="stock.inventory.line",
        string="Merged Inventory Line",
        readonly=True,
        copy=False,
    )

    source_inventory_line_ids = fields.One2many(
        string="Source Inventory Lines",
        comodel_name="stock.inventory.line",
        inverse_name="merged_inventory_line_id",
        readonly=True,
    )

    source_inventory_ids = fields.One2many(
        string="Source Inventories",
        comodel_name="stock.inventory",
        compute="_compute_source_inventory_ids",
        readonly=True,
    )

    @api.depends("product_id")
    def _compute_price_unit(self):
        for line in self:
            line.price_unit = line.product_id and line.product_id.standard_price or 0.0

    @api.depends("price_unit", "product_qty")
    def _compute_valuation(self):
        for line in self:
            line.valuation = line.price_unit * line.product_qty

    @api.depends("price_unit", "product_qty")
    def _compute_source_inventory_ids(self):
        for line in self:
            line.source_inventory_ids = line.mapped(
                "source_inventory_line_ids.inventory_id"
            )

    @api.depends("price_unit", "product_qty", "theoretical_qty")
    def _compute_variation(self):
        for line in self:
            line.variation_qty = line.product_qty - line.theoretical_qty
            line.variation_valuation = line.variation_qty * line.price_unit

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

    @api.depends("product_id")
    def _compute_product_active(self):
        for line in self:
            line.product_active = line.product_id.active

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

    @api.constrains("product_id")
    def _check_product_id(self):
        """As no quants are created for consumable products,
        it should not be possible do adjust their quantity.
        """
        for line in self:
            if line.product_id.type != "product":
                raise ValidationError(
                    _(
                        "You can only inventory storable products."
                        "\n\n%(product_name)s -> %(product_type)s",
                        product_name=line.product_id.display_name,
                        product_type=line.product_id.type,
                    )
                )

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if "product_id" in values and "product_uom_id" not in values:
                values["product_uom_id"] = (
                    self.env["product.product"].browse(values["product_id"]).uom_id.id
                )
        return super().create(vals_list)

    # ===========================
    # Private Section
    # ===========================
    def _generate_stock_moves(self):
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
            vals_list.append(line._prepare_stock_move_vals())
        return self.env["stock.move"].create(vals_list)

    def _prepare_stock_move_vals(self):
        self.ensure_one()
        diff = self.theoretical_qty - self.product_qty
        if diff < 0:  # found more than expected
            location_id = self.product_id.property_stock_inventory.id
            location_dest_id = self.location_id.id
            out = False
        else:
            location_id = self.location_id.id
            location_dest_id = self.product_id.property_stock_inventory.id
            out = True

        qty = abs(diff)

        return {
            "name": _("INV: %(inventory_name)s", inventory_name=self.inventory_id.name),
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
                Command.create(
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
                    }
                )
            ],
        }

    def _get_keys(self):
        self.ensure_one()
        keys = []
        for field_name in self._KEY_FIELDS:
            if self._fields[field_name].type == "many2one":
                keys.append(getattr(self, field_name).id)
            else:
                raise NotImplementedError()
        return str(keys)
