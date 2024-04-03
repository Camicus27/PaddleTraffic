<script setup lang="ts">
</script>

<template>
    <div>
        <header>
            <h1>Welcome to PaddleTraffic!</h1>
            <p>View live Pickleball court activity with ease</p>
        </header>

        <main>
            <section>
                <h2>Find a Court Near You</h2>
                <p>Discover nearby Pickleball courts with <strong>real-time updates and availability.</strong></p>
                <RouterLink to="/map" class="dark-solid-button">Explore Courts</RouterLink>
            </section>

            <section>
                <h2>Join a Game</h2>
                <p>Connect with <strong>other players and form teams</strong> using our matchmaking feature.</p>
                <RouterLink to="/matchmaking" class="dark-solid-button">Find Players</RouterLink>
            </section>

            <section>
                <h2>Learn More About Us</h2>
                <p>Find out more about <strong>PaddleTraffic</strong> and our mission to enhance your Pickleball
                    experience.</p>
                <RouterLink to="/about" class="dark-solid-button">About PaddleTraffic</RouterLink>
            </section>
        </main>
    </div>
</template>

<style scoped lang="scss">
@use '@/styles/components';
@use '@/styles/abstracts';

div {
    @extend %main-page;
}

header {
    @extend %flex-col-center;
    h1 {
        margin-bottom: 1rem;
        text-align: center;
    }

    p {
        margin: 0;
        margin-bottom: 2rem;
    }
}

main {
    padding: 1rem;
    background-color: #f5f5f5;
    border-radius: 8px;

    p {
        text-align: center;
        margin-block: .6rem;
    }
}

section {
    margin-bottom: .5rem;
}
</style>