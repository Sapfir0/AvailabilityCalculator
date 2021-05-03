
const urlBase = 'https://api.mapbox.com/isochrone/v1/mapbox/';
const defaultLon = 44.5
const defaultLat = 48.7
let lon = defaultLon;
let lat = defaultLat;
let profile = 'walking';
let minutes = 10;

mapboxgl.accessToken = 'pk.eyJ1Ijoic2FwZmlyMCIsImEiOiJja284ZGk3aTkwNnZoMnBxbXM4eWl4Mmw4In0.XwtrCKXKgPC5fY_6a18XJg';

const map = new mapboxgl.Map({
    container: 'map', // container id
    style: 'mapbox://styles/mapbox/streets-v11', // stylesheet
    center: [defaultLon, defaultLat], // starting position [lng, lat]
    zoom: 11.5 // starting zoom
});

map.on('click', async function (e) {
    l = e.lngLat
    lon = l.lng
    lat = l.lat
    marker.setLngLat(e.lngLat).addTo(map);
    await getIso();
});

// Target the params form in the HTML
const params = document.getElementById('params');


// Set up a marker that you can use to show the query's coordinates
const marker = new mapboxgl.Marker({
    'color': '#314ccd'
});

// Create a LngLat object to use in the marker initialization
// https://docs.mapbox.com/mapbox-gl-js/api/#lnglat
const lngLat = {
    lon: lon,
    lat: lat
};

async function getIso() {
    const query = `${urlBase}${profile}/${lon},${lat}?contours_minutes=${minutes}&polygons=true&access_token=${mapboxgl.accessToken}`;
    const data = await fetch(query)
    const res = await data.json()
    map.getSource('iso').setData(res);
}

// When a user changes the value of profile or duration by clicking a button, change the parameter's value and make the API query again
params.addEventListener('change', async function (e) {
    if (e.target.name === 'profile') {
        profile = e.target.value;
        await getIso();
    } else if (e.target.name === 'duration') {
        minutes = e.target.value;
        await getIso();
    }
});

map.on('load', async function () {
    // When the map loads, add the source and layer
    map.addSource('iso', {
        type: 'geojson',
        data: {
            'type': 'FeatureCollection',
            'features': []
        }
    });

    map.addLayer(
    {
        'id': 'isoLayer',
        'type': 'fill',
        'source': 'iso',
        'layout': {},
        'paint': {
        'fill-color': '#5a3fc0',
        'fill-opacity': 0.3
        }
    },
    'poi-label'
    );

    // Initialize the marker at the query coordinates
    marker.setLngLat(lngLat).addTo(map);

    // Make the API call
    await getIso();
});
