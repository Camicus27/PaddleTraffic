<script setup lang="ts">
import { ref, onActivated, onMounted, type Ref } from 'vue';
import { getAllUsers, getCurrentUser, getAllEvents, createJoinGame, createLeaveGame } from '@/api/functions';
import type { PickleUser } from '@/api/types';

import CalendarButtonContainer from "@/components/Calendar/CalendarButtonContainer.vue"

const isFetching = ref(true)
const didJoin = ref(true)
const failedToJoinID = ref(-1)

const currentUser: Ref<PickleUser | undefined> = ref(undefined)
const allMatches: Ref<any> = ref([])
const allPlayers: Ref<Record<number, string>> = ref({});

// TODO change to be @/api/functions
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
  currentUser.value = await getCurrentUser(URL, true)
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

function playerInEvent(players: number[]) {
  if (currentUser.value) {
    return players.includes(currentUser.value.id)
  }
}

function canJoinGame(players: number[]) {
  if (currentUser.value) {
    return !playerInEvent(players) && players.length <= 3;
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
    <div class="match" v-for="{ id, name, location, host, players, description, date, time } in allMatches" :key="id">
      <h2>
        {{ name }}
      </h2>
      <p class="host">
        Hosted by <RouterLink class="link" :to="{ path: '/profile/' + allPlayers[host] }">
          {{ allPlayers[host] }}
        </RouterLink>
      </p>
      <p class="location">
        Held at <RouterLink class="link"
          :to="{ path: '/map/', query: { lat: location.latitude, lon: location.longitude } }"><strong>{{ location.name
            }}</strong></RouterLink>
      </p>
      <p class="date-time">
        on <strong>{{ date }}</strong> at <strong>{{ time }}</strong>
      </p>
      <p class="description">
        {{ description }}
      </p>
      <hr />
      <div class="players">
        <h3>Attending Players:</h3>
        <ul>
          <li v-for="playerId in players" :key="playerId">
            <RouterLink class="link" v-if="currentUser?.id != playerId"
              :to="{ path: '/profile/' + allPlayers[playerId] }">
              {{ allPlayers[playerId] }}
            </RouterLink>
            <p v-else>{{ allPlayers[playerId] }} (You)</p>
          </li>
        </ul>
      </div>
      <div v-if="playerInEvent(players)">
        <h4 class="mb-1">You've joined this event! Add it to you calendar:</h4>
        <CalendarButtonContainer class="mb-4" :title="name" :description="description" :start-date="date" :start-time="time" :duration="[1, 'hour']"
          :location="location" />
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

.mb-4 {
  margin-bottom: 16px;
}

.mb-1 {
  margin-bottom: 4px;
}
</style>
