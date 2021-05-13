import processing

bufferDist = 500
mapLayer = QgsProject.instance().mapLayersByName("Кадастр")[0]
fieldName = "NeighborsCount"
fieldNameLength = 10
roadLayer = QgsProject.instance().mapLayersByName("HighwayTula AllHighwaysTags")[0]

realFieldName = fieldName[0:fieldNameLength]

if not mapLayer.isValid():
    QMessageBox.information(None, 'AvailabilityCalculator', f'Layer loading failed')
else:
    QgsProject.instance().addMapLayer(mapLayer)


for id, feat in enumerate(mapLayer.getFeatures()):
    geometry = feat.geometry()
    centroid = geometry.centroid().asPoint()
    lat, lon = centroid.x(), centroid.y()


    buffer = geometry.buffer(bufferDist, 16)
    feat = QgsFeature(id)
    feat.setGeometry(buffer)

    layer_crs = mapLayer.sourceCrs().toWkt()
    buff_layer = QgsVectorLayer('Polygon?crs='+layer_crs, "Buffered "+ mapLayer.sourceName(), "memory")

    
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
    
    if id > 0:
        break