# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Quentin DUPONT (https://twitter.com/pondupont)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Default Code with Company Code",
    "summary": "Generate product default code based on sequence"
    " defined by company, prefixed by company code",
    "version": "12.0.1.1.0",
    "category": "Product",
    "author": "GRAP",
    "website": "http://www.grap.coop",
    "license": "AGPL-3",
    "depends": [
        "product",
        "res_company_code",
    ],
    "post_init_hook": "_create_company_sequence",
    "installable": True,
}
