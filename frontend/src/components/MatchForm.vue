<script setup lang="ts">
import { ref, onMounted, type Ref } from 'vue'
import axios from 'axios'

const isFetching = ref(true)

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
        })
        .catch(error => {
            // Handle errors here
            console.error('Error:', error);
        });
}

// function updatePlayers(event: Event) {
//     // Manually update the model based on the selected options
//     if (event.target != null) {
//         const players = eventForm.value.players
//         const select = event.target as HTMLSelectElement
//         const selections = Array.from(select.selectedOptions).map(option => option.value)

//         selections.forEach(function (selection) {
//             if (players.includes(selection)) {
//                 players.splice(players.indexOf(selection), 1)
//             }
//             else {
//                 players.push(selection)
//             }
//         })
//     }
// }

</script>

<template>
    <div>
        <form @submit.prevent="submitForm">
            <div>
                <label for="name">Event Name:</label>
                <input type="text" id="name" v-model="eventForm.name">
            </div>

            <div>
                <label for="description">Description:</label>
                <textarea id="description" v-model="eventForm.description"></textarea>
            </div>

            <div>
                <label for="location">Location:</label>
                <select id="location" v-model="eventForm.location">
                    <!-- Options should be populated dynamically -->
                    <option v-for="{ id, name } in allLocations" :key="id" :value="id">{{ name }}</option>
                </select>
            </div>

            <div>
                <label for="host">Host:</label>
                <select id="host" v-model="eventForm.host">
                    <!-- Options should be populated dynamically -->
                    <option v-for="{ id, username } in allPlayers" :key="id" :value="id">{{ username }}</option>
                </select>
            </div>
            <div>
                <div>
                    <label for="players">Players:</label>
                    <select id="players" multiple v-model="eventForm.players"><!--@change="updatePlayers"-->
                        <option v-for="{ id, username } in allPlayers" :key="id" :value="id">{{ username }}</option>
                        <!-- Options should be populated dynamically -->
                    </select>
                </div>
                <div class="selected-players">
                    <span v-for="player in eventForm.players" :key="player.toString()" class="selected-player">
                        {{ allPlayers.filter((p: any) => p.id === player)[0].username }}
                    </span>
                </div>
            </div>
            <div>
                <label for="date">Date:</label>
                <input type="date" id="date" v-model="eventForm.date">
            </div>

            <div>
                <label for="time">Time:</label>
                <input type="time" id="time" v-model="eventForm.time">
            </div>

            <button type="submit">Submit</button>
        </form>
    </div>
</template>

<style scoped>
/* General Form Styling */
form {
    max-width: 500px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Form Elements Styling */
form div {
    margin-bottom: 15px;
}

label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
}

input[type="text"],
input[type="date"],
input[type="time"],
textarea,
select {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-sizing: border-box;
}

textarea {
    height: 100px;
    resize: vertical;
}

select[multiple] {
    height: auto;
}

/* Button Styling */
button[type="submit"] {
    padding: 10px 15px;
    background-color: #0056b3;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

button[type="submit"]:hover {
    background-color: #004494;
}

.selected-players {
    margin-top: 10px;
}

.selected-player {
    display: inline-block;
    margin-right: 5px;
    padding: 5px 10px;
    background-color: #f2f2f2;
    border-radius: 4px;
    border: 1px solid #ddd;
}
</style>