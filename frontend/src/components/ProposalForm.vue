<script setup lang="ts">
import { ref, onMounted, onActivated, type Ref } from 'vue'
import axios from 'axios'
import { URL, getCurrentUser } from '@/api/functions';
import type { PickleUser } from '@/api/types';

const submittedSuccessfully = ref(false)

const currentUser: Ref<PickleUser | undefined> = ref(undefined)

const newLocationForm = ref({
    name: '',
    latitude: 0.0,
    longitude: 0.0,
    court_count: 1,
    proposer: -1
})

onMounted(async () => {
    currentUser.value = await getCurrentUser(true)
    submittedSuccessfully.value = false
    clearForm()
})

function submitForm() {
    if (currentUser.value) {
        newLocationForm.value.proposer = currentUser.value.id
    }
    else {
        newLocationForm.value.proposer = -1
    }
    
    axios.post(`${URL}/location/new/`, { location: newLocationForm.value })
        .then(response => {
            console.log('New location:', response.data);
            submittedSuccessfully.value = true;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function clearForm() {
    newLocationForm.value.name = ''
    newLocationForm.value.latitude = 0.0
    newLocationForm.value.longitude = 0.0
    newLocationForm.value.court_count = 1
}
</script>

<template>
    <div id="new-location-form-wrapper">
        <form @submit.prevent="submitForm">
            <section>
                <label for="name">Location Name:</label>
                <input type="text" id="name" v-model="newLocationForm.name" autofocus tabindex="1" placeholder="Park or Location Name..." required>
            </section>

            <section>
                <label for="latitude">Latitude:</label>
                <input type="number" id="latitude" v-model="newLocationForm.latitude" tabindex="2" step="0.000001" min="-90" max="90" required>
                <label for="longitude">Longitude:</label>
                <input type="number" id="longitude" v-model="newLocationForm.longitude" tabindex="3" step="0.000001" min="-180" max="180" required>
            </section>
                
            <section>
                <label for="court-count">Number of Courts at Location:</label>
                <input type="number" id="court-count" v-model="newLocationForm.court_count" tabindex="4" min="1" required>
            </section>

            <button v-if="!submittedSuccessfully" class="dark-solid-button" type="submit" tabindex="5">Submit</button>
            <div id="success-alert" v-else>
                <p>
                    <strong>Success!</strong> Your proposal has been submitted.
                </p>
            </div>
        </form>
    </div>
</template>

<style scoped lang="scss">
@use '../styles/components';
@use '@/styles/abstracts' as *;
$mobile-size: 800px;

#event-form-wrapper {
  @extend %main-page;
  width: 85%;

  @include responsive($mobile-size) {
    width: 90%;
  }
}

.radio-select {
    div {
        display: flex;
        flex-direction: row;
        margin-block: 0;
    }
    input {
        width: auto;
        appearance: auto;
    }
    div label {
        font-weight: normal;
        padding-left: .5rem;
        margin-block: 0;
    }
    p {
        color: #272727;
        font-size: .85rem;
        margin: 0;
    }
}

#location, #date, #time {
    width: fit-content;
}

#back-link {
    margin-bottom: 5rem;
    a {
        font-size: 1.25rem;
    }
}

#success-alert {
    display: flex;
    justify-content: center;
    p {
        font-size: 1.33rem;
    }
}
</style>