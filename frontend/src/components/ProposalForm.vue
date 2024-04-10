<script setup lang="ts">
import { ref, onMounted, onActivated, type Ref } from 'vue'
import { VNumberInput } from 'vuetify/labs/VNumberInput'
import axios from 'axios'
import { URL, getCurrentUser } from '@/api/functions';
import type { PickleUser } from '@/api/types';

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

const nameRules = ref([
    (value: string) => {
        if (value) return true

        return 'Missing a name.'
    },
])

const latRules = ref([
    (value: number) => {
        if (value) return true

        return 'Missing value.'
    },
    (value: number) => {
        if (90 > value && value > -90) return true

        return 'Latitude must be between 90 and -90 degrees'
    },
])

const longRules = ref([
    (value: number) => {
        if (value) return true

        return 'Missing value.'
    },
    (value: number) => {
        if (180 > value && value > -180) return true

        return 'Longitude must be between 180 and -180 degrees'
    },
])

const courtRules = ref([
    (value: number) => {
        if (value) return true

        return 'Missing value.'
    },
    (value: number) => {
        if (value > 0) return true

        return 'Court count must be a positive number'
    },
])

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
                :rules="nameRules"
                v-model="newLocationForm.name"
                label="New Location Name..."
                autofocus
                tabindex="0"
                required
            ></v-text-field>

            <v-number-input
                bg-color="white"
                :rules="latRules"
                v-model="newLocationForm.latitude"
                label="Latitude"
                control-variant="split"
                :max="90"
                :min="-90"
                :step="0.000001"
                inset
                tabindex="1"
                required
            ></v-number-input>

            <v-number-input
                bg-color="white"
                :rules="longRules"
                v-model="newLocationForm.longitude"
                label="Longitude"
                control-variant="split"
                :max="180"
                :min="-180"
                :step="0.000001"
                inset
                tabindex="2"
                required
            ></v-number-input>

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

            <button v-if="!submittedSuccessfully" class="dark-solid-button" type="submit" tabindex="---">Submit</button>
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
    width: 50%;

    @include responsive($mobile-size) {
        width: 100%;
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
    margin-bottom: .75rem;
}
</style>