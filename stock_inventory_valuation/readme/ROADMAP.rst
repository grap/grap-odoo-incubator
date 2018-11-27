the field ```valuation``` on ```stock.inventory.line``` is not designed
correctly for the time being : It is a computed field, and should be a
classical field with onchange. It is due to the dual API in odoo 8.0.
When porting this module in version 10.0, should be refactored in normal
field.
