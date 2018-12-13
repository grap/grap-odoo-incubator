* Go to 'Setting / Technical / Mass Operations / Merging Content'

* Create a new item

  ..figure: ../static/description/mass_merging_content_form.png

* Set a name for the button that will appear on the target model

* choose a model, and select a ``one2many`` fields of this model

* for each field of this submodel, select the operation type

1. 'Group' : the lines will not be merged if this field is different

2. 'Sum': the value of this field will be sumed into the merged lines.
   (usefull for ``integer`` and ``float`` fields)

3. 'Join Texts': the value of this field will be joined.
    (usefull for ``char`` fields)

4. 'Related Value': the value will be recomputed, based on the given extra
   argument.

* Once done, click on the 'Add Sidebar button' to generate a new 'More options'
  button.


**Extra options**

* you can define a domain, to limit the merge operation to items that match
  with that domain.
* you can define groups whose members will have access to that option.
