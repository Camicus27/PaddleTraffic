<script setup lang="ts">
import { ref, onMounted, onUnmounted, type Ref, computed } from 'vue'
import mapboxgl from "mapbox-gl"
import MapboxGeocoder from '@mapbox/mapbox-gl-geocoder';
import '@mapbox/mapbox-gl-geocoder/dist/mapbox-gl-geocoder.css';
import { useRoute } from "vue-router"
import Popup from '@/components/Map/Popup.vue'
import CommonHeader from '@/components/CommonHeader.vue'
import {
    getAllLocations,
    getLocationId,
    getLocationsByBounds,
    getLocationsByList,
    getNearestLocation,
    postLocationReport
} from '@/api/functions'
import { type Location } from '@/api/types'
// import { appendFile } from 'fs'
// TODO handle error messages more elegantly
// TODO maybe add debug flag and console.error statments or something

// -------------------------------- REFACTOR ZONE -------------------------------------------- //

interface MapItem {
    location: Ref<Location>
    marker: mapboxgl.Marker
}

// [Location.id] : MapItem
const mapItems: Map<number, MapItem> = new Map()
const currSelected = ref<number | undefined>()

function addMapItem(location: Location, map: mapboxgl.Map) {
    if (mapItems.has(location.id)) return

    // Create Map Marker
    let marker: mapboxgl.Marker;
    marker = new mapboxgl.Marker()
        .setLngLat([location.longitude, location.latitude])
        .addTo(map)

    // Add MapItem
    const newMapItem: MapItem = {
        location: ref(location),
        marker: marker
    }
    mapItems.set(location.id, newMapItem)

    // update color!
    updateMarkerColor(location.id)

    // TODO change to be for event listener on like the Popup instead of just on click
    marker.getElement().addEventListener('click', () => {
        selectMarker(location.id)
    })

}

function addAllMapItems(locations: Location[], map: mapboxgl.Map) {
    for (let location of locations) {
        addMapItem(location, map)
    }
}

// Update the info section with location data
function selectMarker(locId: number) {
    if (!mapItems.has(locId)) return

    const selectedClassName = 'selected'
    if (currSelected.value) { // if a marker is selected
        let mapItem = mapItems.get(currSelected.value)
        let old_marker = mapItem!.marker.getElement()
        old_marker.classList.remove(selectedClassName)
        if (currSelected.value == locId) { // and it's the same one
            currSelected.value = undefined // then none is selected in state
            return // return
        }
    }

    // otherwise set the new one
    currSelected.value = locId
    let fill_el = mapItems.get(locId)!.marker.getElement()
    fill_el.classList.add(selectedClassName)
}

function removeMapItem(locId: number) {
    let mapItem = mapItems.get(locId)
    if (!mapItem) return
    // remove it from the map
    mapItem.marker.remove()
    // from mapItems
    mapItems.delete(locId)
}

function removeAllMapItems() {
    let keys = mapItems.keys()
    for (let key of keys) { // for-of iterator, not for-in for properties in object :/
        removeMapItem(key)
    }
}

function refreshMapItems() {
    let locationIds = Array.from(mapItems.keys())
    getLocationsByList(locationIds).then((locations) => {
        if (!locations) return // don't refresh if data is undefined AKA error could be received
        locations.forEach((value, index) => {
            let mapItem = mapItems.get(value.id)
            if (mapItem) {
                mapItem.location.value = value
                updateMarkerColor(mapItem.location.value.id)
            }
        })
    })
}

function refreshMapItemsByCenter() {
    let { lat, lng } = getMap().getCenter()
    getLocationsByBounds(lat, lng).then((locations) => {
        if (!locations) return // don't refresh if no new data could be received
        removeAllMapItems()
        addAllMapItems(locations, getMap())
    })
}

// -------------------------------- REFACTOR ZONE -------------------------------------------- //

const mapContainer = ref<HTMLElement | undefined>() // reference to the <div> mapContainer
// for the URL ?lat=:number&lon=:number
const props = {
    lat: Number(useRoute().query.lat),
    lon: Number(useRoute().query.lon)
}

// TODO: improve token handling
mapboxgl.accessToken = 'pk.eyJ1Ijoic3VudHp1Y2Fwc3RvbmUiLCJhIjoiY2xwOHl6MGZiMWQwcjJ2bzNpdTh3ZXZ5diJ9.2OxP9v87qKxpFmL7FFrD-g'
const map: Ref<mapboxgl.Map | undefined> = ref() // TODO can we make this just like not undefined? or something
const getMap = () => {
    if (map.value)
        return map.value
    throw new Error("💀I LOVE ERROR MESSAGES💀")
}

let URL: string
// This is the collection of environment variables.
const env = import.meta.env
if (env.MODE === 'production')
    URL = env.VITE_PROD_URL
else
    URL = env.VITE_DEV_URL


