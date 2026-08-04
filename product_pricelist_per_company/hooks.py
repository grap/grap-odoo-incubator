# Copyright (C) 2026 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging
from collections import defaultdict

from openupgradelib import openupgrade
from psycopg2.extensions import AsIs

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    companies = env["res.company"].with_context(active_test=False).search([])
    pricelists = env["product.pricelist"].with_context(active_test=False).search([])

    if len(pricelists.mapped("company_id")) > 1:
        return

    if len(companies) == 1:
        return

    main_company = pricelists.mapped("company_id")

    for company in companies:
        if company == main_company:
            continue

        mapping = defaultdict(int)
        _logger.info(f"Handling company #{company.id} - {company.complete_name}")

        # Part 1) Handle classic fields
        for field in env["ir.model.fields"].search(
            [
                ("ttype", "=", "many2one"),
                ("relation", "=", "product.pricelist"),
                ("model_id.transient", "=", False),
            ]
        ):
            if field.name.startswith("x_"):
                continue

            if not env[field.model]._auto:
                continue

            if (
                field.model in ["res.partner", "res.users"]
                and field.name == "property_product_pricelist"
            ):
                # Weird implementation
                # see product/models/res_partner.py
                continue

            domain_field_name = "company_id"
            if field.model == "res.company":
                domain_field_name = "id"
            domain = [(domain_field_name, "=", company.id)]

            used_pricelist_ids = set(
                [
                    x[field.name][0]
                    for x in env[field.model]
                    .with_context(active_test=False)
                    .read_group(domain, [field.name], field.name)
                    if x[field.name]
                ]
            )
            for use_pricelist_id in used_pricelist_ids:
                if use_pricelist_id not in mapping:
                    original_pricelist = pricelists.filtered(
                        lambda x, use_pricelist_id=use_pricelist_id: x.id
                        == use_pricelist_id
                    )
                    if "code" in env["res.company"]._fields:
                        new_pricelist_name = (
                            f"{company.code} - {original_pricelist.name}"
                        )
                    else:
                        new_pricelist_name = original_pricelist.name
                    new_pricelist = original_pricelist.copy(
                        {"company_id": company.id, "name": new_pricelist_name}
                    )
                    mapping[use_pricelist_id] = new_pricelist.id
                    _logger.info(
                        f"Creating New product.pricelist #{new_pricelist.id} "
                        f"Name: '{new_pricelist.name}'"
                    )

                openupgrade.logged_query(
                    env.cr,
                    """
                    UPDATE %(table_name)s
                    SET %(pricelist_field_name)s = %(new_pricelist_id)s
                    WHERE %(pricelist_field_name)s = %(old_pricelist_id)s
                    AND %(domain_field_name)s = %(company_id)s
                    """,
                    {
                        "table_name": AsIs(env[field.model]._table),
                        "pricelist_field_name": AsIs(field.name),
                        "new_pricelist_id": mapping[use_pricelist_id],
                        "old_pricelist_id": use_pricelist_id,
                        "domain_field_name": AsIs(domain_field_name),
                        "company_id": company.id,
                    },
                )

        # Part 2) Handle properties

        property_domain = [
            ("value_reference", "in", [f"product.pricelist,{x.id}" for x in pricelists])
        ]

        # Handle properties set to specific items
        properties = env["ir.property"].search(
            property_domain + [("res_id", "!=", False)]
        )

        for _property in properties:
            _model_name, _id = _property.res_id.split(",")
            item = env[_model_name].browse(_id)
            import pdb

            pdb.set_trace()

    import pdb

    pdb.set_trace()
