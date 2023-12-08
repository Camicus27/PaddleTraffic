<script setup lang="ts">
import MatchList from '@/components/MatchList.vue'
</script>

<template>
  <div id="match-main-content">
    <h1 class="header">Welcome to Matchmaking!</h1>
    <MatchList />
  </div>
</template>

<style scoped>
.header {
  color: #333;
  /* Dark grey text */
  padding: 20px 40px;
  /* Padding around the content */
  text-align: center;
  /* Center align text */
  font-size: 45px;
  /* Font size for the header */
  font-family: Arial, sans-serif;
  /* Font family (can be changed to match your design) */
  margin-bottom: .5em;
}</style>
