<template>
  <div id="app">
    {{info}}
  </div>
</template>

<script>
const axios = require("axios");

export default {
  name: "app",
  data: () => {
    return {
      info: 4
    };
  },
  mounted() {
    axios
      .get("https://api.coindesk.com/v1/bpi/currentprice.json")
      .then(response => (this.info = response));
  }
};
</script>

<style lang="scss">
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
