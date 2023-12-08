<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <header>
    <RouterLink to="/">
        <img src="@/assets/logo.png" class="logo" alt="PaddleTraffic Logo" width="125" height="125">
    </RouterLink>
    <div id="header-text">
      <h1>PaddleTraffic</h1>
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/map">Map</RouterLink>
        <RouterLink to="/matchmaking">Matchmaking</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div>
  </header>
</template>

<style scoped>
  header {
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: flex-start;
      padding: 1rem max(2.75rem, calc((100% - 105rem)/2)) 1rem max(2.75rem, calc((100% - 105rem)/2));
      margin-bottom: 3rem;
      background-color: #9fb184;
      box-shadow: 0px 0px 5px #152a03;
  }
      header > a {
          padding-right: 1rem;
      }
      #header-text {
          display: flex;
          flex-direction: column;
      }
      #header-text h1 {
          padding-bottom: .5rem;
          font-size: 2.5rem;
          font-weight: bold;
          color: #183400;
          text-shadow: 2px 2px 1px #080f0180;
      }
      #header-text nav {
          display: flex;
          flex-direction: row;
          width: 100%;
          font-size: 1.75rem;
          font-weight: bold;
      }
      #header-text nav a {
          padding-right: 2rem;
          text-shadow: 1px 1px 1px #080f01a0;
          text-decoration: none;
      }
      #header-text nav a:any-link {
          color: #234a00;
      }
      #header-text nav a:active {
          color: #ffffff;
      }
      #header-text nav a:hover {
          color: #2f6500;
          text-decoration: underline;
      }
</style>
