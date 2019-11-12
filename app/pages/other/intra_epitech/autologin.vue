<template>
  <div class="centered">
    <el-form ref="form" :model="form" label-width="120px">
      <el-form-item label="Token Autologin">
        <el-input
          v-model="form.autologin"
          placeholder="Enter yout autologin"
        ></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">Send</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  data: () => {
    return {
      form: {
        autologin: ""
      }
    };
  },
  methods: {
    onSubmit() {
      const redirectUri = decodeURIComponent(
        window.location.href.split("?")[1].split("=")[1]
      );
      window.open(redirectUri + "#token=" + this.form.autologin, "_self");
    }
  }
};
</script>

<style scoped>
.centered {
  display: flex;
  flex-direction: column;
  align-content: center;
  justify-content: center;
  height: 100%;
}
</style>
