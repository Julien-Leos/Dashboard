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
        :label="param.desc"
      >
        <el-select v-if="param.type == 'list'" v-model="form[param.name]">
          <el-option
            v-for="item in param.list"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
        <el-date-picker
          v-else-if="param.type == 'date'"
          v-model="form[param.name]"
          :type="param.dateType != undefined ? param.dateType : 'date'"
          :value-format="
            param.dateFormat != undefined ? param.dateFormat : 'yyyy-M-d'
          "
          placeholder="Pick a date"
        >
        </el-date-picker>
        <el-date-picker
          v-else-if="param.type == 'dateRange'"
          v-model="form[param.name]"
          type="daterange"
          :value-format="
            param.dateFormat != undefined ? param.dateFormat : 'yyyy-M-d'
          "
          start-placeholder="Start date"
          end-placeholder="End date"
        >
        </el-date-picker>
        <el-input
          v-else
          v-model="form[param.name]"
          :type="typeMap[param.type]"
        />
      </el-form-item>
      <el-form-item label="Timer">
        <el-input v-model="timer" type="number"
          ><template slot="prepend"
            >Each</template
          ><template slot="append"
            >minutes</template
          ></el-input
        ></el-form-item
      >
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
    },
    timerData: {
      type: Number,
      default: 10
    }
  },
  data: () => {
    return {
      form: {},
      saveParamsData: {},
      timer: 10,
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
    this.timer = this.timerData || 10;
    this.saveParamsData = JSON.parse(JSON.stringify(this.paramsData));
    for (const item of Object.entries(this.paramsData)) {
      this.$set(this.form, item[0], item[1]);
    }
  },
  methods: {
    checkForm() {
      if (Object.keys(this.form).length !== this.params.length || !this.timer) {
        this.$message({
          showClose: true,
          message: "One of the parameter is empty.",
          type: "error"
        });
      } else {
        this.$emit("submit", { form: this.form, timer: this.timer });
      }
    }
  }
};
</script>

<style scoped>
.el-select,
.el-date-editor {
  width: 100%;
}
</style>
