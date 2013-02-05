
Installation
=======================================


Requirements
---------------------------------------

Maya-Impress requires PyMEL and Maya 2009 or later on any platform.

Some features do have specific requirements beyond this:

    ========================================= =======================
    Feature                                   Requirement
    ========================================= =======================
    :mod:`impress.widgets.pathBrowserGrp`     Maya 2011 or later
    ----------------------------------------- -----------------------
    :mod:`impress.models.PathBrowser`         Maya 2011 or later
    ----------------------------------------- -----------------------
    :mod:`impress.utils.revealInFileManager`  OSX or Windows
    ========================================= =======================


Download
---------------------------------------

A release version of **Maya-Impress** can downloaded from:

    http://www.kinetifex.com/projects/maya-impress/

Developers can create a clone of the repository:

Once you have a copy of maya-impress downloaded and extracted somewhere, you need to tell Maya where to find it.


Setup Maya Module
---------------------------------------

maya-impress is structured as a Maya Module [1]_. To tell Maya how to access it, a module description file needs to be placed in Maya's MAYA_MODULE_PATH..

1.  **Locate Maya Module Path:**

    The default locations for these paths are:

    ================= =================================================
    OS                MAYA_MODULE_PATH
    ================= =================================================
    OSX               ~/Library/Preferences/Autodesk/maya/modules
    ----------------- -------------------------------------------------
    Windows           drive:\\My Documents\\maya\\modules
    ----------------- -------------------------------------------------
    Linux             ~/maya/modules
    ================= =================================================

    If a ``modules`` folder doesn't exist in the ``maya`` directory, simply create a new folder named ``modules``. If you only want the maya-impress module for a particular version of Maya, simply create a ``modules`` folder under the version folder you want (i.e. ~/maya/2013/modules).

2.  **Create Module Description File:**

    * Copy the ``maya-impress-module.txt`` from the maya-impress folder this modules folder.
    * Open in a text editor, and replace ``/path/to/maya-impress`` with the path to your extracted maya-impress folder.


.. [1] See the `Maya Module Documentation`_ for more details.


Verify Setup
---------------------------------------

To test if your setup is correct, start up Maya and run the follow line in a python script editor::

    import impress

If there are no errors then everything is set up properly!


.. _`Maya Module Documentation`: http://docs.autodesk.com/MAYAUL/2013/ENU/Maya-API-Documentation/index.html?url=files/GUID-130A3F57-2A5D-4E56-B066-6B86F68EEA22.htm,topicNumber=d30e28803

.. _`Maya Module Path Docs`: http://docs.autodesk.com/MAYAUL/2013/ENU/Maya-API-Documentation/index.html?url=files/GUID-130A3F57-2A5D-4E56-B066-6B86F68EEA22.htm,topicNumber=d30e28803