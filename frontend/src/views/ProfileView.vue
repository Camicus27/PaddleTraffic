<script setup lang="ts">
import { ref, onMounted, type Ref } from 'vue';

import axios from 'axios'

// This should be undefined when there is no user currently logged in.
const myUser: Ref<any> = ref(undefined);
const incomingRequests: Ref<any> = ref([]);
const outgoingRequests: Ref<any> = ref([]);
const searchQuery: Ref<string> = ref('');
const searchResults: Ref<any> = ref([]);



let URL: string
// This is the collection of environment variables.
const env = import.meta.env
if (env.MODE === 'production')
  URL = env.VITE_PROD_URL
else
  URL = env.VITE_DEV_URL


onMounted(() => {
  getCurrentUser()
  getFriendRequests()
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

function getFriendRequests() {
  if (!myUser.value) return;

  axios.get(`${URL}/friend-requests/`, { withCredentials: true })
    .then((response) => {
      incomingRequests.value = response.data.incoming;
      outgoingRequests.value = response.data.outgoing;
    })
    .catch((error) => console.error("Failed to fetch friend requests:", error));
}

function acceptFriendRequest(requestId: number) {
  axios.post(`${URL}/friend-requests/accept/${requestId}`, {}, { withCredentials: true })
    .then(() => {
      getFriendRequests(); // Refresh the list of friend requests
    })
    .catch((error) => console.error("Failed to accept friend request:", error));
}

function createFriendRequest(receiverId: number) {
  axios.post(`${URL}/friend-requests/${receiverId}`, {}, { withCredentials: true })
    .then(() => {
      getFriendRequests(); // Refresh the list of friend requests
    })
    .catch((error) => console.error("Failed to create friend request:", error));
}

function searchUsers() {
  if (searchQuery.value.trim() === '') {
    searchResults.value = [];
    return;
  }

  axios.get(`${URL}/users/?search=${searchQuery.value}`, { withCredentials: true })
    .then(response => {
      searchResults.value = response.data.users.filter((user: { id: any; }) => user.id !== myUser.value.id); // Filter out the current user from search results
    })
    .catch(error => console.error('Failed to search users:', error));
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
  <div class="card friend-requests" v-if="incomingRequests.length || outgoingRequests.length">
    <h2>Pending Friend Requests</h2>
    <div>
      <h3>Incoming</h3>
      <ul>
        <li v-for="request in incomingRequests" :key="request.id">
          {{ request.requester.username }}
          <button @click="acceptFriendRequest(request.id)">Accept</button>
        </li>
      </ul>
    </div>
    <div>
      <h3>Outgoing</h3>
      <ul>
        <li v-for="request in outgoingRequests" :key="request.id">
          {{ request.receiver.username }}
          <!-- Optionally, add a cancel button here -->
        </li>
      </ul>
    </div>
  </div>
  <div class="search-section">
    <input type="text" v-model="searchQuery" @input="searchUsers" placeholder="Search Users...">
    <div class="search-results" v-if="searchResults.length > 0">
      <ul>
        <li v-for="user in searchResults" :key="user.id">
          {{ user.username }}
          <button @click="createFriendRequest(user.id)">Add Friend</button>
        </li>
      </ul>
    </div>
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
  color: #71864f;
  /* Green accent */
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
  color: #71864f;
  /* Green accent */
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

.friend-requests h3 {
  color: #71864f;
  /* Darker green for subheadings */
  margin-top: 10px;
}

.friend-requests button {
  margin-left: 10px;
  background-color: #71864f;
  /* Green accent */
  color: white;
  border: none;
  border-radius: 5px;
  padding: 5px 10px;
  cursor: pointer;
}

.friend-requests button:hover {
  background-color: #5a6e3f;
}

.search-section {
  margin-top: 20px;
}

.search-results ul {
  list-style: none;
  padding: 0;
}

.search-results li {
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-results button {
  background-color: #71864f;
  /* Green accent */
  color: white;
  border: none;
  border-radius: 5px;
  padding: 5px 10px;
  cursor: pointer;
}

.search-results button:hover {
  background-color: #5a6e3f;
}
</style>
