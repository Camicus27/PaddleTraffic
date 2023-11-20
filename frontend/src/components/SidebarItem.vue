<script setup lang="ts">
defineProps<{
  location?: string
  time?: string
  skillLevel?: string
}>()
</script>

<template>
  <div class="sidebar-item">
    <h3>Match at {{ location }}</h3>
    <h3>Time: {{ time }}</h3>
    <h3>Skill level: {{ skillLevel }}</h3>
  </div>
</template>

<style scoped>
    .sidebar-item {
        border: 3px solid black;
        background-color: lightsteelblue;
    }
</style>
