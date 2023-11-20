<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="header">
    <img src="@/assets/logo.png" class="logo" alt="PaddleTraffic Logo" width="125" height="125" />
    <h1>PaddleTraffic</h1>
    <RouterLink to="/">Home</RouterLink>
    <RouterLink to="/map">Map</RouterLink>
    <RouterLink to="/matchmaking">Matchmaking</RouterLink>
    <RouterLink to="/about">About</RouterLink>
  </div>
</template>

<style scoped>
.header {
  display: flex;
  flex-direction: row;
  align-items: center;
  background-color: #9fb184;
}

.header h1 {
  padding: 0.5em;
}

.header a {
  padding: 1em;
}
</style>
