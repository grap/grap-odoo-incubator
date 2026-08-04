
<!-- /!\ Non OCA Context : Set here the badge of your runbot / runboat instance. -->
[![Pre-commit Status](https://github.com/grap/grap-odoo-incubator/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/grap/grap-odoo-incubator/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/grap/grap-odoo-incubator/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/grap/grap-odoo-incubator/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/grap/grap-odoo-incubator/branch/16.0/graph/badge.svg)](https://codecov.io/gh/grap/grap-odoo-incubator)
<!-- /!\ Non OCA Context : Set here the badge of your translation instance. -->

<!-- /!\ do not modify above this line -->

# Incubator of Odoo (formely OpenERP) modules before they are shared to the OCA

This repository contains Odoo modules developped by the company GRAP before they are shared to the Odoo Community Association.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_move_attachment_count](account_move_attachment_count/) | 16.0.1.0.2 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Account Invoices - Attachment Count
[account_move_reversal_stock](account_move_reversal_stock/) | 16.0.1.1.0 |  | Facilitates the link between customer and inventory management.
[calendar_security](calendar_security/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Add a group to display 'Calendar' Application menu entry
[create_recursive_abstract](create_recursive_abstract/) | 16.0.2.0.3 |  | Create recursively parents item.
[create_recursive_pos_category](create_recursive_pos_category/) | 16.0.1.0.2 |  | Extra GRAP Tools to import product data for Point of sale module
[create_recursive_product_category](create_recursive_product_category/) | 16.0.1.0.3 |  | Create recursively parents item for the Product Categories model.
[hr_expense_vat_incl_improved](hr_expense_vat_incl_improved/) | 16.0.1.1.3 |  | Improve HR Expense management, regarding VAT.
[l10n_fr_account_move_partner_required_fields](l10n_fr_account_move_partner_required_fields/) | 16.0.1.1.3 |  | L10N FR Account Move Partner Required Fields
[pos_account_bank_statement_line_cash_move_reason](pos_account_bank_statement_line_cash_move_reason/) | 16.0.2.0.0 |  | PoS Account Bank Statement Line - Cash Move Reason
[pos_sector](pos_sector/) | 16.0.1.1.5 |  | Set Sectors to the products and display in given PoS Sessions
[product_accounts](product_accounts/) | 16.0.1.0.2 |  | Compute and display income - expense account at product level
[product_simple_pricelist](product_simple_pricelist/) | 16.0.1.1.2 |  | Provides Wizard to manage easily Pricelist By Products
[product_uom_company_favorite](product_uom_company_favorite/) | 16.0.1.0.4 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Possilibity to set favorite product units of Measure per company
[sale_down_payment_product_per_company](sale_down_payment_product_per_company/) | 16.0.1.0.0 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> <a href='https://github.com/quentinDupont'><img src='https://github.com/quentinDupont.png' width='32' height='32' style='border-radius:50%;' alt='quentinDupont'/></a> | Handle Down Payment products per company and tax
[stock_picking_account_move](stock_picking_account_move/) | 16.0.1.2.1 |  | Stock Picking Account Move
[stock_picking_quick_quantity_done](stock_picking_quick_quantity_done/) | 16.0.2.0.0 |  | Stock Picking Quick Quantity Done
[stock_picking_quick_quantity_done_sale](stock_picking_quick_quantity_done_sale/) | 16.0.2.0.0 | <a href='https://github.com/quentinDupont'><img src='https://github.com/quentinDupont.png' width='32' height='32' style='border-radius:50%;' alt='quentinDupont'/></a> | Sale - Picking Quick Confirm
[stock_picking_valuation](stock_picking_valuation/) | 16.0.1.1.1 |  | Stock Picking Valuation
[user_limited_access_settings](user_limited_access_settings/) | 16.0.1.0.6 |  | Create a new Administration group with limited access to create only users and companies
[user_reduced_configuration](user_reduced_configuration/) | 16.0.3.0.0 |  | Allow user to have limited access to configuration elements
[user_reduced_configuration_account](user_reduced_configuration_account/) | 16.0.2.0.0 |  | Glue module to allow users to have limited access to configuration elements, when account is installed.
[user_reduced_configuration_pos](user_reduced_configuration_pos/) | 16.0.1.0.1 |  | Glue module to allow users to have limited access to configuration elements, when point of sale is installed.
[web_select_only_child_company](web_select_only_child_company/) | 16.0.1.0.2 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | When selecting a company, automatically select all the child companies.
[web_widget_attachment_count](web_widget_attachment_count/) | 16.0.1.0.2 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Web Widget - Attachment Count

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to GRAP
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----

## About GRAP

<p align="center">
   <img src="http://www.grap.coop/wp-content/uploads/2016/11/GRAP.png" width="200"/>
</p>

GRAP, [Groupement Régional Alimentaire de Proximité](http://www.grap.coop) is a
french company which brings together activities that sale food products in the
region Rhône Alpes. We promote organic and local food, social and solidarity
economy and cooperation.

The GRAP IT Team promote Free Software and developp all the Odoo modules under
AGPL-3 Licence.

You can find all these modules here:

* on the [OCA Apps Store](https://odoo-community.org/shop?&search=GRAP)
* on the [Odoo Apps Store](https://www.odoo.com/apps/modules/browse?author=GRAP).
* on [Odoo Code Search](https://odoo-code-search.com/ocs/search?q=author%3AOCA+author%3AGRAP)

You can also take a look on the following repositories:

* [grap-odoo-incubator](https://github.com/grap/grap-odoo-incubator)
* [grap-odoo-business](https://github.com/grap/grap-odoo-business)
* [grap-odoo-business-supplier-invoice](https://github.com/grap/grap-odoo-business-supplier-invoice)
* [odoo-addons-logistics](https://github.com/grap/odoo-addons-logistics)
* [odoo-addons-cae](https://github.com/grap/odoo-addons-cae)
* [odoo-addons-intercompany-trade](https://github.com/grap/odoo-addons-intercompany-trade)
* [odoo-addons-multi-company](https://github.com/grap/odoo-addons-multi-company)
* [odoo-addons-company-wizard](https://github.com/grap/odoo-addons-company-wizard)
