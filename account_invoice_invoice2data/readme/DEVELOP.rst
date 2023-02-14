**Regex Attention**

When you write the 'lines' regex, be careful that writing a multi lines regex in the
yaml file create implicite space for each return to the line :

.. code-block:: yaml
    line: ^(?P<product_code>\d+)
      (?P<product_name>.*)

is equivalent to

.. code-block:: yaml
    line: ^(?P<product_code>\d+)\s(?P<product_name>.*)

**Regex Common Pattern**

* Float quantity : ``\d+\.\d+`` ; exemple : ``47.53``
* Price with space delimiter : ``[\d\s?]+\.\d+`` ; exemple : ``1 422.99``
* Long date format : ``\d{2}/\d{2}/\d{4}`` ; exemple : ``22/04/1982``
* Short date format : ``\d{2}/\d{2}/\d{2}`` ; exemple : ``22/04/82``
