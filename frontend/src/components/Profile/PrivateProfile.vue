<script setup lang="ts">

import { ref, onMounted, watch, type Ref, resolveDirective } from 'vue'
import { redirect } from '@/api/utils'

import { getCurrentUser, updateCurrentUser, getFriendRequests, deleteFriendRequest, createFriendRequest, getAllUsers } from '@/api/functions'
import type { FriendRequest, PendingFriendRequests, PickleUser, RestrictedUser } from '@/api/types'

const loading: Ref<boolean> = ref(true)

let myUser: Ref<PickleUser>
let pendingRequests: Ref<PendingFriendRequests>

// Variables for sending friend requests
let allUsers: Ref<RestrictedUser[]>
const filteredUserList: Ref<RestrictedUser[]> = ref([])
const selectedUsers: Ref<RestrictedUser[]> = ref([])
const friendReqButtonText: Ref<string> = ref("Send")
watch(selectedUsers, () => {
    if (selectedUsers.value.length > 1)
        friendReqButtonText.value = "Send All"
    else
        friendReqButtonText.value = "Send"
})


const revealSkillLvl: Ref<boolean> = ref(false)
const skillLvl: Ref<"Beginner" | "Advanced Beginner" | "Intermediate Beginner" | "Intermediate" | "Advanced Intermediate" | "Expert" | "Advanced Expert" | "Professional"> = ref("Beginner")

const revealBio: Ref<boolean> = ref(false)
const bio: Ref<string> = ref("")

onMounted(async () => {
    // Get current user
    const user = await getCurrentUser(true)
    if (!user)
        redirect('/login')
    myUser = ref(user as PickleUser)

    // Get pending friend requests
    pendingRequests = ref(await getFriendRequestsOrEmpty())

    // Get list of all users
    const users = await getAllUsers(true)
    if (!users)
        allUsers = ref([])
    else
        allUsers = ref(users)

    // Get updated filtered users
    filteredUserList.value = getUpdatedFilteredUserList()

    // Setup initial profile variables
    skillLvl.value = myUser.value.skill_level
    bio.value = myUser.value.bio

    // Let the UI know we have finished loading
    loading.value = false
})

async function updateFriendState() {
    pendingRequests.value = await getFriendRequestsOrEmpty()
    filteredUserList.value = getUpdatedFilteredUserList()
}

async function getFriendRequestsOrEmpty(): Promise<PendingFriendRequests> {
    const reqs = await getFriendRequests(true)
    if (!reqs)
        return { incoming_requests: [], outgoing_requests: [] }
    else
        return reqs as PendingFriendRequests
}

async function updateSkillLevel() {
    const userCopy = { ...myUser.value }
    userCopy.skill_level = skillLvl.value
    if (await updateCurrentUser(userCopy, true))
        myUser.value = userCopy
    else
        console.log("Unable to update skill level")
    revealSkillLvl.value = false
}

async function updateBio() {
    const userCopy = { ...myUser.value }
    userCopy.bio = bio.value
    if (await updateCurrentUser(userCopy, true))
        myUser.value = userCopy
    else
        console.log("Unable to update bio")
    revealBio.value = false
}

async function clearFriendRequest(id: number) {
    await deleteFriendRequest(id, true)
    await updateFriendState()
}

async function createAllFriendRequests() {
    for (const user of selectedUsers.value) {
        await createFriendRequest(user.id, true)
    }
    selectedUsers.value.length = 0
    await updateFriendState()
}

function getUpdatedFilteredUserList() {
    let currList = allUsers.value
    // Remove current user from the list
    currList = currList.filter(user => user.id !== myUser.value.id)
    // Remove all pending friend requests
    currList = currList.filter(user => !(pendingRequests.value.incoming_requests.map(req => req.requester.id)).includes(user.id))
    currList = currList.filter(user => !(pendingRequests.value.outgoing_requests.map(req => req.receiver.id)).includes(user.id))
    // Remove all current friends
    currList = currList.filter(user => !(myUser.value.friends.map(friend => friend.id)).includes(user.id))
    return currList
}

</script>

