<template>
  <el-row :gutter="20" class="header">
    <el-col :span="18"
      ><h1><nuxt-link to="/">Dashboard</nuxt-link></h1></el-col
    >
    <el-col :span="3">
      <el-button type="info" plain size="medium"
        ><nuxt-link to="/signIn">SignIn</nuxt-link></el-button
      ></el-col
    >
    <el-col :span="3">
      <el-button type="primary"
        ><nuxt-link to="/signUp">SignUp</nuxt-link></el-button
      ></el-col
    >
  </el-row>
</template>

<script>
export default {
  name: "Header"
};
</script>

<style scoped>
.header {
  padding: 2vh;
  background-color: cornflowerblue;
  display: flex;
  align-items: center;
}
</style>
