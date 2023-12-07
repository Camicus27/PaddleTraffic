<script setup lang="ts">
</script>

<template>
  <footer>
    <div id="extra-info">
      <strong>Extra info goes here like contact or support or other links</strong>
      <nav>
          <a href="https://google.com">just google it</a>
      </nav>
    </div>
    <p id="legal">
      © PaddleTraffic 2023, All rights reserved
    </p>
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
    background-color: #9fb184;
    text-shadow: 1px 1px 1px #080f01;
    color: #183400;
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
    }
</style>