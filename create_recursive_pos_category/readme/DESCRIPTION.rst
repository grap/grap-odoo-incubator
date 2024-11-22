Implement the recursive creation of parent for the model PoS Categories.
(``pos.category``).

In the product view, if a user enter in the PoS category field the name
**'Chairs / Little'**, it will not create a category with such name.
Instead, it will look for a category named **'Chairs'** (and create it if it
doesn't exists), then create a new category named **'Little'** with the category
**'Chairs'** as parent.

If a user create or update the name of a PoS category, any **'/'** char will
be replaced by the char **'-'**.

At the installation, all **'/'** in the names of the PoS categories
will be replaced by **'-'**.