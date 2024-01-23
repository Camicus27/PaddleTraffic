<script setup lang="ts">
import { ref, onMounted, onUnmounted, type Ref } from 'vue'
import mapboxgl from "mapbox-gl";
import axios from 'axios'

interface Location {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
  court_count: number;
  courts_occupied: number;
  number_waiting: number;
  estimated_wait_time: number;
}

// interface MapMarker {
//   id: number,
//   marker: mapboxgl.Marker
// }

const mapContainer = ref();
const currSelection = ref<Location | undefined>();
const allLocations: Ref<Location[]> = ref([])
const mapMarkers = ref<{ [key: number]: mapboxgl.Marker }>({});

// Todo: improve token handling
mapboxgl.accessToken = 'pk.eyJ1Ijoic3VudHp1Y2Fwc3RvbmUiLCJhIjoiY2xwOHl6MGZiMWQwcjJ2bzNpdTh3ZXZ5diJ9.2OxP9v87qKxpFmL7FFrD-g';
const map: Ref<mapboxgl.Map | undefined> = ref();

let URL: string
// This is the collection of environment variables.
const env = import.meta.env
if (env.MODE === 'production')
  URL = env.VITE_PROD_URL
else
  URL = env.VITE_DEV_URL

// Get users geolocation if permitted
function initGeoloc(mapVal: mapboxgl.Map) {
  const geolocateControl = new mapboxgl.GeolocateControl({
    fitBoundsOptions: { maxZoom: 11 },
    positionOptions: { enableHighAccuracy: true },
    trackUserLocation: true,
    showAccuracyCircle: false
  });

  mapVal.addControl(geolocateControl);
  mapVal.on('load', () => geolocateControl.trigger());
}

// Add markers to map
function addMarkers(mapVal: mapboxgl.Map) {
  axios.get(`${URL}/locations/`)
    .then((response) => {
      allLocations.value = response.data.locations
      allLocations.value.forEach(loc => {
        const marker = new mapboxgl.Marker()
          .setLngLat([loc.longitude, loc.latitude])
          .addTo(mapVal);

        mapMarkers.value[loc.id] = marker

        let fill_el = marker.getElement().querySelector('path')
        // affects how much to take into account the court_count, greater means more tolerance, less means less tolerance
        updateMarkerColor(loc, fill_el);

        // Add an event listener to each marker
        marker.getElement().addEventListener('click', () => {
          updateInfoSection(loc.id);
        });
      });
    })
    .catch((error) => console.log(error))
}

function updateMarkerColor(loc: Location, fill_el: SVGPathElement | null) {
  let waiting_constant = 1.2;
  // ratio for number waiting / c * court_count
  let waiting_ratio = loc.number_waiting / (waiting_constant * loc.court_count);

  // caps at 1
  waiting_ratio = waiting_ratio > 1 ? 1 : waiting_ratio; // ooga booga

  // ratio of # of courts occupied
  let courts_occupied_ratio = loc.courts_occupied / loc.court_count;

  // distribution of how much to take into account people waiting vs courts occupied
  let percent_full = 0.4 * courts_occupied_ratio + 0.6 * waiting_ratio;
  let scalar = Math.floor(percent_full * 511);
  let r = (scalar < 255) ? scalar : 255;
  let g = (scalar < 255) ? 255 : 511 - scalar;
  let b = 0;

  let darker_val = 0.95;
  fill_el?.setAttribute("fill", `rgb(${r * darker_val}, ${g * darker_val}, ${b * darker_val})`);
}

// Update the info section with location data
function updateInfoSection(locId: number) {
  currSelection.value = allLocations.value.find(location => location.id === locId);
}

const locForm = ref({
  courts_occupied: 0,
  number_waiting: 0
})

function submitForm() {
  let c_o = locForm.value.courts_occupied
  // if(locForm.value.number_waiting < 30 && c_o <= (currSelection.value?.court_count ?? 0) && 0 <= c_o) {
  axios.post(`${URL}/locations/${currSelection.value?.id}/report/`, { report: locForm.value })
    .then(response => {
      // Handle the response here. For example, logging the new location ID.
      console.log('New event ID:', response.data);
      axios.get(`${URL}/locations/`)
        .then((response) => { // todo update just current location?
          allLocations.value = response.data.locations
        })
        .catch((error) => console.log(error))
      currSelection.value = response.data.location
      let svg_element = mapMarkers.value[currSelection.value!!.id].getElement().querySelector('path')
      updateMarkerColor(currSelection.value!!, svg_element)
    })
    .catch(error => {
      // Handle errors here
      console.error('Error:', error);
    });
  // } else {

  // }
}

onMounted(() => {
  map.value = new mapboxgl.Map({
    container: mapContainer.value,
    style: 'mapbox://styles/mapbox/streets-v12',
    center: [-111.876183, 40.758701], // Default to SLC
    zoom: 11
  });

  if (map.value) {
    initGeoloc(map.value);
    addMarkers(map.value);
  }
})

onUnmounted(() => {
  map.value?.remove();
  map.value = undefined;
})
</script>

<template>
  <div class="container">
    <div ref="mapContainer" class="map-container"></div>
    <div class="info-section flex-row" v-if="currSelection">
      <div class="info padding-x">
        <h3>{{ currSelection.name }}</h3>
        <p>Number of Courts: {{ currSelection.court_count }}</p>
        <p>Courts Occupied: {{ currSelection.courts_occupied }}</p>
        <p>Number Waiting: {{ currSelection.number_waiting }}</p>
        <p>Estimated Wait Time: {{ currSelection.estimated_wait_time }}</p>
      </div>
      <div class="padding-x">
        <form @submit.prevent="submitForm">
          <label for="courtsOccupied">Courts Occupied:</label><br>
          <input type="number" id="courtsOccupied" name="courtsOccupied" min="0" :max="currSelection.court_count"
            v-model="locForm.courts_occupied" required><br><br>
          <label for="numberWaiting">Number Waiting:</label><br>
          <input type="number" id="numberWaiting" name="numberWaiting" min="0" max="10" v-model="locForm.number_waiting"
            required><br><br>
          <input type="submit" value="Update Status">
        </form>
      </div>
    </div>
    <div class="info-section" v-else>Select a court for more information</div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  padding: 1em;
  width: 100%;
}

.map-container {
  min-height: 45em;
}

.info-section {
  margin-top: 1em;
  padding: 1em;
  border: 3px solid black;
  background-color: #d0d4ca;
}

.flex-row {
  display: flex;
  justify-content: space-between;
}

.info {
  display: flex;
  flex-direction: column;
  font-size: larger;
  justify-content: center;
}

.info>p {
  margin-top: 0.25em;
}

.padding-x {
  padding-left: 1em;
  padding-right: 1em;
}

form {
  background-color: #b2bda2;
  padding: 10px;
  border: 1px solid black;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

label {
  color: #555;
  font-size: 14px;
  font-weight: bold;
  display: block;
}

input[type="number"] {
  width: 100%;
  padding: 3px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

input[type="submit"] {
  width: 100%;
  background-color: #849b62;
  color: white;
  padding: 3px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

input[type="submit"]:hover {
  background-color: #69794f;
}
</style>
