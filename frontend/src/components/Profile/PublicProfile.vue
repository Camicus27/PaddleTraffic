<script setup lang="ts">
import { ref, onMounted, watch, type Ref, resolveDirective } from 'vue'
import { useRoute } from 'vue-router'
import { redirect } from '../../api/utils'

import { getCurrentUser, getFriendRequests } from '../../api/functions'
import type { FriendRequest, PickleUser, RestrictedUser } from '../../api/types'

let myUser: Ref<PickleUser>

onMounted(async () => {
    const user = await getCurrentUser(true)
    if (!user)
        redirect('/login')
    myUser.value = user as PickleUser
})
</script>

<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12" sm="6"><h1>This is column 1</h1></v-col>
      <v-col cols="12" sm="6"><h1>This is column 2</h1></v-col>
    </v-row>
  </v-container>
</template>

<style scoped lang="scss"></style>
