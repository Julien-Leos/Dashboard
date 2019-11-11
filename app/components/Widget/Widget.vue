<template>
  <div
    class="widget"
    :style="
      'flex-direction: ' +
        value.direction +
        ';background: #' +
        backgroundColor +
        ';color: #' +
        textColor
    "
  >
    <a
      v-for="(item, index) in value.items"
      :key="index"
      :class="typeof item.value == 'object' ? '' : 'centeredDisplay'"
      :style="directive + (item.span / totalSpan) * 100 + '%'"
      :href="item.link"
    >
      <Widget
        v-if="typeof item.value == 'object'"
        :value="item.value"
        :color="backgroundColor"
      />
      <span
        v-else
        :style="
          'font-size: ' +
            (textSize < inversedTextSize ? textSize : inversedTextSize) *
              ((item.span < 2 ? 2 : item.span) / 4) +
            'vh'
        "
      >
        {{ item.value }}
      </span>
    </a>
  </div>
</template>

<script>
export default {
  name: "Widget",
  props: {
    value: {
      type: Object,
      default: () => {}
    },
    color: {
      type: String,
      default: "ffffff"
    },
    w: {
      type: Number,
      default: 4
    },
    h: {
      type: Number,
      default: 7
    }
  },
  data: () => {
    return {
      totalSpan: 0,
      directive: "",
      backgroundColor: "",
      textColor: ""
    };
  },
  computed: {
    textSize() {
      const offset = this.value.direction === "column" ? this.h : this.w;
      return 1 * offset;
    },
    inversedTextSize() {
      const offset = this.value.direction === "column" ? this.w : this.h;
      return 1 * offset;
    }
  },
  beforeMount() {
    for (const item of Object.values(this.value.items)) {
      item.span = item.span || 1;
      this.totalSpan += item.span;
    }
    this.directive = this.value.direction === "column" ? "height: " : "width: ";
    this.backgroundColor = this.$brighterColor(this.color, 60);
    this.textColor = this.$idealTextColor(this.backgroundColor);
  }
};
</script>

<style>
.widget {
  display: flex;
  overflow: scroll;
  height: 100%;
  border-radius: 0.3em;
  padding: 0.3vh;
}

.widget a {
  min-width: calc(5% + 4vh);
  min-height: calc(5% + 4vh);
  padding: 0.8vh;
}

.centeredDisplay {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
