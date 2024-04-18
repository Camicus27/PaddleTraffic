<script setup lang="ts">
import CommonHeader from '@/components/CommonHeader.vue';
</script>

<template>
    <CommonHeader />
    <h1>Tutorials</h1>
    <div class="grid">
        <div>
            <h2>Map</h2>

            <iframe width="560" height="315" src="https://www.youtube.com/embed/zcbgX5TXNxs?si=FpQD6B87mAUzQyot"
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
            <iframe width="560" height="315" src="https://www.youtube.com/embed/I6fztruG7GE?si=PuIlEJVCshCeiIMv"
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

h1 {
    margin-top: 20px;
}

iframe {
    border-radius: 3%;
    box-shadow: 2px 4px 6px rgba(0, 0, 0, 0.4);
}

.grid {
    display: grid;
    column-gap: 75px;
    row-gap: 50px;
    grid-template-columns: repeat(2, 1fr);
    margin-top: 30px;
}
</style>