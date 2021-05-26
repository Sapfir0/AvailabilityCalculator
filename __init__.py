import os.path
from PyQt5.QtWidgets import QAction, QMessageBox
from qgis.core import QgsVectorLayer, QgsField, QgsVectorFileWriter, QgsProject, QgsWkbTypes, QgsFeature
from qgis.utils import iface
from PyQt5 import uic
from PyQt5.QtCore import QVariant
from PyQt5 import QtWidgets
import processing
from enum import Enum
from .calculator_dialog import CalculatorDialog
from qgis.PyQt.QtWidgets import (
    QAction, QFileDialog, QMessageBox)

class STRATEGY(Enum):
    ShortestPath = 0
    FastestPath = 1


def classFactory(iface):
    return MinimalPlugin(iface)

class MinimalPlugin:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.action = QAction('Go!', self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def setAttribute(self, layer, attributeName, attributeValue, feat):
        layer.startEditing()
        fieldIdx = layer.dataProvider().fields().indexFromName(attributeName)
        layer.dataProvider().changeAttributeValues({int(feat.id()): {fieldIdx: attributeValue} })
        layer.commitChanges()
    
    def bufferProcessing(self, layer, bufferDist, bufferAttributeName):
        for id, feat in enumerate(layer.getFeatures()):
            geometry = feat.geometry()
            buffer = geometry.buffer(bufferDist, 16)
            feat = QgsFeature(id)
            feat.setGeometry(buffer)


            layer_crs = layer.sourceCrs().toWkt()
            buffLayer = QgsVectorLayer('Polygon?crs='+layer_crs, "Buffered "+ layer.sourceName(), "memory")
            buffLayer.dataProvider().addFeatures([feat])
            try:
                res = processing.run("qgis:extractbylocation", 
                    {'INPUT': layer, 'PREDICATE': 0, 'INTERSECT': buffLayer, 'OUTPUT': 'TEMPORARY_OUTPUT'}
                )['OUTPUT']

                featuresCount = res.featureCount()
                self.setAttribute(layer, bufferAttributeName, featuresCount, feat)
                #QgsProject.instance().addMapLayer(res)
            except:
                print(f"Error while processing on {id}")


    def isochroneProcessing(self, layer, roadLayer, bufferDist, isochroneFeaturesCountAttributeName, isochroneFeaturesAvgAreaAttributeName):
        # мы должны ходить по фичам, относящимся к дороге   
        isochrones = []
        for id, feat in enumerate(roadLayer.getFeatures()):
            geometry = feat.geometry()
            centroid = geometry.centroid().asPoint()
            lat, lon = centroid.x(), centroid.y()
            print("Isochrone building")
            isochrone = processing.run("qneat3:isoareaaspolygonsfrompoint", {
                'INPUT': roadLayer,
                'START_POINT': f'{lat},{lon} []',
                'MAX_DIST': bufferDist,
                'INTERVAL': bufferDist / 5,
                'CELL_SIZE': 5,
                'STRATEGY': STRATEGY.ShortestPath.value,
                'ENTRY_COST_CALCULATION_METHOD':0,'DIRECTION_FIELD':None,
                'VALUE_FORWARD':'','VALUE_BACKWARD':'','VALUE_BOTH':'','DEFAULT_DIRECTION':2,'SPEED_FIELD':None,
                'DEFAULT_SPEED':5,'TOLERANCE':0,'OUTPUT_INTERPOLATION':'TEMPORARY_OUTPUT','OUTPUT_POLYGONS':'TEMPORARY_OUTPUT'}
            )['OUTPUT_POLYGONS']
            print("Extracting")
            isochrones.append(isochrone)

            mapInIsochrone = processing.run("native:extractbylocation", {'INPUT':layer,'PREDICATE':[0],'INTERSECT':isochrone,'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']
            areas = [isofeat.geometry().area() for isofeat in mapInIsochrone.getFeatures()]

            countOfFeaturesInIsochrone = len(areas)
            avgAreaOfFeaturesInIsochrone = sum(areas) / len(areas)

            self.setAttribute(layer, isochroneFeaturesCountAttributeName, countOfFeaturesInIsochrone, feat)
            self.setAttribute(layer, isochroneFeaturesAvgAreaAttributeName, avgAreaOfFeaturesInIsochrone, feat)
            
        QgsProject.instance().addMapLayer(isochrones)

    def run(self):
        self.dialog = CalculatorDialog()
        self.dialog.show()
        self.dialog.adjustSize()
        result = self.dialog.exec_()
        if result == QFileDialog.Rejected:
            return

        notFound = -1

        layer = QgsProject.instance().mapLayersByName(self.dialog.featuresLayer.currentText())[0]
        roadLayer = QgsProject.instance().mapLayersByName(self.dialog.roadLayer.currentText())[0]

        fieldNameLength = 10
        bufferAttributeName = "NeighborsCount"[0:fieldNameLength]
        isochroneFeaturesAvgAreaAttributeName = "AvgAreaIsochrone"[0:fieldNameLength]
        isochroneFeaturesCountAttributeName = "CountIsochrone"[0:fieldNameLength]

        bufferDist = int(self.dialog.bufferSize.value())

        bufferAttributeName = bufferAttributeName[0:fieldNameLength]

        if not layer.isValid():
            QMessageBox.information(None, 'AvailabilityCalculator', f'Layer loading failed')
        else:
            QgsProject.instance().addMapLayer(layer)


        layerDataProvider=layer.dataProvider()
        for field in [bufferAttributeName, isochroneFeaturesAvgAreaAttributeName, isochroneFeaturesCountAttributeName]:
            if (layer.fields().indexFromName(field) == notFound):
                layerDataProvider.addAttributes([QgsField(field,QVariant.Int)])
                layer.updateFields()


        bufferMode = self.dialog.bufferizationMode.currentText().lower()
        
        if bufferMode == "isochrone":
            self.isochroneProcessing(layer, roadLayer, bufferDist, isochroneFeaturesCountAttributeName, isochroneFeaturesAvgAreaAttributeName)
        elif bufferMode == "buffer":
            self.bufferProcessing(layer, bufferDist, bufferAttributeName)