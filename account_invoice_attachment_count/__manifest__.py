# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Account Invoices - Attachment Count",
    "version": "12.0.1.0.1",
    "category": "Tools",
    "license": "AGPL-3",
    "author": "GRAP,Odoo Community Association (OCA)",
    "maintainers": ["legalsylvain"],
    "website": "https://github.com/grap/grap-odoo-incubator",
    "depends": [
        "account",
        "web_widget_attachment_count",
    ],
    "data": [
        "views/view_account_invoice.xml",
    ],
    "pre_init_hook": "_hook_store_attachment_count_value",
    "installable": True,
}
