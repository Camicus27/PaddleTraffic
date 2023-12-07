<script setup lang="ts">
import { ref } from 'vue'
import SidebarItem from './SidebarItem.vue'

let matchList = ref([
  { id: 1, loc: 'The Playground', players: ['Jim', 'Ian'], desiredPlayers: 2, time: '12:00 pm', skillLvl: 'Beginner' },
  { id: 2, loc: 'Picklecoin HQ', players: ['Camron', 'Ian', 'Jake', 'PickleCoin CEO'], desiredPlayers: 4, time: '4:30 pm', skillLvl: 'Intermediate' },
  { id: 3, loc: 'The CS Department', players: ['Jake'], desiredPlayers: 2, time: '3:00 pm', skillLvl: 'Advanced' },
  { id: 4, loc: 'The Moon', players: ['PickleCoin CEO'], desiredPlayers: 4, time: '9:00 pm', skillLvl: 'Expert' }
])
</script>

<template>
  <div class="sidebar">
    <SidebarItem
      v-for="{ id, loc, players, desiredPlayers, time, skillLvl } in matchList"
      :key="id"
      :location="loc"
      :players="players"
      :desiredPlayers="desiredPlayers"
      :time="time"
      :skillLevel="skillLvl"
    />
  </div>
</template>

<style scoped>
  .sidebar {
    display: flex;
    flex-direction: column;
    align-items: start;
    width: 20%;
    margin-right: 2.5rem;
  }
</style>
