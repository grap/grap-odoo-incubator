from odoo import models


class AccountChartTemplate(models.Model):
    _inherit = "account.chart.template"

    def _load(self, company):
        # we replace a test of is_admin() by a
        # test if user belong to account.group_account_manager
        if (
            self.env.context.get("execute_in_reduced_configuration_context")
            and not self.env.is_admin()
            and self.env.user.has_group("account.group_account_manager")
        ):
            return super(AccountChartTemplate, self.sudo())._load(company)
        return super()._load(company)
