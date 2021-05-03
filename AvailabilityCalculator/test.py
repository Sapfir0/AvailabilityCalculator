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


for id, feat in enumerate(layer.getFeatures()):
    geometry = feat.geometry()
    buffer = geometry.buffer(bufferDist, 16)
    feat = QgsFeature(id)
    feat.setGeometry(buffer)

    layer_crs = layer.sourceCrs().toWkt()
    buff_layer = QgsVectorLayer('Polygon?crs='+layer_crs, "Buffered "+ layer.sourceName(), "memory")
    if id > 2:
        break