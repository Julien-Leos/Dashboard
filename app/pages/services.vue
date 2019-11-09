<template>
  <div>
    <el-container class="bg-gray-light">
      <el-header height="5vh">Activated Services</el-header>
      <el-main class="bg-gray">
        <span v-if="activatedServices.length === 0"
          >There are no service connected</span
        >
        <Card
          v-for="(service, name) in activatedServices"
          v-else
          :key="name"
          :name="service['name']"
          :isOauth="Boolean(service['isOauth'])"
          :color="service['color']"
        />
      </el-main>
    </el-container>
    <el-container class="bg-gray-light">
      <el-header height="5vh">Available Services</el-header>
      <el-main class="cards bg-gray">
        <span v-if="availableServices.length === 0"
          >There are no more service availables</span
        >
        <Card
          v-for="(service, name) in availableServices"
          v-else
          :key="name"
          :name="service['name']"
          :isOauth="Boolean(service['isOauth'])"
          :color="service['color']"
        />
      </el-main>
    </el-container>
  </div>
</template>

<script>
import Card from "../components/Card/Card";

const axios = require("axios");

export default {
  middleware: "auth",
  components: {
    Card
  },
  data: () => {
    return {
      availableServices: [],
      activatedServices: []
    };
  },
  mounted() {
    axios({
      method: "get",
      url: "http://localhost:8080/services"
    })
      .then(response => {
        if (response) {
          this.availableServices = response.data.data.services;
        }
      })
      .catch(error => {
        if (error) {
          this.$message({
            showClose: true,
            message: error.response.data.message,
            type: "error"
          });
        }
      });
  }
};
</script>

<style scoped>
.el-container {
  border-radius: 1em;
  margin-bottom: 3vh;
}

.el-header {
  margin: 1vh 3vh;
  font-size: 1.5em;
}

.el-main {
  margin: 0 1.5vh 1.5vh 1.5vh;
  border-radius: 0.5em;
}

.cards {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: space-evenly;
}

.el-main {
  text-align: center;
}
</style>
