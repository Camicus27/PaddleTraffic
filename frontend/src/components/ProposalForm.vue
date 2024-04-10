<script setup lang="ts">
import { ref, onMounted, onActivated, type Ref } from 'vue'
import { VNumberInput } from 'vuetify/labs/VNumberInput'
import axios from 'axios'
import { URL, getCurrentUser } from '@/api/functions';
import type { PickleUser } from '@/api/types';
import { generalTextRule, latRules, longRules, courtRules } from '@/api/rules';
import { redirect } from '@/api/utils';

const submittedSuccessfully = ref(false)
const submissionError = ref(false)

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
    clearForm()
})

onActivated(async () => {
    currentUser.value = await getCurrentUser(true)
    submissionError.value = false
    submittedSuccessfully.value = false
    clearForm()
})

function submitForm() {
    submissionError.value = false
    submittedSuccessfully.value = false

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
            if (currentUser.value?.is_superuser) {
                redirect(`${URL}/new-location/`)
            }
        })
        .catch(error => {
            console.error('Error:', error);
            submissionError.value = true;
        });
}

function clearForm() {
    newLocationForm.value.name = ''
    newLocationForm.value.latitude = 40.765911
    newLocationForm.value.longitude = -111.843703
    newLocationForm.value.court_count = 1
}
</script>

<template>
    <v-container class="form-container">
        <v-form class="proposal-form" validate-on="submit lazy" @submit.prevent="submitForm">
            <v-text-field
                bg-color="white"
                :rules="generalTextRule"
                v-model="newLocationForm.name"
                label="New Location Name..."
                autofocus
                tabindex="0"
                required
            ></v-text-field>

            <v-text-field
                bg-color="white"
                style="width: 50%;"
                :rules="latRules"
                v-model="newLocationForm.latitude"
                label="Latitude"
                type="number"
                hide-spin-buttons
                :max="90"
                :min="-90"
                :step="0.000001"
                tabindex="1"
                required
            ></v-text-field>

            <v-text-field
                bg-color="white"
                style="width: 50%;"
                :rules="longRules"
                v-model="newLocationForm.longitude"
                label="Longitude"
                type="number"
                hide-spin-buttons
                :max="180"
                :min="-180"
                :step="0.000001"
                tabindex="2"
                required
            ></v-text-field>

            <v-number-input
                bg-color="white"
                :rules="courtRules"
                v-model="newLocationForm.court_count"
                label="Number of Courts"
                control-variant="split"
                :max="100"
                :min="1"
                :step="1"
                inset
                tabindex="3"
                required
            ></v-number-input>

            <button v-if="!submittedSuccessfully" class="dark-solid-button" type="submit" tabindex="4">Submit</button>
            <div id="success-alert" v-else>
                <p>
                    <strong>Success!</strong> Your proposal has been submitted and is awaiting admin approval.
                </p>
            </div>
            <div v-if="submissionError">
                <p id="error-msg">There was an error submitting your event.</p>
            </div>
        </v-form>
    </v-container>
</template>

<style scoped lang="scss">
@use '../styles/components';
@use '@/styles/abstracts' as *;
$thin-size: 1250px;
$mobile-size: 800px;

.form-container {
    width: 75%;

    @include responsive($thin-size) {
        width: 95%;
        margin-inline: 0;
        padding-inline: 0;
    }

    .proposal-form {
        width: 100%;
    }
}

.v-number-input--split {
    width: 30%;

    @include responsive($mobile-size) {
        width: 80%;
    }
    
    .v-field__input {
        text-align: left;
    }
}

#error-msg {
    display: flex;
    justify-content: center;
    margin-top: 1rem;
    font-weight: bold;
    color: #8e0000;

    p {
        text-align: center;
    }
}

#success-alert p {
    text-align: center;
}

.v-messages__message {
    margin-bottom: 1rem;
}
</style>