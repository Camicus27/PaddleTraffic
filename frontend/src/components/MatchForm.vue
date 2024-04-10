<script setup lang="ts">
import { ref, onMounted, onActivated, type Ref } from 'vue'
import { getCurrentUser, getAllLocations, createEvent } from '@/api/functions';
import type { PickleUser, RestrictedUser, Location } from '@/api/types';
import { redirect } from '@/api/utils';
import { VTimePicker } from 'vuetify/labs/components';
import { format } from 'date-fns'
import { generalTextRule, nameRules } from '@/api/rules';

const submissionError = ref(false)

let currentUser: Ref<PickleUser>
const allFriends: Ref<RestrictedUser[]> = ref([])
const allLocations: Ref<Location[]> = ref([])

const eventForm = ref({
    name: '',
    description: '',
    location: 1,
    host: -1,
    players: new Array<number>(),
    date: new Date(),
    time: format(new Date(), "HH:mm"),
    isPublic: true
})
const isHostPlaying = ref(true);

onMounted(async () => {
    currentUser = ref(await getCurrentUserOrRedirect())
    eventForm.value.host = currentUser.value.id
    allFriends.value = currentUser.value.friends
    const locs = await getAllLocations(true)
    if (locs)
        allLocations.value = locs
})

onActivated(async () => {
    submissionError.value = false
    clearForm()
    currentUser.value = await getCurrentUserOrRedirect()
    allFriends.value = currentUser.value.friends
})

async function getCurrentUserOrRedirect() {
    const user = await getCurrentUser(true)
    if (!user) {
        redirect('/login')
    }
    return user as PickleUser
}

async function submitForm() {
    if (isHostPlaying.value) {
        eventForm.value.players.push(currentUser.value.id)
    }

    const formData = { ...eventForm.value, date: format(eventForm.value.date, "yyyy-MM-dd") }
    if (await createEvent(formData, true))
        redirect("/matchmaking/")
    else {
        submissionError.value = true
        if (isHostPlaying.value)
            eventForm.value.players.pop()
    }
}

function clearForm() {
    eventForm.value.name = ''
    eventForm.value.description = ''
    eventForm.value.location = allLocations.value[0].id || 1
    eventForm.value.host = currentUser.value.id
    eventForm.value.players = []
    eventForm.value.date = new Date()
    eventForm.value.time = format(new Date(), "HH:mm")
    eventForm.value.isPublic = true
    isHostPlaying.value = true
}
</script>

<template>
    <v-container class="form-container">
        <v-form class="pickle-form" validate-on="submit lazy" @submit.prevent="submitForm">
            <v-text-field
                bg-color="white"
                :rules="nameRules"
                v-model="eventForm.name"
                label="Awesome Event Name..."
                autofocus
                tabindex="0"
                required
            ></v-text-field>

            <v-textarea
                bg-color="white"
                v-model="eventForm.description"
                label="Description of your event..."
                tabindex="1"
            ></v-textarea>

            <v-autocomplete
                bg-color="white"
                :rules="generalTextRule"
                v-model="eventForm.location"
                :items="allLocations"
                item-title="name"
                item-value="id"
                label="Location"
                tabindex="2"
                required
            >
                <template v-slot:item="{ props, item }">
                    <v-list-item v-bind="props" :subtitle="`${item.raw.city_state_country}`" :title="item.raw.name"></v-list-item>
                </template>
            </v-autocomplete>

            <v-autocomplete
                bg-color="white"
                v-model="eventForm.players"
                :items="allFriends"
                item-title="username"
                item-value="id"
                label="Select friends"
                chips
                closable-chips
                multiple
                counter="4"
                :counter-value="eventForm.players.length"
                hide-selected
                :menu-props="{ disabled: eventForm.players.length >= 4 }"
                no-data-text="No friends found"
                tabindex="3"
                required
            >
                <template v-slot:chip="{ props, item }">
                    <v-chip v-bind="props" :text="item.raw.username"></v-chip>
                </template>

                <template v-slot:item="{ props, item }">
                    <v-list-item v-bind="props" :title="item.raw.username"></v-list-item>
                </template>
            </v-autocomplete>

            <div class="date-container">
                <v-date-picker
                    :rules="generalTextRule"
                    v-model="eventForm.date"
                    class="mx-2 mb-4"
                    tabindex="4"
                    required
                ></v-date-picker>

                <v-time-picker
                    :rules="generalTextRule"
                    v-model="eventForm.time"
                    class="mx-2 mb-4"
                    scrollable
                    tabindex="5"
                    required
                ></v-time-picker>
            </div>

            <v-label for="isPublic">Public or private match?</v-label>
            <v-switch
                id="isPublic"
                v-model="eventForm.isPublic"
                :label="`${eventForm.isPublic ? 'PUBLIC' : 'PRIVATE'}`"
                inset
                tabindex="6"
                required
            ></v-switch>

            <v-label for="isAttending">Are you participating?</v-label>
            <p>(We'll add you to the roster of players automatically)</p>
            <v-switch
                id="isAttending"
                v-model="isHostPlaying"
                :label="`${isHostPlaying ? 'PLAYING' : 'NOT PLAYING'}`"
                inset
                tabindex="7"
                required
            ></v-switch>

            <button class="dark-solid-button" type="submit" tabindex="8">Submit</button>

            <div v-if="submissionError">
                <p id="error-msg">There was an error submitting your event.</p>
            </div>
        </v-form>
        
    </v-container>
</template>

<style scoped lang="scss">
@use '../styles/components';
@use '@/styles/abstracts' as *;
$thin-size: 1650px;
$mobile-size: 800px;

.form-container {
    width: 75%;

    @include responsive($thin-size) {
        width: 95%;
        margin-inline: 0;
        padding-inline: 0;
    }

    .pickle-form {
        width: 100%;
    }
}

.date-container {
    display: flex;
    justify-content: space-around;

    @include responsive($mobile-size) {
        flex-direction: column;
        align-items: center;
    }
}

#error-msg {
    display: flex;
    justify-content: center;
    margin-top: 1rem;
    font-weight: bold;
    color: #8e0000;
}
</style>