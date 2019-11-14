<template>
  <client-only>
    <div>
      <grid-layout
        :layout="widgets"
        :col-num="12"
        :row-height="30"
        :margin="[15, 15]"
        :vertical-compact="false"
      >
        <grid-item
          v-for="widget in widgets"
          :key="widget.i"
          :x="widget.x"
          :y="widget.y"
          :w="widget.w"
          :h="widget.h"
          :i="widget.i"
          :min-w="2"
          :min-h="3"
          class="widgetContainer"
          :style="'background-color: #' + widget.color"
          @moved="widgetsUpdates = true"
          @resized="widgetsUpdates = true"
        >
          <span
            :style="
              'color: #' +
                $idealTextColor(widget.color) +
                ';font-size: ' +
                (widget.w < widget.h ? widget.w : widget.h) * 0.8 +
                'vh'
            "
            >{{ widget.name | widgetName }}</span
          >
          <Widget
            :value="widget.data"
            :color="widget.color"
            :w="widget.w"
            :h="widget.h"
          />
        </grid-item>
      </grid-layout>
      <el-button
        v-show="widgetsUpdates"
        class="saveBtn"
        type="success"
        @click="saveUpdates"
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
  filters: {
    widgetName: value => {
      return value
        .replace(/_/gi, " ")
        .split(" ")
        .map(element => element[0].toUpperCase() + element.slice(1))
        .join(" ");
    }
  },
  data: () => {
    return {
      services: [],
      widgets: [],
      widgetsUpdates: false,
      intervalIds: []
    };
  },
  async mounted() {
    await this.$axios
      .get("/services")
      .then(response => {
        if (response) {
          this.services = response.data.data.services;
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
    await this.$axios
      .get("users/" + this.$store.state.auth.userId + "/services")
      .then(response => {
        if (response) {
          Object.entries(response.data.data.services).forEach(service => {
            Object.entries(service[1].widgets).forEach(async widget => {
              this.setWidgetTimer(service[1], widget[1]);
              await this.getWidgetAPI(service[1].name, widget[1]).then(
                data => (widget[1].data = data)
              );
              widget[1].color = this.services.find(
                i => i.name === service[1].name
              ).color;
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
  beforeDestroy() {
    for (const id of Object.values(this.intervalIds)) {
      clearInterval(id);
    }
  },
  methods: {
    setWidgetTimer(service, widget) {
      this.intervalIds.push(
        window.setInterval(async () => {
          await this.getWidgetAPI(service.name, widget).then(
            data => (widget.data = data)
          );
        }, widget.timer * 1000 * 60)
      );
    },
    getWidgetAPI(serviceName, widget) {
      const bodyFormData = new FormData();

      bodyFormData.set("params", widget.params);
      bodyFormData.set("userId", this.$store.state.auth.userId);
      return this.$axios({
        method: "post",
        url: serviceName + "/" + widget.name,
        data: bodyFormData,
        config: { headers: { "Content-Type": "multipart/form-data" } }
      }).then(response => {
        if (response) {
          return response.data;
        }
      });
    },
    async saveUpdates() {
      for (const widget of Object.values(this.widgets)) {
        const bodyFormData = new FormData();

        bodyFormData.set("x", widget.x);
        bodyFormData.set("y", widget.y);
        bodyFormData.set("w", widget.w);
        bodyFormData.set("h", widget.h);
        await this.$axios({
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
      this.widgetsUpdates = false;
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
.saveBtn {
  position: absolute;
  right: 4vh;
  bottom: 4vh;
  font-size: 1.2em;
  z-index: 3;
}

.widgetContainer {
  display: flex;
  flex-direction: column;
  padding: 1vh;
  border-radius: 0.3em;
}

.widgetContainer span {
  padding-bottom: 1vh;
  padding-left: 1vh;
}
</style>
