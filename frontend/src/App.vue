<script setup lang="ts">
import { RouterView } from 'vue-router'

import CommonHeader from './components/CommonHeader.vue'
import CommonSidebar from './components/CommonSidebar.vue'
import CommonFooter from './components/CommonFooter.vue'
</script>

<template>
  <CommonHeader />
  <div class="main-wrapper">
    <CommonSidebar />
    <RouterView />
  </div>
  <CommonFooter />
</template>

<style scoped>
  .main-wrapper {
    display: flex;
    
  }
</style>
