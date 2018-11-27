This module permits to quickly see the different prices of a product : price with taxes and price without taxes.

.. figure:: ../static/description/product_different_prices.png

**The four use cases**

In Customer taxes, there's a boolean called "Tax included in Price".

.. figure:: ../static/description/taxes_creation.png

**According to the customer taxes** of the product (choosen in accouting part), there are 4 possibilities :

- The sale price **AND** the sale price without taxes are displayed.

.. figure:: ../static/description/product_tax_included.png

- **Or** the sale price **AND** the sale price with taxes.

.. figure:: ../static/description/product_tax_excluded.png

- **Or** if you choose two customer taxes, one included in price, and the other one not included in price,
  this module displays the sale price and the two calculated prices.

.. figure:: ../static/description/product_tax_included_and_not.png

- **And lastly** if there's no taxe choosen, only the normal price is displayed. 
