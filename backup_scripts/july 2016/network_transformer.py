"""
/***************************************************************************
 NetworkTransformer
                                 A QGIS plugin
 This plugin performs basic transformation on a network class in qgis.
                              -------------------
        begin                : 2016-02-29
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Stephen Law
        email                : s.law@spacesyntax.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

# -*- coding: utf-8 -*-
"""
/***************************************************************************
 NetworkTransformer
                                 A QGIS plugin
 This plugin performs basic transformation on a network class in qgis.
                              -------------------
        begin                : 2016-02-29
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Stephen Law
        email                : s.law@spacesyntax.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from network_transformer_dialog import NetworkTransformerDialog
import os.path
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt, QVariant, pyqtSlot
from PyQt4.QtGui import QAction, QIcon, QFileDialog, QMessageBox, QProgressBar,QComboBox
from qgis.core import *
#from qgis.gui import *
import os
#from PyQt4 import QtCore, QtGui
import math
import Transformer_analysis
#import Transformer_analysis

# this import python deploy-debug package, hashtag is_debug if debugging is not used.
is_debug = True
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
        self.transformer_analysis = Transformer_analysis.transformer_analysis(self.iface)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'NetworkTransformer_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference *creates new dialog object runs dialog __init__
        self.dlg = NetworkTransformerDialog()


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&NetworkTransformer')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'NetworkTransformer')
        self.toolbar.setObjectName(u'NetworkTransformer')

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
        return QCoreApplication.translate('NetworkTransformer', message)

    def add_action(self,icon_path,text,callback,enabled_flag=True,add_to_menu=True,add_to_toolbar=True,status_tip=None,whats_this=None,parent=None):
        x=1

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

        icon_path = ':/plugins/NetworkTransformer/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'qgis network transformer'),
            callback=self.run,
            parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&NetworkTransformer'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

################################# activate dialog box #############################

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()

        ###### YOUR OWN CODE ######

        # click pushButtons
        # put code about some radio button has to be pressed
        self.dlg.run_button.clicked.connect(self.run_method)
        self.dlg.close_button.clicked.connect(self.close_method)

        # put current layers into comboBox
        layers = QgsMapLayerRegistry.instance().mapLayers().values()
        layer_objects =[]
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == QGis.Line:
                layer_objects.append((layer.name(),layer))
        self.dlg.update_layer(layer_objects)

        # Run the dialog event loop
        result = self.dlg.exec_()


################################# run and close methods #############################
    def run_method(self):
        self.dlg.show()
        layer=self.dlg.get_layer()
        transformation,value = self.dlg.get_transformation()

        if transformation==1:
            #self.rotate_line(value)
            self.transformer_analysis.rotate_line02(layer,value)

        elif transformation==2:
            #self.resize_line(value)
            self.transformer_analysis.resize_line02(layer,value)

        elif transformation==3:
            #self.rescale_line(value)
            self.transformer_analysis.rescale_line02(layer,value)

        self.close_method()

    def close_method(self):
        self.dlg.close()
        # run close method


########################### transformation block ########################

# rotate_line_scripts
    def rotate_line(self,value):

        layer=self.dlg.get_layer()
        #provider = layer.dataProvider()
        layer.startEditing()
        layer.selectAll()
        set_angle = value

        for i in layer.selectedFeatures():
            geom=i.geometry()
            geom.rotate(set_angle,QgsPoint(geom.centroid().asPoint()))
            layer.changeGeometry(i.id(),geom)

        layer.updateExtents()
        layer.reload()
        layer.removeSelection()

# resize_line_scripts
    def resize_line(self,value):

        layer = self.dlg.get_layer()

        layer_provider = layer.dataProvider()
        layer.startEditing()
        layer.selectAll()

        set_length=value

        for i in layer.selectedFeatures():
            geom=i.geometry()
            pt=geom.asPolyline()
            dy=pt[1][1] - pt[0][1]
            dx=pt[1][0] - pt[0][0]
            angle = math.atan2(dy,dx)
            length=geom.length()
            startx=geom.centroid().asPoint()[0]+((0.5*length*set_length/length)*math.cos(angle))
            starty=geom.centroid().asPoint()[1]+((0.5*length*set_length/length)*math.sin(angle))
            endx=geom.centroid().asPoint()[0]-((0.5*length*set_length/length)*math.cos(angle))
            endy=geom.centroid().asPoint()[1]-((0.5*length*set_length/length)*math.sin(angle))
            n_geom=QgsFeature()
            n_geom.setGeometry(QgsGeometry.fromPolyline([QgsPoint(startx,starty),QgsPoint(endx,endy)]))
            layer.changeGeometry(i.id(),n_geom.geometry())


        #layer.commitChanges()
        layer.updateExtents()
        layer.reload()
        layer.removeSelection()

# rescale_line_scripts
    def rescale_line(self,value):

        layer = self.dlg.get_layer()
        layer_provider = layer.dataProvider()
        layer.startEditing()
        layer.selectAll()

        set_scale=value

        for i in layer.selectedFeatures():
            geom=i.geometry()
            pt=geom.asPolyline()
            dy=pt[1][1] - pt[0][1]
            dx=pt[1][0] - pt[0][0]
            angle = math.atan2(dy,dx)
            length=geom.length()
            startx=geom.centroid().asPoint()[0]+((0.5*length*set_scale)*math.cos(angle))
            starty=geom.centroid().asPoint()[1]+((0.5*length*set_scale)*math.sin(angle))
            endx=geom.centroid().asPoint()[0]-((0.5*length*set_scale)*math.cos(angle))
            endy=geom.centroid().asPoint()[1]-((0.5*length*set_scale)*math.sin(angle))
            new_geom=QgsFeature()
            new_geom.setGeometry(QgsGeometry.fromPolyline([QgsPoint(startx,starty),QgsPoint(endx,endy)]))
            layer.changeGeometry(i.id(),new_geom.geometry())

        #layer.commitChanges()
        layer.updateExtents()
        layer.reload()
        layer.removeSelection()