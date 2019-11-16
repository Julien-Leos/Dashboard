<template>
  <div>
    <el-container class="bg-gray-light">
      <el-header height="5vh">Activated Services</el-header>
      <el-main class="serviceCard bg-gray">
        <span v-if="activatedServices.length === 0"
          >There are no service connected</span
        >
        <ServiceCard
          v-for="service in activatedServices"
          v-else
          :key="service.id"
          :service="service"
          :is-connected="true"
          @onAction="actionBtn"
        />
      </el-main>
    </el-container>
    <el-container class="bg-gray-light">
      <el-header height="5vh">Available Services</el-header>
      <el-main class="serviceCard bg-gray">
        <span v-if="availableServices.length === 0"
          >There are no more service to connect</span
        >
        <ServiceCard
          v-for="service in availableServices"
          v-else
          :key="service.id"
          :service="service"
          :is-connected="false"
          @onAction="actionBtn"
        />
      </el-main>
    </el-container>
  </div>
</template>

<script>
import ServiceCard from "../components/Card/ServiceCard";

export default {
  middleware: "auth",
  components: {
    ServiceCard
  },
  data: () => {
    return {
      services: {},
      availableServices: [],
      activatedServices: []
    };
  },
  async mounted() {
    await this.$axios
      .get("services")
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
    if (document.location.hash || document.location.href.split("?").length > 1)
      this.connectService(null);
    else this.getActivatedServices();
  },
  methods: {
    actionBtn(params) {
      if (params[0] === true) this.connectService(params[1]);
      else this.disconnectService(params[1]);
    },
    async connectService(service) {
      let serviceName = "";
      const bodyFormData = new FormData();

      if (service) serviceName = service.name;
      else serviceName = this.parseUrlHref();

      bodyFormData.set("name", serviceName);
      bodyFormData.set("accessToken", "null");
      await this.$axios({
        method: "post",
        url: "users/" + this.$store.state.auth.userId + "/services",
        data: bodyFormData,
        config: { headers: { "Content-Type": "multipart/form-data" } }
      })
        .then(response => {
          if (response) {
            this.$message({
              showClose: true,
              message: response.data.message,
              type: "success"
            });
            if (!service) this.oauth2Callback(serviceName);
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
      this.getActivatedServices();
    },
    async disconnectService(service) {
      await this.$axios({
        method: "delete",
        url:
          "users/" + this.$store.state.auth.userId + "/services/" + service.id
      })
        .then(response => {
          if (response) {
            this.$message({
              showClose: true,
              message: response.data.message,
              type: "success"
            });
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
      this.getActivatedServices();
    },
    getActivatedServices() {
      this.$axios
        .get("users/" + this.$store.state.auth.userId + "/services")
        .then(response => {
          if (response) {
            this.activatedServices = [];
            this.availableServices = [];
            this.services.forEach(service => {
              const activatedService = Object.entries(
                response.data.data.services
              ).find(
                dbActivatedService =>
                  dbActivatedService[1].name === service.name
              );
              if (activatedService) {
                service.id = activatedService[0];
                this.activatedServices.push(service);
              } else this.availableServices.push(service);
            });
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
    },
    parseUrlHref() {
      const url = window.location.href.split("#")[0];
      const urlArgs = url.split("?")[1];
      const urlArg = urlArgs.split("&");
      const data = urlArg
        .find(arg => arg.split("=")[0] === "from")
        .split("=")[1];

      return data;
    },
    async oauth2Callback(serviceName) {
      const bodyFormData = new FormData();

      bodyFormData.set(
        "url",
        window.location.hash ? window.location.hash : window.location.href
      );
      bodyFormData.set("userId", this.$store.state.auth.userId);
      await this.$axios({
        method: "post",
        url: serviceName + "/oauth2",
        data: bodyFormData,
        config: { headers: { "Content-Type": "multipart/form-data" } }
      });
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

.serviceCard {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: space-evenly;
}

.el-main {
  text-align: center;
}
</style>
