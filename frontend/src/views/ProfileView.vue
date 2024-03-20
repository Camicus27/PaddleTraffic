<script setup lang="ts">
import { ref, onMounted, watch, type Ref } from 'vue'
import { useRoute } from 'vue-router'

import axios from 'axios'
import CommonHeader from '@/components/CommonHeader.vue';

import { getCurrentUser, getFriendRequests } from '@/api/functions';
import type { FriendRequest, PickleUser, RestrictedUser } from '@/api/types';

const route = useRoute()
// This should be undefined when there is no user currently logged in.

const incomingRequests: Ref<Array<FriendRequest>> = ref([])
const outgoingRequests: Ref<Array<FriendRequest>> = ref([])
const searchQuery: Ref<string> = ref('')
const users: Ref<any> = ref([])
const searchResults: Ref<any> = ref([])

const pageUser: Ref<any> = ref(undefined)

const username: Ref<string> = ref(route.params.username as string)
const routeUser: Ref<any> = ref(undefined)
const myUser: Ref<PickleUser | undefined> = ref(undefined)

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
  myUser.value = await getCurrentUser(URL, true)
  if (!myUser.value && !username.value)
    redirect("/login")
  if (myUser.value) {
    const requests = await getFriendRequests(URL, true) // Refresh the list of friend requests
    if (requests)
      ({ incoming_requests: incomingRequests.value, outgoing_requests: outgoingRequests.value } = requests)
    else {
      incomingRequests.value = []
      outgoingRequests.value = []
    }
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

async function acceptFriendRequest(requestId: number) {
  try {
    await axios.post(`${URL}/friend-requests/accept/${requestId}/`, {}, { withCredentials: true })
    myUser.value = await getCurrentUser(URL, true)
    console.log(myUser.value)
    const requests = await getFriendRequests(URL, true) // Refresh the list of friend requests
    if (requests)
      ({ incoming_requests: incomingRequests.value, outgoing_requests: outgoingRequests.value } = requests)
    else {
      incomingRequests.value = []
      outgoingRequests.value = []
    }

    runFilter()
  } catch (error) {
    return console.error('Failed to accept friend request:', error)
  }
}

async function createFriendRequest(receiverId: number) {
  try {
    await axios.post(`${URL}/friend-requests/${receiverId}/`, {}, { withCredentials: true })
    const requests = await getFriendRequests(URL, true) // Refresh the list of friend requests
    if (requests)
      ({ incoming_requests: incomingRequests.value, outgoing_requests: outgoingRequests.value } = requests)
    else {
      incomingRequests.value = []
      outgoingRequests.value = []
    }
    runFilter()
    usersAreFriends.value = checkFriendshipStatus()
  } catch (error) {
    return console.error('Failed to create friend request:', error)
  }
}

async function deleteFriendRequest(reqId: number) {
  try {
    await axios.delete(`${URL}/friend-requests/${reqId}/`, { withCredentials: true })
    const requests = await getFriendRequests(URL, true) // Refresh the list of friend requests
    if (requests)
      ({ incoming_requests: incomingRequests.value, outgoing_requests: outgoingRequests.value } = requests)
    else {
      incomingRequests.value = []
      outgoingRequests.value = []
    }
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
    ])


    if (myUser.value) {
      // Add the current user's ID to exclude them from the results
      excludedUserIds.add(myUser.value.id)
      // Add all of the current user's friends' IDs to exclude them as well
      myUser.value.friends.forEach((friend: RestrictedUser) => excludedUserIds.add(friend.id));
    }

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
  <CommonHeader />
  <div v-if="pageUser && (!username || routeUser)" class="profile-page">
    <div class="header">
      <h1>{{ pageUser.username }}</h1>
      <h3>
        <span v-if="pageUser.first_name">{{ pageUser.first_name }}</span>&nbsp;<span v-if="pageUser.last_name">{{
    pageUser.last_name }}</span>
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
            <input type="text" v-model="searchQuery" placeholder="Search Users..." class="search-box" />
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

<style scoped lang="scss">
// i didn't even want to touch this so. here ya go.
.form-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-inline: 3rem;
}

.form-wrapper header {
  display: flex;
  flex-direction: column;
  font-family: 'Open Sans', sans-serif;
  margin-bottom: .5em;
  margin-top: 3rem;
  color: #4b5320;
  text-align: center;
}

.form-wrapper #logo-title {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}

.form-wrapper #logo-title h1 {
  padding-left: .5rem;
  font-size: 3rem;
  font-weight: bold;
  text-shadow: 0px 0px 1px #080f0180;
}

.form-wrapper h2 {
  margin: 0;
  font-size: 2rem;
  line-height: 3rem;
}

.form-wrapper header p {
  font-size: 1.5rem;
  line-height: 2rem;
  margin-top: .33rem;
}

