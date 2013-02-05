from __future__ import with_statement

import pymel.core as pm
from impress import ui


MAYA_WINDOW = pm.getMelGlobal( 'string', 'gMainWindow' )


def show( reset=False ):
    if pm.about(batch=True):
        print 'menu not available in batch mode.'
        return
    else:
        # -- get things ready for building the menu

        menu_name = "Impress Example"
        pm.setParent( MAYA_WINDOW )

        if pm.menu( menu_name, exists=True ):
            if reset:
                pm.deleteUI( menu_name )
            else:
                main_menu = pm.menu( menu_name, edit=True )
                return main_menu

        if not pm.menu( menu_name, exists=True ):
            main_menu = pm.menu( menu_name, tearOff=True )

        # -- build the menu

        with  main_menu:
            with pm.subMenuItem( 'Display', aob=True, tearOff=True ):
                ui.commandMenuItem( performExample )


show(True)