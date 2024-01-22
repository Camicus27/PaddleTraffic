<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
    <div id="profile-login">
        <RouterLink to="/login">
            <img src="@/assets/default_user.png" class="pfp" alt="User profile" width="32" height="32">
        </RouterLink>
    </div>
    <header id="site-header">
        <div id="logo-title">
            <RouterLink to="/">
                <img src="@/assets/logo.png" class="logo" alt="PaddleTraffic Logo" width="64" height="64">
                <h1>PaddleTraffic</h1>
            </RouterLink>
        </div>
        <nav>
            <RouterLink to="/">HOME</RouterLink>
            <RouterLink to="/map">MAP</RouterLink>
            <RouterLink to="/matchmaking">MATCHMAKING</RouterLink>
            <RouterLink to="/about">ABOUT</RouterLink>
        </nav>
    </header>
</template>