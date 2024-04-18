<script setup lang="ts">
import { defineProps } from 'vue'
defineProps<{
    imagePath: string,
}>()
</script>

<template>
    <div>
        <v-card class="main" variant="tonal">
            <img :src="imagePath" alt="Staff member profile image">
            <div class="info">
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
    @use '@/styles/abstracts' as *;

    * {
        display: flex;
    }
    
    .main {
        flex-direction: row;
        max-width: 750px;
        padding: 16px;
        justify-content: space-around;
    }

    
    .info {
        flex-direction: column;
        padding: 0;
        padding-left: 24px;
        justify-content: start;
    }

    .bio {
        $text: 1.4rem;

        padding: 0;
        font-size: $text;
        line-height: $text;
        font-family: sans-serif;
        color: $pickle-500;
        align-items: center;
    }

    .contact {
        padding: 0;
    }

    img {
        border-radius: 50%;
        height: 150px;
        width: 150px;
    }



</style>