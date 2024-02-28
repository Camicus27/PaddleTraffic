<script setup lang="ts">
import { ref, onMounted, watch, type Ref } from 'vue'
import { useRoute } from 'vue-router'

import axios from 'axios'

const route = useRoute()
// This should be undefined when there is no user currently logged in.

const incomingRequests: Ref<any> = ref([])
const outgoingRequests: Ref<any> = ref([])
const searchQuery: Ref<string> = ref('')
const users: Ref<any> = ref([])
const searchResults: Ref<any> = ref([])

const pageUser: Ref<any> = ref(undefined)

const username: Ref<string> = ref(route.params.username as string)
const routeUser: Ref<any> = ref(undefined)
const myUser: Ref<any> = ref(undefined)

enum Relationship {
  Same,
  Friends,
  Requested,
  NotFriends,
  Invalid
}

const usersAreFriends: Ref<Relationship> = ref(Relationship.Invalid)

const doneLoading: Ref<boolean> = ref(false)

let URL: string
// This is the collection of environment variables.
const env = import.meta.env
if (env.MODE === 'production') URL = env.VITE_PROD_URL
else URL = env.VITE_DEV_URL

onMounted(async () => {
  await getCurrentUser()
  if (myUser.value) {
    await getFriendRequests()
    await fetchUsers()
  }
  await handleRouteChange()
})

function redirect(path: string) {
  window.location.href = path
}

async function handleRouteChange() {
  // Perform actions based on the route change
  username.value = route.params.username as string
  if (username.value) {
    await fetchUser(username.value)
    pageUser.value = routeUser.value
  } else {
    routeUser.value = undefined
    pageUser.value = myUser.value
  }
  usersAreFriends.value = checkFriendshipStatus()
  doneLoading.value = true
}

