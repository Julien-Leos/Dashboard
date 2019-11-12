<template>
  <div>
    <ConfigurePanel
      :is-visible="configurePanel"
      :params="widget.params"
      :params-data="widget.paramsData"
      :timer-data="parseFloat(widget.timer)"
      @submit="connect"
    />
    <div
      class="card"
      :style="'background: #' + backgroundColor"
      @mouseover="isOvered = true"
      @mouseleave="isOvered = false"
    >
      <el-button
        v-if="isOvered && isConnected"
        class="actionBtn"
        style="top: 20%"
        type="primary"
        plain
        rounded
        @click="configurePanel = true"
        >Configure</el-button
      >
      <el-button
        v-if="isOvered"
        class="actionBtn"
        :style="isConnected ? 'bottom: 20%' : ''"
        type="primary"
        plain
        rounded
        @click="actionBtn"
        >{{ isConnected ? "Remove" : "Add" }}</el-button
      >
      <span
        class="cardName"
        :style="'color: #' + nameColor + ';opacity: ' + (isOvered ? 0.4 : 1)"
      >
        {{ widget.name | widgetName }}
      </span>
      <img
        class="cardImage"
        :src="'/' + widget.serviceName + '.png'"
        :style="'opacity: ' + (isOvered ? 0.1 : 0.2)"
      />
      <span
        class="cardDesc"
        :style="'color: #' + nameColor + ';opacity: ' + (isOvered ? 0.4 : 1)"
      >
        {{ widget.description }}
      </span>
    </div>
  </div>
</template>

<script>
import ConfigurePanel from "./ConfigurePanel";

export default {
  name: "WidgetCard",
  components: {
    ConfigurePanel
  },
  filters: {
    widgetName: value => {
      return value
        .replace(/_/gi, " ")
        .split(" ")
        .map(element => element[0].toUpperCase() + element.slice(1))
        .join(" ");
    }
  },
  props: {
    widget: {
      type: Object,
      default: () => ({})
    },
    isConnected: {
      type: Boolean,
      default: false
    }
  },
  data: () => {
    return {
      backgroundColor: "#FFFFFF",
      nameColor: "#000000",
      isOvered: false,
      configurePanel: false
    };
  },
  mounted() {
    this.backgroundColor = this.$brighterColor(this.widget.color, 65);
    this.nameColor = this.$idealTextColor(this.widget.color);
  },
  methods: {
    actionBtn() {
      if (this.isConnected) {
        this.disconnect();
      } else {
        this.configurePanel = true;
      }
    },
    connect(data) {
      this.configurePanel = false;
      if (data) {
        const bodyFormData = new FormData();
        const urlSuffix = this.isConnected ? "/" + this.widget.id : "";

        if (!this.isConnected) bodyFormData.set("name", this.widget.name);
        bodyFormData.set("timer", data.timer);
        bodyFormData.set("params", JSON.stringify(data.form));
        this.$axios({
          method: this.isConnected ? "put" : "post",
          url:
            "users/" +
            this.$store.state.auth.userId +
            "/services/" +
            this.widget.serviceId +
            "/widgets" +
            urlSuffix,
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
            }
            this.$emit("onConnect");
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
      }
    },
    disconnect() {
      this.$axios
        .delete(
          "users/" +
            this.$store.state.auth.userId +
            "/services/" +
            this.widget.serviceId +
            "/widgets/" +
            this.widget.id
        )
        .then(response => {
          if (response) {
            this.$message({
              showClose: true,
              message: response.data.message,
              type: "success"
            });
          }
          this.widget.paramsData = {};
          this.$emit("onConnect");
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
    }
  }
};
</script>

<style scoped>
.card {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;
  width: 25vh;
  height: 25vh;
  border-radius: 0.3em;
  margin: 1.3vh;
}

.cardName {
  display: block;
  margin: 1.5vh 0.5vh;
  font-size: 1.4em;
  font-weight: bold;
  z-index: 1;
}

.cardDesc {
  display: block;
  margin: 0.5vh 2vh;
  font-size: 1em;
  z-index: 1;
}

.cardImage {
  position: absolute;
}

.actionBtn {
  position: absolute;
  z-index: 2;
}

.el-button + .el-button {
  margin: 0;
}
</style>
