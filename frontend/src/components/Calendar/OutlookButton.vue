<script setup lang="ts">
import { outlook } from "calendar-link";
import type { CalendarEvent } from "calendar-link"
import type { UnitType } from "dayjs"
import type { Location } from "@/api/types"

const props = defineProps<{
    title: string
    start: Date
    duration?: [number, UnitType]
    description?: string
    location?: Location
}>()

const calendarEvent: CalendarEvent = {
    title: props.title,
    description: props.description,
    start: props.start,
    duration: props.duration,
    location: props.location?.name
}

const outlookUrl = outlook(calendarEvent)
</script>


<template>
    <a :href="outlookUrl" class="calendar-button" target="_blank">
        <img src="https://res-1.cdn.office.net/shellux/outlook_24x.59692ba8e1f344194426952916c16896.svg" alt="Outlook Logo"
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
    border-radius: 4px;
    box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    /* Subtle shadow */
    transition: background-color 0.3s;
    /* Smooth transition on hover */
}

.calendar-button:hover {
    background-color: $pickle-200;
    /* Slightly darker color on hover */
}

.logo {
    height: 22px;
    margin-right: 8px;
}
</style>