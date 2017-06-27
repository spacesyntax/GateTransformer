# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GateTransformer
                                 A QGIS plugin
 This plugin performs basic transformation on a line in qgis.
                              -------------------
        begin                : 2016-02-29
        author               : Stephen Law
        copyright            : (C) 2016 by Space Syntax Limited
        email                : s.law@spacesyntax.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 3 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

#from network_transformer_dialog import NetworkTransformerDialog
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt, QVariant, pyqtSlot
from PyQt4.QtGui import QAction, QIcon

from qgis.core import *
#from qgis.gui import *

import os.path
import os

import transformer_analysis
#import processing

# this import python deploy-debug package, hashtag is_debug if debugging is not used.
is_debug = False
try:
    import pydevd
    has_pydevd = True
except ImportError, e:
    has_pydevd = False
    is_debug = False


class NetworkTransformer:
    """QGIS Plugin Implementation."""

################################# GUI Interface #############################

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # transformer analysis class initialisation
        self.transformer_analysis = transformer_analysis.TransformerAnalysis(self.iface)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'GateTransformer_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference *creates new dialog object runs dialog __init__
        #self.dlg = NetworkTransformerDialog()

        # Declare instance attributes#
        self.actions = []
        self.menu = self.tr(u'&Space Syntax Toolkit')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'GateTransformer')
        self.toolbar.setObjectName(u'GateTransformer')

        # connects to QGIS-deployment
        if has_pydevd and is_debug:
            pydevd.settrace('localhost', port=53100, stdoutToServer=True, stderrToServer=True, suspend=False)

    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('GateTransformer', message)

    def add_action(self,icon_path,text,callback,enabled_flag=True,add_to_menu=True,add_to_toolbar=True,status_tip=None,whats_this=None,parent=None):

        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/GateTransformer/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'& Gate Transformer'),
            callback=self.run,
            parent=self.iface.mainWindow(),
            status_tip='Gate Transformer'
        )

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                #self.tr(u'&NetworkTransformer'),
                self.menu,
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

        self.transformer_analysis.unload_gui()

    def run(self):
        """Run method that performs all the real work"""
        self.transformer_analysis.load_gui()