// TODO: Remove and add backend endpoint to get ALL location names & coords & address ORRRR figure out backend search
interface Feature {
    type: string;
    properties: {
        title: string;
        place_name?: string;
        center?: [number, number];
        place_type?: string[];
    };
    geometry: {
        coordinates: [number, number];
        type: string;
    };
    place_name?: string;
    center?: [number, number];
    place_type?: string[];
}

interface CustomData {
    features: Feature[];
    type: string;
}

const customData: CustomData = {
    features: [
        {
            type: 'Feature',
            properties: {
                title: 'Picklecoin HQ'
            },
            geometry: {
                type: 'Point',
                coordinates: [-111.845182, 40.767807]
            }
        },
        {
            type: 'Feature',
            properties: {
                title: 'Hogan Park'
            },
            geometry: {
                type: 'Point',
                coordinates: [-111.901010, 40.874055]
            }
        },
        {
            type: 'Feature',
            properties: {
                title: '11th Avenue Park'
            },
            geometry: {
                type: 'Point',
                coordinates: [-111.862134, 40.783488]
            }
        },
        {
            type: 'Feature',
            properties: {
                title: '5th Ave & C Street'
            },
            geometry: {
                type: 'Point',
                coordinates: [-111.880206, 40.774847]
            }
        },
        {
            type: 'Feature',
            properties: {
                title: 'West Bountiful'
            },
            geometry: {
                type: 'Point',
                coordinates: [-111.901440, 40.895123]
            }
        },
        {
            type: 'Feature',
            properties: {
                title: 'Twin Hollow'
            },
            geometry: {
                type: 'Point',
                coordinates: [-111.862690, 40.903635]
            }
        }
    ],
    type: 'FeatureCollection'
};

function forwardGeocoder(query: string): any[] {
    const matchingFeatures: any[] = [];
    for (const feature of customData.features) {
        if (feature.properties.title.toLowerCase().includes(query.toLowerCase())) {
            const result: any = {
                type: "Feature",
                relevance: 1,
                geometry: {
                    type: 'Point',
                    coordinates: feature.geometry.coordinates
                },
                place_name: `🎾 ${feature.properties.title}, Bountiful, Utah, United States`
            };
            matchingFeatures.push(result);
        }
    }
    return matchingFeatures;
}

function initMap() {
    if (!mapContainer?.value) throw new Error("OH MY FREAKING GOSH WHAT THE FRICK 💀💀💀💀💀💀💀💀\n💀💀💀💀💀💀💀💀\n💀💀💀💀💀💀💀💀\n💀💀💀💀💀💀💀💀\n💀💀💀💀💀💀💀💀\n💀💀💀💀💀💀💀💀\n")
    map.value = new mapboxgl.Map({
        container: mapContainer.value,
        style: 'mapbox://styles/mapbox/streets-v12',
        center: [-111.876183, 40.758701], // Default to SLC 
        zoom: 11
    })

    // stank sector
    map.value.doubleClickZoom.disable()
    map.value.on('style.load', () => {
        getMap().setFog({
            color: '#4b5320', // Lower atmosphere
            'high-color': 'rgb(200, 200, 200)', // Upper atmosphere
            'horizon-blend': 0.1, // Atmosphere thickness (default 0.2 at low zooms)
            'space-color': '#183400', // Background color - deep purple to simulate a strange, dark sky
            'star-intensity': 1 // Background star brightness (default 0.35 at low zooms)
        });
    });
    // stank sector

    const geocoder = new MapboxGeocoder({
        accessToken: mapboxgl.accessToken,
        mapboxgl: mapboxgl,
        flyTo: { duration: 0 },
        types: 'place',
        marker: false,
        zoom: getMap().getZoom(),
        localGeocoder: forwardGeocoder
    });

    getMap().addControl(geocoder, 'top-left');
    getMap().addControl(new mapboxgl.NavigationControl());
}

/**
 * Initialized Mapbox with settings, and loading things
 * Gets users geolocation if permitted
 */
function initGeoloc() {
    const geolocateControl = new mapboxgl.GeolocateControl({
        fitBoundsOptions: { maxZoom: 11 },
        positionOptions: { enableHighAccuracy: true },
        trackUserLocation: true,
        showAccuracyCircle: false
    })
    getMap().addControl(geolocateControl);

    // change bc mapSearchedCenter
    geolocateControl.on('geolocate', (e: any) => {
        // bc it's every time the page loads, probably not this here.
        // let userLocation = new mapboxgl.LngLat(e.coords.longitude, e.coords.latitude);
        // mapVal.setCenter(userLocation);
        console.log(`CENTER ON GEOLOCATE CALLBACK ${getMap().getCenter()}`)
    }); // when 'turning on' geolocate finishes / page is loaded anew

    if (props.lat && props.lon) {
        let lonLatLike = new mapboxgl.LngLat(props.lon, props.lat)
        getMap().setCenter(lonLatLike)
        getNearestLocation(props.lat, props.lon).then((location) => {
            if(location) {
                addMapItem(location, getMap()) // this IS safe. addIfNotIn(...)
                selectMarker(location.id)
            }
        })
    }

    getMap().on('load', () => {
        geolocateControl.trigger() // Basically 'turn on geolocate'
        console.log(`CENTER ON LOAD ${getMap().getCenter()}`)
    });
    refreshMapItemsByCenter()
}

