<template>
  <client-only>
    <div>
      <grid-layout
        :layout="widgets"
        :col-num="12"
        :row-height="30"
        :margin="[15, 15]"
      >
        <grid-item
          v-for="widget in widgets"
          :key="widget.i"
          :x="widget.x"
          :y="widget.y"
          :w="widget.w"
          :h="widget.h"
          :i="widget.i"
          @moved="movedWidget"
          @resized="resizedWidget"
        >
          {{ widget.x }}
          {{ widget.y }}
          {{ widget.w }}
          {{ widget.h }}
          <Widget type="number" />
        </grid-item>
      </grid-layout>
      <el-button
        v-show="widgetsUpdates"
        @click="saveUpdates"
        class="saveBtn"
        type="success"
        >Save Updates</el-button
      >
    </div>
  </client-only>
</template>

<script>
import Widget from "../components/Widget/Widget";

export default {
  middleware: "auth",
  components: {
    Widget
  },
  data: () => {
    return {
      widgets: [],
      widgetsUpdates: false
    };
  },
  mounted() {
    this.$axios
      .get("users/" + this.$store.state.auth.userId + "/services")
      .then(response => {
        if (response) {
          Object.entries(response.data.data.services).forEach(service => {
            Object.entries(service[1].widgets).forEach(widget => {
              widget[1].serviceId = service[0];
              widget[1].i = widget[0];
              for (const [key, value] of Object.entries(widget[1]))
                if (key === "x" || key === "y" || key === "h" || key === "w")
                  widget[1][key] = parseInt(value);
              this.widgets.push(widget[1]);
            });
          });
        }
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
  },
  methods: {
    movedWidget() {
      this.widgetsUpdates = true;
    },
    resizedWidget() {
      this.widgetsUpdates = true;
    },
    saveUpdates() {
      for (const widget of Object.values(this.widgets)) {
        const bodyFormData = new FormData();

        bodyFormData.set("x", widget.x);
        bodyFormData.set("y", widget.y);
        bodyFormData.set("w", widget.w);
        bodyFormData.set("h", widget.h);
        this.$axios({
          method: "put",
          url:
            "users/" +
            this.$store.state.auth.userId +
            "/services/" +
            widget.serviceId +
            "/widgets/" +
            widget.i,
          data: bodyFormData,
          config: { headers: { "Content-Type": "multipart/form-data" } }
        }).catch(error => {
          if (error.response) {
            this.$message({
              showClose: true,
              message: error.response.data.message,
              type: "error"
            });
          }
        });
      }
      this.$message({
        showClose: true,
        message: "Widgets's position and size successfully saved.",
        type: "success"
      });
    }
  }
};
</script>

<style scoped>
.vue-grid-item {
  background-color: aqua;
}
.saveBtn {
  position: absolute;
  right: 4vh;
  bottom: 4vh;
  font-size: 1.2em;
  z-index: 3;
}
</style>
