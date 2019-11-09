<template>
  <div>
    <el-container class="bg-gray-light">
      <el-header height="5vh">Activated Widgets</el-header>
      <el-main class="widgetCard bg-gray">
        <span v-if="activatedWidgets.length === 0"
          >There are no widgets configured</span
        >
        <WidgetCard
          v-for="widget in activatedWidgets"
          v-else
          :id="widget.id"
          :key="widget.id"
          :name="widget['name']"
          :color="widget['color']"
          :is-connected="true"
          @onConnect="getActivatedWidgets"
        />
      </el-main>
    </el-container>
    <el-container class="bg-gray-light">
      <el-header height="5vh">Available Widgets</el-header>
      <el-main class="widgetCard bg-gray">
        <span v-if="availableWidgets.length === 0"
          >There are no more widgets to configure</span
        >
        <WidgetCard
          v-for="widget in availableWidgets"
          v-else
          :key="widget.id"
          :name="widget['name']"
          :color="widget['color']"
          :is-connected="false"
          @onConnect="getActivatedWidgets"
        />
      </el-main>
    </el-container>
  </div>
</template>

<script>
import WidgetCard from "../components/Card/WidgetCard";

const axios = require("axios");

export default {
  middleware: "auth",
  components: {
    WidgetCard
  },
  data: () => {
    return {
      services: {},
      widgets: {},
      activatedServices: [],
      availableWidgets: [],
      activatedWidgets: []
    };
  },
  mounted() {
    axios
      .get("http://localhost:8080/services")
      .then(response => {
        if (response) {
          this.services = response.data.data.services;
        }
      })
      .catch(error => {
        if (error.response) {
          this.$message({
            showClose: true,
            message: error.response.data.message,
            type: "error"
          });
        }
      });
    axios
      .get("http://localhost:8080/widgets")
      .then(response => {
        if (response) {
          this.widgets = response.data.data.widgets;
        }
      })
      .catch(error => {
        if (error.response) {
          this.$message({
            showClose: true,
            message: error.response.data.message,
            type: "error"
          });
        }
      });
    axios
      .get(
        "http://localhost:8080/users/" +
          this.$store.state.auth.userId +
          "/services"
      )
      .then(response => {
        if (response) {
          this.activatedServices = response.data.data.services;
        }
      })
      .catch(error => {
        if (error.response) {
          this.$message({
            showClose: true,
            message: error.response.data.message,
            type: "error"
          });
        }
      });
    this.getActivatedWidgets();
  },
  methods: {
    getActivatedWidgets() {
      // axios({
      //   method: "get",
      //   url:
      //     "http://localhost:8080/users/" +
      //     this.$store.state.auth.userId +
      //     "/services"
      // })
      //   .then(response => {
      //     if (response) {
      //       this.activatedWidgets = [];
      //       this.availableWidgets = [];
      //       this.services.forEach(service => {
      //         const dbActivatedWidgets = Object.entries(
      //           response.data.data.services
      //         );
      //         const activatedService = dbActivatedWidgets.find(
      //           dbActivatedService =>
      //             dbActivatedService[1].name === service.name
      //         );
      //         if (activatedService) {
      //           service.id = activatedService[0];
      //           this.activatedWidgets.push(service);
      //         } else this.availableWidgets.push(service);
      //       });
      //     }
      //   })
      //   .catch(error => {
      //     if (error.response) {
      //       this.$message({
      //         showClose: true,
      //         message: error.response.data.message,
      //         type: "error"
      //       });
      //     }
      //   });
    }
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

.widgetCard {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: space-evenly;
}

.el-main {
  text-align: center;
}
</style>
