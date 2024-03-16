<script setup lang="ts">
import { ref, onMounted, onUnmounted, type Ref, getCurrentInstance, createApp } from 'vue'
import mapboxgl, { LngLat } from "mapbox-gl"
import axios from 'axios'
import { useRoute } from "vue-router"
import Popup from '@/components/Map/Popup.vue'
import CommonHeader from '@/components/CommonHeader.vue'

interface Location {
    id: number
    name: string
    latitude: number
    longitude: number
    court_count: number
    courts_occupied: number
    number_waiting: number
    estimated_wait_time: number
}

// TODO: prevent desync
// interface MapItem {
//   location: Location
//   marker: mapboxgl.Marker
// }

// const mapItems: Ref<MapItem[]> = ref([])

const mapContainer = ref<HTMLElement | undefined>() // reference to the <div> mapContainer
const currSelection = ref<Location | undefined>() // can be none

const allLocations: Ref<Location[]> = ref([]) // all locations currently on the map, coincides with mapMarkers
const mapMarkers = ref<{ [key: number]: mapboxgl.Marker }>({}) // dictionary of locationID -> mapMarkers, right now coincides with allLocations
// for the URL ?lat=:number&lon=:number
const props = {
    lat: Number(useRoute().query.lat),
    lon: Number(useRoute().query.lon)
}

// => let mapCenterAtTimeOfSearchArea: LngLat
let mapSearchedCenter: LngLat // TODO why are we using this instead of just like, map.getCenter() ?
// I think before we were storing the old center so when we do queries it'll like be where the old center was, that's not really working so, maybe we get rid of it and add an endpoint 💀

// TODO: improve token handling
mapboxgl.accessToken = 'pk.eyJ1Ijoic3VudHp1Y2Fwc3RvbmUiLCJhIjoiY2xwOHl6MGZiMWQwcjJ2bzNpdTh3ZXZ5diJ9.2OxP9v87qKxpFmL7FFrD-g'
const map: Ref<mapboxgl.Map | undefined> = ref()

let URL: string
// This is the collection of environment variables.
const env = import.meta.env
if (env.MODE === 'production')
    URL = env.VITE_PROD_URL
else
    URL = env.VITE_DEV_URL

/**
 * Initialized Mapbox with settings, and loading things
 * Gets users geolocation if permitted
 */
function initGeoloc(mapVal: mapboxgl.Map) {
    const geolocateControl = new mapboxgl.GeolocateControl({
        fitBoundsOptions: { maxZoom: 11 },
        positionOptions: { enableHighAccuracy: true },
        trackUserLocation: true,
        showAccuracyCircle: false
    })

    if (props?.lat && props?.lon) {
        let lonLatLike = new mapboxgl.LngLat(props.lon, props.lat)
        map.value?.setCenter(lonLatLike)
    }

    mapSearchedCenter = mapVal.getCenter()
    mapVal.addControl(geolocateControl)
    mapVal.on('load', () => geolocateControl.trigger())
}


/**
 * GET latest info about markers at center of map
 */
function addMarkersQuery(mapVal: mapboxgl.Map, selectLatLonProps: boolean = false) {
    // TODO why not use mapVal.getCenter()??
    let lat = mapSearchedCenter?.lat
    let lng = mapSearchedCenter?.lng
    axios.get(`${URL}/locations/bounds?lat=${lat}&lon=${lng}`)
        .then((response) => {
            allLocations.value = response.data.locations
            allLocations.value.forEach(loc => {
                const popupComponent = createApp(Popup, { location: loc, onSubmitCallback: updateMarkerColor, currSelection: currSelection })

                // Mount the component and render it to HTML
                const popupHtml = document.createElement('div')
                popupComponent.mount(popupHtml);

                const popup = new mapboxgl.Popup({ closeButton: false, offset: 25 }).setDOMContent(
                    popupHtml
                )
                const marker = new mapboxgl.Marker()
                    .setLngLat([loc.longitude, loc.latitude])
                    .setPopup(popup)
                    .addTo(mapVal)

                mapMarkers.value[loc.id] = marker

                // affects how much to take into account the court_count, greater means more tolerance, less means less tolerance
                updateMarkerColor(loc)

                // Add an event listener to each marker
                marker.getElement().addEventListener('click', () => {
                    selectMarker(loc.id)
                })
            })
            if (selectLatLonProps)
                selectLatLonMarker()
        })
        .catch((error) => console.log(error))
}

function updateMarkersOnSearch() {
    Object.entries(mapMarkers.value).forEach(marker => {
        marker[1].remove()
    })
    mapMarkers.value = []
    allLocations.value = []
    mapSearchedCenter = map.value!.getCenter()
    currSelection.value = undefined
    addMarkersQuery(map.value!)
}

