<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="header">
    <RouterLink to="/">
      <img src="@/assets/logo.png" class="logo" alt="PaddleTraffic Logo" width="125" height="125" />
    </RouterLink>
    <RouterLink class="paddletraffic nav-button" to="/">PaddleTraffic</RouterLink>
    <RouterLink class="nav-button" to="/map">Map</RouterLink>
    <RouterLink class="nav-button" to="/matchmaking">Matchmaking</RouterLink>
    <RouterLink class="nav-button" to="/about">About</RouterLink>
  </div>
</template>

<style scoped>
.header {
  display: flex;
  flex-direction: row;
  align-items: center;
  background-color: #9fb184;
  padding: .5em;
}

.header>h1 {
  padding: 0.5em;
}


.nav-button {
  font-size: x-large;
  /* Large font size for navigation buttons */
  margin-left: .5em;
  /* Space the buttons out a bit more */
  color: #333333;
  /* Dark gray color for links */
  background-color: transparent;
  /* Transparent background */
  text-decoration: none;
  /* Removes underline */
  transition: all 0.2s ease;
  /* Smooth transition for hover effect */
  font-weight: bold;
  /* Makes the text stand out */
  padding: 10px 20px;
  /* Add some padding for button-like appearance */
  border-radius: 5px;
  /* Slightly rounded corners for a softer look */
}

.nav-button:hover,
.nav-button:focus {
  color: #9fb184;
  /* Theme color for hover */
  background-color: #333333;
  /* Dark gray background on hover */
  text-decoration: none;
  /* Keeps underline off on hover */
  transform: scale(1.05);
  /* Slightly enlarges the link on hover */
  cursor: pointer;
  /* Changes cursor to indicate it's clickable */
}

.paddletraffic {
  font-size: xx-large;
}
</style>