function updateMarkerColor(locationId: number) {
    let mapItem = mapItems.get(locationId)
    if (!mapItem) return // do not update if not found
    let { location, marker } = mapItem

    let fill_el = marker.getElement().querySelector('path')
    if (!fill_el) return

    let waiting_constant = 1.2
    // ratio for number waiting / c * court_count
    let waiting_ratio = location.value.number_waiting / (waiting_constant * location.value.court_count)

    // caps at 1
    waiting_ratio = waiting_ratio > 1 ? 1 : waiting_ratio

    // ratio of # of courts occupied
    let courts_occupied_ratio = location.value.courts_occupied / location.value.court_count

    // distribution of how much to take into account people waiting vs courts occupied
    let percent_full = 0.4 * courts_occupied_ratio + 0.6 * waiting_ratio
    let scalar = Math.floor(percent_full * 511)
    let r = (scalar < 255) ? scalar : 255
    let g = (scalar < 255) ? 255 : 511 - scalar
    let b = 0

    let darker_val = 0.95
    fill_el.setAttribute("fill", `rgb(${r * darker_val}, ${g * darker_val}, ${b * darker_val})`)
}


let locationsInterval: number | undefined
onMounted(() => {
    initMap()
    initGeoloc()
    locationsInterval = window.setInterval(refreshMapItems, 3000)
    document.querySelector('.mapboxgl-ctrl-bottom-right')?.remove()
    document.querySelector('.mapboxgl-ctrl-bottom-left')?.setAttribute('style', 'transform: scale(0.85);')
})

onUnmounted(() => {
    map.value?.remove()
    map.value = undefined
    if (locationsInterval) {
        window.clearInterval(locationsInterval)
    }
    locationsInterval = undefined
})

const selectedLocation = computed(() => {
    let v = currSelected.value ? mapItems.get(currSelected.value)?.location : undefined;
    return v;
});
</script>

<template>
    <div class="main-page">
        <CommonHeader />
        <div class="orientation">
            <div class="map-overlay-container">
                <button id="search-bt" @click="refreshMapItemsByCenter">Search This Area</button>
                <div ref="mapContainer" class="mapbox-container"></div>
            </div>
            <Transition name="popup-transition">
                <Popup class="popup" v-if="currSelected" :location="selectedLocation"
                    :on-submit-callback="updateMarkerColor" />
            </Transition>
        </div>
    </div>
</template>

<style scoped lang="scss">
@use '@/styles/abstracts' as *;
@use '@/styles/components';
$mobile-size: 800px;
* {
    display: flex;
}

.orientation {
    flex-direction: row-reverse;
    position: relative;
    flex-grow: 1;
    align-self: stretch;

    @include responsive($mobile-size) {
        flex-direction: column;
    }
}

$popup-width: 30%;
$time: 1s;
$transition: "popup-transition";

@include off-state($transition) {
    opacity: 0;
    flex-basis: 0;
}

 @include on-state($transition) {
    opacity: 1;
    flex-basis: $popup-width;
}

@include transition-state($transition) {
    transition: opacity $time ease, flex-basis $time ease; /* Smooth transition for width and opacity */
}

.main-page {
    @extend %flex-col-center;
    height: 100vh;
    overflow: hidden;
}

.popup {
    flex-grow: 1;
    flex-basis: $popup-width;
}

.map-overlay-container {
    position: relative;
    flex-grow: 1;
    flex-basis: 100%;
}

.mapbox-container {
    height: 100%;
    flex-grow: 1;

    @include responsive($mobile-size) {
        width: 100%;
        flex-grow: 1;
    }
}

#search-bt {
    position: absolute;
    bottom: 20px; // Adjust as needed for correct placement from the bottom
    left: 50%;
    transform: translateX(-50%); // Center horizontally
    z-index: 1; // Ensure the button is above the map layers
    // Rest of your button styling...
    background-color: white;
    color: #333;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 6px 12px;
    cursor: pointer;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);

    &:hover {
        background-color: #f8f8f8;
    }
}

// Must use :deep directive as components are loaded dynamically by mapboxgl
:deep(.mapboxgl-popup-content) {
    width: max-content;
}

:deep(path) {
    transition: stroke 0.3s ease, stroke-width 0.3s ease, stroke-linejoin 0.3s ease
}

:deep(.selected path) {
    stroke: #007bff;
    stroke-width: 2.25px;
    stroke-linejoin: round;
}

:deep(svg) {
    cursor: pointer;
    overflow: visible;
    transform-origin: 50% 100%;
    transition: transform 0.3s ease, filter 0.3s ease;
}

:deep(svg:hover) {
    transform: scale(1.1);
    filter: brightness(1.01);
}
</style>