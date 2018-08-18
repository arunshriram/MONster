# Copyright (c) 2016 Riverbank Computing Limited <info@riverbankcomputing.com>
# 
# This file is part of PyQt4.
# 
# This file may be used under the terms of the GNU General Public License
# version 3.0 as published by the Free Software Foundation and appearing in
# the file LICENSE included in the packaging of this file.  Please review the
# following information to ensure the GNU General Public License version 3.0
# requirements will be met: http://www.gnu.org/copyleft/gpl.html.
# 
# If you do not wish to use this file under the terms of the GPL version 3.0
# then you may purchase a commercial license.  For more information contact
# info@riverbankcomputing.com.
# 
# This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
# WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#
# This module is intended to be used by the configuration scripts of extension
# modules that %Import PyQt4 modules.


import sipconfig


# These are installation specific values created when PyQt4 was configured.
_pkg_config = {
    'pyqt_bin_dir':      '/usr/local/Cellar/pyqt@4/4.12.1_1/bin',
    'pyqt_config_args':  '--confirm-license --bindir=/usr/local/Cellar/pyqt@4/4.12.1_1/bin --destdir=/usr/local/Cellar/pyqt@4/4.12.1_1/lib/python2.7/site-packages --sipdir=/usr/local/Cellar/pyqt@4/4.12.1_1/share/sip',
    'pyqt_mod_dir':      '/usr/local/Cellar/pyqt@4/4.12.1_1/lib/python2.7/site-packages/PyQt4',
    'pyqt_modules':      'QtCore QtGui QtHelp QtMultimedia QtNetwork QtDeclarative QtScript QtScriptTools QtOpenGL QtSql QtSvg QtTest QtXml QtXmlPatterns QtDesigner',
    'pyqt_sip_dir':      '/usr/local/Cellar/pyqt@4/4.12.1_1/share/sip',
    'pyqt_sip_flags':    '-x VendorID -t WS_MACX -x PyQt_NoPrintRangeBug -t Qt_4_8_6 -x Py_v3 -g',
    'pyqt_version':      0x040c01,
    'pyqt_version_str':  '4.12.1',
    'qt_archdata_dir':   '/usr/local/opt/qt@4/etc/qt4',
    'qt_data_dir':       '/usr/local/opt/qt@4/etc/qt4',
    'qt_dir':            '/usr/local/opt/qt@4',
    'qt_edition':        'free',
    'qt_framework':      1,
    'qt_inc_dir':        '/usr/local/opt/qt@4/include',
    'qt_lib_dir':        '/usr/local/opt/qt@4/lib',
    'qt_threaded':       1,
    'qt_version':        0x040807,
    'qt_winconfig':      'shared'
}

