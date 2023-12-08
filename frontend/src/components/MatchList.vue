<script setup lang="ts">
import { ref, onMounted, type Ref } from 'vue';
import axios from 'axios'
import MatchForm from './MatchForm.vue'

const matches: Ref<any> = ref({})

let URL: string
// This is the collection of environment variables.
const env = import.meta.env
if (env.MODE === 'production')
  URL = env.VITE_PROD_URL
else
  URL = env.VITE_DEV_URL

onMounted(() => {
  getEvents()
})

function getEvents() {
  axios.get(`${URL}/events/`)
    .then((response) => {
      matches.value = response.data
      console.log(matches.value)
    })
    .catch((error) => console.log(error))
}

</script>

<template>
  <MatchForm />
  <button @click="getEvents">Reload Events</button>
  <template v-if="matches.length">
    <div class="matches" v-for="{ id, name, location, host, players, date, time } in matches" :key="id">
      <h2>{{ name }}</h2>
      <h3>Players:</h3>
      <ul>
        <!-- Maybe shouldn't use player for the key, since not guaranteed to be unique -->
        <li>{{ host }} (Host)</li>
        <li v-for="player in players" :key="player">{{ player }}</li>
      </ul>
      <h3>Match at {{ location }}, {{ date }} {{ time }}</h3>
    </div>
  </template>
</template>

<style scoped>
.matches {
  border: 2px solid gray;
  background-color: lightcyan;
  padding: 1em;
  margin: 1em;
}
</style>
