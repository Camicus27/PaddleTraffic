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
  <div class="profile-page" v-if="myUser">
    <div class="header">
      <h1>{{ myUser.username }}</h1>
      <p class="bio">{{ myUser.bio }}</p>
    </div>
    <div class="info">
      <div class="card skill-level">
        <h2>Skill Level</h2>
        <p>{{ myUser.skill_level }}</p>
      </div>
      <div class="card matches">
        <h2>Match Statistics</h2>
        <div class="statistics">
          <div>Matches Attended: <span>{{ myUser.matches_attended }}</span></div>
          <div>Matches Created: <span>{{ myUser.matches_created }}</span></div>
          <div>Wins: <span>{{ myUser.win_count }}</span></div>
          <div>Losses: <span>{{ myUser.loss_count }}</span></div>
        </div>
      </div>
      <div class="card friends-list">
        <h2>Friends</h2>
        <ul>
          <li v-for="friend in myUser.friends" :key="friend.id">{{ friend.username }}</li>
        </ul>
      </div>
    </div>
  </div>
  <div v-else>
    <h1>User not found or not logged in.</h1>
  </div>
</template>

<style scoped>
.profile-page {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  color: #333;
}

.header h1 {
  color: #71864f; /* Green accent */
  text-align: center;
  font-size: 2rem;
  margin-bottom: 10px;
}

.bio {
  margin-bottom: 20px;
  text-align: center;
  color: #666;
}

.info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.card {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease-in-out;
}

.card:hover {
  transform: translateY(-5px);
}

.statistics {
  display: grid;
  row-gap: 10px;
}

.statistics div {
  display: flex;
  justify-content: space-between;
}

.statistics span {
  font-weight: bold;
}

h2 {
  color: #71864f; /* Green accent */
  text-align: center;
  margin-bottom: 15px;
}

ul {
  list-style-type: none;
  padding: 0;
  margin-top: 0;
}

li {
  border-bottom: 1px solid #eee;
  padding: 8px 0;
}

li:last-child {
  border-bottom: none;
}
</style>
