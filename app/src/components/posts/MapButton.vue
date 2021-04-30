<template>
  <div class="mb-2">
    <v-btn clas="btn-dark" dark @click="open = !open">
      <v-icon>map</v-icon>
      {{ open ? "Karte ausblenden" : "Karte anzeigen" }}
    </v-btn>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
export default Vue.extend({
  name: "MapButton",
  props: {
    value: {
      type: Boolean,
      required: true,
    },
  },
  data: function () {
    return {
      open: this.value,
    };
  },
  watch: {
    value() {
      this.open = this.value;
    },
    open() {
      this.$emit("input", this.open);
    },
  },
});
</script>