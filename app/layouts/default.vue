<template>
  <div>
    <el-container>
      <el-header><Header /></el-header>
      <el-main><nuxt /></el-main>
    </el-container>
  </div>
</template>

<script>
import Header from "../components/Header";

export default {
  components: {
    Header
  }
};
</script>

<style>
html {
  font-family: "Source Sans Pro", -apple-system, BlinkMacSystemFont, "Segoe UI",
    Roboto, "Helvetica Neue", Arial, sans-serif;
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

a {
  text-decoration: none;
}

a:visited {
  color: inherit;
}

.el-header {
  padding: 0;
}
</style>
