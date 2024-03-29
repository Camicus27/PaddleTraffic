<script setup lang="ts">
import CommonHeader from '@/components/CommonHeader.vue';
import MatchList from '@/components/MatchList.vue'
</script>

<template>
  <CommonHeader />
  <div id="matchmaking-wrapper">
    <h1>Matchmaking Events</h1>
    <MatchList />
  </div>
</template>

<style scoped lang="scss">
@use '../styles/abstracts';

h1 {
  margin-bottom: 1.5rem;
}

#matchmaking-wrapper {
  @extend %main-page;
  width: 85%;
}

// /* Media query for narrower screens */
// @media only screen and (max-width: 850px) {
//     #match-wrapper #event-form-wrapper {
//         width: 100%;
//     }

//     #match-wrapper {
//         margin: .75rem;
//         width: 85%;
//     } 
// } 
</style>