<template>
  <v-select
    class="radius_select"
    label="Umkreis"
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
  name: "RadiusSelect",
  props: {
    value: {
      type: Object as () => Radius,
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
      radius: this.value as Radius,
    };
  },
  watch: {
    /** change selection on value change */
    value(): void {
      this.setRadius();
    },
    international(): void {
      if (this.international) this.radius = this.defaultRadii;
    },
  },
  computed: {
    disabled(): boolean {
      return this.international;
    },
    defaultRadii(): Radius {
      return this.radii[0];
    },
  },
  mounted(): void {
    this.setRadius();
  },
  methods: {
    setRadius() {
      this.radius = this.value || this.defaultRadii;
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
    width: 100px;
  }
}
</style>