_default_macros = {
    'AIX_SHLIB':                '',
    'AR':                       'ar cq',
    'CC':                       'clang',
    'CFLAGS':                   '-pipe -mmacosx-version-min=10.7',
    'CFLAGS_APP':               '',
    'CFLAGS_CONSOLE':           '',
    'CFLAGS_DEBUG':             '-g',
    'CFLAGS_EXCEPTIONS_OFF':    '',
    'CFLAGS_EXCEPTIONS_ON':     '',
    'CFLAGS_MT':                '',
    'CFLAGS_MT_DBG':            '',
    'CFLAGS_MT_DLL':            '',
    'CFLAGS_MT_DLLDBG':         '',
    'CFLAGS_RELEASE':           '-O2',
    'CFLAGS_RTTI_OFF':          '',
    'CFLAGS_RTTI_ON':           '',
    'CFLAGS_SHLIB':             '-fPIC',
    'CFLAGS_STL_OFF':           '',
    'CFLAGS_STL_ON':            '',
    'CFLAGS_THREAD':            '',
    'CFLAGS_WARN_OFF':          '-w',
    'CFLAGS_WARN_ON':           '-Wall -W',
    'CHK_DIR_EXISTS':           'test -d',
    'CONFIG':                   'qt warn_on release app_bundle incremental global_init_link_order lib_version_first plugin_no_soname link_prl clang_pch_style',
    'COPY':                     'cp -f',
    'CXX':                      'clang++',
    'CXXFLAGS':                 '-pipe -stdlib=libc++ -mmacosx-version-min=10.7',
    'CXXFLAGS_APP':             '',
    'CXXFLAGS_CONSOLE':         '',
    'CXXFLAGS_DEBUG':           '-g',
    'CXXFLAGS_EXCEPTIONS_OFF':  '',
    'CXXFLAGS_EXCEPTIONS_ON':   '',
    'CXXFLAGS_MT':              '',
    'CXXFLAGS_MT_DBG':          '',
    'CXXFLAGS_MT_DLL':          '',
    'CXXFLAGS_MT_DLLDBG':       '',
    'CXXFLAGS_RELEASE':         '-O2',
    'CXXFLAGS_RTTI_OFF':        '',
    'CXXFLAGS_RTTI_ON':         '',
    'CXXFLAGS_SHLIB':           '-fPIC',
    'CXXFLAGS_STL_OFF':         '',
    'CXXFLAGS_STL_ON':          '',
    'CXXFLAGS_THREAD':          '',
    'CXXFLAGS_WARN_OFF':        '-w',
    'CXXFLAGS_WARN_ON':         '-Wall -W',
    'DEFINES':                  '',
    'DEL_FILE':                 'rm -f',
    'EXTENSION_PLUGIN':         '',
    'EXTENSION_SHLIB':          'dylib',
    'INCDIR':                   '',
    'INCDIR_OPENGL':            '/System/Library/Frameworks/OpenGL.framework/Headers 	/System/Library/Frameworks/AGL.framework/Headers/',
    'INCDIR_QT':                '/usr/local/opt/qt@4/include',
    'INCDIR_X11':               '',
    'LFLAGS':                   ' -headerpad_max_install_names -stdlib=libc++ -mmacosx-version-min=10.7',
    'LFLAGS_CONSOLE':           '',
    'LFLAGS_CONSOLE_DLL':       '',
    'LFLAGS_DEBUG':             '',
    'LFLAGS_DLL':               '',
    'LFLAGS_OPENGL':            '',
    'LFLAGS_PLUGIN':            '-single_module -dynamiclib',
    'LFLAGS_RELEASE':           '',
    'LFLAGS_RPATH':             '',
    'LFLAGS_SHLIB':             '-single_module -dynamiclib',
    'LFLAGS_SONAME':            '-install_name ',
    'LFLAGS_THREAD':            '',
    'LFLAGS_WINDOWS':           '',
    'LFLAGS_WINDOWS_DLL':       '',
    'LIB':                      '',
    'LIBDIR':                   '',
    'LIBDIR_OPENGL':            '',
    'LIBDIR_QT':                '/usr/local/opt/qt@4/lib',
    'LIBDIR_X11':               '',
    'LIBS':                     '',
    'LIBS_CONSOLE':             '',
    'LIBS_CORE':                '',
    'LIBS_GUI':                 '',
    'LIBS_NETWORK':             '',
    'LIBS_OPENGL':              '-framework OpenGL -framework AGL',
    'LIBS_RT':                  '',
    'LIBS_RTMT':                '',
    'LIBS_THREAD':              '',
    'LIBS_WEBKIT':              '',
    'LIBS_WINDOWS':             '',
    'LIBS_X11':                 '',
    'LINK':                     'clang++',
    'LINK_SHLIB':               'clang++',
    'LINK_SHLIB_CMD':           '',
    'MAKEFILE_GENERATOR':       'UNIX',
    'MKDIR':                    'mkdir -p',
    'MOC':                      '/usr/local/opt/qt@4/bin/moc',
    'RANLIB':                   'ranlib -s',
    'RPATH':                    '',
    'STRIP':                    ''
}


class Configuration(sipconfig.Configuration):
    """The class that represents PyQt configuration values.
    """
    def __init__(self, sub_cfg=None):
        """Initialise an instance of the class.

        sub_cfg is the list of sub-class configurations.  It should be None
        when called normally.
        """
        if sub_cfg:
            cfg = sub_cfg
        else:
            cfg = []

        cfg.append(_pkg_config)

        sipconfig.Configuration.__init__(self, cfg)


