<script setup lang="ts">
defineProps<{
  name?: string
  location?: string
  host?: string
  players?: Array<string>
  date?: string
  time?: string
}>()
</script>

<template>
  <div class="sidebar-item">
    <h2>{{ name }}</h2>
    <h3>Players:</h3>
    <ul>
      <!-- Maybe shouldn't use player for the key, since not guaranteed to be unique -->
      <li>{{ host }} (Host)</li>
      <li v-for="player in players" :key="player">{{ player }}</li>
    </ul>
    <h3>Match at {{ location }}, {{ date }} {{ time }}</h3>
  </div>
</template>

<style scoped>
.sidebar-item {
  text-align: center;
  width: 15em;
  border: 3px solid black;
  background-color: lightsteelblue;
  padding: .5em;
  margin: .5em;
}
</style>
