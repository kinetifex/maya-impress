"""
Module for registering functions with Maya.
"""

import traceback
import pymel.core as pm
import utils
import views
import models

class RuntimeCommand( object ):
    """
    Callable class for registering functions as runtime commands.
    """

    def __init__( self, func, name=None, runtime_name=None, category=None, annotation=None, register=True, args=(), kwargs={} ):

        self.func = func
        self.args = args
        self.kwargs = kwargs

        self.__doc__ = self.func.__doc__

        if runtime_name is None:
            runtime_name = utils.pascalCase( self.func.__name__ )
        self.runtime_name = runtime_name

        if name is None:
            (filename,line_number,function_name,text) = traceback.extract_stack()[-2]
            try:
                name = text[:text.find('=')].strip()
            except AttributeError:
                assert False, "'name' not provided and could not be extrapolated."

        self.__name__ = self.name = name

        if category is None:
            if self.func.__module__ != '__main__':
                category = ' '.join( [c.capitalize() for c in self.func.__module__.split( '.' )] )
        self.category = category

        if annotation is None:
            try:
                annotation = self.func.__doc__.strip().splitlines()[0].split('.')[0]
            except:
                annotation = self.runtime_name
        self.annotation = annotation

        if register:
            self.register()


    @property
    def func_name( self ):
        return self.func.__name__


    @property
    def _perform_func_str( self ):

        func_str = self.name
        if self.func.__module__ != '__main__':
            func_str = '%s.%s' % ( self.func.__module__, func_str )

        return func_str


    @property
    def _func_str( self ):

        func_str = self.func.__name__
        if self.func.__module__ != '__main__':
            func_str = '%s.%s' % ( self.func.__module__, func_str )

        return func_str


    def _get_args(self):
        return self.args

    def _get_kwargs(self):
        return self.kwargs


    def get_cmd_str(self):

        args = self._get_args()
        kwargs = self._get_kwargs()

        kwargs_list = ["%s=%s" % ( k, v ) for k, v in kwargs.iteritems()]

        if args or kwargs_list:
            args_str = ', '.join( list(args)+kwargs_list )
        else:
            args_str = ''

        cmd_str = '%s(%s)' % ( self._func_str, args_str )

        return cmd_str


    def __call__( self ):

        print "# Result: %s #" % self.get_cmd_str()

        kwargs = self._get_kwargs()
        self.func( **kwargs )


    def register( self ):

        kwargs = {}

        name = self.runtime_name
        cmd_str = self.get_cmd_str()

        kwargs['annotation'] = self.annotation

        if not pm.versions.current() >= pm.versions.v2008:
            kwargs['command'] = 'python("%s")' % cmd_str
        else:
            kwargs['command'] = cmd_str
            kwargs['commandLanguage'] = 'python'

        if self.category is not None:
            kwargs['category'] = self.category

        if not pm.runTimeCommand( name, exists=1 ):
            pm.runTimeCommand( name, default=True, **kwargs )
            print "# Adding runtime:", name, ':', cmd_str


class PerformCommand( RuntimeCommand ):
    """
    Callable class for registering functions with OptionModels and as runtime commands.
    """

    def __init__( self, func, optionmodel=None, view=views.OptionBoxView, name=None, runtime_name=None, category=None, annotation=None, args=(), kwargs={} ):

        if name is None:
            (filename,line_number,function_name,text) = traceback.extract_stack()[-2]
            try:
                name = text[:text.find('=')].strip()
            except AttributeError:
                name = 'perform' + utils.pascalCase(func.__name__)
                pm.mel.warning("'name' not provided and could not be extrapolated. Assuming: '%s'" % name )

        self.__name__ = self.name = name

        super(PerformCommand, self).__init__( func, name, runtime_name, category, annotation, False, args, kwargs )

        self.view = view

        if optionmodel is not None:
            if not isinstance( optionmodel, models.OptionModel ) and not issubclass( optionmodel, models.OptionModel ):
                raise TypeError( "`optionmodel` must subclass of %s" % models.OptionModel )
            elif not hasattr( optionmodel, 'options' ):
                optionmodel = optionmodel()

        self.optionmodel = optionmodel

        self.register()


    @property
    def has_fields( self ):
        return self.optionmodel is not None


    def _get_kwargs(self):
        kwargs = self.kwargs

        if self.has_fields:
            preResults = self.optionmodel.preApply()
            if preResults is None:
                return None

            kwargs.update( preResults )

            for o in self.optionmodel.fields:
                if hasattr(o, 'get'):
                    kwargs[o.name] = o.get()

        return kwargs


    def __call__( self, action=0 ):

        if action == 0:
            kwargs = self._get_kwargs()
            self.func( **kwargs )
        elif action == 1:
            if self.optionmodel is not None:
                self.view(self.optionmodel, self).show()
            else:
                pm.mel.error( "This command has no fields." );

        if action in (0,2):
            print "# Result: %s #" % self.get_cmd_str()


    def register( self ):

        kwargs = {}

        for i in range( 1 + self.has_fields ):
            name = [self.runtime_name, self.runtime_name + 'Options'][i]

            if self.has_fields:
                cmd_str = '%s(%d)' % ( self._perform_func_str, i )
            else:
                cmd_str = '%s()' % ( self._perform_func_str, )

            if i == self.has_fields:
                kwargs['annotation'] = utils.niceName( name )
            else:
                kwargs['annotation'] = self.annotation

            if not pm.versions.current() >= pm.versions.v2008:
                kwargs['command'] = 'python("%s")' % cmd_str
            else:
                kwargs['command'] = cmd_str
                kwargs['commandLanguage'] = 'python'

            if self.category is not None:
                kwargs['category'] = self.category

            if not pm.runTimeCommand( name, exists=1 ):
                pm.runTimeCommand( name, default=True, **kwargs )
                print "# Adding runtime:", name, ':', cmd_str



def runtime( func, name=None, runtime_name=None, category=None, annotation=None, args=(), kwargs={} ):
    """
    Decorator which makes functions available as Runtime Commands.
    """

    if name is None:
        name = func.__name__

    runtimeCmd = RuntimeCommand( func, name, runtime_name, category, annotation, True, args, kwargs )

    def wrapped( *args, **kwargs ):
        return runtimeCmd()

    return wrapped
