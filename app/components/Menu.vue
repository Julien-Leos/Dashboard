<template>
  <el-menu
    :collapse="isCollapse"
    class="el-menu-vertical-demo bg-primary-light"
  >
    <el-button class="expand-btn" type="primary" @click="collapse">
      <font-awesome-icon
        :icon="'angle-double-' + (isCollapse == false ? 'left' : 'right')"
        style="font-size: 2em"
      />
    </el-button>
    <nuxt-link to="/home">
      <el-menu-item index="1">
        <font-awesome-icon icon="th-large" />
        <span slot="title">Home</span>
      </el-menu-item>
    </nuxt-link>
    <nuxt-link to="/services">
      <el-menu-item index="2">
        <font-awesome-icon icon="cogs" />
        <span slot="title">Services</span>
      </el-menu-item>
    </nuxt-link>
    <nuxt-link to="/services">
      <el-menu-item index="3">
        <font-awesome-icon icon="puzzle-piece" />
        <span slot="title">Widgets</span>
      </el-menu-item>
    </nuxt-link>
  </el-menu>
</template>

<script>
export default {
  name: "Menu",
  data: () => {
    return {
      isCollapse: false
    };
  },
  methods: {
    collapse() {
      this.isCollapse = this.isCollapse === false;
      this.$emit("onCollapse", this.isCollapse ? 8 : 20);
    }
  }
};
</script>

<style scoped>
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 20vh;
  min-height: 100%;
}

.el-menu {
  min-height: 100%;
}

.expand-btn {
  margin: 2vh;
  width: -webkit-fill-available;
  padding: 0.5vh;
}

svg {
  margin-right: 2vh;
}
</style>
