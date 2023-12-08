<script setup lang="ts">
import { ref, onMounted, onUnmounted, type Ref } from 'vue'
import mapboxgl from "mapbox-gl";

interface Location {
  name: string;
  latitude: number;
  longitude: number;
  court_count: number;
  courts_occupied: number;
  number_waiting: number;
  estimated_wait_time: number;
}

const mapContainer = ref();
const infoSection = ref("Select a location for more info");

// Todo: improve token handling
mapboxgl.accessToken = 'pk.eyJ1Ijoic3VudHp1Y2Fwc3RvbmUiLCJhIjoiY2xwOHl6MGZiMWQwcjJ2bzNpdTh3ZXZ5diJ9.2OxP9v87qKxpFmL7FFrD-g';
const map: Ref<mapboxgl.Map | undefined> = ref();

// Get users geolocation if permitted
function initGeoloc(mapVal: mapboxgl.Map) {
  const geolocateControl = new mapboxgl.GeolocateControl({
    fitBoundsOptions: { maxZoom: 11 },
    positionOptions: { enableHighAccuracy: true },
    trackUserLocation: true,
  });

  mapVal.addControl(geolocateControl);
  mapVal.on('load', () => geolocateControl.trigger());
}

// Add markers to map
function addMarkers(mapVal: mapboxgl.Map) {
  // Todo: get locations from backend
  const locations: Location[] = [
    {
      name: "Hogan Park",
      latitude: 40.874056,
      longitude: -111.901012,
      court_count: 6,
      courts_occupied: 3,
      number_waiting: 0,
      estimated_wait_time: 0
    }
  ];

  locations.forEach(loc => {
    const marker = new mapboxgl.Marker()
      .setLngLat([loc.longitude, loc.latitude])
      .addTo(mapVal);
    // Add an event listener to each marker
    marker.getElement().addEventListener('click', () => {
      updateInfoSection(loc);
    });
  });
}

// Update the info section with location data
function updateInfoSection(loc: Location) {
  infoSection.value = `
    ${loc.name} <br>
    Number of Courts: ${loc.court_count} <br>
    Courts Occupied: ${loc.courts_occupied} <br>
    Number Waiting: ${loc.number_waiting} <br>
    Estimated Wait Time: ${loc.estimated_wait_time} minutes
  `;
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
    <div class="info-section" v-html="infoSection"></div>
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
  min-height: 40em;
}

.info-section {
  margin-top: 1em;
  padding: 1em;
  border: 3px solid black;
  background-color: lightsteelblue;
}

.info-section::first-line {
  font-weight: bold;
  font-size: large;
}
</style>
