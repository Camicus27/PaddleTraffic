<script setup lang="ts">
import MatchList from '@/components/MatchList.vue'
import CommonHeader from '@/components/CommonHeader.vue';
</script>

<template>
  <CommonHeader />
  <div id="matchmaking-wrapper">
    <h1>Matchmaking Events</h1>
    <MatchList />
  </div>
</template>

<style scoped lang="scss">
@use '@/styles/abstracts' as *;
$mobile-size: 800px;

h1 {
  margin-bottom: 1.5rem;
}

#matchmaking-wrapper {
  @extend %main-page;
  width: 85%;

  @include responsive($mobile-size) {
    width: 90%;
  }
}
</style>
