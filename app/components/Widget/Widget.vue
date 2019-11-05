<template>
  <div>
    <Wd-Number v-if="type == 'number'" :number="5" />
    <div v-else>
      Pas un Nombre
    </div>
  </div>
</template>

<script>
import WdNumber from "./Type/Number";

export default {
  name: "Widget",
  components: {
    WdNumber
  },
  props: {
    type: { type: String, default: "number" }
  }
};
</script>
