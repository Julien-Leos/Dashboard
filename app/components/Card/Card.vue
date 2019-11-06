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
      {{ name }}
    </span>
    <img
      class="cardImage"
      :src="'/' + imageName + '.png'"
      :style="'opacity: ' + (isOvered ? 0.4 : 1)"
    />
  </div>
</template>

<script>
export default {
  name: "Card",
  props: {
    name: {
      type: String,
      default: "Name"
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
      imageName: "widget",
      isOvered: false
    };
  },
  methods: {
    adaptImageName(name) {
      return name.replace(" ", "_").toLowerCase();
    },
    actionBtn() {
      //  TO-DO: CALL AXIOS TO ACTIVATE THE SERVICE
    }
  },
  mounted() {
    this.backgroundColor = this.$brighterColor(this.color, 65);
    this.nameColor = this.$idealTextColor(this.color);
    this.imageName = this.adaptImageName(this.name);
  }
};
</script>

<style scoped>
.card {
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;
  width: 25vh;
  height: 25vh;
  border-radius: 0.3em;
  margin: 1.3vh;
  text-align: center;
  font-size: 1.2em;
  font-weight: bold;
}

.cardName {
  display: block;
  margin: 1.5vh 0.5vh;
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
