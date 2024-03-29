<script setup lang="ts">
import { onMounted, ref, type ComputedRef, type Ref, toRef } from 'vue';
import type { Location, Report } from '@/api/types';
import { postLocationReport } from '@/api/functions';

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
    if (!props.location) return
    // timeout the button
    submitDataDisabled.value = true
    setTimeout(() => {
        submitDataDisabled.value = false
    }, 3000)
    postLocationReport(props.location.value.id, locForm.value).then((l) => {
        if(props.location) {
            if(l) props.location.value = l
            props.onSubmitCallback(props.location?.value.id)
        }
    })
}
</script>

<template>
    <div class="popup">
        <div class="location-info">
            <div class="location-title">
                <h4>{{ props.location?.value.name }}</h4>
                <sub>Courts: {{ props.location?.value.court_count }}</sub>
            </div>
            <div class="data-info">
                <p>Est. Courts Occupied: {{ props.location?.value.courts_occupied }}</p>
                <p>Est. Groups Waiting: {{ props.location?.value.number_waiting }}</p>
                <p>Est. Wait: {{ props.location?.value.estimated_wait_time }}</p>
            </div>
        </div>
        <form @submit.prevent="submitForm">
            <label for="courtsOccupied">Courts Occupied:</label>
            <input type="number" id="courtsOccupied" name="courtsOccupied" min="0" :max="props.location?.value.court_count"
                v-model="locForm.courts_occupied" required>
            <label for="numberWaiting">Groups Waiting:</label>
            <input type="number" id="numberWaiting" name="numberWaiting" min="0"
                :max="(locForm.courts_occupied < (props.location?.value.court_count ?? 0)) ? 0 : 10" v-model="locForm.number_waiting"
                required>
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

.popup {
    flex-direction: column;
    justify-content: center;
    padding: 2px;
    align-items: center;
    width: calc((1/4)*100vw);
    background-color: $pickle-50;
}

$padding-size: 8px;
.location-info {
    justify-content: start;
    align-items: start;
    flex-direction: column;
    flex-grow: 3;
    width: calc(100% - $padding-size);
    padding: 0 $padding-size;
    h4 {
        margin: 0;
        margin-top: 1rem;
        margin-bottom: 0.2rem;
        font-size: xx-large;
        line-height: 2rem;
    }

    p {
        margin: 0;
        font-size: large;
        line-height: 2rem;
    }

    sub {
        margin-bottom: 1rem;
        font-size: medium
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
    background-color: #dddddd;
    flex-grow: 2;
    width: calc(100% - $padding-size);
    padding: 0 $padding-size;
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
</style>