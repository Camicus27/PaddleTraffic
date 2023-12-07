<script setup lang="ts">
import { ref, onMounted, onUnmounted, type Ref } from 'vue'
import mapboxgl from "mapbox-gl";

const mapContainer = ref()

mapboxgl.accessToken = 'pk.eyJ1Ijoic3VudHp1Y2Fwc3RvbmUiLCJhIjoiY2xwOHl6MGZiMWQwcjJ2bzNpdTh3ZXZ5diJ9.2OxP9v87qKxpFmL7FFrD-g';
const map: Ref<mapboxgl.Map | undefined> = ref()
onMounted(() => {
  map.value = new mapboxgl.Map({
    container: mapContainer.value,
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [-111.876183, 40.758701],
    zoom: 11
  });

  const popup = new mapboxgl.Popup().setText('This is a pickleball location!');

  new mapboxgl.Marker()
  .setLngLat([-111.880222, 40.774807])
  .setPopup(popup)
  .addTo(map.value);

  new mapboxgl.Marker()
  .setLngLat([-111.862977, 40.720215])
  .addTo(map.value);

  new mapboxgl.Marker()
  .setLngLat([-111.862123, 40.783499])
  .addTo(map.value);
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
