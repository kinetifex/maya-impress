"""
Module for defining models to organize the data and options to be tracked.
"""

import itertools
import maya.cmds as mc
import pymel.core as pm
import utils
import ui


class Model( object ):
    """
    The base model.
    """

    class Meta:
        pass

    def __init__( self ):
        self.fields = []

        # -- prepare fields and add to list
        for name, field in self.__class__.__dict__.iteritems():
            if isinstance( field, Field ):
                if field.name is None:
                    field.name = name

                self.fields.append( field )

        self.fields.sort( key=lambda field: field.id )



class OptionModel( Model ):
    """
    Used to setup fields that have stored optionVar settings.
    """

    def preApply( self ):
        """
        Must return a dict of kwargs which will be passed to function.
        Returning None will cancel the command.
        """
        return {}


class Field( object ):
    """
    The base field.
    """

    newid = itertools.count().next

    def __init__( self, **kwargs ):
        self.id = Field.newid()


class Separator( Field ):
    """
    Dummy field used to add seperation between gui controls in a view.
    """

    def __init__( self, name=None, **kwargs ):
        super( Separator, self ).__init__()

        self.name = name
        self.widget_kwargs = kwargs


    def buildWidget( self, **kwargs ):
        """Builds the field gui control."""

        kwargs.update( self.widget_kwargs )

        self._widget = pm.separator( **kwargs )



class OptionField( Field ):
    """
    The Base Option field which supports optionVar settings and gui controls.

    Must be subclassed and requires properties for:
        widget_command as statcmethod
        widget_value_arg
        widget_numberof_arg
    """

    def __init__( self, default, label=None, labels=[], requires=None, name=None, varname=None, **kwargs ):
        super( OptionField, self ).__init__()

        if not hasattr( self, 'widget_command' ):
            raise NotImplementedError( "OptionField must be sub-classed with required properties: 'widget_command', 'widget_value_arg'." )

        self.default = default
        self.label = label
        self.labels = labels
        self.requires = requires

        self.name = name
        self._varname = varname
        self.as_list = isinstance( default, ( list, tuple ) ) and hasattr( self, 'widget_numberof_arg' )
        self.widget_kwargs = kwargs

    @staticmethod
    def _valueArgs( values ):
        return dict( zip( ['value1', 'value2', 'value3', 'value4'][:len( values )], values ) )

    @staticmethod
    def _labelArgs( labels ):
        return dict( zip( ['label1', 'label2', 'label3', 'label4'][:len( labels )], labels ) )

    @property
    def varname( self ):
        if self._varname is None:
            self._varname = "%s_%s" % ( self.__class__.__name__, self.name )
        return self._varname


    def setDefault( self ):
        """Set the optionVar to default value."""
        pm.optionVar[ self.varname ] = self.default


    def get( self ):
        """Gets the optionVar value, or default if it has not been set."""
        try:
            value = pm.optionVar[ self.varname ]
            if self.as_list:
                if not isinstance( value, ( list, tuple ) ):
                    value = ( value, )
            return value
        except:
            return self.default


    def set( self, value ):
        """Sets the optionVar to the specified value."""
        pm.optionVar[ self.varname ] = value


    @property
    def widget_label( self ):
        if self.label is not None:
            return self.label
        else:
            return utils.niceName( self.name )


    def buildWidget( self, **kwargs ):
        """Builds the field gui control."""

        kwargs.update( self.widget_kwargs )

        if self.as_list:
            kwargs[ self.widget_numberof_arg] = len( self.default )
            kwargs.update( self._valueArgs( self.get() ) )
            kwargs.update( self._labelArgs( self.labels ) )
        else:
            kwargs[self.widget_value_arg] = self.get()
            if self.labels:
                kwargs.update( self._labelArgs( self.labels ) )

        self._widget = self.widget_command( label=self.widget_label, **kwargs )


    def updateWidget( self ):
        """Updates the field gui control."""
        self.setWidgetValue( self.get() )

        if self.requires:
            field, cmp = self.requires
            if hasattr( cmp, '__call__' ):
                enable = cmp( field.getWidgetValue() )
            else:
                enable = field.getWidgetValue() == cmp

            self.widget_command( self._widget, edit=1, enable=enable )


    def getWidgetValue( self ):
        """Gets the current value of the field gui control."""
        if self.as_list:
            values = []
            for i in range( len( self.default ) ):
                kwarg = {'value%d' % ( i + 1 ):True}
                values.append( self.widget_command( self._widget, query=1, **kwarg ) )
            return values
        else:
            return self.widget_command( self._widget, query=1, **{self.widget_value_arg:True} )


    def setWidgetValue( self, value ):
        """Sets the value of the field gui control."""
        kwargs = {}
        if self.as_list:
            kwargs.update( self._valueArgs( value ) )
        else:
            kwargs[self.widget_value_arg] = self.get()

        self.widget_command( self._widget, edit=1, **kwargs )


class CheckBox( OptionField ):
    """
    Store one to four booleans with check box controls.

    :default type:  bool or bool list
    :command:       `checkBoxGrp`
    """

    widget_command = staticmethod( mc.checkBoxGrp )
    widget_value_arg = 'value1'
    widget_numberof_arg = 'numberOfCheckBoxes'


