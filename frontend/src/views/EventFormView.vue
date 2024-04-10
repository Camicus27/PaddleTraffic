<script setup lang="ts">
import MatchForm from '@/components/MatchForm.vue'
import CommonHeader from '@/components/CommonHeader.vue';
</script>

<template>
  <CommonHeader />
  <div id="events-wrapper">
    <h1>New Matchmaking Event</h1>
    <MatchForm />
  </div>
</template>

<style scoped lang="scss">
@use '@/styles/abstracts' as *;
$mobile-size: 800px;

h1 {
  margin-bottom: 1.5rem;
}

#events-wrapper {
  @extend %main-page;
  width: 85%;

  @include responsive($mobile-size) {
    width: 100%;
  }
}
</style>
