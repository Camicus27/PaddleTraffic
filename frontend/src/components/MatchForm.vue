<script setup lang="ts">
import { ref, onMounted, onActivated, type Ref } from 'vue'
import axios from 'axios'
import { getCurrentUser, getAllLocations } from '@/api/functions';
import type { PickleUser } from '@/api/types';

const isFetching = ref(true)
const submittedSuccessfully = ref(false)

const currentUser: Ref<PickleUser | undefined> = ref(undefined)
const allFriends: Ref<any> = ref([])
const allLocations: Ref<any> = ref([])

const eventForm = ref({
    name: '',
    description: '',
    location: '',
    host: -1,
    players: new Array<String>(),
    date: '',
    time: '',
    isPublic: true
})
const matchVisibility = ref("public")


onMounted(async () => {
    currentUser.value = await getCurrentUser(true)
    if (!currentUser.value) {
        window.location.href = '/login'
    }
    else {
        allFriends.value = currentUser.value.friends
    }
    allLocations.value = await getAllLocations(URL, true)
})

onActivated(async () => {
    submittedSuccessfully.value = false
    currentUser.value = await getCurrentUser(true)
    if (!currentUser.value) {
        window.location.href = '/login'
    }
    else {
        allFriends.value = currentUser.value.friends
    }
})

let URL: string
// This is the collection of environment variables.
const env = import.meta.env
if (env.MODE === 'production')
    URL = env.VITE_PROD_URL
else
    URL = env.VITE_DEV_URL

function submitForm() {
    eventForm.value.host = currentUser.value ? currentUser.value.id : -1
    eventForm.value.isPublic = matchVisibility.value === 'public'
    axios.post(`${URL}/events/`, { event: eventForm.value })
        .then(response => {
            // Handle the response here. For example, logging the new location ID.
            console.log('New event ID:', response.data);
            submittedSuccessfully.value = true;
        })
        .catch(error => {
            // Handle errors here
            console.error('Error:', error);
        });
}
</script>

<template>
    <div v-if="currentUser" id="event-form-wrapper">
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
                    <option v-for="{ id, name } in allLocations" :key="id" :value="id">{{ name }}</option>
                </select>
            </div>

            <div>
                <div>
                    <label for="players">Players:</label>
                    <select id="players" multiple v-model="eventForm.players" tabindex="4">
                        <optgroup v-if="allFriends.length === 0" label="Add friends to invite them here"></optgroup>
                        <option v-for="{ id, username } in allFriends" :key="id" :value="id">{{ username }}</option>
                    </select>
                </div>
                <div class="selected-players">
                    <span v-for="player in eventForm.players" :key="player.toString()" class="selected-player" tabindex="6">
                        {{ allFriends.filter((p: any) => p.id === player)[0].username }}
                    </span>
                </div>
            </div>
            <div>
                <label for="date">Date:</label>
                <input type="date" id="date" v-model="eventForm.date" tabindex="5" required>
            </div>

            <div>
                <label for="time">Time:</label>
                <input type="time" id="time" v-model="eventForm.time" tabindex="6" required>
            </div>

            <div>
                <label for="isPublic">Match Privacy:</label>
                <input type="radio" id="public" value="public" v-model="matchVisibility">
                <p>
                    Public
                </p>
                <input type="radio" id="private" value="private" v-model="matchVisibility">
                <p>
                    Private
                </p>
            </div>

            <button type="submit">Submit</button>
        </form>
    </div>
    <div v-else>
        <h3>Sign in to access event creation</h3>
    </div>
    <div>
        <RouterLink to="/matchmaking">&larr; Return to Events</RouterLink>
    </div>
    <div class="alert-wrapper" v-if="submittedSuccessfully">
        <div class="alert-success">
            <span class="closebtn" @click="submittedSuccessfully = !submittedSuccessfully">&times;</span>
            <strong>Success!</strong> Your form has been submitted.
        </div>
    </div>
</template>

<style scoped lang="scss">
@use '../styles/components';

form {
    display: flex;
    flex-direction: column;
    width: 100%;
    padding: 1.75rem;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 2px 4px #ffffff40;

    div {
        display: flex;
        flex-direction: column;
        margin-block: .5rem;
    }

    label {
        display: block;
        margin-bottom: .5rem;
        font-weight: bold;
    }

    input,
    textarea,
    select {
        width: 100%;
        padding: 8px;
        border: 1px solid #ddd;
        border-radius: 4px;
        box-sizing: border-box;
    }

    textarea {
        height: 5rem;
        resize: vertical;
    }
}

// @media only screen and (max-width: 850px) {
//     #event-form-wrapper {
//             width: 100%;
//     }
// }

// #event-form-wrapper {
//     display: flex;
//     justify-content: center;
//     margin-top: 1.5rem;
//     width: 80%;
// }
</style>