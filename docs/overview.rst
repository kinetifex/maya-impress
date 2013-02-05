
Overview
=======================================

Impress is a Maya Python module that helps make custom functions feel like native Maya commands.
This package implements a MVC framework for Maya and reduces code repetition.
A major influence for this package is the Django web framework.


Models
---------------------------------------

Models are stored settings of the arguments to your function, coupled with ui controls.
Fields are added as members of a Model class.

When defining fields, name them the same as the arguments of your function.
The order in which field members are defined is the order that the ui controls will appear in.
Fields keep track of their value settings, storing them as option variables across Maya sessions.


Views
---------------------------------------

A View is a Maya inteface that displays the controls of an Model.
The default View uses the Maya built-in OptionBox.
Custom intefaces can be developed and passed as a viewtype when instanciating a PerformCommand.


PerformCommands
---------------------------------------

Instantiate a PerformCommand to register a function with a Model and an View.
Controls are automatically populated in the View based on the Model's fields.

A PerformCommand can be called with an action argument with the follwing 3 values:

- 0 - The function will be called with user's last option settings.
- 1 - The OptionBox window will display with ui controls for each field.
- 2 - This does a "dry-run" of the command, printing the function and arguments that would be executed.

PerformCommands also register with Maya as Runtime Commands, available in the Hotkey Editor.


RuntimeCommands
---------------------------------------

Use RuntimeCommands to register functions with Maya as Runtime Commands, making them available in the Hotkey Editor.
These can also be used as create shortcuts for common function variants with predefined arguments.