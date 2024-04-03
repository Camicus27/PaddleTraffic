<script setup lang="ts">
import CommonHeader from '@/components/CommonHeader.vue';
import { RouterView } from 'vue-router'
import './styles/globals/_index.scss'
</script>

<template>
  <v-app>
    <v-main>
      <div class="main-wrapper">
        <!-- <CommonSidebar />   This is now going to be dynamically loaded as a popup menu so it isn't always visible   -->
        <!-- This allows us to keep all pages loaded, and avoids too many API calls -->
        <RouterView v-slot="{ Component }">
          <KeepAlive>
            <component :is="Component" />
          </KeepAlive>
        </RouterView>
      </div>
    </v-main>
  </v-app>
</template>

<style scoped lang="scss">
.main-wrapper {
  display: flex;
  flex-grow: 1;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
}
</style>