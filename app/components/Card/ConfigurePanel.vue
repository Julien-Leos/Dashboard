<template>
  <el-dialog
    title="Configure Widget"
    :visible="computedIsVisible"
    :show-close="false"
  >
    <el-form :model="form">
      <el-form-item
        v-for="param in params"
        :key="param.name"
        :label="param.name | ParamName"
      >
        <el-input v-model="form[param.name]" :type="typeMap[param.type]" />
      </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
      <el-button
        @click="
          form = saveParamsData;
          $emit('submit', null);
        "
        >Cancel</el-button
      >
      <el-button type="primary" @click="checkForm">Confirm</el-button>
    </span>
  </el-dialog>
</template>

<script>
export default {
  name: "ConfigurePanel",
  filters: {
    ParamName: value => {
      return value
        .replace("_", " ")
        .split(" ")
        .map(element => element[0].toUpperCase() + element.slice(1))
        .join(" ");
    }
  },
  props: {
    isVisible: {
      type: Boolean,
      default: false
    },
    params: {
      type: Array,
      default: () => []
    },
    paramsData: {
      type: Object,
      default: () => {
        return {};
      }
    }
  },
  data: () => {
    return {
      form: {},
      saveParamsData: {},
      typeMap: {
        string: "text",
        integer: "number"
      }
    };
  },
  computed: {
    computedIsVisible() {
      return this.isVisible;
    }
  },
  mounted() {
    this.saveParamsData = JSON.parse(JSON.stringify(this.paramsData));
    for (const item of Object.entries(this.paramsData)) {
      this.$set(this.form, item[0], item[1]);
    }
  },
  methods: {
    checkForm() {
      if (Object.keys(this.form).length !== this.params.length) {
        this.$message({
          showClose: true,
          message: "One of the parameter is empty.",
          type: "error"
        });
      } else {
        this.$emit("submit", this.form);
      }
    }
  }
};
</script>

<style scoped></style>
