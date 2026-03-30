This module is a glue auto installable module, to make working
`user_reduced_configuration`, when `point_of_sale` is installed.

- It allows non admin user to edit receipt header and footer.
- It avoids to make the original module failing, if user
  doesn't belong to Point Of Sale groups, and can not access `pos.config` model.
