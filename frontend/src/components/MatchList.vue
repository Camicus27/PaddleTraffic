<script setup lang="ts">
import { ref, onActivated, onMounted, type Ref } from 'vue';
import { getAllUsers, getCurrentUser, getAllEvents, createJoinGame, createLeaveGame } from '@/api/functions';
import type { PickleUser } from '@/api/types';

const isFetching = ref(true)
const didJoin = ref(true)
const failedToJoinID = ref(-1)

const currentUser: Ref<PickleUser | undefined> = ref(undefined)
const allMatches: Ref<any> = ref([])
const allPlayers: Ref<Record<number, string>> = ref({});

let URL: string
// This is the collection of environment variables.
const env = import.meta.env
if (env.MODE === 'production')
  URL = env.VITE_PROD_URL
else
  URL = env.VITE_DEV_URL

onMounted(async () => {
  const allUsers = await getAllUsers(URL, true)

  if (allUsers) {
    allUsers.forEach(player => {
      allPlayers.value[player.id] = player.username;
    });
  }
})

onActivated(async () => {
  currentUser.value = await getCurrentUser(true)
  allMatches.value = await getAllEvents(URL, true)
  isFetching.value = false
})

async function tryJoinGame(eventId: number) {
  didJoin.value = await createJoinGame(eventId, URL, true)

  if (didJoin.value) {
    allMatches.value = await getAllEvents(URL, true)
  }
  else {
    failedToJoinID.value = eventId
    console.log("Failed to join")
  }
}

async function tryLeaveGame(eventId: number) {
  didJoin.value = await createLeaveGame(eventId, URL, true)

  if (didJoin.value) {
    allMatches.value = await getAllEvents(URL, true)
  }
  else {
    failedToJoinID.value = eventId
    console.log("Failed to leave")
  }
}

function canJoinGame(players: number[]) {
  if (currentUser.value) {
    const playerIsInEvent = players.includes(currentUser.value.id)
    return !playerIsInEvent && players.length <= 3;
  }
  else {
    return false;
  }
}

function canLeaveGame(players: number[]) {
  if (currentUser.value) {
    const playerIsInEvent = players.includes(currentUser.value.id)
    return playerIsInEvent;
  }
  else {
    return false;
  }
}
</script>

<template>
  <h3 v-if="!currentUser">
    <a href="/login/">Sign in</a> to create your own events!
  </h3>
  <RouterLink v-else class="dark-solid-button" to="/matchmaking/create-event">Create Your Own Event</RouterLink>
  <div v-if="!isFetching" id="event-list-wrapper">
    <div class="match p-2" v-for="{ id, name, location, host, players, description, date, time } in allMatches"
      :key="id">
      <h2 class="mb-4">
        {{ name }}
      </h2>
      <p class="host mb-4">
        Hosted by <RouterLink class="link" :to="{ path: '/profile/' + allPlayers[host] }">
          {{ allPlayers[host] }}
        </RouterLink>
      </p>
      <p class="location">
        Held at <RouterLink class="link"
          :to="{ path: '/map/', query: { lat: location.latitude, lon: location.longitude } }"><strong>{{ location.name
            }}</strong></RouterLink>
      </p>
      <p class="date-time mb-4">
        on <strong>{{ date }}</strong> at <strong>{{ time }}</strong>
      </p>
      <p class="description mb-3">
        {{ description }}
      </p>
      <hr class="mb-4" />
      <div class="players mb-4">
        <h3 class="mb-4">Attending Players:</h3>
        <ul class="m-4 ml-10">
          <li v-for="playerId in players" :key="playerId">
            <RouterLink class="link" v-if="currentUser?.id != playerId"
              :to="{ path: '/profile/' + allPlayers[playerId] }">
              {{ allPlayers[playerId] }}
            </RouterLink>
            <p v-else>{{ allPlayers[playerId] }} (You)</p>
          </li>
        </ul>
      </div>
      <div>
        <button class="dark-solid-button" v-if="canJoinGame(players)" id="join-game" @click="tryJoinGame(id)">Join
          game</button>
        <button class="dark-solid-button" v-if="canLeaveGame(players)" id="leave-game" @click="tryLeaveGame(id)">Leave
          game</button>
      </div>
      <p id="error-msg" v-if="!didJoin && failedToJoinID === id">
        <strong>* Failed to join match.</strong>
      </p>
    </div>
  </div>
  <div v-else>
    Loading events...
  </div>
</template>

<style scoped lang="scss">
@use '../styles/components';
@use '../styles/abstracts/_colors' as *;

#event-list-wrapper {
  @extend %main-page;
  width: 60%;
}

#error-msg {
  color: red;
}

.match {
  padding: 1rem;
  margin: 1rem;
  width: 100%;
  border: 2px solid $pickle-500;
  border-radius: 3px;
  background-color: $pickle-100;
  box-shadow: 2px 2px 3px $pickle-500;
}

.players p {
  margin-block: 0;
  margin-inline: .15rem;
}

.host {
  font-size: 1.25rem;
}

.location {
  font-size: 1.1rem;
  margin-bottom: .1rem;
}

.date-time {
  font-size: 1.1rem;
  margin-block: .1rem;
}

.description {
  color: #272727
}

li {
  font-size: 1.15rem;
  margin-block: .2rem;
}
</style>
