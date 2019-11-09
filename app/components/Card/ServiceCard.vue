<template>
  <div
    class="card"
    :style="'background: #' + backgroundColor"
    @mouseover="isOvered = true"
    @mouseleave="isOvered = false"
  >
    <el-button
      v-show="isOvered"
      class="actionBtn"
      type="primary"
      plain
      rounded
      @click="actionBtn"
      >{{ isConnected ? "Disconnect" : "Connect" }}</el-button
    >
    <span
      class="cardName"
      :style="'color: #' + nameColor + ';opacity: ' + (isOvered ? 0.4 : 1)"
    >
      {{ name | serviceName }}
    </span>
    <img
      class="cardImage"
      :src="'/' + name + '.png'"
      :style="'opacity: ' + (isOvered ? 0.4 : 1)"
    />
  </div>
</template>

<script>
export default {
  name: "ServiceCard",
  filters: {
    serviceName: value => {
      return value
        .replace("_", " ")
        .split(" ")
        .map(element => element[0].toUpperCase() + element.slice(1))
        .join(" ");
    }
  },
  props: {
    id: {
      type: String,
      default: ""
    },
    name: {
      type: String,
      default: "Service"
    },
    isOauth: {
      type: Boolean,
      default: false
    },
    color: {
      type: String,
      default: "FFFFFF"
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
      isOvered: false
    };
  },
  mounted() {
    this.backgroundColor = this.$brighterColor(this.color, 65);
    this.nameColor = this.$idealTextColor(this.color);
  },
  methods: {
    actionBtn() {
      if (this.isConnected) {
        this.$axios({
          method: "delete",
          url: "users/" + this.$store.state.auth.userId + "/services/" + this.id
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
      } else {
        const bodyFormData = new FormData();

        bodyFormData.set("name", this.name);
        this.$axios({
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
}

.cardImage {
  width: 40%;
  flex-shrink: 0;
}

.actionBtn {
  position: absolute;
  z-index: 1;
}
</style>
