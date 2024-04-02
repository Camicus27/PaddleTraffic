<script setup lang="ts">
import GoogleCalendarButton from "./GoogleCalendarButton.vue"
import ICSButton from "./ICSButton.vue"
import OutlookButton from "./OutlookButton.vue"
import YahooButton from "./YahooButton.vue"

defineProps<{
    title: string
    start: Date
    end: Date
    description: string
    location: string
}>()

</script>


<template>
    <GoogleCalendarButton :title="title" :start="start" :end="end" :description="description" :location="location">Google Calendar</GoogleCalendarButton>
    <OutlookButton :title="title" :start="start" :end="end" :description="description" :location="location">Outlook Calendar</OutlookButton>
    <YahooButton :title="title" :start="start" :end="end" :description="description" :location="location">Yahoo Calendar</YahooButton>
    <ICSButton :title="title" :start="start" :end="end" :description="description" :location="location">ICS File</ICSButton>
</template>

<style scoped lang="scss">
</style>