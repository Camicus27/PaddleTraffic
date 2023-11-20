<script setup lang="ts">
import { ref } from 'vue'
import SidebarItem from "./SidebarItem.vue"

let matchList = ref([
    {loc: "The playground", time: "12:00 pm", skillLvl: "beginner"},
    {loc: "Picklecoin Tournament", time: "3:00 pm", skillLvl: "advanced"},
])
</script>

<template>
  <div class="sidebar">
        <SidebarItem v-for="{loc, time, skillLvl} in matchList" :location="loc" :time="time" :skillLevel="skillLvl"/>
  </div>
</template>

<style scoped></style>
