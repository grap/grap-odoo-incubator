# coding: utf-8
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import json
from hashlib import sha256


from openerp import api, fields, models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    _SELECTION_CERTIFICATION_STATE = [
        ('not_concerned', 'Not Concerned'),
        ('certified', 'Certified'),
        ('corrupted', 'Corrupted'),
    ]

    l10n_fr_secure_state = fields.Selection(
        string='Inalterability State',
        compute='_compute_l10n_fr_secure_state',
        selection=_SELECTION_CERTIFICATION_STATE, help="State of the hash.\n"
        " * 'Not Concerned' : The hash has not be generated. No Inalterability"
        " can be granted\n"
        " * 'Certified': The stored hash is conform with the current data"
        " Inalterability is granted\n"
        " * 'Corrupted': The stored hash is not conform with the current data")

    l10n_fr_string_to_hash_display = fields.Text(
        string='Inalterable Data',
        compute='_compute_l10n_fr_string_to_hash_display')

    l10n_fr_previous_order = fields.Many2one(
        string='Inalterability Previous Order', comodel_name='pos.order',
        compute='_compute_l10n_fr_previous_order')

    # Compute Section
    @api.multi
    def _compute_l10n_fr_secure_state(self):
        for order in self:
            if order.l10n_fr_secure_sequence_number == 0\
                    and not order.l10n_fr_hash:
                order.l10n_fr_secure_state = 'not_concerned'
            elif order.l10n_fr_hash != order._recompute_hash():
                order.l10n_fr_secure_state = 'corrupted'
            else:
                order.l10n_fr_secure_state = 'certified'

    @api.multi
    @api.depends('l10n_fr_string_to_hash')
    def _compute_l10n_fr_string_to_hash_display(self):
        for order in self:
            order.l10n_fr_string_to_hash_display = json.dumps(
                json.loads(order.l10n_fr_string_to_hash), sort_keys=True,
                indent=2, separators=(',', ': '))

    @api.multi
    @api.depends('l10n_fr_secure_sequence_number')
    def _compute_l10n_fr_previous_order(self):
        for order in self:
            order.l10n_fr_previous_order = self.search([
                ('company_id', '=', self.company_id.id),
                ('l10n_fr_secure_sequence_number', '=',
                    order.l10n_fr_secure_sequence_number - 1)])

    @api.multi
    def _recompute_hash(self):
        """Return the hash of an object, computed on its current data_
        (l10n_fr_string_to_hash) and the hash of the previous object (if
        exist)"""
        self.ensure_one()
        previous_number = self.l10n_fr_secure_sequence_number - 1
        if previous_number == 0:
            previous_hash = ''
        else:
            previous_order = self.l10n_fr_previous_order
            if not previous_order:
                return ''
            previous_hash = previous_order.l10n_fr_hash
        return sha256(
            previous_hash + (self.l10n_fr_string_to_hash) or '').hexdigest()

    @api.multi
    def get_certification_information(self):
        """This function is made to allow overload for custom module
        like 'pos_order_load'"""
        return self.read(['pos_reference', 'l10n_fr_hash'])
