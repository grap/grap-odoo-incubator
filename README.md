
<!-- /!\ Non OCA Context : Set here the badge of your runbot / runboat instance. -->
[![Pre-commit Status](https://github.com/grap/grap-odoo-incubator/actions/workflows/pre-commit.yml/badge.svg?branch=12.0)](https://github.com/grap/grap-odoo-incubator/actions/workflows/pre-commit.yml?query=branch%3A12.0)
[![Build Status](https://github.com/grap/grap-odoo-incubator/actions/workflows/test.yml/badge.svg?branch=12.0)](https://github.com/grap/grap-odoo-incubator/actions/workflows/test.yml?query=branch%3A12.0)
[![codecov](https://codecov.io/gh/grap/grap-odoo-incubator/branch/12.0/graph/badge.svg)](https://codecov.io/gh/grap/grap-odoo-incubator)
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
[account_fiscal_position_tax_included](account_fiscal_position_tax_included/) | 12.0.1.1.3 | [![legalsylvain](https://github.com/legalsylvain.png?size=30px)](https://github.com/legalsylvain) | Allow to map from tax excluded to tax included
[account_invoice_attachment_count](account_invoice_attachment_count/) | 12.0.1.0.1 | [![legalsylvain](https://github.com/legalsylvain.png?size=30px)](https://github.com/legalsylvain) | Account Invoices - Attachment Count
[base_company_legal_info](base_company_legal_info/) | 12.0.1.1.4 | [![legalsylvain](https://github.com/legalsylvain.png?size=30px)](https://github.com/legalsylvain) | Adds Legal informations on company model
[database_synchronization](database_synchronization/) | 12.0.2.2.4 |  | Synchronize many Odoo Databases (datas, ...)
[duplication_account_invoice](duplication_account_invoice/) | 12.0.1.1.2 |  | Duplication Tools for Invoices with a given frequency
[duplication_sale_order](duplication_sale_order/) | 12.0.1.1.2 |  | Duplication Tools for Sale Orders with a given frequency
[mobile_kiosk_abstract](mobile_kiosk_abstract/) | 12.0.1.1.6 | [![legalsylvain](https://github.com/legalsylvain.png?size=30px)](https://github.com/legalsylvain) | Abstract Module that provides a framework to develop 'kiosk application' for mobile usage like in 'hr_attendance' Odoo module
[mobile_kiosk_inventory](mobile_kiosk_inventory/) | 12.0.1.1.6 | [![legalsylvain](https://github.com/legalsylvain.png?size=30px)](https://github.com/legalsylvain) | Mobile interface to make inventories
[mobile_kiosk_purchase](mobile_kiosk_purchase/) | 12.0.1.1.5 | [![legalsylvain](https://github.com/legalsylvain.png?size=30px)](https://github.com/legalsylvain) | Mobile interface to make purchases
[mrp_production_purchase_order_link](mrp_production_purchase_order_link/) | 12.0.1.0.1 |  | This module adds a smart button in PO and MO to link them.
[multi_search_abstract](multi_search_abstract/) | 12.0.1.1.3 |  | Multi Search - Abstract
[multi_search_partner](multi_search_partner/) | 12.0.1.1.3 |  | Multi Search - Partners
[multi_search_product](multi_search_product/) | 12.0.1.1.2 |  | Multi Search - Products
[name_search_reset_res_partner](name_search_reset_res_partner/) | 12.0.1.1.4 |  | Reset _name_search function for res.partner model
[pos_multicompany](pos_multicompany/) | 12.0.1.1.2 |  | Point of Sale Settings in Multi company context
[pos_sector](pos_sector/) | 12.0.1.1.4 |  | Set Sectors to the products and display in given PoS Sessions
[product_category_product_qty](product_category_product_qty/) | 12.0.1.1.2 |  | Product Category - Product Quantity
[product_category_usage_group](product_category_usage_group/) | 12.0.1.1.2 |  | Restrict Usage of Product Categories to a given Group
[product_default_code_res_company_code](product_default_code_res_company_code/) | 12.0.1.1.3 |  | Generate product default code based on sequence defined by company, prefixed by company code
[product_print_category](product_print_category/) | 12.0.1.1.9 |  | Automate products print, when data has changed
[product_simple_pricelist](product_simple_pricelist/) | 12.0.1.1.6 |  | Provides Wizard to manage easily Pricelist By Products
[product_uom_package](product_uom_package/) | 12.0.1.1.3 |  | Product - Package UoM and Quantity
[sale_deposit_product_per_company](sale_deposit_product_per_company/) | 12.0.1.1.2 |  | Handle one deposit product (down payment) per company
[stock_internal_use_of_products](stock_internal_use_of_products/) | 12.0.1.1.4 |  | Declare the use of products for specific uses (eg: gifts,...)
[stock_inventory_disabled_product](stock_inventory_disabled_product/) | 12.0.1.0.3 |  | Stock - Inventory disabled Products
[stock_inventory_merge](stock_inventory_merge/) | 12.0.1.1.3 |  | Allow to merge multiples partial inventories
[stock_inventory_valuation](stock_inventory_valuation/) | 12.0.1.1.4 |  | Stock Inventory - Valuation
[stock_inventory_valuation_merge](stock_inventory_valuation_merge/) | 12.0.1.1.2 |  | Stock Inventory - Valuation - Merge - Glue Module
[stock_picking_quick_quantity_done](stock_picking_quick_quantity_done/) | 12.0.1.1.4 |  | Stock Picking Quick Quantity Done
[web_base_url_force](web_base_url_force/) | 12.0.1.0.3 |  | Force the value of the setting 'web.base.url'
[web_widget_attachment_count](web_widget_attachment_count/) | 12.0.1.0.2 | [![legalsylvain](https://github.com/legalsylvain.png?size=30px)](https://github.com/legalsylvain) | Web Widget - Attachment Count

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
