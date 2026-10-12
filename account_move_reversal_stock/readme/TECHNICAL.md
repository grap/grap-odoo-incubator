In order to Keep it stupid Simple :

* code doesn't handle multiple sale lines linked to one line in invoice,
that's why you can read "invoice_line.sale_line_ids[:1]"
* code takes first picking of the Invoice to get Pickings locations, see
'first_picking = account_move.picking_ids[:1]'

Limits:

* if you add a second credit note after a first one, qty in SO is not updated well
