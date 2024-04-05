<script setup lang="ts">
import { ref, watch, type Ref } from 'vue'
import { useRoute } from 'vue-router'

import PublicProfile from '@/components/Profile/PublicProfile.vue'
import CommonHeader from '@/components/CommonHeader.vue'
import PrivateProfile from '@/components/Profile/PrivateProfile.vue'

const route = useRoute()
const username: Ref<string> = ref(route.params.username as string)

watch(route, () => {
  username.value = route.params.username as string
})
</script>

<template>
  <CommonHeader />
  <PublicProfile v-if="username" :username="username" />
  <PrivateProfile v-else />
</template>

<style scoped lang="scss"></style>
