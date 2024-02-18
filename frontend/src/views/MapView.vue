<script setup lang="ts">
import PickleballMap from '@/components/PickleballMap.vue';
import {useRoute} from "vue-router";
</script>

<template>
    <div id="map-wrapper">
        <header>
            <h1>Pickleball Court Map</h1>
        </header>
        <PickleballMap :lat=useRoute().query.lat :lon=useRoute().query.lon />
    </div>
</template>