# coding: utf-8
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import fields
from openerp.addons.point_of_sale.wizard.pos_box import PosBox


class PosBoxJournalReason(PosBox):
    _register = False


class PosBoxOut(PosBoxJournalReason):
    _inherit = 'cash.box.out'

    ref = fields.Char(
        string='Reference')

    def _compute_values_for_statement_line(self, box, record):
        values = super(PosBoxOut, self).\
            _compute_values_for_statement_line(box, record)
        values['ref'] = (box.ref or '')
        return values
