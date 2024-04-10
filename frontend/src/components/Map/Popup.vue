<script setup lang="ts">
import { onMounted, ref, type ComputedRef, type Ref, toRef, computed } from 'vue';
import type { Location, Report } from '@/api/types';
import { postLocationReport } from '@/api/functions';
import { formatDistanceToNow } from 'date-fns';
import QRCode from './QRCode.vue';

const props = defineProps<{
    location: Ref<Location>,
    onSubmitCallback: (locationId: number) => void,
}>()

const locForm: Ref<Report> = ref({
    courts_occupied: 0,
    number_waiting: 0
})

const submitDataDisabled = ref<boolean>(false)
const qr_dialog = ref<boolean>(false)
const loc_dialog = ref<boolean>(false)

const success_snackbar = ref<boolean>(false)
const outofrange_snackbar = ref<boolean>(false)
const toomany_snackbar = ref<boolean>(false)

const qrcode_cmp = ref()

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
            (response) => {
                if (response) {
                    if (response.status === 200 && response.data.location) {
                        location.value = response.data.location
                        props.onSubmitCallback(location.value.id)
                        success_snackbar.value = true
                    } else if (response.status === 401) {
                        outofrange_snackbar.value = true
                    } else if (response.status === 429) {
                        toomany_snackbar.value = true
                    } else {
                        console.error(`Server Error Occurred ${response.status}`)
                    }
                }
            }
        )
}

const navigatorFailCallback = () => {
    loc_dialog.value = true
}

function submitForm() {
    let location = props.location
    if (!location) return
    // timeout the button
    submitDataDisabled.value = true
    if (locForm.value.number_waiting > 10) {
        return
    }

    setTimeout(() => {
        submitDataDisabled.value = false
    }, 1500)

    var options = {
        enableHighAccuracy: true,
        timeout: 3000,
        maximumAge: 1000 * 60 * 5 // 5 mins in ms
    }

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => navigatorSuccessCallback(position, location),
            () => { navigatorFailCallback() }, // geolocation NOT ENABLED or an ERROR occurred
            options
        )
    } else {
        navigatorFailCallback() // geolocation NOT ENABLED
    }
}

const location_url = computed(() => {
    const l = props.location.value
    return `https://paddletraffic.net/map/?lat=${l.latitude}&lon=${l.longitude}`
})


const download = () => {
    let d = qrcode_cmp.value.download
    if (d) {
        d(`${props.location.value.name}-QRCode`)
    }
}

const courtsOccupiedError = ref(' ')
const groupsWaitingError = ref(' ')

function validateFormInputs() {
    let error_flag = false
    if (locForm.value.courts_occupied < 0) {
        courtsOccupiedError.value = 'Must be over 0'
        error_flag = true
    } else if (locForm.value.courts_occupied > props.location.value.court_count) {
        courtsOccupiedError.value = `Must be under ${props.location.value.court_count}`
        error_flag = true
    } else {
        courtsOccupiedError.value = ' '
    }

    if (locForm.value.number_waiting < 0) {
        groupsWaitingError.value = 'Must be over 0'
        error_flag = true
    } else if ( // Courts Available Case
        0 <= locForm.value.courts_occupied
        && locForm.value.courts_occupied < props.location.value.court_count
        && locForm.value.number_waiting > 0
    ) {
        groupsWaitingError.value = `Open courts, must be 0`
        error_flag = true
    } else if (locForm.value.number_waiting > 10) {
        groupsWaitingError.value = `Must under 10`
        error_flag = true
    } else {
        groupsWaitingError.value = ' '
    }

    submitDataDisabled.value = error_flag
}
</script>

