# Part of Odoo CE V12. LGPL.

from odoo import Command, _, api, fields, models
from odoo.exceptions import UserError


class Inventory(models.Model):
    _name = "stock.inventory"
    _description = "Inventory"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date desc, id desc"
    _check_company_auto = True

    name = fields.Char(
        string="Inventory Reference",
        readonly=True,
        required=True,
        states={
            "draft": [("readonly", False)],
            "in_progress": [("readonly", False)],
        },
        tracking=True,
    )
    date = fields.Datetime(
        string="Inventory Date",
        readonly=True,
        required=True,
        copy=False,
        default=fields.Datetime.now,
        help="If the inventory adjustment is not validated,"
        " date at which the theoritical quantities have been checked.\n"
        "If the inventory adjustment is validated,"
        " date at which the inventory adjustment has been validated.",
    )
    merged_inventory_id = fields.Many2one(
        string="Merged into",
        comodel_name="stock.inventory",
        readonly=True,
        copy=False,
    )
    source_inventory_ids = fields.One2many(
        string="Source Inventories",
        comodel_name="stock.inventory",
        inverse_name="merged_inventory_id",
        readonly=True,
    )
    source_inventory_qty = fields.Integer(
        string="Source Inventories Quantity",
        compute="_compute_source_inventory_qty",
        store=True,
    )
    line_ids = fields.One2many(
        string="Inventory Lines",
        comodel_name="stock.inventory.line",
        inverse_name="inventory_id",
        copy=True,
        readonly=False,
        states={"done": [("readonly", True)]},
    )
    line_qty = fields.Integer(
        string="Lines Quantity",
        compute="_compute_line_qty",
        store=True,
    )
    duplicates_qty = fields.Integer(
        string="Duplicates Quantity", compute="_compute_duplicates_qty"
    )
    move_ids = fields.One2many(
        string="Created Moves",
        comodel_name="stock.move",
        inverse_name="inventory_id",
        readonly=True,
    )
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("in_progress", "In Progress"),
            ("pending_merge", "Pending Merge"),
            ("merged", "Merged"),
            ("done", "Validated"),
            ("cancel", "Cancelled"),
        ],
        copy=False,
        index=True,
        readonly=True,
        default="draft",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        index=True,
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        default=lambda self: self.env.company,
    )
    location_id = fields.Many2one(
        string="Inventoried Location",
        comodel_name="stock.location",
        index=True,
        required=True,
        domain=[("usage", "=", "internal")],
        readonly=True,
        states={"draft": [("readonly", False)]},
        default=lambda x: x._default_location_id(),
        check_company=True,
    )
    partner_id = fields.Many2one(
        string="Inventoried Owner",
        comodel_name="res.partner",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Specify Owner to focus your inventory on a particular owner.",
    )
    supplier_id = fields.Many2one(
        string="Inventoried Supplier",
        comodel_name="res.partner",
        readonly=True,
        states={"draft": [("readonly", False)]},
        domain=lambda x: x._domain_supplier_id(),
        help="Specify Suplier to focus your inventory on a particular supplier.",
    )
    filter = fields.Selection(
        string="Inventory of",
        selection="_selection_filter",
        required=True,
        default="partial",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="If you do an entire inventory, you can choose 'All Products'"
        " and it will prefill the inventory with the current stock."
        " If you only do some products"
        " (e.g. Cycle Counting) you can choose 'Manual Selection of Products'"
        " and the system won't propose anything.",
    )
    category_id = fields.Many2one(
        string="Product Category",
        comodel_name="product.category",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Specify Product Category to focus your inventory"
        " on a particular Category.",
    )
    racking_id = fields.Many2one(
        string="Racking",
        comodel_name="stock.racking",
        readonly=True,
        states={"draft": [("readonly", False)]},
        domain=[("type", "=", "normal")],
        help="Specify Racking to focus your inventory"
        " on a particular racking of your stock location.",
    )
    exhausted = fields.Boolean(
        string="Include Exhausted Products",
        default=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="company_id.currency_id",
        store=True,
    )

    valuation = fields.Monetary(
        compute="_compute_valuation",
        store=True,
        tracking=True,
    )

    @api.model
    def _domain_supplier_id(self):
        current_date = fields.Date.context_today(self)

        partner_ids = [
            x["partner_id"][0]
            for x in self.env["product.supplierinfo"].read_group(
                [
                    "|",
                    ("date_start", "=", False),
                    ("date_start", "<=", current_date),
                    "|",
                    ("date_end", "=", False),
                    ("date_end", ">", current_date),
                ],
                ["partner_id"],
                ["partner_id"],
            )
        ]
        return [("id", "in", partner_ids)]

    @api.depends("line_ids")
    def _compute_duplicates_qty(self):
        for inventory in self:
            inventory.duplicates_qty = len(inventory._get_groups_of_duplicated_lines())

    @api.depends("line_ids")
    def _compute_line_qty(self):
        for inventory in self:
            inventory.line_qty = len(inventory.line_ids)

    @api.depends("source_inventory_ids")
    def _compute_source_inventory_qty(self):
        for inventory in self:
            inventory.source_inventory_qty = len(inventory.source_inventory_ids)

    @api.depends("line_ids.valuation")
    def _compute_valuation(self):
        for inventory in self:
            inventory.valuation = sum(inventory.mapped("line_ids.valuation"))

    def _default_location_id(self):
        warehouse = self.env["stock.warehouse"].search(
            [("company_id", "=", self.env.company_id.id)], limit=1
        )
        if warehouse:
            return warehouse.lot_stock_id.id
        return False

    @api.constrains("filter", "state", "location_id")
    def _check_filter_state_location_id(self):
        for inventory in self.filtered(
            lambda x: x.state == "in_progress" and x.filter == "none"
        ):
            other_inventories = self.search(
                [
                    ("state", "=", "in_progress"),
                    ("filter", "=", "none"),
                    ("id", "!=", inventory.id),
                    ("location_id", "=", inventory.location_id.id),
                ]
            )
            if other_inventories:
                raise UserError(
                    _(
                        "You can not put in progress state the inventory"
                        " %(inventory_name)s because there are other full"
                        " inventories in progress for the same stock location"
                        " '%(location_name)s'.\n\n- %(inventories_names)s",
                        inventory_name=inventory.name,
                        inventories_names="\n- ".join(other_inventories.mapped("name")),
                        location_name=inventory.location_id.name,
                    )
                )

    def unlink(self):
        for inventory in self:
            if (
                inventory.state not in ("draft", "cancel")
                and not inventory.source_inventory_qty
            ):
                raise UserError(
                    _("You can only delete draft, canceled or merge inventories.")
                )
        self.mapped("source_inventory_ids").write({"state": "in_progress"})
        return super().unlink()

    @api.returns("self", lambda value: value.id)
    def copy(self, default=None):
        default = dict(default or {})
        if "name" not in default:
            default.update(name=_("%s (copy)", self.name))
        default.update(state=self.state == "draft" and "draft" or "in_progress")
        return super().copy(default)

    @api.model
    def _selection_filter(self):
        """Get the list of filter allowed according to the options checked
        in 'Settings Warehouse'."""
        res_filter = [
            ("partial", _("Select products manually")),
            ("none", _("All products")),
            ("category", _("One product category")),
            ("racking", _("One racking")),
        ]

        # We give access to admin, to let the possibility to test,
        # even if the admin user is not member of groups,
        # or if the module purchase is not installed
        if (
            self.user_has_groups("stock.group_tracking_owner")
            or self.env.user._is_admin()
        ):
            res_filter += [("owner", _("One owner"))]

        if (
            self.user_has_groups("purchase.group_purchase_user")
            or self.env.user._is_admin()
        ):
            res_filter += [("supplier", _("One supplier"))]

        return res_filter

    @api.onchange("filter")
    def _onchange_filter(self):
        if self.filter != "owner":
            self.partner_id = False
        if self.filter != "category":
            self.category_id = False
        if self.filter != "racking":
            self.racking_id = False
        if self.filter != "owner":
            self.partner_id = False
        if self.filter != "supplier":
            self.supplier_id = False

        self.exhausted = self.filter not in ("partial", "owner")

    def action_validate(self):
        # Check line quantity
        if not all(self.mapped("line_qty")):
            raise UserError(_("You can not validate inventories without any lines."))

        # Check about inventory state
        if self.mapped("state") != ["in_progress"]:
            raise UserError(_("You can only validate pending inventories."))

        # Check about duplicated lines in the same inventory
        if any(self.mapped("duplicates_qty")):
            raise UserError(
                _("You can not validate inventories with duplicated lines.")
            )

        # Check negative lines
        negative_lines = self.mapped("line_ids").filtered(lambda x: x.product_qty < 0)
        if negative_lines:
            product_list = [
                _(
                    "Product: %(product_name)s - Quantity: %(product_qty)s",
                    product_name=line.product_id.name,
                    product_qty=line.product_qty,
                )
                for line in negative_lines
            ]
            raise UserError(
                _(
                    "You cannot set a negative product quantity"
                    " in an inventory line:\n\n- %(product_list)s",
                    product_list="\n- ".join(product_list),
                )
            )

        # Check about mandatory tracking data
        incorrect_lot_inventory_lines = self.line_ids.filtered(
            lambda line: line.product_id.tracking in ["lot", "serial"]
            and not line.prod_lot_id
            and line.product_qty
        )
        if incorrect_lot_inventory_lines:
            raise UserError(_("Incorrect Lot Inventory Lines."))

        # Check about duplicated lines in other pending inventories
        all_pending_duplicates = self.env["stock.inventory.line"]
        for group_of_duplicated_lines in self.search(
            [("state", "=", "in_progress")]
        )._get_groups_of_duplicated_lines():
            all_pending_duplicates |= group_of_duplicated_lines
        duplicated_lines = all_pending_duplicates.filtered(
            lambda x, inventory_ids=self.ids: x.inventory_id in inventory_ids
        )
        if duplicated_lines:
            duplicate_list = [
                _(
                    "Product: %(product_name)s - Quantity: %(product_qty)s",
                    product_name=line.product_id.name,
                    product_qty=line.product_qty,
                )
                for line in duplicated_lines
            ]
            raise UserError(
                _(
                    "You can not validate inventories with the following lines"
                    " because there are inventoried in other pending inventories:\n\n"
                    "- %(duplicate_list)s",
                    duplicate_list="\n- ".join(duplicate_list),
                )
            )

        # Let's go !
        self.mapped("line_ids")._generate_stock_moves()
        self.mapped("move_ids")._action_done()
        self.mapped("source_inventory_ids").filtered(
            lambda x: x.state == "pending_merge"
        ).write({"state": "merged"})
        return self.write({"state": "done", "date": fields.Datetime.now()})

    def action_cancel(self):
        inventories = self.filtered(lambda x: x.state in ("in_progress", "draft"))
        return inventories.write({"state": "cancel"})

    def action_start(self):
        for inventory in self.filtered(lambda x: x.state == "draft"):
            vals = {"state": "in_progress", "date": fields.Datetime.now()}
            if inventory.filter != "partial":
                vals.update(
                    {
                        "line_ids": [
                            Command.create(line_values)
                            for line_values in inventory._get_inventory_lines_values()
                        ]
                    }
                )
            inventory.write(vals)
        return True

    def action_merge_duplicated_lines(self):
        for inventory in self:
            for duplicated_lines in inventory._get_groups_of_duplicated_lines():
                sum_quantity = 0
                keeped_line = False
                for duplicated_line in duplicated_lines:
                    if not keeped_line:
                        # First line
                        keeped_line = duplicated_line
                        sum_quantity = duplicated_line.product_qty
                    else:
                        # Same UoM
                        if keeped_line.product_uom_id == duplicated_line.product_uom_id:
                            sum_quantity += duplicated_line.product_qty
                        else:
                            sum_quantity += (
                                duplicated_line.product_uom_id._compute_quantity(
                                    duplicated_line.product_qty,
                                    keeped_line.product_uom_id,
                                )
                            )

                # Update the first line with the sumed quantity
                keeped_line.write({"product_qty": sum_quantity})

                # Delete all the other lines
                other_lines = duplicated_lines.filtered(
                    lambda x, keeped_line=keeped_line: x != keeped_line
                )
                other_lines.unlink()

    def action_view_duplicates(self):
        self.ensure_one()
        action = self.env.ref("stock_inventory_mgmt.action_inventory_line_tree")
        action_data = action.read()[0]
        all_duplicated_lines = self.env["stock.inventory.line"]
        for group_of_duplicated_lines in self.search(
            [("state", "=", "in_progress")]
        )._get_groups_of_duplicated_lines():
            all_duplicated_lines |= group_of_duplicated_lines
        action_data["domain"] = [("id", "in", all_duplicated_lines.ids)]
        return action_data

    def action_inventory_line_tree(self):
        action = self.env.ref("stock_inventory_mgmt.action_inventory_line_tree")
        action_data = action.read()[0]
        action_data["context"] = {
            "default_location_id": self.location_id.id,
            "default_partner_id": self.partner_id.id,
            "default_inventory_id": self.id,
        }
        return action_data

    def _get_inventory_lines_values(self):
        self.ensure_one()
        # TDE CLEANME: is sql really necessary ? I don't think so
        locations = self.env["stock.location"].search(
            [("id", "child_of", [self.location_id.id])]
        )
        domain = " sq.location_id in %s AND sq.quantity != 0 AND sq.company_id = %s"
        args = (
            tuple(locations.ids),
            self.company_id.id,
        )

        vals = []
        ProductProduct = self.env["product.product"]

        # Empty recordset of products available in stock_quants
        quant_products = self.env["product.product"]

        # Empty recordset of products to filter
        products_to_filter = self.env["product.product"]

        # case 1: Filter on One owner only
        if self.partner_id:
            domain += " AND sq.owner_id = %s"
            args += (self.partner_id.id,)

        # case 2: Filter on One product category
        if self.category_id:
            categ_products = ProductProduct.search(
                [("categ_id", "child_of", self.category_id.id)]
            )
            domain += " AND sq.product_id = ANY (%s)"
            args += (categ_products.ids,)
            products_to_filter |= categ_products

        # case 3: Filter on One racking
        if self.racking_id:
            racking_products = self.racking_id.product_ids
            domain += " AND sq.product_id = ANY (%s)"
            args += (racking_products.ids,)
            products_to_filter |= racking_products

        # case 4: Filter on One supplier
        if self.supplier_id:
            current_date = fields.Date.context_today(self)
            supplierinfos = self.env["product.supplierinfo"].search(
                [
                    ("partner_id", "=", self.supplier_id.id),
                    "|",
                    ("date_start", "=", False),
                    ("date_start", "<=", current_date),
                    "|",
                    ("date_end", "=", False),
                    ("date_end", ">", current_date),
                ]
            )
            supplier_products = supplierinfos.mapped(
                "product_tmpl_id.product_variant_ids"
            ) | supplierinfos.mapped("product_id")
            domain += " AND sq.product_id = ANY (%s)"
            args += (supplier_products.ids,)
            products_to_filter |= supplier_products

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
            if product_data["product_id"]:
                product_data["product_uom_id"] = ProductProduct.browse(
                    product_data["product_id"]
                ).uom_id.id
                quant_products |= ProductProduct.browse(product_data["product_id"])
            product_data["product_qty"] = 0.0
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
        self.ensure_one()
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
                    "product_qty": 0.0,
                }
            )
        return vals

    # Duplicate managements
    def _get_groups_of_duplicated_lines(self):
        check_dict = {}
        result = []
        for line in self.mapped("line_ids"):
            key = line._get_keys()
            if key in check_dict:
                check_dict[key] |= line
            else:
                check_dict[key] = line
        for _k, v in check_dict.items():
            if len(v) > 1:
                result.append(v)
        return result
