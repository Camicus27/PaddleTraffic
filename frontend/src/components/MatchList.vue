<script setup lang="ts">
import { ref, onBeforeMount, type Ref } from 'vue';
import axios from 'axios'

const posts : Ref<any> = ref({})

onBeforeMount(() => {
    axios.get('https://jsonplaceholder.typicode.com/posts')
        .then((response) => posts.value = response.data)
        .catch((error) => console.log(error))
})

</script>

<template>
  <h1>tmp</h1>
  <div class="posts" v-for="post in posts" :key="post.id">
    <h3>Title: {{ post.title }}</h3>
    <h4>Body: {{ post.body }}</h4>
  </div>
</template>

<style scoped>
.posts {
    border: 2px solid gray;
    background-color: lightcyan;
    padding: 1em;
    margin: 1em;
}
</style>
