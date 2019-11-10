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
          :min-w="3"
          :min-h="4"
          @moved="movedWidget"
          @resized="resizedWidget"
          :style="'background-color: #' + widget.color"
          class="widgetContainer"
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
        .replace("_", " ")
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
      testData: {
        direction: "column",
        items: [
          {
            value: 5
          }
        ]
      }
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
              await this.getWidgetAPI(service[1].name, widget[1].name).then(
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
  methods: {
    movedWidget() {
      this.widgetsUpdates = true;
    },
    resizedWidget() {
      this.widgetsUpdates = true;
    },
    getWidgetAPI(serviceName, widgetName) {
      return this.$axios.get(serviceName + "/" + widgetName).then(response => {
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
