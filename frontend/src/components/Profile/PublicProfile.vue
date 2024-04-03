<script setup lang="ts">
import { ref, onMounted, watch, type Ref } from 'vue'
import { useRoute } from 'vue-router'

import axios from 'axios'

import { getCurrentUser, getFriendRequests } from '../../api/functions';
import type { FriendRequest, PickleUser, RestrictedUser } from '../../api/types';
</script>

<template>
    <h1>Private Profile</h1>
</template>

<style scoped lang="scss"></style>



