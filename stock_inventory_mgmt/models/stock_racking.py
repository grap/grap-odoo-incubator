from random import randint

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class StockRacking(models.Model):
    _name = "stock.racking"
    _description = "Stock Racking"
    _rec_name = "complete_name"
    _order = "complete_name"
    _check_company_auto = True

    location_id = fields.Many2one(
        string="Location",
        comodel_name="stock.location",
        default=lambda x: x._default_location_id(),
        domain=[("usage", "=", "internal")],
        required=True,
        check_company=True,
        compute="_compute_location_id",
        readonly=False,
        recursive=True,
        store=True,
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        related="location_id.company_id",
        store=True,
    )
    name = fields.Char(required=True)

    parent_id = fields.Many2one(
        string="Parent",
        comodel_name="stock.racking",
        index=True,
        check_company=True,
        domain=[("type", "=", "view")],
    )

    child_ids = fields.One2many(
        string="Child Rackings", comodel_name="stock.racking", inverse_name="parent_id"
    )

    complete_name = fields.Char(
        compute="_compute_complete_name", store=True, recursive=True
    )

    type = fields.Selection(
        selection=[("view", "View"), ("normal", "Normal")],
        string="Racking Type",
        default="normal",
        required=True,
        help="A racking of the view type is a virtual racking"
        " that can be used as the parent of another rackings"
        " to create a hierarchical structure.",
    )

    color = fields.Integer(string="Color Index", default=lambda x: x._default_color())

    product_ids = fields.Many2many(string="Products", comodel_name="product.product")

    product_qty = fields.Integer(
        string="Product Quantity", compute="_compute_product_qty"
    )

    _sql_constraints = [
        (
            "complete_name_uniq",
            "unique (complete_name)",
            "Racking complete name already exists!",
        )
    ]

    def _default_color(self):
        return randint(1, 11)

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

    @api.depends("name", "parent_id.complete_name")
    def _compute_complete_name(self):
        for racking in self.filtered(lambda x: not x.parent_id):
            racking.complete_name = racking.name
        for racking in self.filtered(lambda x: x.parent_id):
            racking.complete_name = (
                racking.parent_id.complete_name + " / " + racking.name
            )

    @api.depends("parent_id.location_id")
    def _compute_location_id(self):
        for racking in self.filtered(lambda x: x.parent_id):
            racking.location_id = racking.parent_id.location_id

    @api.depends("product_ids")
    def _compute_product_qty(self):
        for racking in self:
            racking.product_qty = len(racking.product_ids)

    @api.model_create_multi
    def create(self, vals_list):
        new_rackings = super().create(vals_list)
        # new created parent rackings will be set to 'view' type
        # to avoid futur misconfiguration
        new_rackings.filtered(lambda x: x.child_ids and x.type == "normal").write(
            {"type": "view"}
        )
        return new_rackings

    @api.returns("self", lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        default = default or {}
        if "name" not in default:
            default["name"] = _("%s (copy)", self.name)
        return super().copy(default=default)

    @api.constrains("parent_id", "location_id")
    def _check_parent_location(self):
        for racking in self:
            if (
                racking.parent_id
                and racking.parent_id.location_id != racking.location_id
            ):
                raise ValidationError(
                    _("Racking should have the same location has its parent racking.")
                )
