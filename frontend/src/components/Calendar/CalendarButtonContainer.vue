<script setup lang="ts">
import type { UnitType } from "dayjs"
import type { Location } from "@/api/types"

import GoogleCalendarButton from "./GoogleCalendarButton.vue"
import ICSButton from "./ICSButton.vue"
import OutlookButton from "./OutlookButton.vue"
import YahooButton from "./YahooButton.vue"
import { onMounted } from "vue"
import { parse } from "date-fns"

const props = defineProps<{
    title: string
    startDate: string
    startTime: string
    duration?: [number, UnitType]
    description?: string
    location?: Location
}>()

const startDateTime = parse(`${props.startDate} ${props.startTime}`, "EEEE, MMMM d, yyyy hh:mmaa", new Date())
</script>


<template>
    <div>
        <GoogleCalendarButton class="m-2" :title="title" :start="startDateTime" :duration="duration"
            :description="description" :location="location">Google</GoogleCalendarButton>
        <OutlookButton class="m-2" :title="title" :start="startDateTime" :duration="duration" :description="description"
            :location="location">Outlook</OutlookButton>
        <YahooButton class="m-2" :title="title" :start="startDateTime" :duration="duration" :description="description"
            :location="location">Yahoo</YahooButton>
        <ICSButton class="m-2" :title="title" :start="startDateTime" :duration="duration" :description="description"
            :location="location">
            ICS</ICSButton>
    </div>
</template>

<style scoped lang="scss">
.m-2 {
    margin: 8px;
}
</style>