class IntField( OptionField ):
    """
    Store one to four integers with int field controls.

    :default type:  int or int list
    :command:       `intFieldGrp`
    """

    widget_command = staticmethod( mc.intFieldGrp )
    widget_value_arg = 'value1'
    widget_numberof_arg = 'numberOfFields'


class IntSlider( OptionField ):
    """
    Store one integer with a slider controls.

    :default type:  int
    :command:       `intSliderGrp`
    """

    widget_command = staticmethod( mc.intSliderGrp )
    widget_value_arg = 'value'


class FloatField( OptionField ):
    """
    Store one to four floats with float field controls.

    :default type:  float or float list
    :command:       `floatFieldGrp`
    """

    widget_command = staticmethod( mc.floatFieldGrp )
    widget_value_arg = 'value1'
    widget_numberof_arg = 'numberOfFields'


class FloatSlider( OptionField ):
    """
    Store one float with a slider controls.

    :default type:  float
    :command:       `floatSliderGrp`
    """

    widget_command = staticmethod( mc.floatSliderGrp )
    widget_value_arg = 'value'


class ColorSlider( OptionField ):
    """
    Store one color (3 element float list) with a slider controls.

    :default type:  float list
    :command:       `colorSliderGrp`
    """

    widget_command = staticmethod( mc.colorSliderGrp )
    widget_value_arg = 'rgbValue'


class RadioButton( OptionField ):
    """
    Store one int with multiple radio button controls.

    :default type:  int
    :command:       `radioButtonGrp`
    """

    widget_command = staticmethod( mc.radioButtonGrp )
    widget_value_arg = 'select'
    widget_numberof_arg = 'numberOfRadioButtons'


    def __init__( self, basezero=False, **kwargs ):
        super( RadioButton, self ).__init__( **kwargs )
        self.basezero = basezero

    def buildWidget( self, **kwargs ):

        kwargs.update( self.widget_kwargs )

        self._widgets = []
        collection = None

        for i in xrange( 0, len( self.labels ), 4 ):

            labels = self.labels[i:i + 4]
            kwargs.update( self._labelArgs( labels ) )
            kwargs[ self.widget_numberof_arg] = len( labels )

            if collection is None:
                kwargs['label'] = self.widget_label
            else:
                kwargs['shareCollection'] = collection
                kwargs['label'] = ''

            try:
                widget = self.widget_command( **kwargs )
            except:
                # for some reason setting the sharedCollection fails...
                # the second time the field window is built..
                # even though it functions properly ???
                kwargs.pop( 'shareCollection' )
                widget = self.widget_command( **kwargs )

            if collection is None:
                collection = widget

            self._widgets.append( widget )


    def updateWidget( self ):
        self.setWidgetValue( self.get() )

        if self.requires:
            field, value = self.requires
            if hasattr( value, '__call__' ):
                enable = value( field.getWidgetValue() )
            else:
                enable = field.getWidgetValue() == value

            for widget in self._widgets:
                self.widget_command( widget, edit=1, enable=enable )


    def getWidgetValue( self ):
        i = 0
        for widget in self._widgets:
            value = self.widget_command( widget, query=1, **{self.widget_value_arg:True} )
            if value < 1:
                i += 4
                continue
            else:
                result = value + i
                if self.basezero:
                    result -= 1
                return result


    def setWidgetValue( self, value ):
        if self.basezero:
            value += 1
        elif value == 0:
            pm.mel.warning( "Can not set %s value to '0'. Requires 'basezero=True' " % self.__class__.__name__ )
            value = 1

        row_num = ( value - 1 ) / 4
        row_value = value - row_num * 4

        self.widget_command( self._widgets[row_num], edit=1, **{self.widget_value_arg:row_value} )


class OptionMenu( OptionField ):
    """
    Store one string with an option menu control.

    :default type:  string
    :command:       `optionMenuGrp`
    """

    widget_command = staticmethod( mc.optionMenuGrp )
    widget_value_arg = 'value'

    def buildWidget( self, **kwargs ):
        kwargs.update( self.widget_kwargs )

        self._widget = self.widget_command( label=self.widget_label, **kwargs )
        for label in self.labels:
            pm.menuItem( label=label )


class EnumOptionMenu( OptionMenu ):
    """
    Store one integer with an option menu control.

    :default type:  int
    :command:       `optionMenuGrp`
    """

    widget_value_arg = 'select'


class TextField( OptionField ):
    """
    Store a string with a text field control.

    :default type:  string
    :command:       `textFieldGrp`
    """

    widget_command = staticmethod( mc.textFieldGrp )
    widget_value_arg = 'text'


class TextFieldButton( OptionField ):
    """
    Store a string with text field and button controls.

    :default type:  string
    :command:       `textFieldButtonGrp`
    """

    widget_command = staticmethod( mc.textFieldButtonGrp )
    widget_value_arg = 'text'


class FileBrowser( OptionField ):
    """
    Store a path string with text field and file browser button controls.

    :default type:  string
    :command:       `impress.ui.fileBrowserGrp`
    """

    widget_command = staticmethod( ui.fileBrowserGrp )
    widget_value_arg = 'text'


