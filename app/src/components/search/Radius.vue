<template>
  <v-select
    class="radius_select"
    label="Umkreis"
    item-value="value"
    :items="radii"
    :dark="dark"
    :disabled="disabled"
    :attach="attachTo"
    v-model="radius"
    @change="onInputChange"
    @keydown.enter="onEnter"
  />
</template>

<script lang="ts">
import Vue from "vue";
import Radius from "@/models/radius";
import radii from "@/resources/radii";

export default Vue.extend({
  name: "Radius",
  props: {
    value: {
      type: String,
      required: true,
    },
    international: {
      type: Boolean,
      default: true,
    },
    dark: {
      type: Boolean,
      default: false,
    },
    attachTo: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      radii: radii as Radius[],
      radius: this.value as string | null,
    };
  },
  watch: {
    /** change selection on value change */
    value(): void {
      this.setRadius();
    },
    international(): void {
      if (this.international) this.radius = null;
    },
  },
  computed: {
    disabled(): boolean {
      return this.international;
    },
  },
  mounted(): void {
    this.setRadius();
  },
  methods: {
    setRadius() {
      this.radius = this.value || this.radii[0].value;
      this.$emit("input", this.radius);
    },
    onInputChange(): void {
      this.$emit("input", this.radius);
    },
    onEnter(): void {
      this.$emit("input", this.radius);
      this.$emit("enter");
    },
  },
});
</script>

<style lang="scss" scoped>
@media (min-width: 600px) {
  .radius_select {
    width: 200px;
  }
}
</style>
