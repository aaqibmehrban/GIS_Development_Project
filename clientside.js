window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        initializeMap: function(id, dataType, selectedFeatures) {
            // Ensure the map is only initialized once
            if (!window.olMap) {
                // Initialize the map
                window.olMap = new ol.Map({
                    target: id,
                    layers: [
                        new ol.layer.Tile({
                            source: new ol.source.OSM(),
                            name: 'base'  // Add name to identify the base layer
                        }),
                        new ol.layer.Tile({
                            source: new ol.source.TileWMS({
                                url: 'http://localhost:8080/geoserver/wms',
                                params: {'LAYERS': 'helsinkiArea:helsinki_boundaries', 'TILED': true},
                                serverType: 'geoserver',
                                crossOrigin: 'anonymous'
                            }),
                            name: 'boundaries'  // Add name to identify this layer
                        })
                    ],
                    view: new ol.View({
                        center: ol.proj.fromLonLat([24.945831, 60.192059]), // Helsinki coordinates
                        zoom: 10
                    })
                });
            }

            const layers = {
                'temperature': null,  // No specific layer for temperature
                'dem': new ol.layer.Tile({
                    source: new ol.source.TileWMS({
                        url: 'http://localhost:8080/geoserver/wms',
                        params: {'LAYERS': 'helsinkiArea:L4133A_Helsinki', 'TILED': true},
                        serverType: 'geoserver',
                        crossOrigin: 'anonymous'
                    }),
                    name: 'dem'
                }),
                'wind_speed': new ol.layer.Tile({
                    source: new ol.source.TileWMS({
                        url: 'http://localhost:8080/geoserver/wms',
                        params: {'LAYERS': 'helsinkiArea:FIN_wind-speed_10m', 'TILED': true},
                        serverType: 'geoserver',
                        crossOrigin: 'anonymous'
                    }),
                    name: 'wind_speed'
                }),
                '3d_buildings': null  // Add layer definition if applicable
            };

            // Remove existing data layers (except base layer and boundaries)
            const layersToRemove = [];
            window.olMap.getLayers().forEach(layer => {
                if (layer.get('name') !== 'base' && layer.get('name') !== 'boundaries') {
                    layersToRemove.push(layer);
                }
            });
            layersToRemove.forEach(layer => window.olMap.removeLayer(layer));

            // Add the selected data type layer
            if (dataType && layers[dataType]) {
                window.olMap.addLayer(layers[dataType]);
            }

            // Clear existing vector layers except the base layers
            const vectorLayersToRemove = [];
            window.olMap.getLayers().forEach(layer => {
                if (layer instanceof ol.layer.Vector) {
                    vectorLayersToRemove.push(layer);
                }
            });
            vectorLayersToRemove.forEach(layer => window.olMap.removeLayer(layer));

            if (selectedFeatures && selectedFeatures.length > 0) {
                const highlightLayer = new ol.layer.Vector({
                    source: new ol.source.Vector(),
                    style: new ol.style.Style({
                        stroke: new ol.style.Stroke({
                            color: '#ff0000',
                            width: 3
                        })
                    })
                });

                selectedFeatures.forEach(selectedFeature => {
                    const featureRequest = new ol.format.WFS().writeGetFeature({
                        srsName: 'EPSG:4326',
                        featurePrefix: 'helsinkiArea',
                        featureTypes: ['helsinki_boundaries'],
                        outputFormat: 'application/json',
                        filter: ol.format.filter.equalTo('Nimi', selectedFeature)
                    });

                    fetch('http://localhost:8080/geoserver/wfs', {
                        method: 'POST',
                        body: new XMLSerializer().serializeToString(featureRequest)
                    }).then(response => {
                        return response.json();
                    }).then(json => {
                        const features = new ol.format.GeoJSON().readFeatures(json);
                        highlightLayer.getSource().clear(); // Clear previous highlights
                        highlightLayer.getSource().addFeatures(features);
                        window.olMap.addLayer(highlightLayer);
                        if (features.length > 0) {
                            const extent = highlightLayer.getSource().getExtent();
                            window.olMap.getView().fit(extent, { duration: 1000 });
                        }
                    });
                });
            }
        }
    }
});
