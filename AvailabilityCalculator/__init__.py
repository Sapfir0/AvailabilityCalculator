import os.path
from PyQt5.QtWidgets import QAction, QMessageBox
from qgis.core import QgsVectorLayer, QgsVectorFileWriter, QgsProject, QgsWkbTypes, QgsFeature
from qgis.utils import iface
import processing
from PyQt5 import uic
from PyQt5 import QtWidgets

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'main.ui'))

def classFactory(iface):
    return MinimalPlugin(iface)


class MinimalPlugin(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(MinimalPlugin, self).__init__(parent)
        self.setupUi(self)

    def initGui(self):
        self.action = QAction('Go!', self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def run(self):
        notFound = -1
        layerName = "Кадастр"
        roadLayerName = "HighwayTula AllHighwaysTags"
        bufferDist = 500
        layer = QgsProject.instance().mapLayersByName(layerName)[0]
        fieldName = "NeighborsCount"
        fieldNameLength = 10
        roadLayer = QgsProject.instance().mapLayersByName(roadLayerName)[0]

        realFieldName = fieldName[0:fieldNameLength]

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

                fieldIdx = layerDataProvider.fields().indexFromName(realFieldName)
                attrValues = {fieldIdx: featuresCount}

                layerDataProvider.changeAttributeValues({int(feat.id()): attrValues })
                layer.commitChanges()
                #QgsProject.instance().addMapLayer(res)
            except:
                print(f"Error while processing on {id}")


            isochrone = processing.run("qneat3:isoareaaspointcloudfrompoint", {
                'INPUT': roadLayer,
                'START_POINT': f'{lat},{lon} []',
                'MAX_DIST':600,
                'STRATEGY':1,'ENTRY_COST_CALCULATION_METHOD':0,
                'DIRECTION_FIELD':None,'VALUE_FORWARD':'','VALUE_BACKWARD':'','VALUE_BOTH':'',
                'DEFAULT_DIRECTION':2,'SPEED_FIELD':None,'DEFAULT_SPEED':5,'TOLERANCE':0,
                'OUTPUT':'TEMPORARY_OUTPUT'
            }
            )['OUTPUT']
            featuresCount = isochrone.featureCount()
            print(featuresCount)
            if id > 1:
                break
            