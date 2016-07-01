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

# dialog class has get and set update functions
# this is in dialog.py
# QtCore.pyqtSignal() - defines a signal
# self.update.emit() - this emits signal
# this is in tool.py
# self.update.connect() - connects with signal
# self.update.disconnect() - this disconnect with signal

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
        # rotate_button is checked for default
        self.rotate_radio.click()


    # define series of function
    # disable buttons - switch between gate transformation
    # update layer - fill combo with layer lists
    def update_layer(self,layer_objects):
        for layer in layer_objects:
            self.comboBox.addItem(layer[0],layer[1])

    # get layer - retrieving the value of the current selected layer
    def get_layer(self):
        index = self.comboBox.currentIndex()
        layer = self.comboBox.itemData(index)
        return layer

    # get transformation - this will retrieve which transformation and value of transformation
    def get_transformation(self):
        transformation = 0
        value = 0
        if self.rotate_radio.isChecked():
            transformation = 1
            value = self.spinBox.value()
        elif self.resize_radio.isChecked():
            transformation = 2
            value = self.spinBox_2.value()
        elif self.rescale_radio.isChecked():
            transformation = 3
            value = self.spinBox_3.value()

        return transformation, value




