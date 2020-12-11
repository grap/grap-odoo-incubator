[![Build Status](https://travis-ci.org/grap/grap-odoo-incubator.svg?branch=12.0)](https://travis-ci.org/grap/grap-odoo-incubator?branch=12.0)
[![codecov](https://codecov.io/gh/grap/grap-odoo-incubator/branch/12.0/graph/badge.svg)](https://codecov.io/gh/grap/grap-odoo-incubator)
[![Coverage Status](https://coveralls.io/repos/github/grap/grap-odoo-incubator/badge.svg?branch=12.0)](https://coveralls.io/github/grap/grap-odoo-incubator?branch=12.0)
[![Code Climate](https://codeclimate.com/github/grap/grap-odoo-incubator/badges/gpa.svg)](https://codeclimate.com/github/grap/grap-odoo-incubator)


# grap-odoo-incubator

This repository contains Odoo modules developped by the company GRAP before
they are shared to the
[Odoo Community Association](https://odoo-community.org/).

If you're interested by some of ones, please contact GRAP IT Team to work
together to improve the code or make a merge proposal into an OCA repository.

You could be interesting too by the following repositories:

* [grap-odoo-business](https://github.com/grap/grap-odoo-business)
* [grap-odoo-custom](https://github.com/grap/grap-odoo-custom)

# TODO

Fixme, remove dependency to grap-odoo-business, adding ``purchase_package_qty`` in the ``grap-odoo-incubator`` repository.

[//]: # (addons)

Available addons
----------------
addon | version | summary
--- | --- | ---
[account_fiscal_position_tax_included](account_fiscal_position_tax_included/) | 12.0.1.0.2 | Allow to map from tax excluded to tax included
[base_company_legal_info](base_company_legal_info/) | 12.0.1.0.1 | Adds Legal informations on company model
[duplication_account_invoice](duplication_account_invoice/) | 12.0.1.0.1 | Duplication Tools for Invoices with a given frequency
[duplication_sale_order](duplication_sale_order/) | 12.0.1.0.1 | Duplication Tools for Sale Orders with a given frequency
[mobile_kiosk_abstract](mobile_kiosk_abstract/) | 12.0.1.0.4 | Mobile Kiosk Absract Module
[mobile_kiosk_inventory](mobile_kiosk_inventory/) | 12.0.1.0.3 | Mobile interface to make inventories
[mobile_kiosk_purchase](mobile_kiosk_purchase/) | 12.0.1.0.6 | Mobile interface to make purchases
[multi_search_abstract](multi_search_abstract/) | 12.0.1.0.3 | Multi Search - Abstract
[multi_search_partner](multi_search_partner/) | 12.0.1.0.2 | Multi Search - Partners
[multi_search_product](multi_search_product/) | 12.0.1.0.2 | Multi Search - Products
[pos_multicompany](pos_multicompany/) | 12.0.1.0.1 | Point of Sale Settings in Multi company context
[pos_sector](pos_sector/) | 12.0.1.0.2 | Set sectors to the products and display in given PoS Sessions
[product_category_product_qty](product_category_product_qty/) | 12.0.1.0.2 | Product Category - Product Quantity
[product_category_type](product_category_type/) | 12.0.1.0.2 | Restore type field on product.category
[product_category_usage_group](product_category_usage_group/) | 12.0.1.0.1 | Restrict Usage of Product Categories to a given Group
[product_default_code_res_company_code](product_default_code_res_company_code/) | 12.0.1.0.3 | Generate product default code based on sequence defined by company, prefixed by company code
[product_print_category](product_print_category/) | 12.0.1.0.3 | Automate products print, when data has changed
[product_simple_pricelist](product_simple_pricelist/) | 12.0.1.0.1 | Provides Wizard to manage easily Pricelist By Products
[sale_deposit_product_per_company](sale_deposit_product_per_company/) | 12.0.1.0.1 | Handle one deposit product (down payment) per company
[stock_internal_use_of_products](stock_internal_use_of_products/) | 12.0.1.0.3 | Declare the use of products for specific uses (eg: gifts,...)
[stock_inventory_merge](stock_inventory_merge/) | 12.0.1.0.1 | Allow to merge multiples partial inventories
[stock_inventory_valuation](stock_inventory_valuation/) | 12.0.1.0.1 | Stock Inventory - Valuation
[stock_inventory_valuation_merge](stock_inventory_valuation_merge/) | 12.0.1.0.1 | Stock Inventory - Valuation - Merge - Glue Module
[stock_picking_quick_quantity_done](stock_picking_quick_quantity_done/) | 12.0.1.0.2 | Stock Picking Quick Quantity Done
[web_base_url_force](web_base_url_force/) | 12.0.1.0.1 | Force the value of the setting 'web.base.url'


Unported addons
---------------
addon | version | summary
--- | --- | ---
[pos_picking_load_partner_name](pos_picking_load_partner_name/) | 8.0.2.0.0 (unported) | Improve load of picking in PoS by partner name

[//]: # (end addons)

## About GRAP

<p align="center">
   <img src="http://www.grap.coop/wp-content/uploads/2016/11/GRAP.png" width="200"/>
</p>

GRAP, [Groupement Régional Alimentaire de Proximité](http://www.grap.coop) is a
french company which brings together activities that sale food products in the
region Rhône Alpes. We promote organic and local food, social and solidarity
economy and cooperation.

The GRAP IT Team promote Free Software and developp all the Odoo modules under
AGPL-3 Licence. You can get find all this modules here :
* on the [OCA Apps Store](https://odoo-community.org/shop?&search=GRAP)
* on the [Odoo Apps Store](https://www.odoo.com/apps/modules/browse?author=GRAP).
