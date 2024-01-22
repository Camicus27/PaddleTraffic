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

const mapContainer = ref();
const currSelection = ref<Location | undefined>();
const allLocations: Ref<Location[]> = ref([])

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
        // Add an event listener to each marker
        marker.getElement().addEventListener('click', () => {
          updateInfoSection(loc.id);
        });
      });
    })
    .catch((error) => console.log(error))
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
  axios.post(`${URL}/locations/${currSelection.value?.id}/report/`, { report: locForm.value })
    .then(response => {
      // Handle the response here. For example, logging the new location ID.
      console.log('New event ID:', response.data);
      axios.get(`${URL}/locations/`)
        .then((response) => {
          allLocations.value = response.data.locations
        })
        .catch((error) => console.log(error))
        currSelection.value = response.data.location
    })
    .catch(error => {
      // Handle errors here
      console.error('Error:', error);
    });
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
          <input type="number" id="courtsOccupied" name="courtsOccupied" min="0" v-model="locForm.courts_occupied"><br><br>
          <label for="numberWaiting">Number Waiting:</label><br>
          <input type="number" id="numberWaiting" name="numberWaiting" min="0" v-model="locForm.number_waiting"><br><br>
          <input type="submit" value="Update Status">
        </form>
      </div>
    </div>
    <div class="info-section" v-else>Select a court for more information</div>
  </div>
</template>
