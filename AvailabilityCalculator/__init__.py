import os.path
from PyQt5.QtWidgets import QAction, QMessageBox
from qgis.core import QgsVectorLayer, QgsVectorFileWriter, QgsProject, QgsWkbTypes
from qgis.utils import iface
import processing

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
        layerName = "Кадастр"
        bufferDist = 500
        layer = QgsProject.instance().mapLayersByName(layerName)[0]
        if not layer.isValid():
            QMessageBox.information(None, 'AvailabilityCalculator', f'Layer loading failed')
        else:
            print("Valid layer")
            QgsProject.instance().addMapLayer(layer)

        bufferLayer = processing.run("qgis:buffer", {'INPUT': layer, 'DISTANCE': bufferDist, 'OUTPUT': 'TEMPORARY_OUTPUT'})['OUTPUT']
        QgsProject.instance().addMapLayer(bufferLayer)

        processing.run('qgis:extractbylocation',  {'INPUT': layer, 'PREDICATE': [0], 'INTERSECT': bufferLayer, 'OUTPUT': 'TEMPORARY_OUTPUT'})





