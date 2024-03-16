<script setup lang="ts">
import { RouterView } from 'vue-router'

import CommonHeader from './components/CommonHeader.vue'
import CommonSidebar from './components/CommonSidebar.vue'
import CommonFooter from './components/CommonFooter.vue'
</script>

<template>
  <div class="main-wrapper">
    <!-- <CommonSidebar />   This is now going to be dynamically loaded as a popup menu so it isn't always visible   -->
    <!-- This allows us to keep all pages loaded, and avoids too many API calls -->
    <RouterView v-slot="{ Component }">
      <KeepAlive>
        <component :is="Component" />
      </KeepAlive>
    </RouterView>
  </div>
</template>

<!-- Not scoped here! global css App wide ... -->
<style>
@import url('https://fonts.googleapis.com/css2?family=Open+Sans&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono&family=Open+Sans:wght@400;800&display=swap');

/* Global general styles */
* {
  font-family: 'Open Sans', sans-serif;
  line-height: 1.25rem;
}

code {
  font-family: 'IBM Plex Mono', monospace;
  font-family: 'Open Sans', sans-serif;
}

strong {
  font-weight: bold;
}

html {
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
}

body {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  overflow-y: hidden;
  overflow-x: hidden;
  margin: 0;
}

#app {
  display: flex;
  flex-direction: column;
  justify-content: start;
}

.main-wrapper {
  display: flex;
  flex-grow: 1;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
}

.main-wrapper header {
  font-family: 'Open Sans', sans-serif;
  color: #4b5320;
  text-align: center;
}

header {
  width: 100vw;
}

.main-wrapper h1 {
  margin: 0;
  margin-bottom: .25rem;
  font-size: 2.75rem;
  line-height: 3rem;
}

.main-wrapper header p {
  font-size: 1.5rem;
}

.main-wrapper h2 {
  color: #4b5320;
  text-align: center;
  font-size: 2rem;
  line-height: 2.5rem;
  margin-block: .33rem;
}

#profile-login {
  position: fixed;
  top: 1rem;
  right: 1rem;
  display: flex;
}

/* Buttons and Links */
button,
#home-wrapper main a,
#about-wrapper a {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-block: .75rem;
  padding: 12px 24px;
  color: white;
  background-color: #4a5834;
  font-size: 1.1rem;
  font-weight: bold;
  border: none;
  border-radius: 4px;
  text-decoration: none;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
}

button:hover,
#home-wrapper main a:hover,
#about-wrapper a:hover {
  background-color: #71864f;
  color: #d3d3d3;
}

/* Localized styles */
#home-wrapper,
#about-wrapper,
#login-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Site header styles */
#site-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-bottom: 3px solid #183400;
  padding-bottom: 5px;
  background-image: linear-gradient(to top, rgba(159, 177, 132, 0), rgba(159, 177, 132, 1))
}

#site-header #logo-title a {
  display: flex;
  flex-direction: row;
  align-items: center;
  text-decoration: none;
}

#site-header #logo-title h1 {
  padding-left: .5rem;
  font-size: 2rem;
  font-weight: bold;
  color: #183400;
  text-shadow: 0px 0px 1px #080f0180;
}

#site-header nav {
  display: flex;
  flex-direction: row;
  margin-top: .25rem;
  justify-content: center;
  font-size: 1.25rem;
}

#site-header nav a,
#login,
#logout,
#register {
  padding: 5px;
  margin-inline: 1rem;
  border-radius: 2px;
  font-weight: bold;
  text-shadow: 0px 0px 1px #080f01a0;
  text-decoration: none;
  color: #234a00;
  transition: background-color 0.3s, color 0.3s;
}

#site-header nav a:active,
#login:active,
#logout:active,
#register:active {
  color: #ffffff;
}

#site-header nav a:hover,
#login:hover,
#logout:hover,
#register:hover {
  color: #142b00;
  background-color: #83b325;
}

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


@media screen and (max-width: 800px) {
  /* Global general styles -----------------------------------------------------------------------------------------------------*/
  .main-wrapper h1 {
    margin-bottom: .25rem;
    font-size: 2rem;
    line-height: 2.25rem;
  }

  .main-wrapper header p {
    font-size: 1rem;
  }

  .main-wrapper h2 {
    font-size: 1.33rem;
    line-height: 1.5rem;
    margin-block: .25rem;
  }

  /* Site header styles */
  #site-header {
    align-items: flex-start;
    padding-block: 1rem;
  }

  #site-header #logo-title h1 {
    font-size: 1.33rem;
  }

  #site-header nav {
    font-size: .8rem;
  }

  nav a,
  #login,
  #logout,
  #register {
    margin-inline: .5rem;
  }

  #profile-login {
    top: .25rem;
    right: .25rem;
    flex-direction: column;
    align-items: flex-end;
  }

  #login,
  #logout,
  #register {
    padding: 0;
  }

  /* Site footer styles */
  footer {
    padding-block: 2rem 0;
  }

  footer>div {
    flex-direction: column;
  }

  #extra-info {
    width: 95%;
    align-items: center;
    margin-bottom: 1rem;
  }

  #extra-info h3 {
    font-size: 1rem;
    margin-bottom: .25rem;
  }

  #extra-info p {
    font-size: .8rem;
  }

  #contact-us {
    width: 95%;
    font-size: .8rem;
    margin-bottom: 1rem;
  }

  #contact-us p {
    margin-block: 0;
  }

  #socials p {
    margin: 0;
    margin-top: .5rem;
  }

  #legal {
    width: 100%;
    align-items: flex-end;
  }
}
</style>