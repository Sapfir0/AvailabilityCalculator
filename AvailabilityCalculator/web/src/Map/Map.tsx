import mapboxgl from 'mapbox-gl';
import React, { useEffect, useRef, useState } from 'react';
import { accessToken, geojsonFormat, isoLayer } from '../config';
import { getIso } from '../services/ApiInteractionService';
import { IsochroneSettings } from './IsochroneSettings';

mapboxgl.accessToken = accessToken;

const Map = () => {
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
            setLat(e.lngLat.lat)
            setLng(e.lngLat.lng)
            marker.setLngLat(e.lngLat).addTo(map);            
            const features = await getIso(e.lngLat.lat, e.lngLat.lng);
            (map.getSource('iso') as any).setData(features)
        });

        return () => map.remove();
    }, []); // eslint-disable-line react-hooks/exhaustive-deps

    return (
        <div>
            <div className="map-container" ref={mapContainerRef} />
            {/* <IsochroneSettings /> */}
        </div>
    );
};

export default Map;
