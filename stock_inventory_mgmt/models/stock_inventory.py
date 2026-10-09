# Part of Odoo CE V12. LGPL.

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


class Inventory(models.Model):
    _name = "stock.inventory"
    _description = "Inventory"
    _order = "date desc, id desc"

    @api.model
    def _default_location_id(self):
        company_user = self.env.user.company_id
        warehouse = self.env["stock.warehouse"].search(
            [("company_id", "=", company_user.id)], limit=1
        )
        if warehouse:
            return warehouse.lot_stock_id.id
        else:
            raise UserError(
                _("You must define a warehouse for the company: %s.")
                % (company_user.name,)
            )

    name = fields.Char(
        string="Inventory Reference",
        readonly=True,
        required=True,
        states={"draft": [("readonly", False)]},
    )
    date = fields.Datetime(
        string="Inventory Date",
        readonly=True,
        required=True,
        default=fields.Datetime.now,
        help="If the inventory adjustment is not validated,"
        " date at which the theoritical quantities have been checked.\n"
        "If the inventory adjustment is validated,"
        " date at which the inventory adjustment has been validated.",
    )
    line_ids = fields.One2many(
        string="Inventory Lines",
        comodel_name="stock.inventory.line",
        inverse_name="inventory_id",
        copy=True,
        readonly=False,
        states={"done": [("readonly", True)]},
    )
    move_ids = fields.One2many(
        string="Created Moves",
        comodel_name="stock.move",
        inverse_name="inventory_id",
        readonly=True,
    )
    state = fields.Selection(
        string="Status",
        selection=[
            ("draft", "Draft"),
            ("cancel", "Cancelled"),
            ("confirm", "In Progress"),
            ("done", "Validated"),
        ],
        copy=False,
        index=True,
        readonly=True,
        default="draft",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        readonly=True,
        index=True,
        required=True,
        states={"draft": [("readonly", False)]},
        default=lambda self: self.env.company,
    )
    location_id = fields.Many2one(
        string="Inventoried Location",
        comodel_name="stock.location",
        readonly=True,
        required=True,
        states={"draft": [("readonly", False)]},
        default=_default_location_id,
    )
    product_id = fields.Many2one(
        "product.product",
        string="Inventoried Product",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Specify Product to focus your inventory on a particular Product.",
    )
    package_id = fields.Many2one(
        string="Inventoried Pack",
        comodel_name="stock.quant.package",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Specify Pack to focus your inventory on a particular Pack.",
    )
    partner_id = fields.Many2one(
        string="Inventoried Owner",
        comodel_name="res.partner",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Specify Owner to focus your inventory on a particular Owner.",
    )
    lot_id = fields.Many2one(
        string="Inventoried Lot/Serial Number",
        comodel_name="stock.lot",
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Specify Lot/Serial Number to focus your inventory"
        " on a particular Lot/Serial Number.",
    )
    filter = fields.Selection(
        string="Inventory of",
        selection="_selection_filter",
        required=True,
        default="none",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="If you do an entire inventory, you can choose 'All Products'"
        " and it will prefill the inventory with the current stock."
        " If you only do some products"
        " (e.g. Cycle Counting) you can choose 'Manual Selection of Products'"
        " and the system won't propose anything.  You can also let the"
        " system propose for a single product / lot /... ",
    )
    total_qty = fields.Float("Total Quantity", compute="_compute_total_qty")
    category_id = fields.Many2one(
        string="Product Category",
        comodel_name="product.category",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Specify Product Category to focus your inventory"
        " on a particular Category.",
    )
    exhausted = fields.Boolean(
        string="Include Exhausted Products",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    @api.depends("product_id", "line_ids.product_qty")
    def _compute_total_qty(self):
        """For single product inventory, total quantity of the counted"""
        for inventory in self:
            if inventory.product_id:
                inventory.total_qty = sum(
                    inventory.mapped("line_ids").mapped("product_qty")
                )
            else:
                inventory.total_qty = 0

    def unlink(self):
        for inventory in self:
            if inventory.state == "done":
                raise UserError(
                    _("You cannot delete a validated inventory adjustement.")
                )
        return super().unlink()

    @api.model
    def _selection_filter(self):
        """Get the list of filter allowed according to the options checked
        in 'Settings Warehouse'."""
        res_filter = [
            ("none", _("All products")),
            ("category", _("One product category")),
            ("product", _("One product only")),
            ("partial", _("Select products manually")),
        ]

        if self.user_has_groups("stock.group_tracking_owner"):
            res_filter += [
                ("owner", _("One owner only")),
                ("product_owner", _("One product for a specific owner")),
            ]
        if self.user_has_groups("stock.group_production_lot"):
            res_filter.append(("lot", _("One Lot/Serial Number")))
        if self.user_has_groups("stock.group_tracking_lot"):
            res_filter.append(("pack", _("A Pack")))
        return res_filter

    @api.onchange("filter")
    def _onchange_filter(self):
        if self.filter not in ("product", "product_owner"):
            self.product_id = False
        if self.filter != "lot":
            self.lot_id = False
        if self.filter not in ("owner", "product_owner"):
            self.partner_id = False
        if self.filter != "pack":
            self.package_id = False
        if self.filter != "category":
            self.category_id = False
        if self.filter != "product":
            self.exhausted = False
        if self.filter == "product":
            self.exhausted = True
            if self.product_id:
                return {
                    "domain": {
                        "product_id": [
                            ("product_tmpl_id", "=", self.product_id.product_tmpl_id.id)
                        ]
                    }
                }

    @api.onchange("location_id")
    def _onchange_location_id(self):
        if self.location_id.company_id:
            self.company_id = self.location_id.company_id

    @api.constrains("filter", "product_id", "lot_id", "partner_id", "package_id")
    def _check_filter_product(self):
        if (
            self.filter == "none"
            and self.product_id
            and self.location_id
            and self.lot_id
        ):
            return
        if self.filter not in ("product", "product_owner") and self.product_id:
            raise ValidationError(
                _("The selected product doesn't belong to that owner..")
            )
        if self.filter != "lot" and self.lot_id:
            raise ValidationError(_("The selected lot number doesn't exist."))
        if self.filter not in ("owner", "product_owner") and self.partner_id:
            raise ValidationError(
                _("The selected owner doesn't have the proprietary of that product.")
            )
        if self.filter != "pack" and self.package_id:
            raise ValidationError(
                _(
                    "The selected inventory options are not coherent,"
                    " the package doesn't exist."
                )
            )

    def action_reset_product_qty(self):
        self.mapped("line_ids").write({"product_qty": 0})
        return True

    def action_validate(self):
        negative = next(
            (
                line
                for line in self.mapped("line_ids")
                if line.product_qty < 0 and line.product_qty != line.theoretical_qty
            ),
            False,
        )
        if negative:
            raise UserError(
                _(
                    "You cannot set a negative product quantity"
                    " in an inventory line:\n\t%(product_name)s - qty: %(quantity)s",
                    product_name=negative.product_id.name,
                    quantity=negative.product_qty,
                )
            )

        inventory_lines = self.line_ids.filtered(
            lambda line: line.product_id.tracking in ["lot", "serial"]
            and not line.prod_lot_id
            and line.theoretical_qty != line.product_qty
        )
        lines = self.line_ids.filtered(
            lambda line: float_compare(
                line.product_qty, 1, precision_rounding=line.product_uom_id.rounding
            )
            > 0
            and line.product_id.tracking == "serial"
            and line.prod_lot_id
        )
        if inventory_lines and not lines:
            # Adapt call of stock.track.confirmation to V16
            raise NotImplementedError()
        else:
            for inventory in self.filtered(lambda x: x.state not in ("done", "cancel")):
                inventory.line_ids._generate_moves()
                inventory.mapped("move_ids")._action_done()
                inventory.write({"state": "done", "date": fields.Datetime.now()})
            return True

    def action_cancel_draft(self):
        # TODO
        self.mapped("move_ids")._action_cancel()
        self.write({"line_ids": [(5,)], "state": "draft"})
        raise NotImplementedError()

    def action_start(self):
        for inventory in self.filtered(lambda x: x.state not in ("done", "cancel")):
            vals = {"state": "confirm", "date": fields.Datetime.now()}
            if (inventory.filter != "partial") and not inventory.line_ids:
                vals.update(
                    {
                        "line_ids": [
                            (0, 0, line_values)
                            for line_values in inventory._get_inventory_lines_values()
                        ]
                    }
                )
            inventory.write(vals)
        return True

    def action_inventory_line_tree(self):
        action = self.env.ref("stock_inventory_mgmt.action_inventory_line_tree").read()[
            0
        ]
        action["context"] = {
            "default_location_id": self.location_id.id,
            "default_product_id": self.product_id.id,
            "default_prod_lot_id": self.lot_id.id,
            "default_package_id": self.package_id.id,
            "default_partner_id": self.partner_id.id,
            "default_inventory_id": self.id,
        }
        return action

    def _get_inventory_lines_values(self):
        # TDE CLEANME: is sql really necessary ? I don't think so
        locations = self.env["stock.location"].search(
            [("id", "child_of", [self.location_id.id])]
        )
        domain = " sq.location_id in %s AND sq.quantity != 0"
        args = (tuple(locations.ids),)

        vals = []
        Product = self.env["product.product"]
        # Empty recordset of products available in stock_quants
        quant_products = self.env["product.product"]
        # Empty recordset of products to filter
        products_to_filter = self.env["product.product"]

        # case 0: Filter on company
        if self.company_id:
            domain += " AND sq.company_id = %s"
            args += (self.company_id.id,)

        # case 1: Filter on One owner only or One product for a specific owner
        if self.partner_id:
            domain += " AND sq.owner_id = %s"
            args += (self.partner_id.id,)
        # case 2: Filter on One Lot/Serial Number
        if self.lot_id:
            domain += " AND sq.lot_id = %s"
            args += (self.lot_id.id,)
        # case 3: Filter on One product
        if self.product_id:
            domain += " AND sq.product_id = %s"
            args += (self.product_id.id,)
            products_to_filter |= self.product_id
        # case 4: Filter on A Pack
        if self.package_id:
            domain += " AND sq.package_id = %s"
            args += (self.package_id.id,)
        # case 5: Filter on One product category + Exahausted Products
        if self.category_id:
            categ_products = Product.search(
                [("categ_id", "child_of", self.category_id.id)]
            )
            domain += " AND sq.product_id = ANY (%s)"
            args += (categ_products.ids,)
            products_to_filter |= categ_products

        self.env.cr.execute(
            """
            SELECT
                sq.product_id as product_id,
                sum(sq.quantity) as product_qty,
                sq.location_id as location_id,
                sq.lot_id as prod_lot_id,
                sq.package_id as package_id,
                sq.owner_id as partner_id
            FROM stock_quant sq
            LEFT JOIN product_product pp
                ON pp.id = sq.product_id
            WHERE %s
            GROUP BY
                sq.product_id,
                sq.location_id,
                sq.lot_id,
                sq.package_id,
                sq.owner_id
            """
            % domain,
            args,
        )

        for product_data in self.env.cr.dictfetchall():
            # replace the None the dictionary by False,
            # because falsy values are tested later on
            for void_field in [
                item[0] for item in product_data.items() if item[1] is None
            ]:
                product_data[void_field] = False
            product_data["theoretical_qty"] = product_data["product_qty"]
            if product_data["product_id"]:
                product_data["product_uom_id"] = Product.browse(
                    product_data["product_id"]
                ).uom_id.id
                quant_products |= Product.browse(product_data["product_id"])
            vals.append(product_data)
        if self.exhausted:
            exhausted_vals = self._get_exhausted_inventory_line(
                products_to_filter, quant_products
            )
            vals.extend(exhausted_vals)
        return vals

    def _get_exhausted_inventory_line(self, products, quant_products):
        """
        This function return inventory lines for exausted products
        :param products: products With Selected Filter.
        :param quant_products: products available in stock_quants
        """
        vals = []
        exhausted_domain = [("type", "not in", ("service", "consu", "digital"))]
        if products:
            exhausted_products = products - quant_products
            exhausted_domain += [("id", "in", exhausted_products.ids)]
        else:
            exhausted_domain += [("id", "not in", quant_products.ids)]
        exhausted_products = self.env["product.product"].search(exhausted_domain)
        for product in exhausted_products:
            vals.append(
                {
                    "inventory_id": self.id,
                    "product_id": product.id,
                    "location_id": self.location_id.id,
                }
            )
        return vals
