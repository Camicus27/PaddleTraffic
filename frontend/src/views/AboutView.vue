<script setup lang="ts">
</script>

<template>
    <div class="about-wrapper">
    <h1>Welcome to PaddleTraffic!</h1>
    <p>At PaddleTraffic, our mission is to revolutionize the way pickleball enthusiasts find and join games at local courts.
        Recognizing the growing popularity of pickleball — now the fastest-growing sport in the United States — we
        identified a need for an innovative solution to help players easily locate available courts and join games.</p>

    <h2>Our Vision</h2>
    <p>PaddleTraffic was born from a simple vision: to make pickleball more accessible and enjoyable for everyone. Whether
        you’re a beginner or a seasoned player, our platform is designed to help you find the perfect spot to play, connect
        with fellow enthusiasts, and enjoy the game to its fullest.</p>
    <h2>Our Team</h2>
    <p>PaddleTraffic is the brainchild of a passionate team of pickleball fans and tech experts: Brensen Villegas, Camron
        Wilson, Ian McBride, and Jacob Knowlton. Each member brings unique skills and a shared love for the game, driving us
        to
        create the most user-friendly and efficient pickleball court locator.</p>

    <h2>How It Works</h2>
    <p>Our website and mobile app offer a real-time map displaying pickleball courts in your area. With just a tap, you can
        view detailed information about each court, including the number of available courts, current occupancy, waiting
        times,
        and historical data trends. This instant insight helps you decide where to play, saving you time and enhancing your
        playing experience.</p>

    <h2>Beyond Finding Courts</h2>
    <p>But we don’t just stop at helping you find courts. PaddleTraffic also facilitates proximity matchmaking and team
        formation, enabling you to connect with other players looking to form a group or complete a team.</p>

    <h2>Community-Driven Data</h2>
    <p>Our innovative approach to data collection relies on crowdsourcing. QR codes at court locations link players to our
        site, where they can report live updates on court status. This community-driven data enriches our service, ensuring
        accurate and current information for all users.</p>

    <h2>Join Us in Growing the Pickleball Community</h2>
    <p>Whether you're looking to find an open court, join a game, or connect with the pickleball community, PaddleTraffic is
        your go-to platform. Join us in our journey to make pickleball more accessible and enjoyable for everyone!
    </p>
</div>
</template>

<style scoped>
.about-wrapper {
    margin: auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: 800px; /* Limit the width for better readability */
    padding: 20px;
}

h1, h2 {
    font-family: 'Open Sans', sans-serif;
    color: #4b5320; /* Olive green color to match the home page */
    text-align: center;
}

h1 {
    margin-bottom: 0.5em;
    font-size: 3rem; /* Slightly smaller than home page for better fit */
}

h2 {
    font-size: 2rem;
    margin-top: 1em;
    margin-bottom: 0.5em;
}

p {
    font-size: 1.2rem;
    line-height: 1.6;
    color: #333; /* Dark grey for readability */
    text-align: justify; /* Justify text for a neat appearance */
    margin-bottom: 1em; /* Add some space after paragraphs */
}

/* If you have links on the about page, style them to match the home page */
a {
    display: inline-block;
    background-color: #4b5320; /* Olive green background */
    color: #fff;
    padding: 10px 15px;
    text-decoration: none;
    border-radius: 5px;
    transition: background-color 0.3s, color 0.3s;
}

a:hover {
    background-color: #6b8e23;
    color: #d3d3d3;
}
</style>