class QtCoreModuleMakefile(sipconfig.SIPModuleMakefile):
    """The Makefile class for modules that %Import QtCore.
    """
    def __init__(self, *args, **kw):
        """Initialise an instance of a module Makefile.
        """
        if "qt" not in kw:
            kw["qt"] = ["QtCore"]

        sipconfig.SIPModuleMakefile.__init__(self, *args, **kw)


class QtGuiModuleMakefile(QtCoreModuleMakefile):
    """The Makefile class for modules that %Import QtGui.
    """
    def __init__(self, *args, **kw):
        """Initialise an instance of a module Makefile.
        """
        if "qt" not in kw:
            kw["qt"] = ["QtCore", "QtGui"]

        QtCoreModuleMakefile.__init__(self, *args, **kw)


class QtHelpModuleMakefile(QtGuiModuleMakefile):
    """The Makefile class for modules that %Import QtHelp.
    """
    def __init__(self, *args, **kw):
        """Initialise an instance of a module Makefile.
        """
        if "qt" not in kw:
            kw["qt"] = ["QtCore", "QtGui", "QtHelp"]

        QtGuiModuleMakefile.__init__(self, *args, **kw)


class QtMultimediaModuleMakefile(QtGuiModuleMakefile):
    """The Makefile class for modules that %Import QtMultimedia.
    """
    def __init__(self, *args, **kw):
        """Initialise an instance of a module Makefile.
        """
        if "qt" not in kw:
            kw["qt"] = ["QtCore", "QtGui", "QtMultimedia"]

        QtGuiModuleMakefile.__init__(self, *args, **kw)


class QtNetworkModuleMakefile(QtCoreModuleMakefile):
    """The Makefile class for modules that %Import QtNetwork.
    """
    def __init__(self, *args, **kw):
        """Initialise an instance of a module Makefile.
        """
        if "qt" not in kw:
            kw["qt"] = ["QtCore", "QtNetwork"]

        QtCoreModuleMakefile.__init__(self, *args, **kw)


class QtDeclarativeModuleMakefile(QtNetworkModuleMakefile):
    """The Makefile class for modules that %Import QtDeclarative.
    """
    def __init__(self, *args, **kw):
        """Initialise an instance of a module Makefile.
        """
        if "qt" not in kw:
            kw["qt"] = ["QtCore", "QtGui", "QtNetwork", "QtDeclarative"]

        QtNetworkModuleMakefile.__init__(self, *args, **kw)


class QtAssistantModuleMakefile(QtNetworkModuleMakefile):
    """The Makefile class for modules that %Import QtAssistant.
    """
    def __init__(self, *args, **kw):
        """Initialise an instance of a module Makefile.
        """
        if "qt" not in kw:
            kw["qt"] = ["QtCore", "QtGui", "QtNetwork", "QtAssistant"]

        QtNetworkModuleMakefile.__init__(self, *args, **kw)


class QtOpenGLModuleMakefile(QtGuiModuleMakefile):
    """The Makefile class for modules that %Import QtOpenGL.
    """
    def __init__(self, *args, **kw):
        """Initialise an instance of a module Makefile.
        """
        kw["opengl"] = 1

        if "qt" not in kw:
            kw["qt"] = ["QtCore", "QtGui", "QtOpenGL"]

        QtGuiModuleMakefile.__init__(self, *args, **kw)


class QtScriptModuleMakefile(QtCoreModuleMakefile):
    """The Makefile class for modules that %Import QtScript.
    """
    def __init__(self, *args, **kw):
        """Initialise an instance of a module Makefile.
        """
        if "qt" not in kw:
            kw["qt"] = ["QtCore", "QtScript"]

        QtCoreModuleMakefile.__init__(self, *args, **kw)


class QtScriptToolsModuleMakefile(QtScriptModuleMakefile):
    """The Makefile class for modules that %Import QtScriptTools.
    """
    def __init__(self, *args, **kw):
        """Initialise an instance of a module Makefile.
        """
        if "qt" not in kw:
            kw["qt"] = ["QtCore", "QtGui", "QtScript", "QtScriptTools"]

        QtScriptModuleMakefile.__init__(self, *args, **kw)


