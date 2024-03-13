<script setup lang="ts">
import axios from 'axios';
import { ref } from 'vue';
import type Location from './Location';

let URL: string
// This is the collection of environment variables.
const env = import.meta.env
if (env.MODE === 'production')
    URL = env.VITE_PROD_URL
else
    URL = env.VITE_DEV_URL

const props = defineProps(['location', 'onSubmitCallback'])
if (!props?.location) {
    throw new Error("no location defined for Popup.vue")
}
const location : Location = props.location
console.log(`location:  ${location} and id: ${location.id}`)

if (!props?.onSubmitCallback) {
    throw new Error("no onSubmitCallback defined for Popup.vue")
}
const onSubmitCallback : (l : Location) => void = props.onSubmitCallback

const locForm = ref({
    courts_occupied: 0,
    number_waiting: 0
})

const submitDataDisabled = ref<boolean>(false)

function pluralize(word: string, num: number): string {
    if (num != 1) {
        word += "s"
    }
    return word
}

function formatTime(timeNum: number): string {
    let timeNumArr = String(timeNum).split(":")

    let formattedString = ""
    let hours = timeNumArr[0].startsWith("0") ? timeNumArr[0].substring(1) : timeNumArr[0]
    let minutes = timeNumArr[1].startsWith("0") ? timeNumArr[1].substring(1) : timeNumArr[1]

    formattedString += hours + " "
    formattedString += pluralize("Hour", Number(timeNumArr[0])) + " "
    formattedString += minutes + " "
    formattedString += pluralize("Minute", Number(timeNumArr[1]))
    return formattedString
}

function submitForm() {
    submitDataDisabled.value = true
    setTimeout(() => {
        submitDataDisabled.value = false
    }, 3000)
    axios.post(`${URL}/locations/${location.id}/report/`, { report: locForm.value })
        .then(response => {
            // Handle the response here. For example, logging the new location ID.
            // location.value = response.data.location // AHHHHH IDK IDK IDK IDK IDK IDK IDK IDK IDK BAD REFACTOR BOI ABD BAD BAD BAD BAD OOGA BOOGA
            onSubmitCallback(location)
            // })
        })
        .catch(error => {
            // Handle errors here
            console.error('Error:', error)
        })
}
</script>

<template>
    <div class="info">
        <h3>{{ location.name }}</h3>
        <sub>Courts: {{ location.court_count }}</sub>
        <p>Estimated Courts Occupied: {{ location.courts_occupied }}</p>
        <p>Estimated Groups Waiting: {{ location.number_waiting }}</p>
        <p>Estimated Wait Time: {{ formatTime(location.estimated_wait_time) }}</p>
    </div>
    <form @submit.prevent="submitForm">
        <label for="courtsOccupied">Courts Occupied:</label><br>
        <input type="number" id="courtsOccupied" name="courtsOccupied" min="0" :max="location.court_count"
            v-model="locForm.courts_occupied" required><br><br>
        <label for="numberWaiting">Number Waiting:</label><br>
        <input type="number" id="numberWaiting" name="numberWaiting" min="0"
            :max="(locForm.courts_occupied < location.court_count) ? 0 : 10" v-model="locForm.number_waiting"
            required><br><br>
        <button :disabled="submitDataDisabled">
            Update Status
        </button>
    </form>
</template>

<style></style>