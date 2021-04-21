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

export default Vue.extend({
  name: "Radius",
  props: {
    value: {
      type: Object as () => Radius,
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
      radii: [] as Radius[],
      radius: this.value as Radius | null,
    };
  },
  watch: {
    /** change selection on value change */
    value(): void {
      this.radius = this.value;
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
    this.radius = this.value;
  },
  methods: {
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
.radius_select {
  margin-left: 10px;
  margin-right: 10px;
}

@media (min-width: 280px) and (max-width: 305px) {
  .radius_select {
    margin-left: 0 !important;
    width: 60%;
  }
}

@media (min-width: 305px) and (max-width: 342px) {
  .radius_select {
    margin-left: 0 !important;
    width: 60%;
  }
}

@media (min-width: 342px) and (max-width: 383px) {
  .radius_select {
    margin-left: 0 !important;
    width: 70%;
  }
}

@media (min-width: 383px) {
  .radius_select {
    margin-left: 0 !important;
    max-width: 77.5%;
  }
}

@media (min-width: 410px) {
  .radius_select {
    margin-left: 0 !important;
    max-width: 90%;
  }
}

@media (min-width: 535px) {
  .radius_select {
    max-width: 20%;
    min-width: none;
    margin-left: 10px !important;
  }
}

@media (min-width: 613px) {
  .radius_select {
    width: 200px;
  }
}
</style>
