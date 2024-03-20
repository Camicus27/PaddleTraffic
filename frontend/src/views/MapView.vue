<script setup lang="ts">
import { ref, onMounted, onUnmounted, type Ref, getCurrentInstance, createApp } from 'vue'
import mapboxgl, { LngLat } from "mapbox-gl"
import axios from 'axios'
import { useRoute } from "vue-router"
import Popup from '@/components/Map/Popup.vue'
import CommonHeader from '@/components/CommonHeader.vue'
import {getAllLocations, getLocationId, } from '@/api/functions'

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


// -------------------------------- REFACTOR ZONE -------------------------------------------- //

interface MapItem {
    location: Location
    marker: mapboxgl.Marker
}

// [Location.id] : MapItem
const mapItems: Ref<Map<number, MapItem>> = ref(new Map())
const currSelected = ref<number | undefined>()

function addMapItem(location: Location, map: mapboxgl.Map) {
    if (mapItems.value.has(location.id)) return


    // Create Popup vue app
    const popupComponent = createApp(Popup,
        {
            location: location,
            onSubmitCallback: updateMarkerColor,
            currSelection: currSelection
        })

    // Mount the component and render it to HTML
    const popupHtml = document.createElement('div')
    popupComponent.mount(popupHtml);
    const popup = new mapboxgl.Popup({ closeButton: false, offset: 25 }).setDOMContent(
        popupHtml
    )

    // Create Map Marker
    let marker: mapboxgl.Marker;
    marker = new mapboxgl.Marker()
        .setLngLat([location.longitude, location.latitude])
        .setPopup(popup)
        .addTo(map)

    // add this to map items
    const newMapItem: MapItem = {
        location: location,
        marker: marker
    }
    mapItems.value.set(location.id, newMapItem)

    // update color!
    updateMarkerColor(location)

    // TODO change to be for event listener on like the Popup instead of just on click
    marker.getElement().addEventListener('click', () => {
        selectMarkerREFACTORED(location.id)
    })

}

// Update the info section with location data
function selectMarkerREFACTORED(locId: number) {
    if (!mapItems.value.has(locId)) return

    const selectedClassName = 'selected'
    if (currSelected.value) { // if a marker is selected
        let mapItem = mapItems.value.get(currSelected.value)
        let old_marker = mapItem!.marker.getElement()
        old_marker.classList.remove(selectedClassName)
        if (currSelected.value == locId) { // and it's the same one
            currSelected.value = undefined // then none is selected in state
            return // return
        }
    }

    // otherwise set the new one
    currSelected.value = locId
    let fill_el = mapItems.value.get(locId)!.marker.getElement()
    fill_el.classList.add(selectedClassName)
}

function removeMapItem(locId: number) {
    let mapItem = mapItems.value.get(locId)
    if (!mapItem) return
    // remove it from the map
    mapItem.marker.remove()
    // from mapItems
    mapItems.value.delete(locId)
}

// -------------------------------- REFACTOR ZONE -------------------------------------------- //

const mapContainer = ref<HTMLElement | undefined>() // reference to the <div> mapContainer

// TODO DELETE
const currSelection = ref<Location | undefined>() // can be none

// TODO DELETE
const allLocations: Ref<Location[]> = ref([]) // all locations currently on the map, coincides with mapMarkers

// TODO DELETE
const mapMarkers = ref<{ [key: number]: mapboxgl.Marker }>({}) // dictionary of locationID -> mapMarkers, right now coincides with allLocations
// for the URL ?lat=:number&lon=:number
const props = {
    lat: Number(useRoute().query.lat),
    lon: Number(useRoute().query.lon)
}


// TODO DELETE
let mapSearchedCenter: LngLat // TODO why are we using this instead of just like, map.getCenter() ?
// I think before we were storing the old center so when we do queries it'll like be where the old center was, that's not really working so, maybe we get rid of it and add an endpoint 💀

// TODO: improve token handling
mapboxgl.accessToken = 'pk.eyJ1Ijoic3VudHp1Y2Fwc3RvbmUiLCJhIjoiY2xwOHl6MGZiMWQwcjJ2bzNpdTh3ZXZ5diJ9.2OxP9v87qKxpFmL7FFrD-g'
const map: Ref<mapboxgl.Map | undefined> = ref() // TODO can we make this just like not undefined? or something

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

    // TODO chagney
    if (props?.lat && props?.lon) {
        let lonLatLike = new mapboxgl.LngLat(props.lon, props.lat)
        map.value?.setCenter(lonLatLike)
        mapSearchedCenter = lonLatLike;
    }
    else {
        mapSearchedCenter = mapVal.getCenter()
    }

    mapVal.addControl(geolocateControl);

    // change bc mapSearchedCenter
    geolocateControl.on('geolocate', (e: any) => {
        let userLocation = new mapboxgl.LngLat(e.coords.longitude, e.coords.latitude);
        mapVal.setCenter(userLocation);
        mapSearchedCenter = userLocation;
        addMarkersQuery(mapVal);
    });

    mapVal.on('load', () => {
        geolocateControl.trigger();
    });
}


