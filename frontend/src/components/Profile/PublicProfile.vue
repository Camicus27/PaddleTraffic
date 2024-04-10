<script setup lang="ts">

import { ref, onMounted, type Ref } from 'vue'

import { getCurrentUser, getUserUsername, getFriendRequests, createFriendRequest, acceptFriendRequest, deleteFriendRequest } from '@/api/functions'
import type { PendingFriendRequests, FriendRequest, PickleUser, RestrictedUser } from '@/api/types'
import { redirect } from '@/api/utils'

const props = defineProps<{
    username: string
}>()

enum Relationship {
    Same,
    Friends,
    OutRequest,
    InRequest,
    NotFriends,
    Invalid
}

const loading: Ref<boolean> = ref(true)
const pageError: Ref<boolean> = ref(false)
const userRelationship: Ref<Relationship> = ref(Relationship.Invalid)

const myUser: Ref<PickleUser | undefined> = ref(undefined)
const pageUser: Ref<RestrictedUser | undefined> = ref(undefined)
const pendingRequests: Ref<PendingFriendRequests> = ref({ incoming_requests: [], outgoing_requests: [] })

onMounted(async () => {
    // Set up initial state
    await updateFriendState()

    if (!pageUser.value)
        pageError.value = true

    // Let the UI know we have finished loading
    loading.value = false
})

async function updateFriendState() {
    myUser.value = await getCurrentUser(true)
    pageUser.value = await getUserUsername(props.username, true)
    if (myUser.value)
        pendingRequests.value = await getFriendRequestsOrEmpty()
    userRelationship.value = checkFriendshipStatus()
}

async function getFriendRequestsOrEmpty(): Promise<PendingFriendRequests> {
    const reqs = await getFriendRequests(true)
    if (!reqs)
        return { incoming_requests: [], outgoing_requests: [] }
    else
        return reqs as PendingFriendRequests
}

function checkFriendshipStatus() {
    // Ensure both users are defined before proceeding
    if (!myUser.value || !pageUser.value)
        return Relationship.Invalid

    // Check if the users are the same
    if (myUser.value.id === pageUser.value.id)
        return Relationship.Same

    // Check if they are already friends
    if (myUser.value.friends.some((friend: RestrictedUser) => friend.id === pageUser.value?.id))
        return Relationship.Friends

    // Check for pending friend requests from the current user to the page user
    const hasOutgoingRequest = pendingRequests.value.outgoing_requests.some(
        (request: FriendRequest) => request.receiver.id === pageUser.value?.id
    )
    if (hasOutgoingRequest)
        return Relationship.OutRequest

    // Check for pending friend requests from the route user to the current user
    const hasIncomingRequest = pendingRequests.value.incoming_requests.some(
        (request: FriendRequest) => request.requester.id === pageUser.value?.id
    )
    if (hasIncomingRequest)
        return Relationship.InRequest

    return Relationship.NotFriends
}

async function createFriendRequestUpdate() {
    if (!pageUser.value)
        return
    await createFriendRequest(pageUser.value.id, true)
    await updateFriendState()
}

async function acceptFriendRequestUpdate() {
    const friendReq = pendingRequests.value.incoming_requests.find(req => req.requester.id === pageUser.value?.id)
    if (!friendReq)
        return
    await createFriendRequest(friendReq.id, true)
    await updateFriendState()
}

async function deleteIncomingFriendRequestUpdate() {
    const friendReq = pendingRequests.value.incoming_requests.find(req => req.requester.id === pageUser.value?.id)
    if (!friendReq)
        return
    await deleteFriendRequest(friendReq.id, true)
    await updateFriendState()
}

async function deleteOutgoingFriendRequestUpdate() {
    const friendReq = pendingRequests.value.outgoing_requests.find(req => req.receiver.id === pageUser.value?.id)
    if (!friendReq)
        return
    await deleteFriendRequest(friendReq.id, true)
    await updateFriendState()
}
</script>