async function getCurrentUser() {
  try {
    const response = await axios.get(`${URL}/current-user/`)
    if (response.data.user) {
      myUser.value = response.data.user
    } else myUser.value = undefined
  } catch {
    myUser.value = undefined
    // Redirect to login page if the user is not logged in
    if (!username.value) redirect('/login')
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
    usersAreFriends.value = checkFriendshipStatus()
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

async function fetchUser(username: string) {
  try {
    const response = await axios.get(`${URL}/users/${username}`, { withCredentials: true })
    routeUser.value = response.data.user
  } catch (error) {
    return console.error('Failed to fetch users:', error)
  }
}

watch(searchQuery, () => {
  runFilter()
})

watch(route, () => {
  handleRouteChange()
})

function runFilter() {
  if (searchQuery.value.trim() === '') {
    searchResults.value = []
  } else {
    const excludedUserIds = new Set([
      ...incomingRequests.value.map((request: { requester: { id: any } }) => request.requester.id),
      ...outgoingRequests.value.map((request: { receiver: { id: any } }) => request.receiver.id),
      // Add the current user's ID to exclude them from the results
      myUser.value.id,
      // Add all of the current user's friends' IDs to exclude them as well
      ...myUser.value.friends.map((friend: { id: any }) => friend.id)
    ])

    searchResults.value = users.value.filter(
      (user: { username: string; id: any }) =>
        user.username.toLowerCase().includes(searchQuery.value.toLowerCase()) &&
        !excludedUserIds.has(user.id) // Exclude users based on the updated set
    )
  }
}

function checkFriendshipStatus() {
  // Ensure both users are defined before proceeding
  if (!myUser.value || !routeUser.value) return Relationship.Invalid

  const currentUserId = myUser.value.id
  const routeUserId = routeUser.value.id

  if (currentUserId === routeUserId) return Relationship.Same

  // Check if they are already friends
  const isAlreadyFriends = myUser.value.friends.some((friend: any) => friend.id === routeUserId)

  if (isAlreadyFriends) return Relationship.Friends

  // Check for pending friend requests from the current user to the route user
  const hasOutgoingRequest = outgoingRequests.value.some(
    (request: any) => request.receiver.id === routeUserId
  )

  // Check for pending friend requests from the route user to the current user
  const hasIncomingRequest = incomingRequests.value.some(
    (request: any) => request.requester.id === routeUserId
  )

  if (hasOutgoingRequest || hasIncomingRequest) return Relationship.Requested

  return Relationship.NotFriends
}

// Call this function at the appropriate place in your component, for example, after both users' data has been fetched
</script>

<template>
  <div v-if="pageUser && (!username || routeUser)" id="profile-page-wrapper">
    <div class="header">
      <h1>{{ pageUser.username }}</h1>
      <h3>
        <span v-if="pageUser.first_name">{{ pageUser.first_name }}</span
        >&nbsp;<span v-if="pageUser.last_name">{{ pageUser.last_name }}</span>
      </h3>
      <p class="bio">{{ pageUser.bio }}</p>
    </div>
    <div class="columns">
      <!-- Player Stats and Bio -->
      <div class="column">
        <div v-if="usersAreFriends === Relationship.NotFriends">
          <button class="friend-button" @click="createFriendRequest(routeUser.id)">
            Add Friend
          </button>
        </div>
        <div v-else-if="usersAreFriends === Relationship.Friends">
          You are friends with {{ pageUser.username }}.
        </div>
        <div v-else-if="usersAreFriends === Relationship.Requested">
          You have a pending friend request with {{ pageUser.username }}.
        </div>
        <div v-else-if="!myUser && usersAreFriends === Relationship.Invalid">
          Please <a href="/login/">sign in</a> to send a friend request to {{ pageUser.username }}.
        </div>
        <div class="player-info">
          <div class="info">
            <div class="card skill-level">
              <h2>Skill Level</h2>
              <p>{{ pageUser.skill_level }}</p>
            </div>
            <div class="card matches">
              <h2>Match Statistics</h2>
              <div class="statistics">
                <div>
                  Matches Attended: <span>{{ pageUser.matches_attended }}</span>
                </div>
                <div>
                  Matches Created: <span>{{ pageUser.matches_created }}</span>
                </div>
                <div>
                  Wins: <span>{{ pageUser.win_count }}</span>
                </div>
                <div>
                  Losses: <span>{{ pageUser.loss_count }}</span>
                </div>
              </div>
            </div>
            <div v-if="pageUser.friends" class="card friends-list">
              <h2>Friends</h2>
              <ul>
                <li v-for="friend in pageUser.friends" :key="friend.id">
                  <a class="profile-link" :href="`/profile/${friend.username}`">{{
                    friend.username
                  }}</a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <!-- Two Column Layout for Friend Requests and Search -->
      <div class="column" v-if="!routeUser">
        <!-- Friend Requests Column -->
        <div class="friend-requests card">
          <h2>Friend Requests</h2>
          <div>
            <h3>Incoming</h3>
            <ul>
              <li v-for="request in incomingRequests" :key="request.id">
                <a class="profile-link" :href="`/profile/${request.requester.username}`">{{
                  request.requester.username
                }}</a>
                <button @click="acceptFriendRequest(request.id)" class="button accept">
                  Accept
                </button>
                <button @click="deleteFriendRequest(request.id)" class="button delete">
                  Delete
                </button>
              </li>
            </ul>
          </div>
          <div>
            <h3>Outgoing</h3>
            <ul>
              <li v-for="request in outgoingRequests" :key="request.id">
                <a class="profile-link" :href="`/profile/${request.receiver.username}`">{{
                  request.receiver.username
                }}</a>
                <button @click="deleteFriendRequest(request.id)" class="button delete">
                  Delete
                </button>
              </li>
            </ul>
          </div>
        </div>

        <!-- Search and Add Friends Column -->
        <div class="search-add-friends card">
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
                  <a class="profile-link" :href="`/profile/${user.username}`">{{
                    user.username
                  }}</a>
                  <button @click="createFriendRequest(user.id)">Add Friend</button>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-else-if="doneLoading" class="error-template">
    <h2>User Not Found</h2>
    <p>We're sorry, but the user you are looking for does not exist or may have been removed.</p>
    <button @click="redirect('/')" class="button">Go to Home</button>
  </div>
</template>