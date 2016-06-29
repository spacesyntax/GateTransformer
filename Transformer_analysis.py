__author__ = 's.law'

# rotate_line_scripts
def rotate_line02(self):

        index = self.dlg.comboBox.currentIndex()
        layer = self.dlg.comboBox.itemData(index)

        #layer = self.iface.activeLayer()
        provider = layer.dataProvider()
        layer.startEditing()
        layer.selectAll()

        set_angle = self.dlg.spinBox.value()

        for i in layer.selectedFeatures():
            geom=i.geometry()
            geom.rotate(set_angle,QgsPoint(geom.centroid().asPoint()))
            layer.changeGeometry(i.id(),geom)
            #print geom.asPolyline()

        layer.commitChanges()
        layer.updateExtents()
        layer.reload()

# resize_line_scripts
def resize_line02(self):

        index = self.dlg.comboBox.currentIndex()
        layer = self.dlg.comboBox.itemData(index)

        #layer = self.iface.activeLayer()
        layer_provider = layer.dataProvider()
        layer.startEditing()
        layer.selectAll()

        set_length=self.dlg.spinBox_2.value()

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

# rescale_line_scripts
def rescale_line02(self):

        index = self.dlg.comboBox.currentIndex()
        layer = self.dlg.comboBox.itemData(index)

        #layer = self.iface.activeLayer()
        layer_provider = layer.dataProvider()
        layer.startEditing()
        layer.selectAll()

        set_scale=self.dlg.doubleSpinBox.value()

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
