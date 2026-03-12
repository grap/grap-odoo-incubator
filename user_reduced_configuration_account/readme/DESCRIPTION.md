This module is a glue auto installable module, to make working
`user_reduced_configuration`, when `account` is installed.
It doesn't bring any new feature,
but avoid to make the original module failing, if user
want to install new accounting package. (`account.chart.template`)
as the original odoo Code hardcode a `is_admin()` test before
installing new chart of accounts.
