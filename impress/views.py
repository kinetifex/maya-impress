"""
Views intended to be populated with models.
"""

import pymel.core as pm
import utils
import models


class BaseView( object ):
    """
    The base view which handles bulding and updating option controls.
    """

    def __init__( self, optionmodel ):

        self.optionmodel = optionmodel
        self.name = utils.niceName( self.optionmodel.__class__.__name__ + "View" )

        if self.optionmodel is not None:
            if not isinstance( optionmodel, models.OptionModel ) and not issubclass( optionmodel, models.OptionModel ):
                raise TypeError( "`optionmodel` must subclass of %s" % models.OptionModel )
            elif not hasattr( self.optionmodel, 'fields' ):
                self.optionmodel = self.optionmodel()


    def _buildWidgets( self, parent ):
        for field in self.optionmodel.fields:
            pm.setParent( parent )
            if hasattr( field, 'updateWidget'):
                field.buildWidget( changeCommand=lambda * args: ( self._updateOptions(), self._updateWidgets() ) )
            elif hasattr( field, 'buildWidget'):
                field.buildWidget()


    def _updateWidgets( self ):
        for field in self.optionmodel.fields:
            if hasattr( field, 'updateWidget'):
                field.updateWidget()


    def _updateOptions( self, forceDefaults=False ):
        if forceDefaults:
            for field in self.optionmodel.fields:
                if hasattr( field, 'setDefault'):
                    field.setDefault()
        else:
            for field in self.optionmodel.fields:
                if hasattr( field, 'set'):
                    field.set( field.getWidgetValue() )


    def show(self):
        pass


    def hide(self):
        del(self)


class OptionBoxView( BaseView ):
    """
    View that hooks into Maya's built-in Option Box window.
    """

    def __init__( self, optionmodel, command ):
        super(OptionBoxView, self).__init__(optionmodel)

        self.command = command

        # -- read Meta data
        self._title = getattr( self.optionmodel.Meta, 'title', utils.niceName( self.optionmodel.__class__.__name__ ) )
        self._help_tag = getattr( self.optionmodel.Meta, 'help_tag', '%sHelp' % self.command.func_name )
        self._button_label = getattr( self.optionmodel.Meta, 'button_label', 'Apply/Close' )


    def _onClickApply(self, close=False):
        self._updateOptions()

        self.command.__call__()

        if hasattr(self.command, 'get_cmd_str'):
            pm.repeatLast( addCommand='python("%s")' % self.command.get_cmd_str(), addCommandLabel=self.command.__name__ )

        if close:
            self.hide()


    def _updateButtons( self ):
        applyCloseBtn = pm.mel.getOptionBoxApplyAndCloseBtn()
        applyBtn = pm.mel.getOptionBoxApplyBtn()

        saveMenuItem = pm.getMelGlobal( 'string', 'gOptionBoxEditMenuSaveItem' )
        reseMenuItem = pm.getMelGlobal( 'string', 'gOptionBoxEditMenuResetItem' )

        pm.button( applyCloseBtn, edit=True, label=self._button_label,
                   command=lambda *args: self._onClickApply(True)
                   )
        pm.button( applyBtn, edit=True,
                   command=lambda *args: self._onClickApply()
                   )
        pm.menuItem( saveMenuItem, edit=True,
                     command=lambda * args: ( self._updateOptions() )
                     )
        pm.menuItem( reseMenuItem, edit=True,
                     command=lambda * args: ( self._updateOptions( forceDefaults=True ), self._updateWidgets() )
                    )


    def show(self):
        self.layout = pm.mel.getOptionBox()

        pm.setParent( self.layout )
        pm.setUITemplate( 'DefaultTemplate', pushTemplate=True )

        self.parentCol = pm.columnLayout( adjustableColumn=1 )
        self._buildWidgets( parent=self.parentCol )
        self._updateWidgets()

        pm.setUITemplate( popTemplate=True )

        pm.mel.setOptionBoxTitle( self._title )
        pm.mel.setOptionBoxHelpTag( self._help_tag )

        pm.mel.showOptionBox()
        self._updateButtons()


    def hide(self):
        pm.mel.hideOptionBox()
        super(OptionBoxView, self).hide()