/**
 * GET latest info about markers at center of map
 */
function addMarkersQuery(mapVal: mapboxgl.Map, selectLatLonProps: boolean = false) {
    // TODO lat / lng will just be center of map probs, or we pass it in idk
    let lat = mapSearchedCenter?.lat
    let lng = mapSearchedCenter?.lng
    axios.get(`${URL}/locations/bounds?lat=${lat}&lon=${lng}`)
        .then((response) => {
            allLocations.value = response.data.locations
            allLocations.value.forEach(loc => {
                // TODO use our 'Class/Library/GigaChadCode' instead of using any of the code here basically 💀💀💀 
                const popupComponent = createApp(Popup, { location: loc, onSubmitCallback: updateMarkerColor, currSelection: currSelection })

                // Mount the component and render it to HTML
                const popupHtml = document.createElement('div')
                popupComponent.mount(popupHtml);

                const popup = new mapboxgl.Popup({ closeButton: false, offset: 25 }).setDOMContent(
                    popupHtml
                )

                let marker: mapboxgl.Marker;
                if (loc.id in mapMarkers.value) {
                    marker = mapMarkers.value[loc.id]
                }
                else {
                    marker = new mapboxgl.Marker()
                        .setLngLat([loc.longitude, loc.latitude])
                        .addTo(mapVal)
                }

                marker.setPopup(popup)

                mapMarkers.value[loc.id] = marker

                // affects how much to take into account the court_count, greater means more tolerance, less means less tolerance
                updateMarkerColor(loc)

                // Add an event listener to each marker
                marker.getElement().addEventListener('click', () => {
                    selectMarker(loc.id)
                })
            })
            if (selectLatLonProps) // TODO this is for QR code Should only happen on loading the URL. Ideally extract two functions for loading and QR and have common code btwn where possible
                selectLatLonMarker()
        })
        .catch((error) => console.log(error))
}

// TODO change a bit because we are using mapItems now
function refreshMapItems() {
    // mapItems.removeAll()
    // mapItems.addAll(API.getLocations(lat, lon))
    Object.entries(mapMarkers.value).forEach(marker => {
        marker[1].remove()
    })
    mapMarkers.value = []
    allLocations.value = []
    mapSearchedCenter = map.value!.getCenter()
    currSelection.value = undefined
    addMarkersQuery(map.value!)
}

function updateMarkerColor(loc: Location) { // TODO change to just take id
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
function updateLocationsInterval() { // TODO implement API for this in backend and frontend /locations/[id1, id2, ... id_n]
    let LngLat = mapSearchedCenter // TODO change to mapItems lmao not cringey af 💀💀💀💀💀💀💀💀bozo
    let lat = LngLat?.lat
    let lng = LngLat?.lng
    if (!lat || !lng) return
    /**
     * {
     * "yuh" : []
     * }
     */

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
// TODO remove this to be an API call
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
    if (!mapContainer?.value) throw new Error("OH MY FREAKING GOSH WHAT THE FRICK 💀💀💀💀💀💀💀💀")
    map.value = new mapboxgl.Map({
        container: mapContainer.value,
        style: 'mapbox://styles/mapbox/streets-v12',
        center: [-111.876183, 40.758701], // Default to SLC 
        zoom: 11
    })
    initGeoloc(map.value)
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
    <div class="main-page">
        <CommonHeader />
        <!-- <button id="search-bt" @click="updateMarkersOnSearch">Search This Area</button> -->
        <div ref="mapContainer" class="mapbox-container">
        </div>
    </div>
    <!-- Dynamic adding to map page popup thingy ... -->
</template>

<style scoped lang="scss">
@use '../styles/abstracts';
@use '../styles/components';

.main-page {
    @extend %flex-col-center;
    height: 100vh;
}

.mapbox-container {
    display: flex;
    width: 100vw;
    flex: 1 1 auto;
}

#search-bt {
    @extend .dark-solid-button;
    border: none;
    background-color: white;
    color: lightskyblue;
    z-index: 1;
    position: relative;
    margin-left: 20px;
    margin-top: 40px;
    height: 2rem;
    width: 4rem;
    height: 2rem;

    &:hover {
        color: white;
        background-color: lightblue;
    }

    &:active {
        background-color: darken($color: lightblue, $amount: 25);
        transition: background-color 0.1s;
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