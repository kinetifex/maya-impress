import random
import pymel.core as pm
from impress import models, register


def randomTransform( translate=False, translateAmount=1.0, translateAxis=(False,False,False),
                     rotate=False,    rotateAmount=1.0,    rotateAxis=(False,False,False),
                     scale=False,     scaleAmount=1.0,     scaleAxis=(False,False,False) ):
    """
    Transforms selected objects with random values.
    """
    objects = pm.ls( selection=True, type='transform')

    assert len(objects), 'randomTransform requires at least 1 selected transform object.'

    for object in objects:
        if translate:
            offset = map(lambda axis: random.uniform( -translateAmount, translateAmount )*float(axis), translateAxis)
            object.setTranslation( offset, relative=True  )
        if rotate:
            offset = map(lambda axis: random.uniform( -rotateAmount, rotateAmount )*float(axis), rotateAxis)
            object.setRotation( offset, relative=True  )
        if scale:
            offset = map(lambda axis: 1 + ( random.uniform( -scaleAmount, scaleAmount )*float(axis) ), scaleAxis)
            object.setScale( offset )

    print '# Results: %i object randomized. #' % len(objects)


class RandomTransformOptions( models.OptionModel ):

    translate = models.CheckBox( default=1, ann='about the checkbox' )
    translateAmount = models.FloatSlider( default=1, precision=3, requires=(translate, 1) )
    translateAxis = models.CheckBox( labels=['X', 'Y', 'Z'], default=[1, 1, 1], requires=(translate, 1) )

    sep1 = models.Separator( style='in', height=14 )

    rotate = models.CheckBox( default=1, ann='about the checkbox' )
    rotateAmount = models.FloatSlider( default=1, precision=3, requires=(rotate, 1) )
    rotateAxis = models.CheckBox( labels=['X', 'Y', 'Z'], default=[1, 1, 1], requires=(rotate, 1) )

    sep2 = models.Separator( style='in', height=14 )

    scale = models.CheckBox( default=1, ann='about the checkbox' )
    scaleAmount = models.FloatSlider( default=1, precision=3, requires=(scale, 1) )
    scaleAxis = models.CheckBox( labels=['X', 'Y', 'Z'], default=[1, 1, 1], requires=(scale, 1) )

    class Meta:
        button_label = 'Randomize'


performRandomTransform = register.PerformCommand( randomTransform, RandomTransformOptions )


performRandomTransform(1)