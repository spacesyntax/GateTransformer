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

from PyQt4.QtCore import *
from qgis.core import *
import math

# analysis class
class transformer_analysis(QObject):

    # initialise class with self and iface
    def __init__(self,iface):
        #QObject.__init__(self)
        self.iface=iface

    # rotate_line_scripts
    def rotate_line02(self,layer,value):

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
    def resize_line02(self,layer,value):

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

        layer.updateExtents()
        layer.reload()
        layer.removeSelection()

    # rescale_line_scripts
    def rescale_line02(self,layer,value):

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

        layer.updateExtents()
        layer.reload()
        layer.removeSelection()
