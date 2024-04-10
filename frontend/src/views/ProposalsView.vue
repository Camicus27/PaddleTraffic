<script setup lang="ts">
import CommonHeader from '@/components/CommonHeader.vue'
import ProposalList from '@/components/ProposalList.vue'
import ProposalForm from '@/components/ProposalForm.vue'

import { ref, onMounted, type Ref } from 'vue'
import { URL, getCurrentUser } from '@/api/functions';
import type { PickleUser } from '@/api/types';

const currentUser: Ref<PickleUser | undefined> = ref(undefined)

onMounted(async () => {
  currentUser.value = await getCurrentUser(true)
})
</script>

<template>
    <CommonHeader />
    <div id="proposal-wrapper">
      <h1>Propose a New Court</h1>
      <div v-if="currentUser?.is_superuser" class="proposal-sub-wrapper">
        <ProposalForm />
        <ProposalList />
      </div>
      <div v-else-if="currentUser" class="proposal-sub-wrapper">
        <ProposalForm />
      </div>
      <div v-else class="proposal-sub-wrapper">
        <a href="/login/">Sign in</a> to propose new Pickelball locations for the map!
      </div>
    </div>
</template>

<style scoped lang="scss">
@use '@/styles/abstracts' as *;
$mobile-size: 800px;

h1 {
  margin-bottom: 1.5rem;
}

#proposal-wrapper {
  @extend %main-page;
  width: 85%;

  @include responsive($mobile-size) {
    width: 100%;
  }
}

.proposal-sub-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;

  @include responsive($mobile-size) {
    width: 100%;
  }
}
</style>