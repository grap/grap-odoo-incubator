This module facilitates the link between customer and inventory management :
it adds a function that create the right Stock Pickings according
to the Refund method you use :

- With classic Credit Note, create a Return Stock Picking with new quantities
- With the 'modify' flow, create Return Stock Picking and / or Stock Picking
according to quantity differentials.

It update quantities in Sale Order and keep links between documents SO, WH, IN

In this example, user invoices 50 units instead of 117 delivered.
So the buttons appears to ease stock adjustements

..figure :: ../static/description/account_move_reversal_stock_invoice_diff.png
..figure :: ../static/description/account_move_reversal_stock_sale_order_diff.png

And it create a Return Pickings.

..figure :: ../static/description/account_move_reversal_stock_pickings.png
