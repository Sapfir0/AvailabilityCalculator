import mapboxgl from 'mapbox-gl';
import { observer } from 'mobx-react';
import React, { useEffect, useRef, useState } from 'react';
import { accessToken, geojsonFormat, isoLayer } from '../config';
import { TYPES } from '../inversify/types';
import { getIso } from '../services/ApiInteractionService';
import { useInject } from '../services/hooks';
import { IsochroneSettings } from './IsochroneSettings';
import { MapStore } from './MapStore';

mapboxgl.accessToken = accessToken;

const Map = observer(() => {
    const mapStore = useInject<MapStore>(TYPES.MapStore);

    const mapContainerRef = useRef(null);

    const [lng, setLng] = useState(44.5);
    const [lat, setLat] = useState(48.7);
    const [zoom, setZoom] = useState(11.5);

    useEffect(() => {
        const map = new mapboxgl.Map({
            container: mapContainerRef.current!,
            style: 'mapbox://styles/mapbox/streets-v11',
            center: [lng, lat],
            zoom: zoom,
        });

        map.on('load', async function () {
            map.addSource('iso', geojsonFormat as any);
            map.addLayer(isoLayer as any, 'poi-label');
        });

        const marker = new mapboxgl.Marker({
            color: '#314ccd',
        });

        map.on('click', async function (e) {
            setLat(e.lngLat.lat);
            setLng(e.lngLat.lng);
            marker.setLngLat(e.lngLat).addTo(map);
            const features = await getIso(e.lngLat.lat, e.lngLat.lng, mapStore.travelMode, mapStore.maxDuration);
            (map.getSource('iso') as any).setData(features);

            const geoJson = map.querySourceFeatures('iso', { sourceLayer: 'isoLayer' });
            console.log(geoJson);
        });

        return () => map.remove();
    }, []);

    return (
        <div>
            <div className="map-container" ref={mapContainerRef} />
            <IsochroneSettings />
        </div>
    );
});

export default Map;
