<script setup lang="ts">
import { ref, onActivated, onMounted, type Ref } from 'vue';
import { VNumberInput } from 'vuetify/labs/VNumberInput'
import {  } from './ProposalForm.vue'
import { getAllUsers, getCurrentUser, getAllProposals, createApproveLocation, createDenyLocation } from '@/api/functions';
import type { PickleUser, ProposedLocation } from '@/api/types';
import { redirect } from '@/api/utils';
import { generalTextRule, latRules, longRules, courtRules } from '@/api/rules';

const isFetching = ref(true)
const didDecide = ref(true)
const failedID = ref(-1)
const editMode = ref(false)
const editID = ref(-1)

const currentUser: Ref<PickleUser | undefined> = ref(undefined)
const allProposals: Ref<any> = ref([])
const allPlayers: Ref<Record<number, string>> = ref({});

const editedProposalForm = ref({
    name: '',
    latitude: 0.0,
    longitude: 0.0,
    court_count: 1
})

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

function startEdit(proposal: ProposedLocation) {
  editID.value = proposal.id

  editedProposalForm.value.name = proposal.name
  editedProposalForm.value.latitude = proposal.latitude
  editedProposalForm.value.longitude = proposal.longitude
  editedProposalForm.value.court_count = proposal.court_count

  editMode.value = true
}

function saveProposalChanges(proposal: ProposedLocation) {
  editID.value = -1

  // const proposal = allProposals.value.find((p: ProposedLocation) => p.id === proposalId)
  
  proposal.name = editedProposalForm.value.name
  proposal.latitude = editedProposalForm.value.latitude
  proposal.longitude = editedProposalForm.value.longitude
  proposal.court_count = editedProposalForm.value.court_count

  editMode.value = false
}

async function tryApproveLocation(proposal: ProposedLocation) {
  console.log(proposal)

  didDecide.value = await createApproveLocation(proposal, true)

  if (didDecide.value) {
    allProposals.value = await getAllProposals(true)
  }
  else {
    failedID.value = proposal.id
    console.log("Failed to approve")
  }
}

async function tryDenyLocation(proposal: ProposedLocation) {
  didDecide.value = await createDenyLocation(proposal.id, true)

  if (didDecide.value) {
    allProposals.value = await getAllProposals(true)
  }
  else {
    failedID.value = proposal.id
    console.log("Failed to deny")
  }
}
</script>

<template>
  <h1>Pending Court Proposals</h1>
  <v-progress-circular indeterminate v-if="isFetching"></v-progress-circular>
  <div v-else id="proposal-list-wrapper">
    <div class="proposal" v-for="proposal in allProposals" :key="proposal.id">
      <h2 v-if="editMode && editID === proposal.id">
        <v-text-field
          bg-color="white"
          :rules="generalTextRule"
          v-model="editedProposalForm.name"
          label="Location Name..."
          tabindex="0"
        ></v-text-field>
      </h2>
      <h2 v-else>
        {{ proposal.name }}
      </h2>
      
      <p class="user">
        Proposed by <RouterLink class="link" :to="{ path: '/profile/' + allPlayers[proposal.proposer] }">
          {{ allPlayers[proposal.proposer] }}
        </RouterLink>
      </p>
      
      <div class="location">
        <v-text-field v-if="editMode && editID === proposal.id"
            bg-color="white"
            style="width: 75%;"
            dense
            :rules="latRules"
            v-model="editedProposalForm.latitude"
            label="Latitude"
            type="number"
            hide-spin-buttons
            :max="90"
            :min="-90"
            :step="0.000001"
            tabindex="1"
        ></v-text-field>
        <p v-else class="latitude">
            Latitude: {{ proposal.latitude }}
        </p>

        <v-text-field v-if="editMode && editID === proposal.id"
            bg-color="white"
            style="width: 75%;"
            dense
            :rules="longRules"
            v-model="editedProposalForm.longitude"
            label="Longitude"
            type="number"
            hide-spin-buttons
            :max="180"
            :min="-180"
            :step="0.000001"
            tabindex="2"
        ></v-text-field>
        <p v-else class="longitude">
            Longitude: {{ proposal.longitude }}
        </p>

        <a class="link" :href="`https://maps.google.com/?q=${proposal.latitude},${proposal.longitude}`" target="_blank">View on Google Maps &#8594;</a>
      </div>

      <v-number-input v-if="editMode && editID === proposal.id"
          bg-color="white"
          :rules="courtRules"
          v-model="editedProposalForm.court_count"
          label="Number of Courts"
          control-variant="split"
          :max="100"
          :min="1"
          :step="1"
          inset
          tabindex="3"
      ></v-number-input>
      <p v-else class="court-count">
        Number of courts: {{ proposal.court_count }}
      </p>

      <hr />
      
      <div class="buttons">
        <button v-if="!editMode" class="dark-solid-button" @click="tryApproveLocation(proposal)">Approve Location</button>
        <button v-if="!editMode" class="deny" @click="tryDenyLocation(proposal)">Deny Location</button>

        <div v-if="editMode && editID === proposal.id" class="edit-actions">
          <button class="dark-solid-button" @click="saveProposalChanges(proposal)">Save</button>
          <button class="deny" @click="editMode = false">Cancel</button>
        </div>
      </div>

      <v-btn class="edit-btn" color="#4b5320" variant="text" elevation="3" v-if="!editMode" @click="startEdit(proposal)">
        <v-icon color="#333" icon="mdi-pencil" left></v-icon>
        Edit
      </v-btn>

      <p id="error-msg" v-if="!didDecide && failedID === proposal.id">
        <strong>Failed to submit decision.</strong>
      </p>
    </div>
  </div>
  <h2 v-if="!isFetching && allProposals.length === 0">
      There are currently no new proposals.
  </h2>
</template>

<style scoped lang="scss">
@use '@/styles/components' as *;
@use '@/styles/abstracts' as *;
$thin-size: 1250px;
$mobile-size: 800px;

#proposal-list-wrapper {
  @extend %main-page;
  width: 100%;
  margin-bottom: 6rem;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;

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

.deny {
  @include round-button(white, #6d0000);
  margin-bottom: 0;
}

.edit-btn {
  position: absolute;
  right: 1rem;
  bottom: 1rem;
  border: 2px solid black;
}

.v-number-input--split {
    width: 40%;

    @include responsive($mobile-size) {
        width: 100%;
    }
    
    .v-field__input {
        text-align: left;
    }
}

.proposal {
  position: relative;
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
  margin-top: .5rem;

  button {
    margin-top: 1rem;
  }
}
</style>
