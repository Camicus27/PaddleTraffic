<script setup lang="ts">
import CommonHeader from '@/components/CommonHeader.vue';
import MatchList from '@/components/MatchList.vue'
</script>

<template>
  <CommonHeader />
  <div id="match-wrapper">
    <header>
      <h1>Matchmaking Services</h1>
    </header>
    <MatchList />
  </div>
</template>

<style scoped>
#match-wrapper {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 1rem;
    margin: 1rem;
    width: 80%;
}

/* Media query for narrower screens */
@media only screen and (max-width: 850px) {
    #match-wrapper #event-form-wrapper {
        width: 100%;
    }

    #match-wrapper {
        margin: .75rem;
        width: 85%;
    } 
} 
</style>