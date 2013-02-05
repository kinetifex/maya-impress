
Advanced Models
=======================================

1. Add dependencies to options.
2. Customize field controls.
3. Pass meta data to our View.


Option Requirements
---------------------------------------

Previously in our tutorial, we made a function that has aurguments for `repeat`, and `count`, which is for the the number of times it should repeat if `repeat` is selected. Now obviously we could just remove `repeat` and set `count` to 0 when we don't want it to repeat. However, `repeat` is there in order to demonstrate the additional field param `requires`:

.. code-block:: python
    :emphasize-lines: 6

    from impress import models

    class MyExampleOptions( models.OptionModel ):
        name = models.TextField( "some text" )
        repeat = models.CheckBox( False )
        count = models.IntField( 3, requires=(repeat, True) )

The `requires` param take a tuple 2 elements: another field and value to test against. In our case, we are watching for when the `repeat` field is set to `True`. The required value's type should coorespond to the tyoe of the required field. More advanced comparisons can be done by using a `lambda` which accepts the required value as an argument.


Customize Control Appearance
---------------------------------------

Options proxy Maya's UI Control Group commands and accept all parameters of their counterparts. For example, the `count` field which is an ``models.IntField``, uses Maya's ``intFieldGrp`` command to construct its UI controls. Some parameters are establish automatically by ``models.IntField``, however most of the visual ones are available for tweaking.

As an example, let's change up the labeling:

.. code-block:: python
    :emphasize-lines: 4

    class MyExampleOptions( models.OptionModel ):
        name = models.TextField( "some text" )
        repeat = models.CheckBox( False )
        count = models.IntField( 3, requires=(repeat, True), label='', extraLabel='times' )

When loading up the option box window now, you'll see that the `count` control no longer has a left label, but now says "times" to the right of the field.


Customize View Appearance
---------------------------------------

Views can have data passed to them via Meta data in Models which can be used to customize elements of the view. To demonstrate this, lets change the button label of the Apply/Close button on the Option Box View:

.. code-block:: python
    :emphasize-lines: 6-7

    class MyExampleOptions( models.OptionModel ):
        name = models.TextField( "some text" )
        repeat = models.CheckBox( False )
        count = models.IntField( 3, requires=(repeat, True), label='', extraLabel='times' )

        class Meta:
            button_label = 'Do Example'

Now when opening the Option Box, the bottom left button should read "Do Example".