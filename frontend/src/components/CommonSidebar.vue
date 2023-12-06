<script setup lang="ts">
import { ref } from 'vue'
import SidebarItem from './SidebarItem.vue'

let matchList = ref([
  { id: 1, loc: 'The playground', time: '12:00 pm', skillLvl: 'beginner' },
  { id: 2, loc: 'Picklecoin Tournament', time: '3:00 pm', skillLvl: 'advanced' },
  { id: 3, loc: 'Picklecoin HQ', time: '4:30 pm', skillLvl: 'intermediate' }
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
