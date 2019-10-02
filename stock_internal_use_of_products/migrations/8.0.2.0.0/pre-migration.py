# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

__name__ = u"Change links between internal.use and stock.move"


def add_internal_use_column(cr):
    sql = """
        ALTER TABLE stock_move ADD column internal_use_id int;
    """
    cr.execute(sql)


def update_internal_use(cr):
    sql = """
    UPDATE stock_move
    SET internal_use_id = tmp.internal_use_id
    FROM (
        SELECT sm.id as move_id,
            iu.id as internal_use_id
        FROM internal_use iu
        INNER JOIN stock_picking sp on sp.id = iu.picking_id
        INNER JOIN stock_move sm on sm.picking_id = sp.id) as tmp
    WHERE stock_move.id = tmp.move_id;
    """
    cr.execute(sql)


def migrate(cr, version):
    if not version:
        return
    add_internal_use_column(cr)
    update_internal_use(cr)
