<script setup lang="ts">
import MatchList from '@/components/MatchList.vue'
</script>

<template>
  <div id="match-main-content">
    <h1>This is the matchmaking view!</h1>
    <h2>
      The elements below are placeholders, fetched from the API
      https://jsonplaceholder.typicode.com/guide/
    </h2>
    <MatchList />
  </div>
</template>

<style scoped></style>
