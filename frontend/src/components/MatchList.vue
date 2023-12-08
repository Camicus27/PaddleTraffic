<script setup lang="ts">
import { ref, onMounted, type Ref } from 'vue';
import axios from 'axios'
import MatchForm from './MatchForm.vue'

const isFetching = ref(true)

const matches: Ref<any> = ref([])

let URL: string
// This is the collection of environment variables.
const env = import.meta.env
if (env.MODE === 'production')
  URL = env.VITE_PROD_URL
else
  URL = env.VITE_DEV_URL

onMounted(() => {
  getEvents()
  getAllPlayers()
})

const allPlayers: Ref<any> = ref([])

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

</script>

<template>
  <MatchForm />
  <div class="button-wrapper">
    <button @click="getEvents">Reload Events</button>
  </div>
  <template v-if="!isFetching">
    <div class="matches" v-for="{ id, name, location, host, players, date, time } in matches" :key="id">
      <h2>{{ name }}</h2>
      <h3>Players:</h3>
      <ul>
        <!-- Maybe shouldn't use player for the key, since not guaranteed to be unique -->
        <li>{{ allPlayers.filter((p: any) => p.id === host)[0].username }} (Host)</li>
        <li v-for="player in players" :key="player">{{ allPlayers.filter((p: any) => p.id === player)[0].username }}</li>
      </ul>
      <h3>Match at {{ location }}, {{ date }} {{ time }}</h3>
    </div>
  </template>
</template>

<style scoped>
.matches {
  border: 3px solid gray;
  background-color: #d0d4ca;
  padding: 1em;
  margin: 1em;
}

.button-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* New styles for the button */
button {
  background-color: #4a5834;
  /* Green background */
  color: white;
  /* White text */
  padding: 12px 24px;
  /* Padding around the text */
  border: none;
  /* No border */
  border-radius: 4px;
  /* Rounded corners */
  cursor: pointer;
  /* Pointer cursor on hover */
  font-size: 16px;
  /* Font size */
  transition: background-color 0.3s;
  /* Smooth transition for hover effect */
  margin-top: 2em;
  margin-bottom: 1em;
  font-size: x-large;
}

button:hover {
  background-color: #71864f;
  /* Darker shade of green on hover */
}</style>
