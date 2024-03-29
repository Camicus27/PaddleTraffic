<script setup lang="ts">
import '@/styles/abstracts/_colors.scss'

import { ref, onMounted, watch, type Ref, resolveDirective } from 'vue'
import { useRoute } from 'vue-router'
import { redirect } from '@/api/utils'

import { getCurrentUser, getFriendRequests } from '@/api/functions'
import type { FriendRequest, PendingFriendRequests, PickleUser, RestrictedUser } from '@/api/types'

let myUser: Ref<PickleUser>
let pendingRequests: Ref<PendingFriendRequests>

onMounted(async () => {
  // Get current user
  const user = await getCurrentUser(true)
  if (!user)
    redirect('/login')
  myUser.value = user as PickleUser

  // Get pending friend requests
  const reqs = await getFriendRequests(true)
  if (!reqs)
    pendingRequests.value = { incoming_requests: [], outgoing_requests: [] }
  else
    pendingRequests.value = reqs as PendingFriendRequests

})
</script>

<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12" md="6" class="d-flex justify-center">
        <!-- THIS IS COLUMN 1 -->
        <v-card class="mx-auto">
          <v-card-text class="d-flex flex-column align-center">
            <h2>Skill Level</h2>
            <p class="text-h6 mx-auto">This is some text</p>
          </v-card-text>
          <v-card-actions>
            <v-btn prepend-icon="mdi-home" :style="{ backgroundColor: 'var(pickle-300)'}">Edit</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col cols="12" md="6" class="d-flex justify-center">
        <!-- THIS IS COLUMN 2 -->
        <h1>This is column 2</h1>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped lang="scss"></style>
