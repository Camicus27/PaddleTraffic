<script setup lang="ts">
import { ref, onActivated, onMounted, type Ref } from 'vue';
import axios from 'axios'
import MatchForm from './MatchForm.vue'

const isFetching = ref(true)

const currentUser: Ref<any> = ref(undefined)
const matches: Ref<any> = ref([])
const allPlayers: Ref<any> = ref([])

let URL: string
// This is the collection of environment variables.
const env = import.meta.env
if (env.MODE === 'production')
  URL = env.VITE_PROD_URL
else
  URL = env.VITE_DEV_URL

onMounted(async () => {
  getAllPlayers()
})

onActivated(async () => {
  await getCurrentUser()
  getEvents()
})

async function getCurrentUser() {
  try {
    const response = await axios.get(`${URL}/current-user/`)
    if (response.data.user) {
      currentUser.value = response.data.user
    } else currentUser.value = undefined
  } catch {
    currentUser.value = undefined
  }
}

function getEvents() {
  axios.get(`${URL}/events/`)
    .then((response) => {
      matches.value = response.data.events
      matches.value.reverse()
    })
    .catch((error) => console.log(error))
}

function getAllPlayers() {
  axios.get(`${URL}/users/`)
    .then((response) => {
      allPlayers.value = response.data.users
      isFetching.value = false
    })
    .catch((error) => console.log(error))
}

function redirect() {
  window.location.href = '/login'
}

</script>

<template>
  <div class="button-wrapper">
    <div v-if="!currentUser">
      <p>
        <a href="/login/">Sign in</a> to create your own events!
      </p>
    </div>
    <RouterLink v-else to="/matchmaking/create-event">Create Your Own Event</RouterLink>
  </div>
  <template v-if="!isFetching">
    <div class="matches" v-for="{ id, name, location, host, players, description, date, time } in matches" :key="id">
      <h2>{{ name }}</h2>
      <h3>Host:</h3>
      <p>{{ allPlayers.filter((p: any) => p.id === host)[0].username }}</p>
      <div class="players" v-if="players.length > 0"> <!-- v-if="0" -->
        <h3>Players:</h3>
        <ul>
          <!-- Maybe shouldn't use player for the key, since not guaranteed to be unique -->
          <li v-for="player in players" :key="player">{{ allPlayers.filter((p: any) => p.id === player)[0].username }}</li>
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
  </template>
</template>
