<script setup lang="ts">
import CommonHeader from '@/components/CommonHeader.vue';

</script>

<template>
    <CommonHeader />
    <div id="home-wrapper">
        <header>
            <h1>Welcome to PaddleTraffic!</h1>
            <p>View live Pickleball court activity with ease</p>
        </header>

        <main>
            <section>
                <h2>Find a Court Near You</h2>
                <p>Discover nearby Pickleball courts with <strong>real-time updates and availability.</strong></p>
                <RouterLink to="/map">Explore Courts</RouterLink>
            </section>

            <section>
                <h2>Join a Game</h2>
                <p>Connect with <strong>other players and form teams</strong> using our matchmaking feature.</p>
                <RouterLink to="/matchmaking">Find Players</RouterLink>
            </section>

            <section>
                <h2>Learn More About Us</h2>
                <p>Find out more about <strong>PaddleTraffic</strong> and our mission to enhance your Pickleball
                    experience.</p>
                <RouterLink to="/about">About PaddleTraffic</RouterLink>
            </section>
        </main>
    </div>
</template>

<style scoped>
#home-wrapper {
    margin-top: 4rem;
}

#home-wrapper main {
    padding: 1rem;
    background-color: #f5f5f5;
    border-radius: 8px;
}

#home-wrapper main section {
    margin-bottom: .5rem;
}

#home-wrapper main h2 {
    color: #4b5320;
}

#home-wrapper main p {
    text-align: center;
    margin-block: .6rem;
}
</style>