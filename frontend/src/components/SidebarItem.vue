<script setup lang="ts">
import { RouterLink } from 'vue-router'
defineProps<{
  name: string
  location: string
  host: string
  players: Array<string>
  date: string
  time: string
}>()
</script>

<template>
  <div class="sidebar-item">
    <p class="match-loc">
      Match at <RouterLink to="/map">{{ location }}</RouterLink>
    </p>
    <p class="player-list">Players: 
      <ul>
        <li class="player-link" v-for="player in players" :key="player">
            <a href="">{{ player }}</a>
        </li>
        <li class="join-match-link" v-if="(players.length < 4)">
          &lbrack; <a href="">Join Game</a> &rbrack;
        </li>
      </ul>
    </p>
    <p class="match-time">
      Time: {{ time }}
    </p>
  </div>
</template>

<style scoped lang="scss">
  // .sidebar-item {
  //   width: 100%;
  //   border: 3px solid #080f01;
  //   background-color: #d0d4ca;
  //   padding: .5rem .25rem 1rem .75rem;
  //   font-weight: bold;
  //   word-wrap: break-word;
  // }
  // .sidebar-item p {
  //   padding-top: .5rem;
  //   margin: 0;
  // }
  // .sidebar-item a {
  //   text-shadow: 1px 1px 1px #080f01b0;
  //   text-decoration: none;
  // }
  // .sidebar-item a:any-link {
  //   color: #61a328;
  // }
  // .sidebar-item a:active {
  //   color: #ffffff;
  // }
  // .sidebar-item a:hover {
  //   color: #79d32b;
  //   text-decoration: underline;
  // }

  // .match-loc {
  //   font-size: 1.2rem;
  //   padding-bottom: .5rem;
  //   border-bottom: 2px solid #080f01;
  // }
  // .player-list {
  //   font-size: 1.1rem;
  // }
  //   .player-list > ul {
  //     margin: 0;
  //   }
</style>
