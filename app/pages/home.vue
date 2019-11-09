<template>
  <client-only>
    <grid-layout
      :layout="layout"
      :col-num="12"
      :row-height="30"
      :is-draggable="true"
      :is-resizable="true"
      :is-mirrored="false"
      :vertical-compact="true"
      :margin="[10, 10]"
      :use-css-transforms="true"
    >
      <grid-item
        v-for="item in layout"
        :key="item.i"
        :x="item.x"
        :y="item.y"
        :w="item.w"
        :h="item.h"
        :i="item.i"
      >
        <Widget :type="item.type" />
      </grid-item>
    </grid-layout>
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
      layout: [
        { x: 0, y: 0, w: 4, h: 7, i: "0", type: "number" },
        // { x: 0, y: 0, w: 1, h: 1, i: "1", type: "autre" },
        { x: 4, y: 0, w: 2, h: 5, i: "2", type: "autre" },
        { x: 6, y: 0, w: 2, h: 3, i: "3", type: "autre" },
        { x: 8, y: 0, w: 2, h: 3, i: "4", type: "number" },
        { x: 10, y: 0, w: 2, h: 3, i: "5", type: "number" }
      ]
    };
  }
};
</script>

<style scoped>
.vue-grid-item {
  background-color: aqua;
}
</style>