<template>
    <v-progress-circular indeterminate v-if="loading"></v-progress-circular>
    <v-container class="container" v-else>

        <v-row>
            <v-col cols="12" class="d-flex flex-column align-center">
                <h1 class="ma-16">{{ myUser.username }}</h1>

                <!-- BIO CARD -->
                <v-card class="mx-auto w-100" min-width="400" elevation="10">
                    <v-card-text class="d-flex flex-column align-center">
                        <h2>Bio</h2>

                        <p class="text-subtitle-1 text--primary px-md-16 w-100"
                            style="height: 100px; align-self: flex-start;">{{
        myUser.bio }}</p>
                    </v-card-text>
                    <v-card-actions>
                        <v-btn color="#4b5320" variant="text" @click="revealBio = true">
                            Edit
                        </v-btn>
                    </v-card-actions>

                    <v-expand-transition>
                        <v-card v-if="revealBio" class="v-card--reveal" style="height: 100%;">
                            <v-card-text class="pb-0">
                                <v-textarea v-model="bio" label="Update your bio" maxlength="200" counter
                                    single-line></v-textarea>
                            </v-card-text>
                            <v-card-actions class="pt-0">
                                <v-btn color="#4b5320" variant="text" @click="revealBio = false">
                                    Cancel
                                </v-btn>
                                <v-btn color="#4b5320" variant="text" @click="updateBio">
                                    Save
                                </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-expand-transition>
                </v-card>
            </v-col>
        </v-row>

        <v-row>
            <v-col cols="12" md="6" class="d-flex justify-center">
                <!-- SKILL LEVEL CARD -->
                <v-card class="mx-auto" min-width="400" elevation="10">
                    <v-card-text class="d-flex flex-column align-center">
                        <h2>Skill Level</h2>
                        <p class="text-h6 text--primary">{{ myUser.skill_level }}</p>
                    </v-card-text>
                    <v-card-actions>
                        <v-btn color="#4b5320" variant="text" @click="revealSkillLvl = true">
                            Edit
                        </v-btn>
                    </v-card-actions>

                    <v-expand-transition>
                        <v-card v-if="revealSkillLvl" class="v-card--reveal" style="height: 100%;">
                            <v-card-text class="pb-0">
                                <p class="text-h6 text--primary">Select your new skill level</p>
                                <v-select v-model="skillLvl" label="SkillLvl"
                                    :items="['Beginner', 'Advanced Beginner', 'Intermediate Beginner', 'Intermediate', 'Advanced Intermediate', 'Expert', 'Advanced Expert', 'Professional',]"></v-select>
                            </v-card-text>
                            <v-card-actions class="pt-0">
                                <v-btn color="#4b5320" variant="text" @click="revealSkillLvl = false">
                                    Cancel
                                </v-btn>
                                <v-btn color="#4b5320" variant="text" @click="updateSkillLevel">
                                    Save
                                </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-expand-transition>
                </v-card>
            </v-col>
            <v-col cols="12" md="6" class="d-flex justify-center">
                <!-- MATCH STATISTICS CARD -->
                <v-card class="mx-auto" min-width="400" elevation="10">
                    <v-card-text class="d-flex flex-column">
                        <div class="statistics">
                            <h2 class="align-self-center">Match Statistics</h2>
                            <p class="text-h6 text--primary">Matches Attended: <span>{{ myUser.matches_attended
                                    }}</span></p>
                            <p class="text-h6 text--primary">Matches Created: <span>{{ myUser.matches_attended }}</span>
                            </p>
                        </div>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>

        <v-row>
            <v-col cols="12" md="6" class="d-flex justify-center">
                <!-- FRIEND REQUESTS CARD -->
                <v-card class="mx-auto" min-width="400" elevation="10">
                    <v-card-text>
                        <h2>Friend Requests</h2>
                        <h3 class="mt-4">Incoming</h3>
                        <v-list lines="one">
                            <v-list-item v-for="incoming in pendingRequests.incoming_requests" :key="incoming.id">
                                <v-list-item-title>
                                    <a class="user-link" :href="`/profile/${incoming.requester.username}`">{{
        incoming.requester.username
    }}</a>
                                </v-list-item-title>
                                <template v-slot:append>
                                    <v-btn icon="mdi-close" variant="text"
                                        @click="clearFriendRequest(incoming.id)"></v-btn>
                                </template>
                            </v-list-item>
                        </v-list>
                        <h3 class="mt-4">Outgoing</h3>
                        <v-list lines="one">
                            <v-list-item v-for="outgoing in pendingRequests.outgoing_requests" :key="outgoing.id">
                                <v-list-item-title>
                                    <a class="user-link" :href="`/profile/${outgoing.receiver.username}`">{{
        outgoing.receiver.username
    }}</a>
                                </v-list-item-title>
                                <template v-slot:append>
                                    <v-btn icon="mdi-close" variant="text"
                                        @click="clearFriendRequest(outgoing.id)"></v-btn>
                                </template>
                            </v-list-item>
                        </v-list>
                    </v-card-text>
                </v-card>
            </v-col>

            <v-col cols="12" md="6">
                <v-card class="mx-auto" min-width="400" max-width="400" elevation="10">
                    <v-card-text class="d-flex flex-column">
                        <div class="statistics">
                            <h2 class="align-self-center">Add Friends</h2>
                        </div>
                        <v-autocomplete v-model="selectedUsers" :items="filteredUserList" item-title="name"
                            item-value="name" label="Select Users" chips closable-chips multiple>
                            <template v-slot:chip="{ props, item }">
                                <v-chip v-bind="props" :text="item.raw.username"></v-chip>
                            </template>

                            <template v-slot:item="{ props, item }">
                                <v-list-item v-bind="props" :subtitle="item.raw.skill_level"
                                    :title="item.raw.username"></v-list-item>
                            </template>
                        </v-autocomplete>
                        <v-btn variant="text" @click="createAllFriendRequests">{{ friendReqButtonText }}</v-btn>
                    </v-card-text>
                </v-card>

            </v-col>
        </v-row>

    </v-container>
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
</style>
