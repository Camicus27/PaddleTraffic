<script setup lang="ts">
</script>

<template>
  <footer>
    <div>
      <h3>PaddleTraffic</h3>
      <p>Connecting Pickleball Players to Courts Everywhere</p>
    </div>
    <div class="contact-us">
      <p>Contact us at: <a href="mailto:support@paddletraffic.com">support@paddletraffic.com</a></p>
      <p>Follow us on social media:</p>
      <a href="https://www.facebook.com/PaddleTraffic" target="_blank">Facebook</a> |
      <a href="https://twitter.com/PaddleTraffic" target="_blank">Twitter</a> |
      <a href="https://www.instagram.com/PaddleTraffic" target="_blank">Instagram</a>
    </div>
    <div>
      <p>&copy; 2023 PaddleTraffic. All rights reserved.</p>
    </div>
  </footer>
</template>

<style scoped>
footer {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  bottom: 0px;
  left: 0px;
  right: 0px;
  padding-left: 3rem max(1rem, calc((100% - 110rem)/2)) 0px max(1rem, calc((100% - 110rem)/2));
  padding-right: 3rem max(1rem, calc((100% - 110rem)/2)) 0px max(1rem, calc((100% - 110rem)/2));
  margin-top: 3rem;
  padding: 1em;
  background-color: #9fb184;
  font-weight: bold;
  color: #183400;
}

.contact-us {
  text-align: center;
}

#legal {
  align-items: center;
  justify-content: flex-end;
  padding: 1.25rem 1.25rem 1.25rem .5rem;
  margin: 0;
}

#extra-info {
  align-items: center;
  width: 60%;
  padding: 1.25rem .5rem 1.25rem 1.25rem;
  margin: 0;
  font-size: 1.5rem;
}

#extra-info nav a {
  padding-left: 1rem;
  text-shadow: 1px 1px 1px #080f01;
  text-decoration: none;
}

#extra-info nav a:any-link {
  color: #234a00;
}

#extra-info nav a:active {
  color: #ffffff;
}

#extra-info nav a:hover {
  color: #2f6500;
  text-decoration: underline;
}</style>