<script setup lang="ts">
function submitForm() {
    console.log("nice")
}
</script>

<template>
    <div class="info">
        <h3>{{name}}</h3>
        <sub>Courts: {{court_count}}</sub>
        <p>Estimated Courts Occupied: {{courts_occupied}}</p>
        <p>Estimated Groups Waiting: {{number_waiting}}</p>
        <p>Estimated Wait Time: {{formatTime(estimated_wait_time)}}</p>
    </div>
    <form @submit.prevent="submitForm">
        <label for="courtsOccupied">Courts Occupied:</label>
        <input type="number" id="courtsOccupied" name="courtsOccupied" min="0" :max="currSelection.court_count"
            v-model="locForm.courts_occupied" required>
        <label for="numberWaiting">Number Waiting:</label><br>
        <input type="number" id="numberWaiting" name="numberWaiting" min="0"
            :max="(locForm.courts_occupied < currSelection.court_count) ? 0 : 10" v-model="locForm.number_waiting"
            required>
        <button :disabled="submitDataDisabled">
            Update Status
        </button>
    </form>

    <script>

        </script>
</template>

<script>
</script>

<style></style>