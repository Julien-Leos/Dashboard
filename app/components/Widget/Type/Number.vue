<template>
  <div>
    {{ number }}
  </div>
</template>

<script>
export default {
  name: "WdNumber",
  props: {
    number: { type: Number, default: 0 }
  }
};
</script>
