<script setup lang="ts">
// TODO deprecated??
</script>

<template>
  <footer>
    <div>
      <div id="extra-info">
        <h3>PaddleTraffic</h3>
        <p>Connecting Pickleball Players to Courts Everywhere</p>
      </div>
      <div id="contact-us">
        <p>Contact us at: <a href="mailto:support@paddletraffic.com">support@paddletraffic.com</a></p>
        <div id="socials">
          <p>Follow us on social media:</p>
          <nav>
            <a href="https://www.facebook.com/PaddleTraffic" target="_blank">Facebook</a> |
            <a href="https://twitter.com/PaddleTraffic" target="_blank">Twitter</a> |
            <a href="https://www.instagram.com/PaddleTraffic" target="_blank">Instagram</a>
          </nav>
        </div>
      </div>
      <div id="legal">
        <p>&copy; 2023 PaddleTraffic</p>
      </div>
    </div>
  </footer>
</template>

<style scoped lang="scss">
/* Site footer styles */
footer {
  position: relative;
  bottom: 0;
  left: 0;
  right: 0;
  margin-top: 3rem;
  padding-block: 2.75rem;
  background-color: #67784c;
  font-weight: bold;
}

footer>div {
  display: flex;
  flex-direction: row;
  align-items: center;
  position: relative;
}

#extra-info {
  display: flex;
  flex-direction: column;
  width: 27.5%;
  margin: 0 .33rem;
}

#extra-info p {
  margin: 0;
}

#contact-us {
  display: flex;
  flex-direction: column;
  width: 45%;
  align-items: center;
  margin: 0 .33rem;
  text-align: center;
  font-size: 1rem;
}

#contact-us p {
  margin-block: 0 .7rem;
}

#contact-us a:any-link {
  margin-inline: .15rem;
  font-weight: bold;
  color: #183400;
  text-shadow: 0px 0px 1px #080f0180;
  text-decoration: none;
}

#contact-us a:active {
  color: #ffffff;
}

#contact-us a:hover {
  color: #2f6500;
  text-decoration: underline;
}

#socials p {
  margin: 0;
}

#legal {
  display: flex;
  flex-direction: column;
  width: 27.5%;
  align-items: flex-end;
  justify-content: center;
  margin: 0 .33rem;
}
</style>