class QtSqlModuleMakefile(QtGuiModuleMakefile):
    """The Makefile class for modules that %Import QtSql.
    """
    def __init__(self, *args, **kw):
        """Initialise an instance of a module Makefile.
        """
        if "qt" not in kw:
            kw["qt"] = ["QtCore", "QtGui", "QtSql"]

        QtGuiModuleMakefile.__init__(self, *args, **kw)


class QtSvgModuleMakefile(QtGuiModuleMakefile):
    """The Makefile class for modules that %Import QtSvg.
    """
    def __init__(self, *args, **kw):
        """Initialise an instance of a module Makefile.
        """
        if "qt" not in kw:
            kw["qt"] = ["QtCore", "QtGui", "QtSvg"]

        QtGuiModuleMakefile.__init__(self, *args, **kw)


class QtTestModuleMakefile(QtGuiModuleMakefile):
    """The Makefile class for modules that %Import QtTest.
    """
    def __init__(self, *args, **kw):
        """Initialise an instance of a module Makefile.
        """
        if "qt" not in kw:
            kw["qt"] = ["QtCore", "QtGui", "QtTest"]

        QtGuiModuleMakefile.__init__(self, *args, **kw)


class QtWebKitModuleMakefile(QtNetworkModuleMakefile):
    """The Makefile class for modules that %Import QtWebKit.
    """
    def __init__(self, *args, **kw):
        """Initialise an instance of a module Makefile.
        """
        if "qt" not in kw:
            kw["qt"] = ["QtCore", "QtGui", "QtNetwork", "QtWebKit"]

        QtNetworkModuleMakefile.__init__(self, *args, **kw)


class QtXmlModuleMakefile(QtCoreModuleMakefile):
    """The Makefile class for modules that %Import QtXml.
    """
    def __init__(self, *args, **kw):
        """Initialise an instance of a module Makefile.
        """
        if "qt" not in kw:
            kw["qt"] = ["QtCore", "QtXml"]

        QtCoreModuleMakefile.__init__(self, *args, **kw)


class QtXmlPatternsModuleMakefile(QtCoreModuleMakefile):
    """The Makefile class for modules that %Import QtXmlPatterns.
    """
    def __init__(self, *args, **kw):
        """Initialise an instance of a module Makefile.
        """
        if "qt" not in kw:
            kw["qt"] = ["QtCore", "QtXmlPatterns"]

        QtCoreModuleMakefile.__init__(self, *args, **kw)


class phononModuleMakefile(QtGuiModuleMakefile):
    """The Makefile class for modules that %Import phonon.
    """
    def __init__(self, *args, **kw):
        """Initialise an instance of a module Makefile.
        """
        if "qt" not in kw:
            kw["qt"] = ["QtCore", "QtGui", "phonon"]

        QtGuiModuleMakefile.__init__(self, *args, **kw)


class QtDesignerModuleMakefile(QtGuiModuleMakefile):
    """The Makefile class for modules that %Import QtDesigner.
    """
    def __init__(self, *args, **kw):
        """Initialise an instance of a module Makefile.
        """
        if "qt" not in kw:
            kw["qt"] = ["QtCore", "QtGui", "QtDesigner"]

        QtGuiModuleMakefile.__init__(self, *args, **kw)


class QAxContainerModuleMakefile(QtGuiModuleMakefile):
    """The Makefile class for modules that %Import QAxContainer.
    """
    def __init__(self, *args, **kw):
        """Initialise an instance of a module Makefile.
        """
        if "qt" not in kw:
            kw["qt"] = ["QtCore", "QtGui", "QAxContainer"]

        QtGuiModuleMakefile.__init__(self, *args, **kw)


class QtDBusModuleMakefile(QtCoreModuleMakefile):
    """The Makefile class for modules that %Import QtDBus.
    """
    def __init__(self, *args, **kw):
        """Initialise an instance of a module Makefile.
        """
        if "qt" not in kw:
            kw["qt"] = ["QtCore", "QtDBus"]

        QtCoreModuleMakefile.__init__(self, *args, **kw)
