"""
Contains custom Maya gui controls and functions.
"""

import pymel.core as pm
import pymel.versions as versions
from pymel.util.path import Path as _Path
import utils


__fileDialog2_keys = ['dialogStyle', 'ds', 'caption', 'cap', 'startingDirectory', 'dir', 'fileFilter', 'ff', 'selectFileFilter', 'sff', 'fileMode', 'fm', 'okCaption', 'okc', 'cancelCaption', 'cc', 'returnFilter', 'rf', 'optionsUICreate', 'ocr', 'optionsUIInit', 'oin', 'fileTypeChanged', 'ftc', 'selectionChanged', 'sc', 'optionsUICommit', 'ocm']


def _updateFileHistory( control, optionName, validate=False, basename=False ):

    historySize = pm.optionVar.get( 'pathHistory_size', 6 )

    pathStr = control.getText().replace( '\\', '/' )
    if pathStr.endswith( '\\' ) or pathStr.endswith( '/' ):
        if len( pathStr ) > 4:
            pathStr = pathStr[:-1]

    path = _Path( pathStr )

    if basename:
        path = path.basename()
        control.setFileName( path )

    valid = True
    if validate:
        if basename:
            pm.mel.warning( "basename and validate args cannot be combine (%s)" % control, False )
        elif path.isdir():
            valid = True
        elif '.' in path.basename() and path.parent.isdir():
            valid = True
        else:
            valid = False

    if valid:
        historyList = pm.optionVar.get( 'pathHistory_%s' % optionName, [] )

        if isinstance( historyList, pm.OptionVarList ):
            historyList = list( historyList )
        elif historyList:
            historyList = [historyList]

        if path in historyList:
            historyList.remove( path )

        historyList.insert( 0, unicode( path ) )

        pm.optionVar['pathHistory_%s' % optionName] = historyList[ 0:historySize ]


def _updateFileHistoryPopup( control, popup, optionName, basename=False ):

    historyList = pm.optionVar.get( 'pathHistory_%s' % optionName, [] )

    if isinstance( historyList, pm.OptionVarList ):
        historyList = list( historyList )
    elif historyList:
        historyList = [historyList]

    pm.popupMenu( popup, edit=True, deleteAllItems=True )

    if historyList:

        for path in historyList:

            pm.setParent( popup, menu=True )
            pm.menuItem ( label=path.replace( '/', '\\' ), command=pm.Callback( control.setText, ( path ) ) )

    if not basename:
        pm.setParent( popup, menu=True )
        pm.menuItem( divider=True )
        pm.menuItem( label='go to folder',
                  command=lambda *args: utils.revealInFileManager( _Path( control.getText() ) )
                  )


