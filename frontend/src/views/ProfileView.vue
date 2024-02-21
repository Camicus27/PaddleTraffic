<script setup lang="ts">
import { ref, onMounted, watch, type Ref } from 'vue'

import axios from 'axios'

// This should be undefined when there is no user currently logged in.
const myUser: Ref<any> = ref(undefined)
const incomingRequests: Ref<any> = ref([])
const outgoingRequests: Ref<any> = ref([])
const searchQuery: Ref<string> = ref('')
const users: Ref<any> = ref([])
const searchResults: Ref<any> = ref([])

let URL: string
// This is the collection of environment variables.
const env = import.meta.env
if (env.MODE === 'production') URL = env.VITE_PROD_URL
else URL = env.VITE_DEV_URL

onMounted(async () => {
  await getCurrentUser()
  await getFriendRequests()
  await fetchUsers()
})

async function getCurrentUser() {
  try {
    const response = await axios.get(`${URL}/current-user/`)
    if (response.data.user) {
      myUser.value = response.data.user
    } else myUser.value = undefined
  } catch {
    myUser.value = undefined
    // Redirect to login page if the user is not logged in
    window.location.href = '/login'
  }
}

async function getFriendRequests() {
  try {
    const response = await axios.get(`${URL}/friend-requests/`, { withCredentials: true })
    incomingRequests.value = response.data.incoming_requests
    outgoingRequests.value = response.data.outgoing_requests
  } catch (error) {
    return console.error('Failed to fetch friend requests:', error)
  }
}

async function acceptFriendRequest(requestId: number) {
  try {
    await axios.post(`${URL}/friend-requests/accept/${requestId}/`, {}, { withCredentials: true })
    await getCurrentUser()
    console.log(myUser.value)
    await getFriendRequests() // Refresh the list of friend requests
    runFilter()
  } catch (error) {
    return console.error('Failed to accept friend request:', error)
  }
}

async function createFriendRequest(receiverId: number) {
  try {
    await axios.post(`${URL}/friend-requests/${receiverId}/`, {}, { withCredentials: true })
    await getFriendRequests() // Refresh the list of friend requests
    runFilter()
  } catch (error) {
    return console.error('Failed to create friend request:', error)
  }
}

async function deleteFriendRequest(reqId: number) {
  try {
    await axios.delete(`${URL}/friend-requests/${reqId}/`, { withCredentials: true })
    await getFriendRequests()
    runFilter()
  } catch (error) {
    return console.error('Failed to delete friend request:', error)
  }
}

async function fetchUsers() {
  try {
    const response = await axios.get(`${URL}/users/`, { withCredentials: true })
    users.value = response.data.users
  } catch (error) {
    return console.error('Failed to fetch users:', error)
  }
}

watch(searchQuery, () => {
  runFilter()
})

function runFilter() {
  if (searchQuery.value.trim() === '') {
    searchResults.value = []
  } else {
    const requestedUserIds = new Set([
      ...incomingRequests.value.map((request: { requester: { id: any } }) => request.requester.id),
      ...outgoingRequests.value.map((request: { receiver: { id: any } }) => request.receiver.id)
    ])
    console.log('Outgoing requests:')
    console.log(outgoingRequests.value)

    searchResults.value = users.value.filter(
      (user: { username: string; id: any }) =>
        user.username.toLowerCase().includes(searchQuery.value.toLowerCase()) &&
        user.id !== myUser.value.id && // Exclude the current user
        !requestedUserIds.has(user.id) // Exclude users with pending friend requests
    )
  }
}
</script>

