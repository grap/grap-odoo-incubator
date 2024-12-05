Implement the recursive creation of parent for the model Product Categories.
(``product.category``).

In the product view, if a user enter in the category field the name
**'All / New Category'**, it will not create a category with such name.
Instead, it will look for a category named **'All'** (and create it if it
doesn't exists), then create a new category named **'New Category'** with the category **'All'** as parent.

If a user create or update the name of a category, any **'/'** char will
be replaced by the char **'-'**.

At the installation, all **'/'** in the names of the categories
will be replaced by **'-'**.