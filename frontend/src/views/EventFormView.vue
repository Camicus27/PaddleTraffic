<script setup lang="ts">
import MatchForm from '@/components/MatchForm.vue'
</script>

<template>
  <div>
    <h1>New Matchmaking Event</h1>
    <MatchForm />
  </div>
</template>

<style scoped lang="scss">
@use '../styles/abstracts';

h1 {
  margin-bottom: 1.5rem;
}

div {
  @extend %main-page;
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