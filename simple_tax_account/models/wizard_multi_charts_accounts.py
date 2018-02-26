# -*- coding: utf-8 -*-
# Copyright (C) 2018-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class WizardMultiChartsAccounts(models.TransientModel):
    _inherit = 'wizard.multi.charts.accounts'

    @api.model
    def _load_template(
            self, template_id, company_id, code_digits=None, obj_wizard=None,
            account_ref=None, taxes_ref=None, tax_code_ref=None):
        res = super(WizardMultiChartsAccounts, self)._load_template(
            template_id, company_id, code_digits=code_digits,
            obj_wizard=obj_wizard, account_ref=account_ref,
            taxes_ref=taxes_ref, tax_code_ref=tax_code_ref)
        for template_id, tax_id in res[1].iteritems():
            template = self.env['account.tax.template'].browse(template_id)
            tax = self.env['account.tax'].browse(tax_id)
            if template.simple_template_id:
                related_tax_id = res[1].get(template.simple_template_id.id)
                tax.simple_tax_id = related_tax_id
        return res
