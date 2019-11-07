<template>
  <el-row :gutter="20" class="header bg-primary-dark">
    <el-col :span="18"
      ><h1><nuxt-link to="/">Dashboard</nuxt-link></h1></el-col
    >
    <el-col
      v-show="!$store.state.auth.accessToken"
      :span="6"
      class="header-auth"
    >
      <el-button type="info" plain size="medium"
        ><nuxt-link to="/login">Sign-In</nuxt-link></el-button
      >
      <el-button type="primary"
        ><nuxt-link to="/register">Sign-Up</nuxt-link></el-button
      >
    </el-col>
    <el-col
      v-show="$store.state.auth.accessToken"
      :span="6"
      class="header-auth"
    >
      <nuxt-link to="/home">
        {{ $store.state.auth.username.toUpperCase() }}
      </nuxt-link>
      <el-button type="danger" @click="logout"
        ><nuxt-link to="/">Sign-Out</nuxt-link></el-button
      >
    </el-col>
  </el-row>
</template>

<script>
export default {
  name: "Header",
  methods: {
    logout() {
      this.$store.commit("auth/logout");
    }
  }
};
</script>

<style scoped>
.header {
  height: 8vh;
  color: white;
  padding: 2vh;
  display: flex;
  align-items: center;
}

.header-auth {
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  align-items: center;
}

.el-button {
  margin-left: 2vh;
}
</style>
