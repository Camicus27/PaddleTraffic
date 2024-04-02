<script setup lang="ts">
import { google } from "calendar-link";
import type { CalendarEvent } from "calendar-link"

const props = defineProps<{
    title: string
    start: Date
    end: Date
    description: string
    location: string
}>()

const calendarEvent: CalendarEvent = {
    title: props.title,
    description: props.description,
    start: props.start,
    end: props.end,
    location: props.location
}

const googleUrl = google(calendarEvent)
</script>


<template>
    <a :href="googleUrl" class="calendar-button" target="_blank">
        <img src="https://www.gstatic.com/images/branding/product/1x/calendar_48dp.png" alt="Google Calendar Logo"
            class="logo">
        <slot></slot>
    </a>

</template>

<style scoped lang="scss">
@use '../../styles/abstracts/_colors' as *;

.calendar-button {
    display: inline-flex;
    align-items: center;
    background-color: white;
    /* Your primary color */
    color: black;
    text-decoration: none;
    padding: 10px 20px;
    border-radius: 6px;
    box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    /* Subtle shadow */
    transition: background-color 0.3s;
    /* Smooth transition on hover */
}

.calendar-button:hover {
    background-color: $pickle-100;
    /* Slightly darker color on hover */
}

.logo {
    height: 22px;
    margin-right: 8px;
}
</style>