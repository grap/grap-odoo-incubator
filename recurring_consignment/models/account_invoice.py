# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    # Column Section
    is_consignment_invoice = fields.Boolean(
        string='Is Consignment Invoice', readonly=True)

    consignment_line_ids = fields.One2many(
        comodel_name='account.move.line',
        inverse_name='consignment_invoice_id',
        string='Commissionned Lines', readonly=True)

    # Public Function
    @api.model
    def get_commission_information_summary(self, invoice):
        move_line_obj = self.env['account.move.line']
        groups = {}
        res = []
        sorted_lines = move_line_obj.search(
            [('id', 'in', invoice.consignment_line_ids.ids)],
            order='tax_code_id, name')
        for move_line in sorted_lines:
            key = self._get_commission_key(move_line)
            groups.setdefault(key, [])
            groups[key].append(move_line)
        for key, value in groups.iteritems():
            (kind, name) = key
            amount = 0
            for move_line in value:
                amount += move_line.credit - move_line.debit
            res.append({
                'type': kind,
                'name': name,
                'amount': amount,
                'is_commission': (kind == 'revenue')})
        return res

    @api.model
    def get_commission_information_accounting_detail(self, invoice):
        move_line_obj = self.env['account.move.line']
        res = []
        sorted_lines = move_line_obj.search(
            [('id', 'in', invoice.consignment_line_ids.ids)],
            order='date, move_id, tax_code_id, name')
        for move_line in sorted_lines:
            tmp = self._get_commission_key(move_line)
            res.append({
                'date': move_line.date,
                'name': move_line.move_id.name,
                'description': tmp[1],
                'debit': move_line.debit,
                'credit': move_line.credit,
                'is_commission': tmp[0] == 'revenue',
            })
        return res

    @api.model
    def get_commission_information_product_detail(self, invoice):
        product_obj = self.env['product.product']

        invoice_obj = self.env['account.invoice']
        invoice_line_obj = self.env['account.invoice.line']
        order_obj = self.env['pos.order']
        order_line_obj = self.env['pos.order.line']

        groups = {}
        res = []

        # Get Product ids
        consignor_products = product_obj.with_context(
            active_test=False).search([
                ('consignor_partner_id', '=', invoice.partner_id.id)])

        # Get Account Move
        move_ids = list(
            set([x.move_id.id for x in invoice.consignment_line_ids]))

        # Get related invoice
        com_invoices = invoice_obj.search([('move_id', 'in', move_ids)])

        com_invoice_lines = invoice_line_obj.search([
            ('invoice_id', 'in', com_invoices.ids),
            ('product_id', 'in', consignor_products.ids),
        ])

        for com_invoice_line in com_invoice_lines:
            key = (
                com_invoice_line.product_id.id,
                com_invoice_line.price_unit,
                com_invoice_line.discount,
            )
            groups.setdefault(key, {
                'quantity': 0,
                'total_vat_excl': 0,
            })
            groups[key] = {
                'quantity': groups[key]['quantity'] +
                com_invoice_line.quantity,
                'total_vat_excl': groups[key]['total_vat_excl'] +
                com_invoice_line.price_subtotal,
            }

        # Tricky. The ORM call this function when basic user without
        # PoS Access want to print invoices
        if self.env.user.has_group(
                'recurring_consignment.group_consignment_user'):
            # Get related pos order
            com_orders = order_obj.search([('account_move', 'in', move_ids)])

            com_order_lines = order_line_obj.search([
                ('order_id', 'in', com_orders.ids),
                ('product_id', 'in', consignor_products.ids),
            ])

            for com_order_line in com_order_lines:
                key = (
                    com_order_line.product_id.id,
                    com_order_line.price_unit,
                    com_order_line.discount,
                )
                groups.setdefault(key, {
                    'quantity': 0,
                    'total_vat_excl': 0,
                })
                groups[key] = {
                    'quantity': groups[key]['quantity'] +
                    com_order_line.qty,
                    'total_vat_excl': groups[key]['total_vat_excl'] +
                    com_order_line.price_subtotal,
                }

        # Compute sum of each product
        for key, value in groups.iteritems():
            (product_id, price_unit, discount) = key
            product = product_obj.browse(product_id)
            res.append({
                'product_code': product.default_code,
                'product_name': product.name,
                'price_unit': price_unit,
                'discount': discount,
                'quantity': value['quantity'],
                'total_vat_excl': value['total_vat_excl'],
            })
        return sorted(
            res,
            key=lambda k: (
                k['product_name'], - k['price_unit'], k['discount']))

    # TODO improve me
    # Please, I, don't like this kind of code
    # I'm so ashamed... (with french sentences..., bad boy...)
    @api.model
    def _get_commission_key(self, move_line):
        if move_line.tax_code_id.consignment_product_id:
            # That is Vat Excl Revenue
            if '2,1' in move_line.tax_code_id.name:
                return (
                    'revenue',
                    _("Encaissement de Chiffre d'affaire HT (TVA à 2,1%)"))
            elif '5,5' in move_line.tax_code_id.name:
                return (
                    'revenue',
                    _("Encaissement de Chiffre d'affaire HT (TVA à 5,5%)"))
            elif '20' in move_line.tax_code_id.name:
                return (
                    'revenue',
                    _("Encaissement de Chiffre d'affaire HT (TVA à 20,0%)"))
            else:
                return (
                    'revenue',
                    _("Erreur Produit. TVA non trouvée"))
        else:
            # That is Tax
            if '2,1' in move_line.name:
                return ('tax', _('Encaissement de TVA à 2,1%'))
            elif '5,5' in move_line.name:
                return ('tax', _('Encaissement de TVA à 5,5%'))
            elif '20' in move_line.name:
                return ('tax', _('Encaissement de TVA à 20,0%'))
            else:
                return ('tax', _('Erreur Taxe. TVA non trouvée'))
