export const accessToken = 'pk.eyJ1Ijoic2FwZmlyMCIsImEiOiJja284ZGk3aTkwNnZoMnBxbXM4eWl4Mmw4In0.XwtrCKXKgPC5fY_6a18XJg'

export const geojsonFormat = {
    type: 'geojson' as const,
    data: {
        type: 'FeatureCollection',
        features: [],
    },
}

export const isoLayer = {
    id: 'isoLayer',
    type: 'fill',
    source: 'iso',
    layout: {},
    paint: {
        'fill-color': '#5a3fc0',
        'fill-opacity': 0.3,
    },
}