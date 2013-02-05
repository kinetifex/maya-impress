import pymel.core as pm
from impress import register


def offsetKeyframes( valueChange=360 ):
    """Offset selected keyframes."""
    pm.keyframe(edit=True, iub=True, relative=True, valueChange=valueChange)


offsetKeyframesUp = register.RuntimeCommand( offsetKeyframes, 'offsetKeyframesUp', kwargs={'valueChange':'360'} )
offsetKeyframesDown = register.RuntimeCommand( offsetKeyframes, 'offsetKeyframesDown', kwargs={'valueChange':'-360'} )


@register.runtime
def toggleInfinityCycle():
    """Toggle infinite cycle with offset for curves on selected object(s)"""

    try:
        if 'constant' not in pm.setInfinity(query=True, poi=True):
            pm.setInfinity( poi='constant', pri='constant')
        else:
            pm.setInfinity( poi='cycleRelative', pri='cycleRelative')
    except:
        pm.mel.warning('Select object(s) with animation curves.')

    pm.animCurveEditor( 'graphEditor1GraphEd', edit=True, displayInfinities='on' )