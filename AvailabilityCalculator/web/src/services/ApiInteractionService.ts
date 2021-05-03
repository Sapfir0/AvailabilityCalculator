import { accessToken } from "../config";

const urlBase = 'https://api.mapbox.com/isochrone/v1/mapbox/';


export async function getIso(lat: number, lon: number, profile='walking', minutes='10') {
    const query = `${urlBase}${profile}/${lon},${lat}?contours_minutes=${minutes}&polygons=true&access_token=${accessToken}`;
    const data = await fetch(query)
    const res = await data.json()
    return res
}