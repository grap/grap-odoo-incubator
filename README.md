
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
[account_move_attachment_count](account_move_attachment_count/) | 16.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Account Invoices - Attachment Count
[create_recursive_abstract](create_recursive_abstract/) | 16.0.2.0.1 |  | Create recursively parents item.
[create_recursive_pos_category](create_recursive_pos_category/) | 16.0.1.0.1 |  | Extra GRAP Tools to import product data for Point of sale module
[create_recursive_product_category](create_recursive_product_category/) | 16.0.1.0.1 |  | Create recursively parents item for the Product Categories model.
[hr_expense_vat_incl_improved](hr_expense_vat_incl_improved/) | 16.0.1.1.1 |  | Improve HR Expense management, regarding VAT.
[l10n_fr_account_move_partner_required_fields](l10n_fr_account_move_partner_required_fields/) | 16.0.1.1.1 |  | L10N FR Account Move Partner Required Fields
[product_accounts](product_accounts/) | 16.0.1.0.1 |  | Compute and display income - expense account at product level
[product_simple_pricelist](product_simple_pricelist/) | 16.0.1.1.1 |  | Provides Wizard to manage easily Pricelist By Products
[product_uom_company_favorite](product_uom_company_favorite/) | 16.0.1.0.3 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Possilibity to set favorite product units of Measure per company
[sale_picking_quick_confirm](sale_picking_quick_confirm/) | 16.0.1.1.1 | <a href='https://github.com/quentinDupont'><img src='https://github.com/quentinDupont.png' width='32' height='32' style='border-radius:50%;' alt='quentinDupont'/></a> | Sale Picking Quick Confirm
[stock_picking_account_move](stock_picking_account_move/) | 16.0.1.2.0 |  | Stock Picking Account Move
[stock_picking_quick_quantity_done](stock_picking_quick_quantity_done/) | 16.0.1.0.1 |  | Stock Picking Quick Quantity Done
[user_limited_access_settings](user_limited_access_settings/) | 16.0.1.0.4 |  | Create a new Administration group with limited access to create only users and companies
[web_select_only_child_company](web_select_only_child_company/) | 16.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | When selecting a company, automatically select all the child companies.
[web_widget_attachment_count](web_widget_attachment_count/) | 16.0.1.0.1 | <a href='https://github.com/legalsylvain'><img src='https://github.com/legalsylvain.png' width='32' height='32' style='border-radius:50%;' alt='legalsylvain'/></a> | Web Widget - Attachment Count

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
