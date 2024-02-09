<script setup lang="ts">
import { ref, onMounted, type Ref } from 'vue';

import axios from 'axios'

// This should be undefined when there is no user currently logged in.
const myUser: Ref<any> = ref(undefined);

let URL: string
// This is the collection of environment variables.
const env = import.meta.env
if (env.MODE === 'production')
  URL = env.VITE_PROD_URL
else
  URL = env.VITE_DEV_URL


onMounted(() => {
  getCurrentUser()
})

function getCurrentUser() {
  axios.get(`${URL}/current-user/`)
    .then((response) => {
      if (response.data.user)
        myUser.value = response.data.user
      else
        myUser.value = undefined
    })
    .catch(() => {
      myUser.value = undefined
      // Redirect to login page if the user is not logged in
      window.location.href = '/login';
    })
}

</script>

<template>
  <p>{{ myUser }}</p>
</template>