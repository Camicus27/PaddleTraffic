<script setup lang="ts">

import { ref, onMounted, watch, type Ref, resolveDirective } from 'vue'
import { useRoute } from 'vue-router'
import { redirect } from '@/api/utils'

import { getCurrentUser, updateCurrentUser, getFriendRequests, deleteFriendRequest } from '@/api/functions'
import type { FriendRequest, PendingFriendRequests, PickleUser, RestrictedUser } from '@/api/types'

const loading: Ref<boolean> = ref(true)

let myUser: Ref<PickleUser>
let pendingRequests: Ref<PendingFriendRequests>

const revealSkillLvl: Ref<boolean> = ref(false)
const skillLvl: Ref<"Beginner" | "Advanced Beginner" | "Intermediate Beginner" | "Intermediate" | "Advanced Intermediate" | "Expert" | "Advanced Expert" | "Professional"> = ref("Beginner")

const revealBio: Ref<boolean> = ref(false)
const bio: Ref<string> = ref("")

onMounted(async () => {
  // Get current user
  const user = await getCurrentUser(true)
  if (!user)
    redirect('/login')
  myUser = ref(user as PickleUser)

  // Get pending friend requests
  const reqs = await getFriendRequests(true)
  if (!reqs)
    pendingRequests = ref({ incoming_requests: [], outgoing_requests: [] })
  else
    pendingRequests = ref(reqs as PendingFriendRequests)

  // Setup initial profile variables
  skillLvl.value = myUser.value.skill_level
  bio.value = myUser.value.bio

  // Let the UI know we have finished loading
  loading.value = false
})

async function updateSkillLevel() {
  const userCopy = { ...myUser.value }
  userCopy.skill_level = skillLvl.value
  if (await updateCurrentUser(userCopy, true))
    myUser.value = userCopy
  else
    console.log("Unable to update skill level")
  revealSkillLvl.value = false
}

async function updateBio() {
  const userCopy = { ...myUser.value }
  userCopy.bio = bio.value
  if (await updateCurrentUser(userCopy, true))
    myUser.value = userCopy
  else
    console.log("Unable to bio")
  revealBio.value = false
}


</script>

<template>
  <v-progress-circular indeterminate v-if="loading"></v-progress-circular>
  <v-container max-width="1200" v-else>

    <v-row>
      <v-col cols="12" class="d-flex flex-column align-center">
        <h1 class="ma-16">{{ myUser.username }}</h1>

        <!-- BIO CARD -->
        <v-card class="mx-auto w-100" min-width="300" elevation="10">
          <v-card-text class="d-flex flex-column align-center">
            <h2>Bio</h2>

            <p class="text-subtitle-1 text--primary px-md-16 w-100" style="height: 100px; align-self: flex-start;">{{
    myUser.bio }}</p>
          </v-card-text>
          <v-card-actions>
            <v-btn color="#4b5320" variant="text" @click="revealBio = true">
              Edit
            </v-btn>
          </v-card-actions>

          <v-expand-transition>
            <v-card v-if="revealBio" class="v-card--reveal" style="height: 100%;">
              <v-card-text class="pb-0">
                <v-textarea v-model="bio" label="Update your bio" maxlength="150" counter single-line></v-textarea>
              </v-card-text>
              <v-card-actions class="pt-0">
                <v-btn color="#4b5320" variant="text" @click="revealBio = false">
                  Cancel
                </v-btn>
                <v-btn color="#4b5320" variant="text" @click="updateBio">
                  Submit
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-expand-transition>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="6" class="d-flex justify-center">
        <!-- SKILL LEVEL CARD -->
        <v-card class="mx-auto" min-width="300" elevation="10">
          <v-card-text class="d-flex flex-column align-center">
            <h2>Skill Level</h2>
            <p class="text-h6 text--primary">{{ myUser.skill_level }}</p>
          </v-card-text>
          <v-card-actions>
            <v-btn color="#4b5320" variant="text" @click="revealSkillLvl = true">
              Edit
            </v-btn>
          </v-card-actions>

          <v-expand-transition>
            <v-card v-if="revealSkillLvl" class="v-card--reveal" style="height: 100%;">
              <v-card-text class="pb-0">
                <p class="text-h6 text--primary">Select your new skill level</p>
                <v-select v-model="skillLvl" label="SkillLvl"
                  :items="['Beginner', 'Advanced Beginner', 'Intermediate Beginner', 'Intermediate', 'Advanced Intermediate', 'Expert', 'Advanced Expert', 'Professional',]"></v-select>
              </v-card-text>
              <v-card-actions class="pt-0">
                <v-btn color="#4b5320" variant="text" @click="revealSkillLvl = false">
                  Cancel
                </v-btn>
                <v-btn color="#4b5320" variant="text" @click="updateSkillLevel">
                  Submit
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-expand-transition>
        </v-card>
      </v-col>
      <v-col cols="12" md="6" class="d-flex justify-center">
        <!-- FRIEND REQUESTS CARD -->
        <v-card class="mx-auto" min-width="300" elevation="10">
          <v-card-text>
            <h2>Friend Requests</h2>
            <h3 class="mt-4">Incoming</h3>
            <v-list lines="one">
              <v-list-item v-for="incoming in pendingRequests.incoming_requests" :key="incoming.id">
                <v-list-item-title><a :href="`/profile/${incoming.requester.username}`">{{ incoming.requester.username
                    }}</a></v-list-item-title>
              </v-list-item>
            </v-list>
            <h3 class="mt-4">Outgoing</h3>
            <v-list lines="one">
              <v-list-item v-for="outgoing in pendingRequests.outgoing_requests" :key="outgoing.id">
                <v-list-item-title><a :href="`/profile/${outgoing.receiver.username}`">{{ outgoing.receiver.username
                    }}</a></v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
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

h1 {
  font-size: 3.5em;
  color: #4b5320;
}
</style>
