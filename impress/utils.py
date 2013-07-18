"""
Contains helper and non-Maya-specific functions.
"""

import re
import platform
import subprocess
from pymel.util.path import Path as _Path


_re_words = re.compile( '([A-Z][a-z0-9]+)' )
_re_numbers = re.compile( '([0-9]+)' )

def niceName( name ):
    """Formats "camelCase" and "wide_name" variable names into "Nice Name"."""

    def _capChar( word ):
        try:
            return word[0].capitalize() + word[1:]
        except IndexError:
            return word

    name = re.sub( _re_words, r' \1', name )
    name = re.sub( _re_numbers, r' \1 ', name )

    word_list = re.split( '[_\s]+', name.strip() )
    result = ' '.join( map( _capChar, word_list ) )

    return result


def wideName( name ):
    """Formats "camelCase" and "Nice Name" variable names into "wide_name"."""

    result = niceName( name ).replace( " ", "_" )

    return result


def camelCase( name ):
    """Formats "Nice Name" and "wide_name" variable names into "camelCase"."""

    result = niceName( name ).replace( " ", "" )

    return result


def pascalCase( name ):
    """Formats strings into "PascalCase"."""

    result = camelCase( name )
    result = result[0].capitalize() + result[1:]

    return result


def revealInFileManager( path ):
    """Reveals the specified folder or file in file manager."""

    path = _Path( path ).normpath()

    #if len(path) > 4: #if the path is something other than the drive
    if path.endswith('/') or path.endswith('\\'):
        path = _Path(path[:-1])

    # -- If the path doesn't exist, try walking up
    attempts = 2
    while not path.exists():
        path = path.parent

        attempts -= 1
        if attempts == 0:
            assert False, 'Invalid path specified.'

    print '# Revealing: %s' % path

    if platform.system() == 'Darwin':
        subprocess.call(["open", "-R", path])
    elif platform.system() == 'Windows':
        subprocess.call(["explorer", "/select,"+path])
    else:
        raise NotImplementedError("Not yet implemented for current OS.")


def safePath( file_path ):
    return _Path( _Path(file_path).realpath().replace('\\','/') )