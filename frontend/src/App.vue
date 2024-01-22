<script setup lang="ts">
import { RouterView } from 'vue-router'

import CommonHeader from './components/CommonHeader.vue'
import CommonSidebar from './components/CommonSidebar.vue'
import CommonFooter from './components/CommonFooter.vue'
</script>

<template>
  <CommonHeader />
  <div class="main-wrapper">
    <!-- <CommonSidebar />   This is now going to be dynamically loaded as a popup menu so it isn't always visible   -->
    <!-- This allows us to keep all pages loaded, and avoids too many API calls -->
    <RouterView v-slot="{ Component }">
      <KeepAlive>
        <component :is="Component" />
      </KeepAlive>
    </RouterView>
  </div>
  <CommonFooter />
</template>