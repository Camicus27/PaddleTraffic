<script setup lang="ts"></script>

<template>
  <div class="header">
    <img src="@/assets/logo.png" class="logo" alt="PaddleTraffic Logo" width="125" height="125" />
    <h1>PaddleTraffic</h1>
    <a href="">Map</a>
    <a href="">Matchmaking</a>
    <a href="">About</a>
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
    padding: .5em;
}

.header a {
    padding: 1em;
}
</style>
