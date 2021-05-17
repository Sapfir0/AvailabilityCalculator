import os.path
from PyQt5.QtWidgets import QAction, QMessageBox
from qgis.core import QgsVectorLayer, QgsVectorFileWriter, QgsProject, QgsWkbTypes, QgsFeature
from qgis.utils import iface
from PyQt5 import uic
from PyQt5 import QtWidgets
import processing
from enum import Enum


class STRATEGY(Enum):
    ShortestPath = 0
    FastestPath = 1

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'form.ui'))

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

    def run(self):
        def setAttribute(layer, attributeName, attributeValue):
            layer.startEditing()
            fieldIdx = layerDataProvider.fields().indexFromName(attributeName)
            layerDataProvider.changeAttributeValues({int(feat.id()): {fieldIdx: attributeValue} })
            layer.commitChanges()


        notFound = -1
        layerName = "Кадастр"
        roadLayerName = "iso highway"
        bufferDist = 500
        layer = QgsProject.instance().mapLayersByName(layerName)[0]
        fieldNameLength = 10
        bufferAttributeName = "NeighborsCount"[0:fieldNameLength]
        isochroneFeaturesAvgAreaAttributeName = "AvgAreaIsochrone"[0:fieldNameLength]
        isochroneFeaturesCountAttributeName = "CountIsochrone"[0:fieldNameLength]

        roadLayer = QgsProject.instance().mapLayersByName(roadLayerName)[0]

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


        for id, feat in enumerate(layer.getFeatures()):
            geometry = feat.geometry()
            buffer = geometry.buffer(bufferDist, 16)
            feat = QgsFeature(id)
            feat.setGeometry(buffer)
            centroid = geometry.centroid().asPoint()
            lat, lon = centroid.x(), centroid.y()

            layer_crs = layer.sourceCrs().toWkt()
            buffLayer = QgsVectorLayer('Polygon?crs='+layer_crs, "Buffered "+ layer.sourceName(), "memory")
            buffLayer.dataProvider().addFeatures([feat])
            try:
                res = processing.run("qgis:extractbylocation", 
                    {'INPUT': layer, 'PREDICATE': 0, 'INTERSECT': buffLayer, 'OUTPUT': 'TEMPORARY_OUTPUT'}
                )['OUTPUT']

                featuresCount = res.featureCount()
                setAttribute(layer, bufferAttributeName, featuresCount)
                #QgsProject.instance().addMapLayer(res)
            except:
                print(f"Error while processing on {id}")

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
                
            mapInIsochrone = processing.run("native:extractbylocation", {'INPUT':layer,'PREDICATE':[0],'INTERSECT':isochrone,'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']
            areas = [isofeat.geometry().area() for isofeat in mapInIsochrone.getFeatures()]

            countOfFeaturesInIsochrone = len(areas)
            avgAreaOfFeaturesInIsochrone = sum(areas) / len(areas)

            setAttribute(layer, isochroneFeaturesCountAttributeName, countOfFeaturesInIsochrone)
            setAttribute(layer, isochroneFeaturesAvgAreaAttributeName, avgAreaOfFeaturesInIsochrone)

            break
  