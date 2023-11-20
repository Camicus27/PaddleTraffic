<script setup lang="ts">
import { ref } from 'vue'
import SidebarItem from './SidebarItem.vue'

let matchList = ref([
  { id: 1, loc: 'The playground', time: '12:00 pm', skillLvl: 'beginner' },
  { id: 2, loc: 'Picklecoin Tournament', time: '3:00 pm', skillLvl: 'advanced' }
])
</script>

<template>
  <div class="sidebar">
    <SidebarItem
      v-for="{ id, loc, time, skillLvl } in matchList"
      :key="id"
      :location="loc"
      :time="time"
      :skillLevel="skillLvl"
    />
  </div>
</template>

<style scoped></style>