main {
  display: flex;
  flex-direction: column;
  width: 50%;
  align-items: center;
}

#required-warning {
  margin-top: 0;
  color: #d00000d0;
  font-size: .75rem;
}

.submit-button {
  align-items: center;
}

.submit-button button {
  width: 80%;
}

.redirect-swap {
  flex-direction: row;
  justify-content: center;
  align-items: center;
  margin: 0;
}

.redirect-swap p {
  margin-block: .25rem;
  margin-right: .5rem;
}

output {
  color: #d00000;
  font-weight: bold;
  text-align: center;
  margin: .5rem;
}


/* Media query for narrower screens */
@media only screen and (max-width: 1300px) {
  .form-wrapper {
    padding-inline: .5rem;
  }

  .form-wrapper header {
    margin-top: 1rem;
  }

  .form-wrapper #logo-title h1 {
    font-size: 1.75rem;
    line-height: 2rem;
  }

  .form-wrapper h2 {
    font-size: 1.25rem;
    line-height: 1.5rem;
  }

  .form-wrapper header p {
    font-size: 1rem;
    line-height: 1.25rem;
  }

  main {
    width: 90vw;
    margin-bottom: 3rem;
  }

  #required-warning {
    font-size: .66rem;
  }

  .redirect-swap {
    flex-direction: column;
  }

  .redirect-swap p {
    margin-block: .5rem;
    margin-right: 0;
  }
}

.profile-page {
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
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  text-align: center;
  margin: 0px auto;
}

.card {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 25px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease-in-out;
  margin-top: 15px;
}

.card:hover {
  transform: translateY(-2px);
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

.friend-button {
  background-color: #71864f;
  /* Green accent */
  color: white;
  border: none;
  border-radius: 5px;
  padding: 5px 10px;
  margin: 10px auto;
  font-size: x-large;
  transition:
    background-color 0.3s,
    transform 0.1s;
  cursor: pointer;
}

.friend-button:hover {
  background-color: #5a6e3f;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.friend-button:active {
  background-color: #4d5a33;
  transform: translateY(1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
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
  border: 2px solid #71864f;
  /* Themed green border */
  border-radius: 20px;
  /* Rounded corners for a modern look */
  width: 80%;
  /* Responsive width */
  max-width: 400px;
  /* Maximum width to maintain aesthetics */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  /* Subtle shadow for depth */
  outline: none;
  /* Remove the default focus outline */
}

.search-box:focus {
  border-color: #5a6e3f;
  /* Darker green on focus for better visibility */
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
  background-color: #71864f;
  /* Green accent */
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
  flex: 1;
  /* Each column takes up equal space */
  padding: 0 15px;
  /* Spacing between columns */
  margin: 5px 15px;
}

@media (max-width: 768px) {
  .columns {
    flex-direction: column;
    align-items: center;
  }
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
  background-color: #71864f;
  /* Your theme's green */
}

.accept:hover {
  background-color: #5a6e3f;
  /* A darker shade of green for hover */
}

.delete {
  background-color: #d9534f;
  /* A subtle red for delete */
}

.delete:hover {
  background-color: #c9302c;
  /* A darker shade of red for hover */
}

.error-template {
  text-align: center;
  padding: 50px;
  margin: 50px auto;
  background-color: #fff3f3;
  /* Light red background for error indication */
  border: 1px solid #ffcccc;
  /* Slightly darker border for depth */
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.error-template h2 {
  color: #d9534f;
  /* Red color for the error title */
  margin-bottom: 20px;
}

.error-template p {
  color: #666;
  /* Grey color for the message */
  margin-bottom: 30px;
}

.error-template .button {
  background-color: #d9534f;
  /* Red button to match the error theme */
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  cursor: pointer;
  transition:
    background-color 0.3s,
    transform 0.1s;
}

.error-template .button:hover {
  background-color: #c9302c;
  /* Darker shade for hover */
  transform: translateY(-2px);
}

.profile-link {
  display: inline-block;
  color: #4b5320;
  /* Green accent to match the current theme */
  text-decoration: none;
  /* Remove underline from links */
  transition:
    color 0.3s,
    text-decoration 0.3s;
  /* Smooth transition for hover effects */
  font-weight: normal;
  /* Keep the text weight normal, less button-like */
}

.profile-link:hover,
.profile-link:focus {
  color: #71864f;
  /* Darker green for hover and focus to indicate interactivity */
  text-decoration: underline;
  /* Add underline on hover/focus for clarity */
  text-decoration-color: rgba(113, 134, 79, 0.5);
  /* Subtle underline color */
  text-decoration-thickness: 2px;
  /* Make the underline a bit thicker */
  text-underline-offset: 3px;
  /* Slightly offset the underline from the text */
}

/* Optional: Slight text shadow on hover for depth (subtle effect) */
.profile-link:hover {
  text-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);
}
</style>
