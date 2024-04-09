<script setup lang="ts">
import { ref, onMounted, onActivated, watch, type Ref } from 'vue'
import axios from 'axios'
import { URL, getCurrentUser, getAllLocations } from '@/api/functions';
import type { PickleUser, RestrictedUser, Location } from '@/api/types';

const isFetching = ref(true)
const submittedSuccessfully = ref(false)

const currentUser: Ref<PickleUser | undefined> = ref(undefined)
const allFriends: Ref<RestrictedUser[]> = ref([])
const allLocations: Ref<Location[]> = ref([])

const eventForm = ref({
    name: '',
    description: '',
    location: '',
    host: -1,
    players: new Array<number>(),
    date: '',
    time: '',
    isPublic: true
})
const matchVisibility = ref("public")
const isHostPlaying = ref("yes")

const rules = ref([
  (value: string) => {
    if (value) return true;
    return 'You must enter a value.';
  },
])

onMounted(async () => {
    currentUser.value = await getCurrentUser(true)
    if (!currentUser.value) {
        window.location.href = '/login'
    }
    else {
        allFriends.value = currentUser.value.friends
    }
    const allLoc = await getAllLocations(true)
    if (allLoc) {
        allLocations.value = allLoc
    }
})

onActivated(async () => {
    submittedSuccessfully.value = false
    clearForm()
    currentUser.value = await getCurrentUser(true)
    if (!currentUser.value) {
        window.location.href = '/login'
    }
    else {
        allFriends.value = currentUser.value.friends
    }
})

function submitForm() {
    if (currentUser.value) {
        eventForm.value.host = currentUser.value.id
        if (isHostPlaying.value === 'yes') {
            eventForm.value.players.push(currentUser.value.id)
        }
    }
    else {
        eventForm.value.host = -1
    }
    
    eventForm.value.isPublic = matchVisibility.value === 'public'
    axios.post(`${URL}/events/`, { event: eventForm.value })
        .then(response => {
            console.log('New event:', response.data);
            submittedSuccessfully.value = true;
        })
        .catch(error => {
            // Handle errors here
            console.error('Error:', error);
        });
}

function clearForm() {
    eventForm.value.name = ''
    eventForm.value.description = ''
    eventForm.value.location = ''
    eventForm.value.host = -1
    eventForm.value.players = []
    eventForm.value.date = ''
    eventForm.value.time = ''
    eventForm.value.isPublic = true
    matchVisibility.value = "public"
    isHostPlaying.value = "yes"
}
</script>

<template>
    <div v-if="currentUser" id="event-form-wrapper">
        <v-form @submit.prevent="submitForm">

            <v-text-field
                class="field"
                v-model="eventForm.name"
                :rules="rules"
                label="Event Name"
                type="text"
                id="name"
                autofocus
                tabindex="1"
                required
            ></v-text-field>

            <v-textarea
                class="field"
                v-model="eventForm.description"
                label="Event Description"
                maxlength="200"
                counter
                multiline
                tabindex="2"
            ></v-textarea>

            <v-autocomplete
                v-model="eventForm.location"
                :items="allLocations"
                item-title="name"
                item-value="id"
                label="Event Location"
                no-data-text="No matching locations."
                tabindex="4"
                >
                    <template v-slot:item="{ props, item }">
                        <v-list-item v-bind="props" :title="item.raw.name"></v-list-item>
                    </template>
            </v-autocomplete>

            <v-autocomplete
                v-model="eventForm.players"
                :items="allFriends"
                item-title="username"
                item-value="id"
                label="Add Friends to Event"
                no-data-text="Add friends to invite them here."
                chips
                closable-chips
                tabindex="4"
                multiple
                max="3"
                >
                    <template v-slot:chip="{ props, item }">
                        <v-chip v-bind="props" :text="item.raw.username"></v-chip>
                    </template>

                    <template v-slot:item="{ props, item }">
                        <v-list-item v-bind="props" :subtitle="item.raw.skill_level"
                            :title="item.raw.username"></v-list-item>
                    </template>
            </v-autocomplete>

            <!-- <section>
                <label for="name">Event Name:</label>
                <input type="text" id="name" v-model="eventForm.name" autofocus tabindex="1" placeholder="Awesome Event Name..." required>
            </section>

            <section>
                <label for="description">Description:</label>
                <textarea id="description" v-model="eventForm.description" tabindex="2" placeholder="Description of your event..."></textarea>
            </section>

            <section>
                <label for="location">Location:</label>
                <select id="location" v-model="eventForm.location" tabindex="3" required>
                    <option v-for="{ id, name } in allLocations" :key="id" :value="id">{{ name }}</option>
                </select>
            </section>

            <section>
                <div>
                    <label for="players">Players:</label>
                    <select id="players" multiple v-model="eventForm.players" tabindex="4">
                        <optgroup v-if="allFriends.length === 0" label="Add friends to invite them here"></optgroup>
                        <option v-for="{ id, username } in allFriends" :key="id" :value="id">{{ username }}</option>
                    </select>
                </div>
                <div class="selected-players">
                    <span v-for="player in eventForm.players" :key="player" class="selected-player" tabindex="6">
                        <p v-if="player != currentUser.id">
                            {{ allFriends.filter((p: any) => p.id === player)[0].username }}
                        </p>
                    </span>
                </div>
            </section> -->

            <section>
                <label for="date">Date:</label>
                <input type="date" id="date" v-model="eventForm.date" tabindex="5" required>
            </section>

            <section>
                <label for="time">Time:</label>
                <input type="time" id="time" v-model="eventForm.time" tabindex="6" required>
            </section>

            <section class="radio-select">
                <label for="isPublic">Match Privacy:</label>
                <div>
                    <input type="radio" name="privacy" id="public" value="public" v-model="matchVisibility" tabindex="7" required>
                    <label for="public">Public</label>
                </div>
                <div>
                    <input type="radio" name="privacy" id="private" value="private" v-model="matchVisibility" tabindex="8" required>
                    <label for="private">Private</label>
                </div>
            </section>

            <section class="radio-select">
                <label for="isAttending">Are You Participating?</label>
                <p>
                    (We'll add you to the roster of players automatically)
                </p>
                <div>
                    <input type="radio" name="participating" id="yes-participation" value="yes" v-model="isHostPlaying" tabindex="9" required>
                    <label for="yes-participation">Yes</label>
                </div>
                <div>
                    <input type="radio" name="participating" id="no-participation" value="no" v-model="isHostPlaying" tabindex="10" required>
                    <label for="no-participation">No</label>
                </div>
            </section>

            <button v-if="!submittedSuccessfully" class="dark-solid-button" type="submit" tabindex="11">Submit</button>
            <div id="success-alert" v-else>
                <p>
                    <strong>Success!</strong> Your form has been submitted.
                </p>
            </div>
        </v-form>
    </div>
    <div v-else>
        <h3>Sign in to access event creation</h3>
    </div>
    <div id="back-link">
        <RouterLink to="/matchmaking">&larr; Return to Events</RouterLink>
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

#location {
    width: fit-content;

    @include responsive($mobile-size) {
        width: auto;
    }
}

#date, #time {
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

.field {
    input {
        background-color: white;
    }
}
</style>