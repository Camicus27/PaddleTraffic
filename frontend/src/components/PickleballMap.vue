<script setup lang="ts">
import { ref, onMounted, onUnmounted, type Ref } from 'vue'
import mapboxgl from "mapbox-gl";

const mapContainer = ref();

// Will improve token handling
mapboxgl.accessToken = 'pk.eyJ1Ijoic3VudHp1Y2Fwc3RvbmUiLCJhIjoiY2xwOHl6MGZiMWQwcjJ2bzNpdTh3ZXZ5diJ9.2OxP9v87qKxpFmL7FFrD-g';
const map: Ref<mapboxgl.Map | undefined> = ref();

function initGeoloc(mapInstance: mapboxgl.Map) {
  const geolocateControl = new mapboxgl.GeolocateControl({
    fitBoundsOptions: { maxZoom: 11 },
    positionOptions: { enableHighAccuracy: true },
    trackUserLocation: true,
  });

  mapInstance.addControl(geolocateControl);
  mapInstance.on('load', () => geolocateControl.trigger());
}

function addMarkers(mapInstance: mapboxgl.Map) {
  const locations = [
    {
      name: "Hogan Park",
      latitude: 40.874056,
      longitude: -111.901012,
      court_count: 6,
      courts_occupied: 3,
      number_waiting: 10,
      estimated_wait_time: "15m"
    }
  ];

  locations.forEach(loc => {
    new mapboxgl.Marker()
      .setLngLat([loc.longitude, loc.latitude])
      .addTo(mapInstance);
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
  <div ref="mapContainer" class="map-container"></div>
</template>

<style scoped>
.map-container {
  flex: 1;
  margin: 2em;
  height: 500px;
}
</style>
