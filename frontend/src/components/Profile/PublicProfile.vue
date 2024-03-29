<script setup lang="ts">
import '@/styles/abstracts/_colors.scss'

import { ref, onMounted, watch, type Ref, resolveDirective } from 'vue'
import { useRoute } from 'vue-router'
import { redirect } from '@/api/utils'

import { getCurrentUser, getFriendRequests } from '@/api/functions'
import type { FriendRequest, PendingFriendRequests, PickleUser, RestrictedUser } from '@/api/types'

const loading: Ref<boolean> = ref(true)

let myUser: Ref<PickleUser>
let pendingRequests: Ref<PendingFriendRequests>

const revealSkillLvl: Ref<boolean> = ref(false)

onMounted(async () => {
  // Get current user
  const user = await getCurrentUser(true)
  if (!user)
    redirect('/login')
  myUser = ref(user as PickleUser)
  console.log(myUser)

  // Get pending friend requests
  const reqs = await getFriendRequests(true)
  if (!reqs)
    pendingRequests = ref({ incoming_requests: [], outgoing_requests: [] })
  else
    pendingRequests = ref(reqs as PendingFriendRequests)

  loading.value = false
})
</script>

<template>
  <v-progress-circular indeterminate v-if="loading"></v-progress-circular>
  <v-container fluid v-else>
    <v-row>
      <v-col cols="12" md="6" class="d-flex justify-center">
        <!-- THIS IS COLUMN 1 -->

        <v-card class="mx-auto" max-width="344">
          <v-card-text class="d-flex flex-column align-center">
            <h2>Skill Level</h2>
            <p class="text-h6 text--primary">{{ myUser.skill_level }}</p>
          </v-card-text>
          <v-card-actions>
            <v-btn color="teal-accent-4" variant="text" @click="revealSkillLvl = true">
              Edit
            </v-btn>
          </v-card-actions>

          <v-expand-transition>
            <v-card v-if="revealSkillLvl" class="v-card--reveal" style="height: 100%;">
              <v-card-text class="pb-0">
                <p class="text-h6 text--primary">
                  Select new skill level
                </p>
              </v-card-text>
              <v-card-actions class="pt-0">
                <v-btn color="teal-accent-4" variant="text" @click="revealSkillLvl = false">
                  Close
                </v-btn>
                <v-btn color="teal-accent-4" variant="text" @click="revealSkillLvl = false">
                  Submit
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-expand-transition>
        </v-card>

      </v-col>
      <v-col cols="12" md="6" class="d-flex justify-center">
        <!-- THIS IS COLUMN 2 -->
        <h1>This is column 2</h1>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped lang="scss">
.v-card--reveal {
  bottom: 0;
  opacity: 1 !important;
  position: absolute;
  width: 100%;
}
</style>
