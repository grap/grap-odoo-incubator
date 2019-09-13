# -*- coding: utf-8 -*-
# Copyright (C) 2017-Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (https://twitter.com/pondupont)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from openupgradelib import openupgrade


logger = logging.getLogger('OpenUpgrade.product_print_category')


def create_print_category(cr, table_name, field_name):
    logger.info(
        "Fast creation of the field"
        " %s.%s (pre)" % (table_name, field_name))
    cr.execute("""
        ALTER TABLE %s
        ADD COLUMN "%s" INTEGER""" % (
        table_name,
        field_name))

    cr.execute("""
        UPDATE product_product pp
        SET print_category_id = pt.print_category_id
        FROM product_template pt
        WHERE pt.id = pp.product_tmpl_id
        """)


@openupgrade.migrate()
def migrate(env, version):
    # Product_template : print_category_id is removed
    # Product_product : print_category_id is not related anymore
    cr = env.cr
    create_print_category(
        cr, 'product_product', 'print_category_id')