<template>
    <div class="popup">
        <div class="location-info">
            <h4 class="location-title mb-2">{{ props.location.value.name }}</h4>
            <sub class="mb-6">Courts: {{ props.location.value.court_count }}</sub>
            <div class="data-info">
                <p>Courts Occupied: {{ props.location.value.courts_occupied }}</p>
                <p>Groups Waiting: {{ props.location.value.number_waiting }}</p>
                <p class="mb-2">Wait Time: {{ formatTime(props.location.value.estimated_wait_time ?? 0) }}</p>
                <sub class="mb-6">Last estimate {{ formatDateTime(props.location.value.calculated_time ?? "") }}</sub>
                <div class="direction-qr">
                    <a class="direction-bt"
                        :href="`https://maps.google.com/?q=${props.location.value.latitude},${props.location.value.longitude}`"
                        target="_blank">Get Directions</a>
                    <img @click="qr_dialog = true" class="qr-icon" src="@/assets/IconQR.png" />
                </div>

                <v-dialog class="qr-dialog" v-model="qr_dialog" max-width="290">
                    <v-card>
                        <QRCode ref="qrcode_cmp" :url="location_url" />
                        <v-card-actions class="qr-actions">
                            <v-btn @click="qr_dialog = false">BACK</v-btn>
                            <img class="download-bt" @click="download" src="@\assets\downloadIconGreen.png">
                        </v-card-actions>
                    </v-card>
                </v-dialog>

            </div>
        </div>
        <form @submit.prevent="submitForm">
            <div class="title">Report Status</div>
            <div class="input-box">
                <label for="courtsOccupied">Courts Occupied:</label>
                <input type="number" id="courtsOccupied" name="courtsOccupied" v-model="locForm.courts_occupied"
                    @input="validateFormInputs" required>
                <span class="error-message">{{ courtsOccupiedError }}</span>
            </div>
            <div class="input-box">
                <label for="numberWaiting">Groups Waiting:</label>
                <input type="number" id="numberWaiting" name="numberWaiting" v-model="locForm.number_waiting"
                    @input="validateFormInputs" required>
                <span class="error-message">{{ groupsWaitingError }}</span>
            </div>

            <v-dialog v-model="loc_dialog" persistent max-width="290">
                <v-card>
                    <v-card-title class="headline">Location Required</v-card-title>
                    <v-card-text>
                        This service requires access to your location. Please enable location services in your browser
                        settings.
                    </v-card-text>
                    <v-card-actions>
                        <v-btn @click="loc_dialog = false">OK</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>

            <v-snackbar color="success" :timeout="2000" v-model="success_snackbar">
                <v-icon icon="mdi-check-bold" />
                Report Successfully Sent
            </v-snackbar>

            <v-snackbar color="red-darken-2" :timeout="2000" v-model="outofrange_snackbar">
                <v-icon icon="mdi-alert-circle" />
                You are too far from the court to submit a report
            </v-snackbar>

            <v-snackbar color="orange-darken-2" :timeout="2000" v-model="toomany_snackbar">
                <v-icon icon="mdi-alert" />
                You have submitted too many requests recently
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

$border: 2px solid $pickle-500;
$no-border: 0 solid transparent;

.title {
    font-weight: bold;
    font-size: large;
    border-bottom: 1px solid grey;
    align-self: stretch;

    @include responsive($mobile-size) {
        font-size: medium;
        line-height: 1rem;
    }
}

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

.direction-qr {
    flex-direction: row;
    align-items: end;
    justify-content: start;
}

.qr-actions {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;

    button {
        margin: 0;
        align-self: auto;
    }
}

.qr-icon {
    border-radius: 4px;
    background-color: $pickle-300;
    width: 44px;
    height: 44px;
    cursor: pointer;

    @include responsive($mobile-size) {
        height: 32px;
        width: 32px;
    }
}

.download-bt {
    background-color: white;

    cursor: pointer;
    transition: background-color 0.4s ease;
    border-radius: 4px;

    &:hover {
        background-color: $pickle-100;
    }

    &:active {
        background-color: lighten($pickle-100, 30%);
    }

    $img-size: 48px;
    height: $img-size;
    width: $img-size;
    padding: 0;
    margin: 0;

}

$padding-size: 8px;

.error-message {
    color: darken(red, 3%);
    font-size: 0.7rem;
    font-weight: bold;
}

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

h4.location-title {
    display: -webkit-box;
    /* Set display mode to box */
    -webkit-box-orient: vertical;
    /* Set box orientation to vertical */
    overflow: hidden;
    /* Hide any overflowing text */
    text-overflow: ellipsis;
    /* Display ellipsis for text overflow */
    -webkit-line-clamp: 2;
    /* Limit number of lines */
    max-height: 2.5em;
    /* Set maximum height */
    line-height: 1em;
    /* Set line height to control vertical spacing */
    font-size: 2em;
    padding-bottom: 0.12em; // make space for y & g characters

    @include responsive($mobile-size) {
        font-size: 1.6em;
    }

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
        margin-right: 4px;
        align-self: stretch;
        flex: 1;

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

    @include responsive($mobile-size) {
        flex-basis: 70%;
    }
}

.input-box {
    flex-direction: column;
    align-self: stretch;

    label {
        margin-bottom: 4px;
        font-size: smaller;
        font-weight: 600;
    }

    input {
        border: none;
        align-self: stretch;
        height: 30px;
    }

    @include responsive($mobile-size) {
        font-size: 0.98rem;
        line-height: 1rem;

        label {
            margin-bottom: 0;
        }
    }
}

button {
    @extend .dark-solid-button;
    font-size: medium;
    height: 2rem;
    margin-top: 1rem;
    line-height: 1rem;
    align-self: stretch;
    margin-bottom: 6px;

    @include responsive($mobile-size) {
        font-size: 0.7rem;
    }
}

button:disabled {
    border: 1px solid #999999;
    background-color: #cccccc;
    color: #666666;
}

.direction-bt {
    min-height: 32px;
    font-size: large !important;

    @include responsive($mobile-size) {
        font-size: 0.9rem !important;
    }
}
</style>