function updateMarkerColor(loc: Location) {
    let fill_el = mapMarkers.value[loc.id]?.getElement().querySelector('path')
    if (fill_el === undefined) return

    let waiting_constant = 1.2
    // ratio for number waiting / c * court_count
    let waiting_ratio = loc.number_waiting / (waiting_constant * loc.court_count)

    // caps at 1
    waiting_ratio = waiting_ratio > 1 ? 1 : waiting_ratio

    // ratio of # of courts occupied
    let courts_occupied_ratio = loc.courts_occupied / loc.court_count

    // distribution of how much to take into account people waiting vs courts occupied
    let percent_full = 0.4 * courts_occupied_ratio + 0.6 * waiting_ratio
    let scalar = Math.floor(percent_full * 511)
    let r = (scalar < 255) ? scalar : 255
    let g = (scalar < 255) ? 255 : 511 - scalar
    let b = 0

    let darker_val = 0.95
    fill_el?.setAttribute("fill", `rgb(${r * darker_val}, ${g * darker_val}, ${b * darker_val})`)
}

// Update the info section with location data
function selectMarker(locId: number) {
    let selectedClassName = 'selected'
    if (currSelection.value) { // if a marker is selected
        let old_marker = mapMarkers.value[currSelection.value.id].getElement()
        old_marker.classList.remove(selectedClassName)
        if (currSelection.value.id == locId) { // and it's the same one
            currSelection.value = undefined
            return
        }
    }

    // set the new one
    currSelection.value = allLocations.value.find(location => location.id === locId)
    let fill_el = mapMarkers.value[locId].getElement()
    fill_el.classList.add(selectedClassName)
}

/**
 * Makes a request for the most recent data about the locations
 * Each of those locations are updated in the Map,
 * and the current selected location attributes are selected
 */
function updateLocationsInterval() {
    let LngLat = mapSearchedCenter // TODO change to be based on the list of locations that you have ... not the center of origin
    let lat = LngLat?.lat
    let lng = LngLat?.lng
    if (!lat || !lng) return

    axios.get(`${URL}/locations/bounds?lat=${lat}&lon=${lng}`)
        .then((response) => {
            allLocations.value = response.data.locations
            allLocations.value.forEach(loc => {
                updateMarkerColor(loc)
                if (loc.id === currSelection.value?.id) {
                    currSelection.value = loc
                }
            })
        })
        .catch((error) => console.log(error))
}

function selectLatLonMarker() {
    if (!props?.lat || !props?.lon) return

    axios.get(`${URL}/location/latlon?lat=${props.lat}&lon=${props.lon}`)
        .then((response) => {
            selectMarker(response.data.location.id)
        })
        .catch((error) => console.log(error))
}

let locationsInterval: number | undefined
onMounted(() => {
    if (!mapContainer?.value)
        return
    map.value = new mapboxgl.Map({
        container: mapContainer.value,
        style: 'mapbox://styles/mapbox/streets-v12',
        center: [-111.876183, 40.758701], // Default to SLC
        zoom: 11
    })
    initGeoloc(map.value)
    addMarkersQuery(map.value, true)
    locationsInterval = window.setInterval(updateLocationsInterval, 3000)
    document.querySelector('.mapboxgl-ctrl-bottom-right')?.remove()
    document.querySelector('.mapboxgl-ctrl-bottom-left')?.setAttribute('style', 'transform: scale(0.85);')
})

onUnmounted(() => {
    map.value?.remove()
    map.value = undefined
    if (locationsInterval) {
        clearInterval(locationsInterval)
    }
    locationsInterval = undefined
})
</script>

<template>
    <CommonHeader />
    <div ref="mapContainer" class="mapbox-container">
        <button id="search-bt" @click="updateMarkersOnSearch">Search This Area</button>
    </div>
    <!-- Dynamic adding to map page popup thingy ... -->
</template>

<style scoped>
h3 {
    margin-bottom: 0;
}

sub {
    margin-bottom: 1rem;
}

p {
    margin: 0.5rem 0;
}

#search-bt {
    background-color: white;
    border-color: lightgrey;
    color: lightskyblue;
    z-index: 1;
    position: relative;
    margin-left: 1rem;
}

.mapboxgl-popup-content {
    max-width: max-content;
}

.mapbox-container {
    min-height: 100vh;
    min-width: 100vw;
    height: 100vh;
    width: 100vw;
}

form {
    width: 30%;
}

/* Map Marker Styling */
:deep(.mapboxgl-popup-content) {
    width: max-content;
}

:deep(path) {
    transition: stroke 0.3s ease, stroke-width 0.3s ease, stroke-linejoin 0.3s ease
}

:deep(.selected path) {
    stroke: #007bff;
    stroke-width: 2.75px;
    stroke-linejoin: round;
}

:deep(svg) {
    cursor: pointer;
    overflow: visible;
    transform-origin: 50% 100%;
    transition: transform 0.3s ease, filter 0.3s ease;

    :deep(&:hover) {
        transform: scale(1.1);
        filter: brightness(1.01);
    }
}
</style>