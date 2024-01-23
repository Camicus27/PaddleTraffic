<script setup lang="ts">
import { ref, onMounted, type Ref } from 'vue'
import axios from 'axios'

const isFetching = ref(true)
const submittedSuccessfully = ref(false)

const eventForm = ref({
    name: '',
    description: '',
    location: '',
    host: '',
    players: new Array<String>(),
    date: '',
    time: ''
})

onMounted(() => {
    getAllPlayers()
    getAllLocations()
})

const allPlayers: Ref<any> = ref([])

function getAllPlayers() {
    axios.get(`${URL}/users/`)
        .then((response) => {
            allPlayers.value = response.data.users
            isFetching.value = false
        })
        .catch((error) => console.log(error))
}

const allLocations: Ref<any> = ref([])

function getAllLocations() {
    axios.get(`${URL}/locations/`)
        .then((response) => {
            allLocations.value = response.data.locations
            isFetching.value = false
        })
        .catch((error) => console.log(error))
}

let URL: string
// This is the collection of environment variables.
const env = import.meta.env
if (env.MODE === 'production')
    URL = env.VITE_PROD_URL
else
    URL = env.VITE_DEV_URL

function submitForm() {
    axios.post(`${URL}/events/`, { event: eventForm.value })
        .then(response => {
            // Handle the response here. For example, logging the new location ID.
            console.log('New event ID:', response.data);
            submittedSuccessfully.value = true
        })
        .catch(error => {
            // Handle errors here
            console.error('Error:', error);
        });
}


</script>

<template>
    <div id="event-form-wrapper">
        <form @submit.prevent="submitForm">
            <div>
                <label for="name">Event Name:</label>
                <input type="text" id="name" v-model="eventForm.name" autofocus tabindex="1" placeholder="Awesome Event Name..." required>
            </div>

            <div>
                <label for="description">Description:</label>
                <textarea id="description" v-model="eventForm.description" tabindex="2" placeholder="Description of your event..."></textarea>
            </div>

            <div>
                <label for="location">Location:</label>
                <select id="location" v-model="eventForm.location" tabindex="3" required>
                    <!-- Options should be populated dynamically -->
                    <option v-for="{ id, name } in allLocations" :key="id" :value="id">{{ name }}</option>
                </select>
            </div>

            <div>
                <label for="host">Host:</label>
                <select id="host" v-model="eventForm.host" tabindex="4" required>
                    <!-- Options should be populated dynamically -->
                    <option v-for="{ id, username } in allPlayers" :key="id" :value="id">{{ username }}</option>
                </select>
            </div>
            <div>
                <div>
                    <label for="players">Players:</label>
                    <select id="players" multiple v-model="eventForm.players" tabindex="5"><!--@change="updatePlayers"-->
                        <option v-for="{ id, username } in allPlayers" :key="id" :value="id">{{ username }}</option>
                        <!-- Options should be populated dynamically -->
                    </select>
                </div>
                <div class="selected-players">
                    <span v-for="player in eventForm.players" :key="player.toString()" class="selected-player" tabindex="6">
                        {{ allPlayers.filter((p: any) => p.id === player)[0].username }}
                    </span>
                </div>
            </div>
            <div>
                <label for="date">Date:</label>
                <input type="date" id="date" v-model="eventForm.date" tabindex="7" required>
            </div>

            <div>
                <label for="time">Time:</label>
                <input type="time" id="time" v-model="eventForm.time" tabindex="8" required>
            </div>

            <button type="submit">Submit</button>
        </form>
        <div class="alert-wrapper" v-if="submittedSuccessfully">
            <div class="alert-success">
                <span class="closebtn" @click="submittedSuccessfully = !submittedSuccessfully">&times;</span>
                <strong>Success!</strong> Your form has been submitted. Please reload the events to see the change.
            </div>
        </div>
    </div>
</template>