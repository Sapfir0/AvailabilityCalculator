import processing
from enum import Enum

class STRATEGY(Enum):
    ShortestPath = 0
    FastestPath = 1

notFound = -1
layerName = "Кадастр"
roadLayerName = "iso highway"
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

for id, feat in enumerate(roadLayer.getFeatures()):
    geometry = feat.geometry()
    buffer = geometry.buffer(bufferDist, 16)
    feat = QgsFeature(id)
    feat.setGeometry(buffer)
    centroid = geometry.centroid().asPoint()
    lat, lon = centroid.x(), centroid.y()
    layer_crs = layer.sourceCrs().toWkt()

    isochrone = processing.run("qneat3:isoareaaspolygonsfrompoint", {
        'INPUT': roadLayer,
        'START_POINT': f'{lat},{lon} []',
        'MAX_DIST':2500,
        'INTERVAL':500,
        'CELL_SIZE':10,
        'STRATEGY': STRATEGY.ShortestPath.value,
        'ENTRY_COST_CALCULATION_METHOD':0,'DIRECTION_FIELD':None,
        'VALUE_FORWARD':'','VALUE_BACKWARD':'','VALUE_BOTH':'','DEFAULT_DIRECTION':2,'SPEED_FIELD':None,
        'DEFAULT_SPEED':5,'TOLERANCE':0,'OUTPUT_INTERPOLATION':'TEMPORARY_OUTPUT','OUTPUT_POLYGONS':'TEMPORARY_OUTPUT'}
    )['OUTPUT_POLYGONS']
        
    mapInIsochrone = processing.run("native:extractbylocation", {'INPUT':layer,'PREDICATE':[0],'INTERSECT':isochrone,'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']
    areas = [isofeat.geometry().area() for isofeat in mapInIsochrone.getFeatures()]

    countOfFeaturesInIsochrone = len(areas)
    avgAreaOfFeaturesInIsochrone = sum(areas) / len(areas)


    break