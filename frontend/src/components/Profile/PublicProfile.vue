<script setup lang="ts">

import { ref, onMounted, type Ref } from 'vue'

import { getCurrentUser, getUserUsername, getFriendRequests, createFriendRequest, acceptFriendRequest } from '@/api/functions'
import type { PendingFriendRequests, PickleUser, RestrictedUser } from '@/api/types'

enum Relationship {
    Same,
    Friends,
    Requested,
    NotFriends,
    Invalid
}

const loading: Ref<boolean> = ref(true)
const pageError: Ref<boolean> = ref(false)

const myUser: Ref<PickleUser | undefined> = ref(undefined)
const pageUser: Ref<RestrictedUser | undefined> = ref(undefined)
const pendingRequests: Ref<PendingFriendRequests> = ref({ incoming_requests: [], outgoing_requests: [] })

onMounted(async () => {
    // Get current user if signed in
    myUser.value = await getCurrentUser(true)
    // pageUser.value = await getUserUsername(true)

    // Get pending friend requests
    pendingRequests.value = await getFriendRequestsOrEmpty()

    // Let the UI know we have finished loading
    loading.value = false
})

async function getFriendRequestsOrEmpty(): Promise<PendingFriendRequests> {
    const reqs = await getFriendRequests(true)
    if (!reqs)
        return { incoming_requests: [], outgoing_requests: [] }
    else
        return reqs as PendingFriendRequests
}

</script>

<template>
    <v-progress-circular indeterminate v-if="loading"></v-progress-circular>
    <v-container class="container" v-else>

        <v-row>
            <v-col cols="12" class="d-flex flex-column align-center">
                <h1 class="ma-16">{{ pageUser?.username }}</h1>

                <!-- BIO CARD -->
                <v-card class="mx-auto w-100" min-width="400" elevation="4">
                    <v-card-text class="d-flex flex-column align-center">
                        <h2>Bio</h2>

                        <p class="text-subtitle-1 text--primary px-md-16 w-100"
                            style="height: 100px; align-self: flex-start;">{{
                                pageUser?.bio }}</p>
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
                            <p class="text-h6 text--primary">Matches Created: <span>{{ pageUser?.matches_attended
                                    }}</span>
                            </p>
                        </div>
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