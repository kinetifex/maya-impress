
Get Started
=======================================

1. Create a function with arguments.
2. Create a model of fields for arguments.
3. Register your function and model.
4. Impress your Maya users!


Set the Stage
---------------------------------------

In order to demostrate how Impress works we should start with a simple example function::

    def myExample( name, repeat=False, count=3 ):
        """Simple command that prints a string."""
        if repeat:
            for i in range( count ):
                print name
        else:
            print name


Okay, so we now have a working function that we want to hand off to our art team. You may be tempted to hand this off as-is, just showing artists how to change input params in the script editor, or copy/paste different versions into shelf scripts, or something like that. However, what you really should do is make them a nice option box window so that they can easily change and save setting. This is where Impress comes in.


Choose the Options
---------------------------------------

The first thing we need to do is define the group of options that we want for this function::

    from impress import models

    class MyExampleOptions( models.OptionModel ):
        name = models.TextField( "some text" )
        repeat = models.CheckBox( False )
        count = models.IntField( 3 )


We do this by creating a new class which inherits from OptionModel. The members of this class are the different `field` that we want to track, and should share the same names as the arguments of our function. The first argument of any `field` is the default value.


Register the Command
---------------------------------------

We now need to register our OptionModel with our function by creating a PerformCommand::

    from impress import register

    performMyExample = register.PerformCommand( myExample, MyExampleOptions )

The name of the PerformCommand instance should be the name of the function with the first character capitalized, preceeded with *perform*. It is important to be consistent with this naming convention when defining PerformCommands. If you wish to use a different name for your instance, you must also instanciate the PerformCommand with the ``name`` kwarg as the alternate name. For example::

    performOtherExample = register.PerformCommand( myExample, MyExampleOptions, name="performOtherExample" )


Execute the Command
---------------------------------------

PerformCommands are patterned off of perform commands commonly found in MEL. They have ``action`` argument which if 0 (default) will execute the function with the last option settings, or if 1, will open the option box window::

    # execute command with last settings
    performMyExample()

    # show the option box
    performMyExample( 1 )


Access the Option Box
---------------------------------------

Go ahead and open up the option box by running::

    performMyExample( 1 )

In it you should see controls for the 3 fields.

*Incomplete*


Assign Hotkeys
---------------------------------------

Creating a PerformCommand also makes it accessible as a runtime command in the Hotkey Editor. By Default, the command category will be based on the module name that the PerformCommand exists in. Since you are probably following along this tutorial in the script editor, the category for our PerformMyExample will end up being *Uncategorized*.

In the *Uncategorized* category, you should see 2 commands: PerformMyExample and PerformMyExampleOptions. Just like built-in Maya commands, this allows users to map hotkeys to execute the function with settings, or to open the option box.

If, for example, you have a PerformCommand in a module such as `myCompany.animation`, the category generated would be `My Company Animation`. A category can also be specified by suppling the `category` argument when initializing the PerformCommand::

    performMyExample = register.PerformExample( myExample, MyExampleOptions, category="Custom Examples" )