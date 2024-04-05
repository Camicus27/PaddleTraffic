<script setup lang="ts">
import { onMounted, ref, type ComputedRef, type Ref, toRef } from 'vue';
import type { Location, Report } from '@/api/types';
import { postLocationReport } from '@/api/functions';
import { formatDistanceToNow } from 'date-fns';

// const props = defineProps(['location', 'onSubmitCallback'])
const props = defineProps<{
    location: Ref<Location> | undefined,
    onSubmitCallback: (locationId: number) => void,
}>()

const locForm: Ref<Report> = ref({
    courts_occupied: 0,
    number_waiting: 0
})

const submitDataDisabled = ref<boolean>(false)
const dialog = ref<boolean>(false)
const success_snackbar = ref<boolean>(false)
const outofrange_snackbar = ref<boolean>(false)

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

function formatDateTime(dateTimeString: string): string {
    const reportDate = new Date(dateTimeString)
    return formatDistanceToNow(reportDate, { addSuffix: true })
}

const navigatorSuccessCallback = (position: GeolocationPosition, location: Ref<Location>) => {
    postLocationReport(
        location.value.id,
        locForm.value,
        position.coords.latitude,
        position.coords.longitude)
        .then(
            (l) => {
                if (l) {
                    location.value = l
                    props.onSubmitCallback(location.value.id)
                    success_snackbar.value = true
                } else {
                    outofrange_snackbar.value = true
                }
            }
        )
}

const navigatorFailCallback = () => {
    dialog.value = true
}

function submitForm() {
    let location = props.location
    if (!location) return
    // timeout the button
    submitDataDisabled.value = true
    setTimeout(() => {
        submitDataDisabled.value = false
    }, 3000)

    var options = {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 1000 * 60 * 5 // 5 mins in ms
    }

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => navigatorSuccessCallback(position, location),
            () => navigatorFailCallback(), // geolocation NOT ENABLED
            options
        )
    } else {
        navigatorFailCallback() // geolocation NOT ENABLED
    }

}
</script>

<template>
    <div class="popup">
        <div class="location-info">
            <div class="location-title">
                <h4 class="my-3">{{ props.location?.value.name }}</h4>
                <sub class="mb-6">Courts: {{ props.location?.value.court_count }}</sub>
            </div>
            <div class="data-info">
                <p>Est. Courts Occupied: {{ props.location?.value.courts_occupied }}</p>
                <p>Est. Groups Waiting: {{ props.location?.value.number_waiting }}</p>
                <p class="mb-2">Est. Wait: {{ formatTime(props.location?.value.estimated_wait_time ?? 0) }}</p>
                <sub>Last updated {{ formatDateTime(props.location?.value.calculated_time ?? "") }}</sub>
                <a class="mt-4"
                    :href="`https://maps.google.com/?q=${props.location?.value.latitude},${props.location?.value.longitude}`"
                    target="_blank">Get Directions</a>
            </div>
        </div>
        <form @submit.prevent="submitForm">
            <div class="input-box">
                <label for="courtsOccupied">Courts Occupied:</label>
                <input type="number" id="courtsOccupied" name="courtsOccupied" min="0"
                    :max="props.location?.value.court_count" v-model="locForm.courts_occupied" required>
            </div>
            <div class="input-box">
                <label for="numberWaiting">Groups Waiting:</label>
                <input type="number" id="numberWaiting" name="numberWaiting" min="0"
                    :max="(locForm.courts_occupied < (props.location?.value.court_count ?? 0)) ? 0 : 10"
                    v-model="locForm.number_waiting" required>
            </div>

            <v-dialog v-model="dialog" persistent max-width="290">
                <v-card>
                    <v-card-title class="headline">Location Required</v-card-title>
                    <v-card-text>
                        This service requires access to your location. Please enable location services in your browser
                        settings.
                    </v-card-text>
                    <v-card-actions>
                        <v-btn @click="dialog = false">OK</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>

            <v-snackbar :timeout="1500" v-model="success_snackbar">
                Report Successfully Sent
            </v-snackbar>

            <v-snackbar :timeout="1500" v-model="outofrange_snackbar">
                You are too far from the court to submit a report
            </v-snackbar>

            <button :disabled="submitDataDisabled">
                Update Status
            </button>
        </form>
    </div>
</template>

<style scoped lang="scss">
@use '@/styles/components';
@use '@/styles/abstracts' as *;

* {
    display: flex;
}

input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

$mobile-size: 800px;
$border: 2px solid $pickle-500;
$no-border: 0 solid transparent;

.popup {
    flex-direction: column;
    justify-content: center;
    padding: 0;
    align-items: start;
    background-color: $pickle-50;
    border-top: $no-border;
    border-right: $border;

    @include responsive($mobile-size) {
        flex-direction: row;
        border-right: $no-border;
        border-top: $border;
    }
}

$padding-size: 8px;

.location-info {
    justify-content: start;
    align-self: stretch;
    flex-direction: column;
    flex-grow: 1;
    flex-basis: 100%;
    padding: 0 $padding-size;

    h4 {
        margin: 0;
        margin-top: 1rem;
        margin-bottom: 0.2rem;
        font-size: xx-large;
        line-height: 2rem;
        text-wrap: wrap;

        @include responsive($mobile-size) {
            font-size: x-large;
            line-height: 1.8rem;
        }
    }

    p {
        margin: 0;
        font-size: large;
        line-height: 2rem;

        @include responsive($mobile-size) {
            font-size: medium;
            line-height: 1.5rem;
        }
    }

    sub {
        margin-bottom: 1rem;
        font-size: small;
        color: #888888;

        @include responsive($mobile-size) {
            font-size: small;
            margin-bottom: 0.7rem;
        }
    }
}

.location-title {
    display: flex;
    flex-direction: column;
    justify-content: start;
}

.data-info {
    display: flex;
    flex-direction: column;
    justify-content: start;
    font-size: small;
    align-self: stretch;

    p {
        text-wrap: nowrap;
    }

    a {
        @extend .dark-solid-button;
        margin-bottom: 20px;
        align-self: stretch;

        @include responsive($mobile-size) {
            height: 8px;
        }
    }
}

form {
    flex-direction: column;
    justify-content: space-around;
    align-items: start;
    align-self: stretch;
    padding: 0 8px;
    background-color: #dddddd;
    flex-grow: 1;
    flex-basis: 50%;
    width: auto;
    border-radius: 0;
}

.input-box {
    flex-direction: column;
    align-self: stretch;

    label {
        margin-bottom: 4px;
    }

    input {
        border: none;
        align-self: stretch;
        height: 30px;
    }
}

button {
    @extend .dark-solid-button;
    font-size: x-small;
    height: 2rem;
    margin-top: 1rem;
    line-height: 1rem;
    align-self: stretch;
}

button:disabled {
    border: 1px solid #999999;
    background-color: #cccccc;
    color: #666666;
}
</style>