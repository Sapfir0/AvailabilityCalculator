import os.path
from PyQt5.QtWidgets import QAction, QMessageBox
from qgis.core import QgsVectorLayer, QgsVectorFileWriter, QgsProject, QgsWkbTypes, QgsFeature
from qgis.utils import iface
import processing

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

        buffered_feat_list = []

        if not layer.isValid():
            QMessageBox.information(None, 'AvailabilityCalculator', f'Layer loading failed')
        else:
            QgsProject.instance().addMapLayer(layer)
        print(layer)

        for id, feat in enumerate(layer.getFeatures()):
            geometry = feat.geometry()
            buffer = geometry.buffer(bufferDist, 16)
            feat = QgsFeature(id)
            feat.setGeometry(buffer)
            # buffered_feat_list.append(feat)

            layer_crs = layer.sourceCrs().toWkt()
            buff_layer = QgsVectorLayer('Polygon?crs='+layer_crs, "Buffered "+ layer.sourceName(), "memory")
            buff_layer.dataProvider().addFeatures([feat])
            res = processing.run("qgis:extractbylocation", 
                {'INPUT': layer, 'PREDICATE': 0, 'INTERSECT': buff_layer, 'OUTPUT': 'TEMPORARY_OUTPUT'}
            )['OUTPUT']
            print(res.featureCount())
            #QgsProject.instance().addMapLayer(res)
            if id >= 5:
                break
            