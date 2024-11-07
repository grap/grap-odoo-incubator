/** @odoo-module **/
/*
Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
*/

import { SwitchCompanyMenu } from "@web/webclient/switch_company_menu/switch_company_menu";
import { browser } from "@web/core/browser/browser";
import { patch } from "@web/core/utils/patch";
import { session } from "@web/session";
import { symmetricalDifference } from "@web/core/utils/arrays";

patch(
    SwitchCompanyMenu.prototype,
    "web_select_only_child_company.SwitchCompanyMenu",
    {
        logIntoCompany(companyId) {
            browser.clearTimeout(this.toggleTimer);
            var newCompanyIds = [companyId].concat(session.user_companies.allowed_companies[companyId].all_child_ids);
            var companiesToToggle = symmetricalDifference(this.companyService.allowedCompanyIds, newCompanyIds);
            if (companiesToToggle.length !== 0) {
                this.companyService.setCompanies("switch", ...newCompanyIds);
            }
        },
    }
);

export default SwitchCompanyMenu;
