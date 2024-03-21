<script setup lang="ts">
import { ref, onActivated, onMounted, type Ref } from 'vue';
import { getAllUsers, getCurrentUser, getAllEvents } from '@/api/functions';
import type { PickleUser } from '@/api/types';

const isFetching = ref(true)

const currentUser: Ref<PickleUser | undefined> = ref(undefined)
const allMatches: Ref<any> = ref([])
const allPlayers: Ref<any> = ref([])

let URL: string
// This is the collection of environment variables.
const env = import.meta.env
if (env.MODE === 'production')
  URL = env.VITE_PROD_URL
else
  URL = env.VITE_DEV_URL

onMounted(async () => {
  allPlayers.value = await getAllUsers(URL, true)
})

onActivated(async () => {
  currentUser.value = await getCurrentUser(URL, true)
  allMatches.value = await getAllEvents(URL, true)
  isFetching.value = false
})
</script>

<template>
  <h3 v-if="!currentUser">
    <a href="/login/">Sign in</a> to create your own events!
  </h3>
  <RouterLink v-else to="/matchmaking/create-event" class="dark-solid-button">Create Your Own Event</RouterLink>
  <div v-if="!isFetching">
    <div class="matches" v-for="{ id, name, location, host, players, description, date, time } in allMatches" :key="id">
      <h2>{{ name }}</h2>
      <h3>Host:</h3>
      <p>{{ allPlayers.filter((p: any) => p.id === host)[0].username }}</p>
      <div class="players" v-if="players.length > 0"> <!-- v-if="0" -->
        <h3>Players:</h3>
        <ul>
          <!-- Maybe shouldn't use player for the key, since not guaranteed to be unique -->
          <li v-for="player in players" :key="player">{{ allPlayers.filter((p: any) => p.id === player)[0].username }}
          </li>
        </ul>
      </div>
      <h3>Details:</h3>
      <div class="match-details">
        <p>
          {{ description }}
        </p>
        <p>
          Being held at <strong>{{ location.name }}</strong>
        </p>
        <p>
          &nbsp;&nbsp; on {{ date }} at {{ time }}
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@use '../styles/components';

.matches {
  margin: .75rem;
  width: 85%;
  border: 3px solid gray;
  border-radius: 3px;
  background-color: #d0d4ca;
  padding: 1rem;
  margin: 1rem;
  width: 65%;
}
</style>
