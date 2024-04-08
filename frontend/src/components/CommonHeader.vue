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

function getCurrentUser() { // TODO change to be from @/api/functions
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
  <header>
    <RouterLink to="/" class="logo">
      <img src="@/assets/logo.png" class="logo" alt="PaddleTraffic Logo" width="64" height="64">
      <h1>PaddleTraffic</h1>
    </RouterLink>
    <v-menu transition="slide-y-transition">
      <template v-slot:activator="{ props }">
        <v-btn class="hamburger" icon="mdi-menu" v-bind="props"></v-btn>
      </template>

      <div class="burger-contents">
        <RouterLink to="/map" class="nav-bt">MAP</RouterLink>
        <RouterLink to="/matchmaking" class="nav-bt">MATCHMAKING</RouterLink>
        <RouterLink to="/new-location" class="nav-bt">PROPOSALS</RouterLink>
        <RouterLink to="/about" class="nav-bt">ABOUT</RouterLink>
        <div class="burger-spacer"></div>
        <div class="user-buttons">
          <template v-if="myUser">
            <RouterLink to="/profile" class="nav-bt">
              <img src="@/assets/default_user.png" class="pfp" alt="User profile" width="32" height="32">
            </RouterLink>
            <a href="/logout/" class="nav-bt">Logout</a>
          </template>
          <template v-else>
            <a href="/login/" class="nav-bt">Login</a>
            <a href="/register/" class="nav-bt">Register</a>
          </template>
        </div>
      </div>
    </v-menu>
  </header>
</template>

<style scoped lang="scss">
@use '@/styles/components';
@use '@/styles/abstracts' as *;

$mobile-size : 800px;

.nav-bt {
  @extend .nav-button;

  @include responsive($mobile-size) {
    padding: 0 0.3rem;
    font-size: 0.8rem;
  }
}

.hamburger {
  border-radius: 0;
  background-color: transparent;
  box-shadow: none !important; // it's all weird if you don't do important lol. vuetify.
  transition: background-color 0.3 ease;

  &:hover {
    box-shadow: none;
  }

  &:active {
    box-shadow: none;
  }
}

.burger-spacer {
  height: 1rem;
}

.burger-contents {
  display: flex;
  flex-direction: column;
  background-color: $pickle-50;
  padding: 0.8rem 0;
  border-radius: 4px;
  
  a {
    font-size: x-large;
    line-height: 1.6rem;
  }

  @include responsive($mobile-size) {
    padding: 0.3rem 0;
    border-radius: 4px;
    
    a {
      font-size: large;
      line-height: 1.6rem;
    }
  }
}

header {
  display: flex;
  flex-direction: row; // Changed to row to align items horizontally
  align-items: center; // Ensure vertical alignment in the center
  justify-content: space-between; // Space out the logo and navigation
  width: 100%;
  border-bottom: 3px solid $pickle-500;
  background-image: linear-gradient(to top, $pickle-600, $pickle-100);
  flex: 0 1 auto;
}

.left-side {
  display: flex;
  flex-direction: row;
}

.user-buttons {
  display: flex;
  flex-direction: row;
}

nav {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  font-size: 1.25rem;

  @include responsive($mobile-size) {
    width: 100%;
    justify-content: space-around;
  }
}

.logo {
  display: flex;
  flex-direction: row;
  align-items: center;
  text-decoration: none;

  h1 {
    padding-left: .5rem;
    font-size: 2rem;
    font-weight: bold;
    color: $pickle-500;
    text-shadow: 0px 0px 1px #080f0180;
  }

  img {
    width: 55px;
    height: auto;
  }

  @include responsive($mobile-size) {
    img {
      width: 40px;
      height: auto;
    }

    h1 {
      font-size: 1.5rem;
    }
  }
}
</style>