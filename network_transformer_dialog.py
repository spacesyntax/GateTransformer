# -*- coding: utf-8 -*-
"""
/***************************************************************************
 NetworkTransformerDialog
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources
import os.path
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt, QVariant, pyqtSlot
from PyQt4.QtGui import QAction, QIcon, QFileDialog, QMessageBox, QProgressBar,QComboBox
from qgis.core import *
from qgis.gui import *
import os
from PyQt4 import QtCore, QtGui
import math


import os

from PyQt4 import QtGui, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'network_transformer_dialog_base.ui'))

class NetworkTransformerDialog(QtGui.QDialog, FORM_CLASS):


############################ initialisation ############################

    def __init__(self, parent=None):
        """Constructor."""
        super(NetworkTransformerDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        ###### YOUR OWN CODE ######
        # click pushButtons
        self.pushButton.clicked.connect(self.run_method)
        self.pushButton_2.clicked.connect(self.close_method)

        # put current layers into comboBox
        layers = QgsMapLayerRegistry.instance().mapLayers().values()
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == QGis.Line:
               self.comboBox.addItem( layer.name(), layer )


        x=1


########################### transformation block ########################

# rotate_line_scripts
    def rotate_line(self):

        index = self.comboBox.currentIndex()
        layer = self.comboBox.itemData(index)

        #layer = self.iface.activeLayer()
        provider = layer.dataProvider()
        layer.startEditing()
        layer.selectAll()

        set_angle = self.spinBox.value()

        for i in layer.selectedFeatures():
            geom=i.geometry()
            geom.rotate(set_angle,QgsPoint(geom.centroid().asPoint()))
            layer.changeGeometry(i.id(),geom)
            #print geom.asPolyline()

        layer.commitChanges()
        layer.updateExtents()
        layer.reload()
        layer.removeSelection()

# resize_line_scripts
    def resize_line(self):

        index = self.comboBox.currentIndex()
        layer = self.comboBox.itemData(index)

        #layer = self.iface.activeLayer()
        layer_provider = layer.dataProvider()
        layer.startEditing()
        layer.selectAll()

        set_length=self.spinBox_2.value()

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


        layer.commitChanges()
        layer.updateExtents()
        layer.reload()
        layer.removeSelection()

# rescale_line_scripts
    def rescale_line(self):

        index = self.comboBox.currentIndex()
        layer = self.comboBox.itemData(index)

        #layer = self.iface.activeLayer()
        layer_provider = layer.dataProvider()
        layer.startEditing()
        layer.selectAll()

        set_scale=self.doubleSpinBox.value()

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

        layer.commitChanges()
        layer.updateExtents()
        layer.reload()
        layer.removeSelection()




################################# run and close methods #############################
    def run_method(self):
        if self.radioButton.isChecked():
            self.rotate_line()
            self.close()

        elif self.radioButton_2.isChecked():
            self.resize_line()
            self.close()

        elif self.radioButton_3.isChecked():
            self.rescale_line()
            self.close()
        else:
            self.close()

    def close_method(self):
        self.close()
        # run close method