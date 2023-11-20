<script setup lang="ts">
import { RouterView } from 'vue-router'

import CommonHeader from './components/CommonHeader.vue'

import CommonFooter from './components/CommonFooter.vue'
</script>

<template>
  <CommonHeader />
  <RouterView />
  <CommonFooter />
</template>

<style scoped></style>
