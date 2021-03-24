import os.path
from PyQt5.QtWidgets import QAction, QMessageBox
from qgis.core import QgsVectorLayer, QgsVectorFileWriter, QgsProject, QgsWkbTypes, QgsFeature
from qgis.utils import iface
import processing

notFound = -1

def classFactory(iface):
    return MinimalPlugin(iface)

#layer_provider=layer.dataProvider()
#layer_provider.addAttributes([QgsField(fieldName,QVariant.Int)])
#layer.updateFields()

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
        layerName = "Кадастр"
        bufferDist = 500
        layer = QgsProject.instance().mapLayersByName(layerName)[0]
        fieldName = "NeighborsCount"
        fieldNameLength = 10

        realFieldName = fieldName[0:fieldNameLength]
        buffered_feat_list = []

        if not layer.isValid():
            QMessageBox.information(None, 'AvailabilityCalculator', f'Layer loading failed')
        else:
            QgsProject.instance().addMapLayer(layer)


        layerDataProvider=layer.dataProvider()
        if (layer.fields().indexFromName(realFieldName) == notFound):
            layerDataProvider.addAttributes([QgsField(fieldName,QVariant.Int)])
            layer.updateFields()


        for id, feat in enumerate(layer.getFeatures()):
            geometry = feat.geometry()
            buffer = geometry.buffer(bufferDist, 16)
            feat = QgsFeature(id)
            feat.setGeometry(buffer)

            layer_crs = layer.sourceCrs().toWkt()
            buff_layer = QgsVectorLayer('Polygon?crs='+layer_crs, "Buffered "+ layer.sourceName(), "memory")
            buff_layer.dataProvider().addFeatures([feat])
            try:
                res = processing.run("qgis:extractbylocation", 
                    {'INPUT': layer, 'PREDICATE': 0, 'INTERSECT': buff_layer, 'OUTPUT': 'TEMPORARY_OUTPUT'}
                )['OUTPUT']

                featuresCount = res.featureCount()
                layer.startEditing()

                updateMap = {}
                fieldIdx = layer_provider.fields().indexFromName(realFieldName)
                attrValues = {fieldIdx: featuresCount}

                layerDataProvider.changeAttributeValues({int(feat.id()): attrValues })
                layer.commitChanges()
                #QgsProject.instance().addMapLayer(res)
            except:
                print(f"Error while processing on {id}")
            