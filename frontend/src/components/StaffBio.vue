<script setup lang="ts">
import { defineProps } from 'vue'
defineProps<{
    imagePath: string,
}>()
</script>

<template>
    <div>
        <v-card class="main" variant="tonal">
            <div class="photo">
                <img :src="imagePath" alt="Staff member profile image">
            </div>
            <div class="info">
                <v-card-title class="title">
                    <slot name="title"></slot>
                </v-card-title>

                <v-card-text class="bio">
                    <slot name="bio"></slot>
                </v-card-text>
                <v-card-subtitle class="contact">
                    <slot name="contact"></slot>
                </v-card-subtitle>
            </div>
        </v-card>
    </div>
</template>

<style scoped lang="scss">
@use '../styles/components';
@use '@/styles/abstracts' as *;

.main {
    display: flex;
    flex-direction: row;
    max-width: 750px;
    width: 80svw;
    padding: 1rem;
    justify-content: space-around;

    @include responsive($mobile-size) {
        display: block;
        width: auto;
    }
}

.photo {
    display: flex;

    @include responsive($mobile-size) {
        justify-content: center;
        padding: 1rem;
        padding-top: 0;
    }
}

.info {
    display: flex;
    flex-direction: column;
    padding: 0;
    padding-left: 1.75rem;
    justify-content: start;

    @include responsive($mobile-size) {
        padding-left: 0;
    }
}

.title {
    padding: 0;
    margin-bottom: .5rem;
    font-weight: bold;
    font-family: sans-serif;
    font-style: italic;
    font-size: 2rem;
    line-height: 2.5rem;
    
    @include responsive($mobile-size) {
        font-size: 1.25rem;
        line-height: 1.75rem;
        text-align: center;
    }
}

.bio {
    padding: 0;
    font-size: 1rem;
    line-height: 1.2rem;
    align-items: center;
    
    @include responsive($mobile-size) {
        font-size: .85rem;
        line-height: .95rem;
    }
}

.contact {
    display: flex;
    flex-direction: column;
    padding: 0;
}

img {
    border-radius: 50%;
    height: 150px;
    width: auto;

    @include responsive($mobile-size) {
        width: 150px;
    }
}
</style>