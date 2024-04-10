<script setup lang="ts">
import { ref, onActivated, onMounted, type Ref } from 'vue';
import { getAllUsers, getCurrentUser, getAllProposals, createApproveLocation, createDenyLocation } from '@/api/functions';
import type { PickleUser } from '@/api/types';
import { redirect } from '@/api/utils';

const isFetching = ref(true)
const didDecide = ref(true)
const failedID = ref(-1)

const currentUser: Ref<PickleUser | undefined> = ref(undefined)
const allProposals: Ref<any> = ref([])
const allPlayers: Ref<Record<number, string>> = ref({});

onMounted(async () => {
  currentUser.value = await getCurrentUser(true)

  const allUsers = await getAllUsers(true)

  if (allUsers) {
    allUsers.forEach(player => {
      allPlayers.value[player.id] = player.username;
    });
  }

  // Only admins allowed to see this component
  if (!currentUser.value || !currentUser.value.is_superuser) {
    redirect("/map/")
  }

  allProposals.value = await getAllProposals(true)
  isFetching.value = false
})

onActivated(async () => {
  isFetching.value = true
  currentUser.value = await getCurrentUser(true)

  // Only admins allowed to see this component
  if (!currentUser.value || !currentUser.value.is_superuser) {
    redirect("/map/")
  }

  allProposals.value = await getAllProposals(true)
  isFetching.value = false
})

async function tryApproveLocation(proposalID: number) {
  didDecide.value = await createApproveLocation(proposalID, undefined, true)

  if (didDecide.value) {
    allProposals.value = await getAllProposals(true)
  }
  else {
    failedID.value = proposalID
    console.log("Failed to approve")
  }
}

async function tryDenyLocation(proposalID: number) {
  didDecide.value = await createDenyLocation(proposalID, true)

  if (didDecide.value) {
    allProposals.value = await getAllProposals(true)
  }
  else {
    failedID.value = proposalID
    console.log("Failed to deny")
  }
}
</script>

<template>
  <h1>Pending Court Proposals</h1>
  <v-progress-circular indeterminate v-if="isFetching"></v-progress-circular>
  <div v-else id="proposal-list-wrapper">
    <div class="proposal" v-for="{ id, name, latitude, longitude, court_count, proposer } in allProposals" :key="id">
      <h2>
        {{ name }}
      </h2>
      <p class="user">
        Proposed by <RouterLink class="link" :to="{ path: '/profile/' + allPlayers[proposer] }">
          {{ allPlayers[proposer] }}
        </RouterLink>
      </p>
      <div class="location">
        <p class="latitude">
            Latitude: {{ latitude }}
        </p>
        <p class="longitude">
            Longitude: {{ longitude }}
        </p>
        <a :href="`https://maps.google.com/?q=${latitude},${longitude}`" target="_blank">View on Google Maps &#8594;</a>
      </div>
      <p class="court-count">
        Number of courts: {{ court_count }}
      </p>
      <hr />
      <div class="buttons">
        <button class="dark-solid-button approve" @click="tryApproveLocation(id)">Approve Location</button>
        <button class="dark-solid-button deny" @click="tryDenyLocation(id)">Deny Location</button>
      </div>
      <p id="error-msg" v-if="!didDecide && failedID === id">
        <strong>* Failed to submit decision.</strong>
      </p>
    </div>
    <h2 v-if="!isFetching && allProposals.length === 0">
      There are currently no new proposals.
    </h2>
  </div>
</template>

<style scoped lang="scss">
@use '../styles/components';
@use '@/styles/abstracts' as *;
$thin-size: 1250px;
$mobile-size: 800px;

#proposal-list-wrapper {
  @extend %main-page;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;

  @include responsive($thin-size) {
    grid-template-columns: repeat(2, 1fr);
  }

  @include responsive($mobile-size) {
    display: flex;
    width: 100%;
    gap: 1.25rem;
  }

  h1 {
    margin-top: 3rem;
  }
}

#error-msg {
  color: red;
}

.proposal {
  padding: 1rem;
  width: 100%;
  border: 2px solid $pickle-500;
  border-radius: 3px;
  background-color: $pickle-100;
  box-shadow: 2px 2px 3px $pickle-500;
}

.user {
  font-size: 1.25rem;
  line-height: 1.5rem;

  @include responsive($mobile-size) {
    font-size: 1rem;
    line-height: 1.2rem;
  }
}

.location {
  margin-block: 1rem;

  .latitude, .longitude {
    font-size: 1.1rem;
    margin-bottom: .1rem;

    @include responsive($mobile-size) {
      font-size: .85rem;
    }
  }

  .longitude {
    margin-bottom: .25rem;
  }
}

.court-count {
  color: #272727;
  margin-bottom: .5rem;
}

.buttons {
  margin-top: 1rem;

  button {
    margin-block: .5rem;
  }
}
</style>
