<script setup lang="ts">
import CommonHeader from '@/components/CommonHeader.vue';
import { useDisplay } from 'vuetify'

const { mobile } = useDisplay()

</script>

<template>
    <CommonHeader />
    <div class="top-bar">
        <v-btn :size="mobile ? 'small' : 'large'" color="#183400" @click="$router.push('/about')"
            variant="outlined">Back</v-btn>
        <h1>Tutorials</h1>
        <div></div>
    </div>
    <div class="grid">
        <div>
            <h2>Map</h2>
            <iframe width="560" height="315" src="https://www.youtube.com/embed/oAXnOtJalxo?si=j6O2J6rWDFdN4Syi"
                title="YouTube video player" frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
        </div>
        <div>
            <h2>Matchmaking</h2>
            <iframe width="560" height="315" src="https://www.youtube.com/embed/rv3Yq-B8qp4?si=k2owhYWYO5DoZIT7"
                title="YouTube video player" frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
        </div>
        <div>
            <h2>Profile</h2>
            <iframe width="560" height="315" src="https://www.youtube.com/embed/aJhFYfkJGLc?si=gT6mHulRGMyDCQB3"
                title="YouTube video player" frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
        </div>
        <div>
            <h2>Proposing 💍</h2>
            <iframe width="560" height="315" src="https://www.youtube.com/embed/48tzWRTkGRA?si=f_K9nPnFju-szYlC"
                title="YouTube video player" frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
        </div>

    </div>
</template>

<style scoped lang="scss">
@use '@/styles/abstracts' as *;

$tutorial-mobile-size : 1200px;

iframe {
    border-radius: 3%;
    box-shadow: 2px 4px 6px rgba(0, 0, 0, 0.4);

    @include responsive($tutorial-mobile-size) {
        width: 90svw;
        max-width: 600px;
    }
}

.grid {
    display: grid;
    column-gap: 75px;
    row-gap: 50px;
    grid-template-columns: repeat(2, 1fr);
    margin-top: 30px;
    padding-bottom: 24px;

    @include responsive($tutorial-mobile-size) {
        grid-template-columns: repeat(1, 1fr);
    }
}

.top-bar {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    padding: 20px;
    width: 75svw;

    @include responsive($mobile-size) {
        width: 95svw;
    }

    button {
        width: fit-content;

        &:hover {
            background-color: lighten($pickle-100, 15%);
        }
    }
}

h1 {
    @include responsive($mobile-size) {
        font-size: 2.5rem;
        line-height: 2.5rem;
    }
}
</style>