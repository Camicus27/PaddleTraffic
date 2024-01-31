<script setup lang="ts">
import { ref, onMounted, type Ref } from 'vue';
import { RouterLink } from 'vue-router'

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
    })
}

</script>

<template>
  <div id="profile-login">
    <!-- <a href="logout/" v-if="myUser" class="logout-btn">Logout</a>
    <a href="login/" v-else class="login-btn">Login</a> -->
    <a v-if="myUser" href="/login/">
      <img src="@/assets/default_user.png" class="pfp" alt="User profile" width="32" height="32">
    </a>
    <a v-else href="/register/">
      <img src="@/assets/default_user.png" class="pfp" alt="User profile" width="32" height="32">
    </a>

  </div>
  <header id="site-header">
    <div id="logo-title">
      <RouterLink to="/">
        <img src="@/assets/logo.png" class="logo" alt="PaddleTraffic Logo" width="64" height="64">
        <h1>PaddleTraffic</h1>
      </RouterLink>
    </div>
    <nav>
      <RouterLink to="/">HOME</RouterLink>
      <RouterLink to="/map">MAP</RouterLink>
      <RouterLink to="/matchmaking">MATCHMAKING</RouterLink>
      <RouterLink to="/about">ABOUT</RouterLink>
    </nav>
  </header>
</template>

<style scoped>
.logout-btn,
.login-btn {
  padding: 5px;
  margin-inline: 1rem;
  border-radius: 2px;
  text-shadow: 0px 0px 1px #080f01a0;
  text-decoration: none;
  color: #234a00;
  transition: background-color 0.3s, color 0.3s;
  font-size: large;
  font-weight: bolder;
}

.logout-btn:active,
.login-btn:active {
  color: #ffffff;
}

.logout-btn:hover,
.login-btn:hover {
  color: #142b00;
  background-color: #83b325;
}
</style>