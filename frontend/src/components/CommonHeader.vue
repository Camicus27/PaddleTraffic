<script setup lang="ts">
import { ref, onMounted, type Ref } from 'vue';
import { RouterLink } from 'vue-router'
import { useDisplay } from 'vuetify'

const { width } = useDisplay()
import { getCurrentUser } from '@/api/functions';
import type { PickleUser } from '@/api/types';

const currentUser: Ref<PickleUser | undefined> = ref(undefined)

onMounted(async () => {
  currentUser.value = await getCurrentUser(true)
})
// This should be undefined when there is no user currently logged in.
const myUser: Ref<any> = ref(undefined);

let URL: string
// This is the collection of environment variables.
const env = import.meta.env
if (env.MODE === 'production')
  URL = env.VITE_PROD_URL
else
  URL = env.VITE_DEV_URL

</script>

<template>
  <header>
    <RouterLink to="/" class="logo">
      <img src="@/assets/logo.png" class="logo" alt="PaddleTraffic Logo" width="64" height="64">
      <h1>PaddleTraffic</h1>
    </RouterLink>

    <v-menu transition="slide-y-transition" v-if="width < 1050">
      <template v-slot:activator="{ props }">
        <v-btn class="hamburger" icon="mdi-menu" v-bind="props"></v-btn>
      </template>

      <div class="burger-contents">
        <RouterLink to="/map" class="nav-bt">Map</RouterLink>
        <RouterLink to="/matchmaking" class="nav-bt">Matchmaking</RouterLink>
        <RouterLink v-if="currentUser?.is_superuser" to="/new-location" class="nav-bt">Proposals</RouterLink>
        <RouterLink to="/about" class="nav-bt">About</RouterLink>
        <div class="burger-spacer"></div>
        <div class="user-buttons">
          <template v-if="currentUser">
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
    <nav v-else>
      <RouterLink to="/map" class="nav-bt">Map</RouterLink>
      <RouterLink to="/matchmaking" class="nav-bt">Matchmaking</RouterLink>
      <RouterLink v-if="currentUser?.is_superuser" to="/new-location" class="nav-bt">Proposals</RouterLink>
      <RouterLink to="/about" class="nav-bt">About</RouterLink>
      <template v-if="currentUser">
        <div class="profile-section">
          <RouterLink to="/profile" class="nav-bt">
            <img src="@/assets/default_user.png" class="pfp" alt="User profile" width="32" height="32">
          </RouterLink>
          <a href="/logout/" class="nav-bt">Logout</a>
        </div>
      </template>
      <template v-else>
        <div class="profile-section">
          <a href="/login/" class="nav-bt">Login</a>
          <a href="/register/" class="nav-bt">Register</a>
        </div>
      </template>
    </nav>
  </header>
</template>

<style scoped lang="scss">
@use '@/styles/components';
@use '@/styles/abstracts' as *;

.nav-bt {
  @extend .nav-button;

  @include responsive($mobile-size) {
    padding: .2rem .25rem;
    margin: .2rem .5rem;
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
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.4);

  a {
    font-size: x-large;
    line-height: 1.6rem;
    padding-bottom: 0.1em;
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
  border-bottom: 2px solid $pickle-500;
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

.profile-section {
  display: flex;
  align-items: center;
  margin-left: 1rem;
  padding-left: 1rem;
  border-left: 1px solid $pickle-500;
}

nav {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  font-size: 1.2rem;

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