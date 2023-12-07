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
    <!-- This allows us to keep all pages loaded, and avoids too many API calls -->
    <RouterView v-slot="{ Component }">
      <KeepAlive>
        <component :is="Component" />
      </KeepAlive>
    </RouterView>
  </div>
  <CommonFooter />
</template>

<style scoped>
  .main-wrapper {
    display: flex;
  }
</style>

<!-- A css reset stylesheet is included in the index.html file, so global styles can be placed here -->
<style>
  h1 {
    font-size: 2em;
    font-weight: bolder;
  }

  h2 {
    font-size: 1.5em;
    font-weight: bolder;
  }

  h3 {
    font-size: 1.17em;
    font-weight: bolder;
  }

  h4 {
    font-size: 1em;
    font-weight: bolder;
  }
  
  h5 {
    font-size: .83em;
    font-weight: bolder;
  }

  h6 {
    font-size: .67em;
    font-weight: bolder;
  }
</style>