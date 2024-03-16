<script setup lang='ts'>
import { ref } from 'vue'
import axios from 'axios'
import SidebarItem from './SidebarItem.vue'

// name = models.CharField(max_length=255)
// location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='scheduled_events', null=False)
// host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_events', null=False)
// players = models.ManyToManyField(User, related_name='attending_events', blank=True)
// date = models.DateField()
// time = models.TimeField()

let matchList = ref([
  { id: 1, name: 'Kids Tournament', location: 'The playground', host: 'Marissa Langley', players: ['Elena Rodriguez', 'Kaito Nakamura', 'Amina Yusuf'], date: '12/10/2023', time: '12:00 pm' },
  { id: 2, name: 'Thursday Night Pickleball', location: 'SLC Court', host: 'Rajiv Patel', players: ['Lucas Schmidt', 'Jordan Abrams'], date: '1/17/2024', time: '3:00 pm' },
  { id: 3, name: 'Picklecoin Tournament', location: 'Picklecoin HQ', host: 'Theo Zimmerman', players: [], date: '3/28/2024', time: '4:30 pm' }
])

// Uncomment the below code after the prototype demo. The above is dummy data for the events a user is part of

// let URL: string
// // This is the collection of environment variables.
// const env = import.meta.env
// if (env.MODE === 'production')
//   URL = env.VITE_PROD_URL
// else
//   URL = env.VITE_DEV_URL

// axios.get(`${URL}/events`)
//       .then((response) => matchList.value = response.data)
//       .catch((error) => console.log(error))
</script>

<template>
  <div class='sidebar'>
    <SidebarItem
      v-for="{ id, name, location, host, players, date, time } in matchList"
      :key="id"
      :name="name"
      :location="location"
      :host="host"
      :players="players"
      :date="date"
      :time="time"
    />
  </div>
</template>

<style scoped lang="scss">
  // .sidebar {
  //   display: flex;
  //   flex-direction: column;
  //   align-items: start;
  //   width: 20%;
  //   margin-right: 2.5rem;
  // }
</style>
