<script setup lang="ts">
</script>

<template>
    <div class="home-wrapper">
        <header>
            <h1>Welcome to PaddleTraffic</h1>
            <p>Find and join Pickleball courts with ease</p>
        </header>

        <main>
            <section>
                <h2>Find a Court Near You</h2>
                <p>Discover nearby Pickleball courts with real-time updates and availability.</p>
                <a href="map.html">Explore Courts</a>
            </section>

            <section>
                <h2>Join a Game</h2>
                <p>Connect with other players and form teams using our matchmaking feature.</p>
                <a href="matchmaking.html">Find Players</a>
            </section>

            <section>
                <h2>Learn More About Us</h2>
                <p>Find out more about PaddleTraffic and our mission to enhance your Pickleball experience.</p>
                <a href="about.html">About PaddleTraffic</a>
            </section>
        </main>
    </div>
</template>

<style scoped>
.home-wrapper {
    margin-left: auto;
    margin-right: auto;
    display: flex;
    flex-direction: column;
    justify-content: space-around;

    align-items: center;
}

/* Header styles */
header {
    font-family: 'Open Sans', sans-serif;
    margin-bottom: .5em;
    color: #4b5320;
    text-align: center;
    padding: 20px 0;
}

header h1 {
    margin: 0;
    margin-bottom: .2em;
    font-size: 4rem;
}

header p {
    font-size: 1.5rem;
}

/* Main content styles */
main {
    padding: 20px;
    margin-bottom: 3.7em;
    background-color: #f5f5f5;
    /* Light background for contrast */
    border-radius: 8px;
}

main section {
    margin-bottom: 20px;
}

main h2 {
    color: #4b5320;
    /* Olive green for headers */
}

main p {
    margin-bottom: 10px;
}

main a {
    display: inline-block;
    background-color: #4b5320;
    /* Olive green background */
    color: #fff;
    padding: 10px 15px;
    text-decoration: none;
    border-radius: 5px;
    transition: background-color 0.3s, color 0.3s;
}

main a:hover {
    background-color: #6b8e23;
    color: #d3d3d3;
}</style>