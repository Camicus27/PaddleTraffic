<script setup lang="ts">
import CommonHeader from '@/components/CommonHeader.vue';

const env = import.meta.env
let map_src: string
if (env.MODE === 'production')
  map_src = '/static/map_screenshot.png'
else
  map_src = 'map_screenshot.png'
</script>

<template>
  <CommonHeader />
  <div class="about">
    <header>
      <h1>About PaddleTraffic</h1>
    </header>
    <nav>
      <v-btn color="#183400" @click="$router.push('/staff')" variant="outlined">Our Team</v-btn>
      <v-btn color="#183400" @click="$router.push('/tutorial')" variant="outlined">Tutorials</v-btn>
    </nav>

    <div>
      <p class="text-center">PaddleTraffic is a community-driven web application designed to streamline the process of finding and using
        pickleball courts. Our mission is to help players spend less time searching and more time playing.</p>

      <img :src="map_src" alt="Map Overview">
      <div class="py-4">
        <h2>Key Features</h2>
        <ul>
          <li>Dynamic Court Map: View nearby courts, their availability, and real-time busyness levels.</li>
          <li>Estimated Wait Times: Our algorithms calculate estimated wait times to help you plan your outing.</li>
          <li>User Profiles & Connections: Create a profile, track your stats, connect with other players, and form
            teams.
          </li>
          <li>Community-Powered Data: PaddleTraffic leverages user-submitted information to provide the most accurate
            and
            up-to-date court details.</li>
          <li>Matchmaking & Event Creation: Easily find players at your skill level, organize games, and schedule
            events.
          </li>
          <li>Propose New Locations: Help expand our database by suggesting pickleball courts that aren't yet listed.
          </li>
        </ul>
      </div>

      <div class="py-4">
        <h2>Technologies</h2>
        <ul>
          <li>Django Backend: A robust framework for user management, data handling, API functionality.</li>
          <li>Vue Frontend: Delivers a responsive and user-friendly interface.</li>
          <li>Mapbox: Provides interactive mapping and location services.</li>
        </ul>
      </div>
      <div class="py-4">
        <h2>Join the PaddleTraffic Community</h2>
        <p class="text-center">Whether you're a casual player or a seasoned competitor, PaddleTraffic makes it easier to find your place on
          the court.</p>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@use '@/styles/abstracts' as *;
$mobile-size: 800px;

nav {
  display: flex;
  justify-content: center;
  padding: 12px;
  width: 50svw;
  gap: 12px;

  @include responsive($mobile-size) {
    flex-direction: column;
  }
}

img {
  padding: 40px 0;
  width: 100%;
  height: auto;
}

button:hover {
  background-color: lighten($pickle-100, 15%);
}

.about {
  @extend %main-page;
  width: 60%;

  @include responsive($mobile-size) {
    width: 90%;
  }

  p {
    font-size: 1.2em;
    line-height: 1.5rem;

    @include responsive($mobile-size) {
      font-size: 1rem;
      line-height: 1.15rem;
    }
  }
}
</style>