def fileBrowserGrp( *args, **kwargs ):
    """
    TextFieldButtonGrp with a fileDialog2 browser and popup menu of recent path history.

    Accepts parameters from both `textFieldButtonGrp` and `fileDialog2`.
    """

    optionName = kwargs.pop( 'optionName', None )
    validate = kwargs.pop( 'validate', False )
    basename = kwargs.pop( 'basename', False )

    if 'fileMode' not in kwargs:
        kwargs['fileMode'] = kwargs.pop( 'fm', 0 )

    # -- Separate fileDialog2 kwargs, remaining are used for textFieldButtonGrp
    dialog_kwargs = {}
    for k in kwargs.keys():
        if k in __fileDialog2_keys:
            dialog_kwargs[k] = kwargs.pop( k )


    if optionName is None:
        optionName = ['files', 'dirs'][ ( dialog_kwargs['fileMode'] in [2, 3] ) ]

    if len( set.intersection( set( kwargs.keys() ), set( ['e', 'q', 'edit', 'query'] ) ) ):
        return pm.textFieldButtonGrp( *args, **kwargs )
    else:
        control = pm.textFieldButtonGrp( *args, **kwargs )

        popControl = pm.popupMenu()
        pm.popupMenu( 
            popControl,
            edit=True,
            postMenuCommand=lambda*args: _updateFileHistoryPopup( 
                control,
                popControl,
                optionName,
                basename=basename
            )
        )

        if versions.current() >= versions.v2011:

            def browsePath():
                path = pm.fileDialog2( **dialog_kwargs )

                if path is None:
                    return
                else:
                    path = path[0]

                control.setText( path, fcc=True )

        else:
            pm.mel.error( 'Requires Maya 2011 or greater.' )
            '''
            if versions.current() < versions.v2008_EXT2:
                callback = 'callback_%s' % control

                cmdStr = 'textFieldButtonGrp -edit -text $path -fcc %s;' \
                       + 'textFieldButtonGrp -edit -fi $path %s;' \
                       % ( control, control )

                # -- Create File Browser Callback
                pm.mel.eval( 'global proc %s( string $path, string $type) { %s }' % ( callback, cmdStr ) )

            else:
                callback = lambda path, type: ( control.setText( path, fcc=True ) )

            if pathType == 'file':
                browsePath = lambda *args: pm.fileBrowserDialog(
                        mode=0,
                        actionName='Choose File',
                        fileCommand=callback
                    )

            elif pathType == 'dir':
                browsePath = lambda *args: pm.fileBrowserDialog(
                        mode=4,
                        actionName='Choose Directory',
                        fileCommand=callback
                    )
            '''

        pm.textFieldButtonGrp( 
            control,
            edit=True,
            buttonCommand=browsePath,
            changeCommand=lambda *args: _updateFileHistory( 
                control,
                optionName,
                validate,
                basename
            )
        )

        return control


def commandMenuItem( command, args=[], label=None, annotation=None, **kwargs ):
    """
    Creates menuItem from python function objects.

    'command' parameter takes a python function object. 'args' can be supplied
    for the command. If 'label' isn't specified, it will be generated from the
    function __name__. If 'annotation' isn't specified, it will be taken from
    the first sentence of the function __doc__. If __doc__ is empty, it will
    use the 'label'.

    Setting 'options' to True will build an optionBox menuItem and supply
    'True' as the arg to the command. See functions that have OptionBox
    classes associated with them for the proper structure.
    """

    def _initMenuItem( *args, **kwargs ):
        keys = kwargs.keys()

        menuItemName = kwargs.pop( 'menuItemName', False )

        if 'command' in keys or 'c' in keys:

            if 'dragMenuCommand' not in keys or 'dmc' not in keys:
                kwargs['dmc'] = 'python("%s")' % kwargs['command']

        if menuItemName:
            return pm.menuItem( menuItemName, *args, **kwargs )
        else:
            return pm.menuItem( *args, **kwargs )

    argStr = ''
    if len( args ) > 0:
        argList = []

        for arg in args:
            if isinstance( arg, str ):
                argList.append( '\"%s\"' % arg )
            else:
                argList.append( str( arg ) )

        argStr = ','.join( argList )

    if hasattr( command, 'func' ):
        command_str = '%s.%s(%s)' % ( command.func.__module__, command.__name__, argStr )
    else:
        command_str = '%s.%s(%s)' % ( command.__module__, command.__name__, argStr )

    if command_str.startswith( '__main__' ):
        command_str = '.'.join( command_str.split( '.' )[1:] )

    if label is None:
        if hasattr( command, 'label' ):
            label = utils.niceName( command.label )
        else:
            label = utils.niceName( command.__name__ )

    if annotation is None:
        if hasattr( command, 'annotation' ):
            annotation = command.annotation
        else:
            try:
                annotation = command.__doc__.strip().splitlines()[0].split( '.' )[0]
            except:
                annotation = label

    item = _initMenuItem( command=command_str, label=label, annotation=annotation, **kwargs )

    # -- add optionBox menuItem for options --

    if hasattr( command, 'optionmodel' ):
        if command.optionmodel is not None:
            optCmdStr = command_str.split( '(' )[0] + '(1)'
            optAnn = label + ' Options'

            optItem = _initMenuItem( command=optCmdStr, annotation=optAnn, optionBox=True, **kwargs )

            return ( item, optItem )

    return item
