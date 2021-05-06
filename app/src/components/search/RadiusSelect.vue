<template>
  <v-select
    class="radius_select"
    label="Umkreis"
    :items="radii"
    :dark="dark"
    :disabled="disabled"
    :attach="attachTo"
    :value="radius"
    @change="onChange"
    @keydown.enter="onEnter"
  />
</template>

<script lang="ts">
import Vue from "vue";
import Radius from "@/models/radius";
import radii, { radii as radiiArray } from "@/resources/radii";

export default Vue.extend({
  name: "RadiusSelect",
  props: {
    value: {
      type: String,
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
      radius: {} as Radius,
    };
  },
  watch: {
    /** change selection on value change */
    value(): void {
      this.setRadius();
    },
  },
  computed: {
    disabled(): boolean {
      return this.international;
    },
    radii(): Radius[] {
      return radiiArray;
    },
  },
  mounted(): void {
    this.setRadius();
  },
  methods: {
    setRadius() {
      if (this.radius.value != this.value) this.radius = this.getRadiusObject();
    },
    onChange(v) {
      if (this.value != v) this.$emit("input", v);
    },
    onEnter(): void {
      this.$emit("input", this.radius.value);
      this.$emit("enter");
    },
    getRadiusObject() {
      return radii.find((r) => r.value == this.value) || radii[0];
    },
  },
});
</script>

<style lang="scss" scoped>
@media (min-width: 600px) {
  .radius_select {
    width: 100px;
  }
}
</style>