<template>
  <div class="profile-page" v-if="myUser">
    <!-- Player Stats and Bio -->
    <div class="header">
      <h1>{{ myUser.username }}</h1>
      <h3>
        <span v-if="myUser.first_name">{{ myUser.first_name }}</span
        >&nbsp;<span v-if="myUser.last_name">{{ myUser.last_name }}</span>
      </h3>
      <p class="bio">{{ myUser.bio }}</p>
    </div>
    <div class="player-info">
      <div class="info">
        <div class="card skill-level">
          <h2>Skill Level</h2>
          <p>{{ myUser.skill_level }}</p>
        </div>
        <div class="card matches">
          <h2>Match Statistics</h2>
          <div class="statistics">
            <div>
              Matches Attended: <span>{{ myUser.matches_attended }}</span>
            </div>
            <div>
              Matches Created: <span>{{ myUser.matches_created }}</span>
            </div>
            <div>
              Wins: <span>{{ myUser.win_count }}</span>
            </div>
            <div>
              Losses: <span>{{ myUser.loss_count }}</span>
            </div>
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
    <!-- Two Column Layout for Friend Requests and Search -->
    <div class="columns">
      <!-- Friend Requests Column -->
      <div class="column friend-requests">
        <h2>Friend Requests</h2>
        <div>
          <h3>Incoming</h3>
          <ul>
            <li v-for="request in incomingRequests" :key="request.id">
              {{ request.requester.username }}
              <button @click="acceptFriendRequest(request.id)" class="button accept">Accept</button>
              <button @click="deleteFriendRequest(request.id)" class="button delete">Delete</button>
            </li>
          </ul>
        </div>
        <div>
          <h3>Outgoing</h3>
          <ul>
            <li v-for="request in outgoingRequests" :key="request.id">
              {{ request.receiver.username }}
              <button @click="deleteFriendRequest(request.id)" class="button delete">Delete</button>
            </li>
          </ul>
        </div>
      </div>

      <!-- Search and Add Friends Column -->
      <div class="column search-add-friends">
        <h2>Add Friends</h2>
        <div class="search-section">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Search Users..."
            class="search-box"
          />
          <div class="search-results" v-if="searchResults.length">
            <ul>
              <li v-for="user in searchResults" :key="user.id">
                {{ user.username }}
                <button @click="createFriendRequest(user.id)">Add Friend</button>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-else>
    <h1>User not found or not logged in.</h1>
  </div>
</template>

<style scoped>
.profile-page {
  max-width: 1600px;
  margin: 20px auto;
  padding: 20px;
  color: #333;
}

.player-info {
  display: flex;
  flex-direction: row;
  text-align: center;
}

.header h1 {
  color: #4b5320;
  /* Green accent */
  text-align: center;
  font-size: 2rem;
  margin-bottom: 10px;
  font-size: 3em;
}

.header h3 {
  color: #4b5320;
  /* Green accent */
  text-align: center;
  font-size: 2rem;
  margin-top: 20px;
  font-size: 1.5em;
}

.bio {
  margin-bottom: 20px;
  text-align: center;
  color: #666;
}

.info {
  display: block;
  /* grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); */
  /* gap: 20px; */
  margin: 20px auto;
  text-align: center;
}

.card {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease-in-out;
  margin-top: 15px;
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
  text-align: center;
}

.search-box {
  padding: 10px 20px;
  font-size: 16px;
  border: 2px solid #71864f; /* Themed green border */
  border-radius: 20px; /* Rounded corners for a modern look */
  width: 80%; /* Responsive width */
  max-width: 400px; /* Maximum width to maintain aesthetics */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
  outline: none; /* Remove the default focus outline */
}

.search-box:focus {
  border-color: #5a6e3f; /* Darker green on focus for better visibility */
}

.search-results ul {
  list-style: none;
  padding: 0;
  text-align: left;
  margin-top: 10px;
}

.search-results li {
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-results button {
  background-color: #71864f; /* Green accent */
  color: white;
  border: none;
  border-radius: 5px;
  padding: 5px 10px;
  transition:
    background-color 0.3s,
    transform 0.1s;
  cursor: pointer;
}

.search-results button:hover {
  background-color: #5a6e3f;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.search-results button:active {
  background-color: #4d5a33;
  transform: translateY(1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.columns {
  display: flex;
  margin-top: 20px;
}

.column {
  flex: 1; /* Each column takes up equal space */
  padding: 0 15px; /* Spacing between columns */
  margin: 5px 15px;
}

.friend-requests,
.search-add-friends {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  min-width: 350px;
}

.search-results ul,
.friend-requests ul {
  list-style: none;
  padding: 0;
}

.search-results li,
.friend-requests li {
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.button {
  padding: 5px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition:
    background-color 0.3s,
    transform 0.1s;
  margin-left: 10px;
  color: white;
  font-weight: bold;
}

.button:hover {
  transform: translateY(-2px);
}

.accept {
  background-color: #71864f; /* Your theme's green */
}

.accept:hover {
  background-color: #5a6e3f; /* A darker shade of green for hover */
}

.delete {
  background-color: #d9534f; /* A subtle red for delete */
}

.delete:hover {
  background-color: #c9302c; /* A darker shade of red for hover */
}
</style>
