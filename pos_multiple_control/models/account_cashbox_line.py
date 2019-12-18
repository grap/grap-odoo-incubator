# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountCashboxLine(models.Model):
    _inherit = "account.cashbox.line"

    _STATEMENT_STATE_SELECTION = [
        ("draft", "New"),
        ("open", "Open"),
        ("confirm", "Closed"),
    ]

    # Columns Section
    is_piece = fields.Boolean(string="Is Piece", readonly=True)


    # // TODO statement_state permet "juste" de mettre readonly la colonne d\'ouverture des espèces
    # // mais ce que je comprends pas, c'est que ça se base sur l'état d'un bank_statement et pas de la caisse.. ?
    # // pourquoi, et à voir si ça existe encore
    # statement_state = fields.Selection(
    #     related="bank_statement_id.state", selection=_STATEMENT_STATE_SELECTION
    # )

    # pour le bank_statement, on peut aller le chercher comme ça si besoin :
    
    # _name = 'account.bank.statement.cashbox'
    # _description = 'Bank Statement Cashbox'

    # cashbox_lines_ids = fields.One2many('account.cashbox.line', 'cashbox_id', string='Cashbox Lines')

    # @api.multi
    # def validate(self):
    #     bnk_stmt_id = self.env.context.get('bank_statement_id', False) or self.env.context.get('active_id', False)
    #     bnk_stmt = self.env['account.bank.statement'].browse(bnk_stmt_id)
    #     total = 0.0