- Ekibio
- Relais Local
- Agrosourcing
- Vitafrais


Unlink vs set price to 0 ?



to have a Generic module that can be shared to the OCA :

- Move in a dedicated module:
    * yaml files in ``invoice2data_templates`` folder.
    * ``_get_extra_products`` in ``wizards/wizard_invoice2data_import_line.py``

- Remove dependencies to triple discount module.
