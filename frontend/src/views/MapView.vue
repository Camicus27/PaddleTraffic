<script setup lang="ts">
import PickleballMap from '@/components/PickleballMap.vue';
import {useRoute} from "vue-router";
</script>

<template>
    <PickleballMap :lat=useRoute().query.lat :lon=useRoute().query.lon />
</template>