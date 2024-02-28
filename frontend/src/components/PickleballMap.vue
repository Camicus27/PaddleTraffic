<script setup lang="ts">
import { ref, onMounted, onUnmounted, type Ref } from 'vue'
import mapboxgl, { LngLat } from "mapbox-gl"
import axios from 'axios'

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
const props = defineProps(['lat', 'lon']) // for the URL ?lat=:number&lon=:number
const submitDataDisabled = ref<boolean>(false)

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

  mapSearchedCenter = mapVal.getCenter()
  mapVal.addControl(geolocateControl)
  mapVal.on('load', () => geolocateControl.trigger())
}


/**
 * GET latest info about markers at center of map
 */
function addMarkersQuery(mapVal: mapboxgl.Map) { // => addMarkersQuery ?
  // TODO why not use mapVal.getCenter()??
  let lat = mapSearchedCenter?.lat
  let lng = mapSearchedCenter?.lng
  axios.get(`${URL}/locations/bounds?lat=${lat}&lon=${lng}`)
    .then((response) => {
      allLocations.value = response.data.locations
      allLocations.value.forEach(loc => {
        const marker = new mapboxgl.Marker()
          .setLngLat([loc.longitude, loc.latitude])
          .addTo(mapVal)


        mapMarkers.value[loc.id] = marker

        // affects how much to take into account the court_count, greater means more tolerance, less means less tolerance
        updateMarkerColor(loc)

        // Add an event listener to each marker
        marker.getElement().addEventListener('click', () => {
          markerCallback(loc.id)
        })
      })
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
  addMarkersQuery(map.value!)
}

function updateMarkerColor(loc: Location) {
  let fill_el = mapMarkers.value[loc.id]?.getElement().querySelector('path')
  if (fill_el === undefined) return

  let waiting_constant = 1.2
  // ratio for number waiting / c * court_count
  let waiting_ratio = loc.number_waiting / (waiting_constant * loc.court_count)

  // caps at 1
  waiting_ratio = waiting_ratio > 1 ? 1 : waiting_ratio // ooga booga

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
function markerCallback(locId: number) {
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

const locForm = ref({
  courts_occupied: 0,
  number_waiting: 0
})

function submitForm() {
  submitDataDisabled.value = true // disable THE BUTTON
  setTimeout(() => {
    submitDataDisabled.value = false
  }, 3000)

  axios.post(`${URL}/locations/${currSelection.value?.id}/report/`, { report: locForm.value })
    .then(response => {
      // Handle the response here. For example, logging the new location ID.
      console.log('New event ID:', response.data)
      //   axios.get(`${URL}/locations/`) // todo just GET current location to get updated date
      //     .then((response) => { 
      //       allLocations.value = response.data.locations
      //     })
      //     .catch((error) => console.log(error))
      currSelection.value = response.data.location
      updateMarkerColor(currSelection.value!!)
      // })
    })
    .catch(error => {
      // Handle errors here
      console.error('Error:', error)
    })
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

function updateOnLonLatURL() {
  if (!props?.lat || !props?.lon) return

  axios.get(`${URL}/location/latlon?lat=${props.lat}&lon=${props.lon}`)
    .then((response) => {
      currSelection.value = response.data.location
    })
    .catch((error) => console.log(error))
}

let interval: number | undefined
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
  addMarkersQuery(map.value)
  updateOnLonLatURL()
  interval = setInterval(updateLocationsInterval, 3000)
})

onUnmounted(() => {
  map.value?.remove()
  map.value = undefined
  if (interval) {
    clearInterval(interval)
  }
  interval = undefined
})

function pluralize(word: string, num: number): string {
  if (num != 1) {
    word += "s"
  }
  return word
}

function formatTime(timeNum: number): string {
  let timeNumArr = String(timeNum).split(":")

  let formattedString = ""
  let hours = timeNumArr[0].startsWith("0") ? timeNumArr[0].substring(1) : timeNumArr[0]
  let minutes = timeNumArr[1].startsWith("0") ? timeNumArr[1].substring(1) : timeNumArr[1]
  
  formattedString += hours + " "
  formattedString += pluralize("Hour", Number(timeNumArr[0])) + " "
  formattedString += minutes + " "
  formattedString += pluralize("Minute", Number(timeNumArr[1]))
  return formattedString
}
</script>

<template>
  <div class="map-page">
    <div ref="mapContainer" class="mapbox-container">
      <button id="search-bt" @click="updateMarkersOnSearch">Search This Area</button>
    </div>

    <Transition name="info-transition">
      <div class="info-section" v-if="currSelection">
        <div class="info">
          <h3>{{ currSelection.name }}</h3>
          <sub>Courts: {{ currSelection.court_count }}</sub>
          <p>Estimated Courts Occupied: {{ currSelection.courts_occupied }}</p>
          <p>Estimated Groups Waiting: {{ currSelection.number_waiting }}</p>
          <p>Estimated Wait Time: {{ formatTime(currSelection.estimated_wait_time) }}</p>
        </div>
        <form @submit.prevent="submitForm">
          <label for="courtsOccupied">Courts Occupied:</label><br>
          <input type="number" id="courtsOccupied" name="courtsOccupied" min="0" :max="currSelection.court_count"
          v-model="locForm.courts_occupied" required><br><br>
          <label for="numberWaiting">Number Waiting:</label><br>
          <input type="number" id="numberWaiting" name="numberWaiting" min="0"
          :max="(locForm.courts_occupied < currSelection.court_count) ? 0 : 10" v-model="locForm.number_waiting"
          required><br><br>
          <button :disabled="submitDataDisabled">
            Update Status
          </button>
        </form>
      </div>
    </Transition>

    </div>
</template>

<style>
.info-transition-enter-from, .info-transition-leave-to {
  max-height: 0;
  opacity: 0;
  overflow: hidden;
}

.info-transition-enter-to, .info-transition-leave-from {
  max-height: 500px;
  opacity: 1;
}

.info-transition-enter-active, .info-transition-leave-active {
  transition: max-height 0.5s ease-in-out, opacity 0.5s ease-in-out;
  overflow: hidden;
}

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

.map-page {
  flex-grow: 1;
}

.mapbox-container {
  min-height: 45em;
  }

.info-section {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
  padding: 1rem;
  border: 3px solid black;
  background-color: #d0d4ca;
}

.info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 55%;
  font-size: larger;
}

form {
  width: 30%;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

svg {
  cursor: pointer;
  overflow: visible;
  transform-origin: 50% 100%;
  transition: transform 0.3s ease, filter 0.3s ease;

  &:hover {
    /* animation: spin 1.5s ease-in-out infinite; */
    transform: scale(1.1);
    filter: brightness(1.01);
  }
}

path {
  transition: stroke 0.3s ease, stroke-width 0.3s ease, stroke-linejoin 0.3s ease
}

.selected path {
  stroke: #007bff;
  stroke-width: 2.75px;
  stroke-linejoin: round;
}

button:disabled {
    border: 1px solid #999999;
    background-color: #cccccc;
    color: #666666;
}
</style>