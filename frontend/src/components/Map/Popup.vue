<script setup lang="ts">
import { ref, type Ref } from 'vue';
import type {Location, Report} from '@/api/types';
import { postLocationReport } from '@/api/functions';

const props = defineProps(['location', 'onSubmitCallback'])

const locForm: Ref<Report> = ref({
    courts_occupied: 0,
    number_waiting: 0
})

// does need to be a ref?
const location = ref<Location>(props.location)

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
    formattedString += pluralize("Hr", Number(timeNumArr[0])) + " "
    formattedString += minutes + " "
    formattedString += pluralize("Min", Number(timeNumArr[1]))
    return formattedString
}

function submitForm() {
    // timeout the button
    submitDataDisabled.value = true
    setTimeout(() => {
        submitDataDisabled.value = false
    }, 3000)

    postLocationReport(location.value.id, locForm.value)
}
</script>

<template>
    <div class="popup">
        <div class="left-side">
            <div class="location-title">
                <h4>{{ location.name }}</h4>
                <sub>Courts: {{ location.court_count }}</sub>
            </div>
            <div class="info">
                <p>Est. Courts Occupied: {{ location.courts_occupied }}</p>
                <p>Est. Groups Waiting: {{ location.number_waiting }}</p>
                <p>Est. Wait: {{ formatTime(location.estimated_wait_time) }}</p>
            </div>
        </div>
        <form @submit.prevent="submitForm">
            <label for="courtsOccupied">Courts Occupied:</label>
            <input type="number" id="courtsOccupied" name="courtsOccupied" min="0" :max="location.court_count"
                v-model="locForm.courts_occupied" required>
            <label for="numberWaiting">Groups Waiting:</label>
            <input type="number" id="numberWaiting" name="numberWaiting" min="0"
                :max="(locForm.courts_occupied < location.court_count) ? 0 : 10" v-model="locForm.number_waiting"
                required>
            <button :disabled="submitDataDisabled">
                Update Status
            </button>
        </form>
    </div>
</template>

<style scoped lang="scss">
@use '@/styles/components';
* {
    display: flex;
}

input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

.popup {
    flex-direction: row;
    justify-content: space-between;
    padding: 2px;
    align-items: center;
    width: auto;
}

.left-side {
    justify-content: space-around;
    flex-direction: column;
    h4 {
        margin: 0;
    }

    p {
        margin: 0;
    }
    padding-right: 2rem;
}

.location-title {
    display: flex;
    flex-direction: column;
    justify-content: start;
}

.info {
    display: flex;
    flex-direction: column;
    justify-content: center;
    font-size: small;
    p {
        text-wrap: nowrap;
    }
}

form {
    flex-direction: column;
    justify-content: space-around;
    align-items: center;
    background-color: #f9f9f9;
    border-radius: 8px;

    input {
        border: none;
        width: 90%;
    }
}

button {
    @extend .dark-solid-button;
    font-size: x-small;
    height: 2rem;
    width: 90%;
    margin-top: 1rem;
    line-height: 1rem;
}

button:disabled {
    border: 1px solid #999999;
    background-color: #cccccc;
    color: #666666;
}
</style>@/api/somethingelse