<template>
    <v-progress-circular indeterminate v-if="loading"></v-progress-circular>
    <div v-else>
        <div v-if="pageError" class="error-template mx-3">
            <h2>User Not Found</h2>
            <p>We're sorry, but the user <b>{{ username }}</b> does not exist or may have been removed.</p>
            <v-btn @click="redirect('/')" color="#d9534f" size="large">Go to Home</v-btn>
        </div>
        <v-container v-else class="container">

            <v-row>
                <v-col cols="12" class="d-flex flex-column align-center">
                    <h1 class="mt-16 mb-8">{{ pageUser?.username }}</h1>
                    <div class="mb-4">
                        <h4 v-if="userRelationship === Relationship.Same">This is your public profile page.</h4>
                        <h4 v-else-if="userRelationship === Relationship.Friends">You are friends with {{
                            pageUser?.username
                        }}</h4>
                        <h4 v-else-if="userRelationship === Relationship.OutRequest">You have sent {{ pageUser?.username
                            }}
                            a friend request <v-btn class="ms-4" variant="outlined" color="red" size="small"
                                @click="deleteOutgoingFriendRequestUpdate">Delete</v-btn>
                        </h4>
                        <h4 v-else-if="userRelationship === Relationship.InRequest">{{ pageUser?.username }}
                            has sent you a friend request <v-btn class="ms-4" variant="outlined" color="green"
                                size="small" @click="acceptFriendRequestUpdate">Accept</v-btn><v-btn class="ms-4"
                                variant="outlined" color="red" size="small"
                                @click="deleteIncomingFriendRequestUpdate">Delete</v-btn></h4>
                        <h4 class="mb-4" v-else-if="userRelationship === Relationship.NotFriends"><v-btn
                                variant="outlined" color="green" size="large" @click="createFriendRequestUpdate">Add
                                Friend</v-btn></h4>
                        <h4 v-else-if="userRelationship === Relationship.Invalid"></h4>
                    </div>
                    <!-- BIO CARD -->
                    <v-card class="mx-auto w-100" min-width="400" elevation="4">
                        <v-card-text class="d-flex flex-column align-center">
                            <h2>Bio</h2>

                            <div class="bio text-subtitle-1 text--primary px-md-16 w-100"
                                style="height: 100px; align-self: flex-start;">{{ pageUser?.bio }}</div>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>

            <v-row>
                <v-col cols="12" md="6" class="d-flex justify-center">
                    <!-- SKILL LEVEL CARD -->
                    <v-card class="mx-auto" min-width="400" elevation="4">
                        <v-card-text class="d-flex flex-column align-center">
                            <h2>Skill Level</h2>
                            <p class="text-h6 text--primary">{{ pageUser?.skill_level }}</p>
                        </v-card-text>
                    </v-card>
                </v-col>
                <v-col cols="12" md="6" class="d-flex justify-center">
                    <!-- MATCH STATISTICS CARD -->
                    <v-card class="mx-auto" min-width="400" elevation="4">
                        <v-card-text class="d-flex flex-column">
                            <div class="statistics">
                                <h2 class="align-self-center">Match Statistics</h2>
                                <p class="text-h6 text--primary">Matches Attended: <span>{{ pageUser?.matches_attended
                                        }}</span></p>
                                <p class="text-h6 text--primary">Matches Created: <span>{{ pageUser?.matches_created
                                        }}</span>
                                </p>
                            </div>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<style scoped lang="scss">
.container {
    max-width: 1000px;
}

.v-card--reveal {
    bottom: 0;
    opacity: 1 !important;
    position: absolute;
    width: 100%;
}

h1 {
    font-size: 3.5em;
    color: #4b5320;
}

.user-link {
    text-decoration: none;
    color: #4b5320;

    &:hover {
        text-decoration: underline;
    }
}

.statistics {
    display: grid;
    row-gap: 10px;

    & p {
        display: flex;
        justify-content: space-between;
    }

    & p span {
        font-weight: bold;
        align-self: center;
    }
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

    & h2 {
        color: #d9534f;
        /* Red color for the error title */
        margin-bottom: 20px;
    }

    & p {
        color: #666;
        /* Grey color for the message */
        margin-bottom: 30px;
    }
}

.bio {
    white-space: pre-wrap;
    word-wrap: break-word;
}
</style>