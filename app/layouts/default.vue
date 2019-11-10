<template>
  <div>
    <el-container>
      <el-header height="8vh"><Header /></el-header>
    </el-container>
    <el-container style="height: 100vh">
      <el-aside v-show="isMenuDisplayed" :width="menuWidth + 'vh'"
        ><Menu @onCollapse="updateWidth"
      /></el-aside>
      <el-main><nuxt /></el-main>
    </el-container>
  </div>
</template>

<script>
import Header from "../components/Header";
import Menu from "../components/Menu";

export default {
  components: {
    Header,
    Menu
  },
  data: () => {
    return {
      menuWidth: 20
    };
  },
  computed: {
    isMenuDisplayed() {
      const pageName = this.$nuxt.$route.name;

      if (
        pageName === "index" ||
        pageName === "login" ||
        pageName === "register"
      )
        return false;
      return true;
    }
  },
  methods: {
    updateWidth(newWidth) {
      setTimeout(() => {
        this.menuWidth = newWidth;
      }, 150);
    }
  }
};
</script>

<style>
html {
  font-family: "Helvetica Neue";
  font-size: 16px;
  word-spacing: 1px;
  -ms-text-size-adjust: 100%;
  -webkit-text-size-adjust: 100%;
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
  box-sizing: border-box;
}

*,
*:before,
*:after {
  box-sizing: border-box;
  margin: 0;
}

.primary {
  color: #3f9eff;
}
.bg-primary {
  background: #3f9eff;
}

.primary-light {
  color: #80cfff;
}
.bg-primary-light {
  background: #80cfff;
}

.primary-dark {
  color: #0070cb;
}
.bg-primary-dark {
  background: #0070cb;
}

.bg-gray {
  background: #e6e6e6;
}
.bg-gray-light {
  background: #f2f2f2;
}

a {
  text-decoration: none;
}

a:visited {
  color: inherit;
}

a:link {
  color: inherit;
}

.el-header {
  padding: 0;
}

.el-link.el-link--default.is-disabled {
  color: inherit;
}
</style>
