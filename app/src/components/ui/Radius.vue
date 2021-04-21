<template>
  <v-select
    label="Umkreis"
    :items="radii"
    item-value="value"
    @input="newSelectedRadius = $event"
    v-bind:value="selectedRadius"
    @keydown.enter="$emit('enter')"
    :dark="dark"
    :disabled="disabled"
    style="margin-left: 10px; margin-right: 10px"
  />
</template>

<script lang="ts">
import Vue from "vue";
import Radius from "@/models/radius";
import { createNamespacedHelpers, mapGetters } from "vuex";
const { mapActions, mapState } = createNamespacedHelpers(
  "locationSearchModule"
);

export default Vue.extend({
  name: "Radius",
  props: {
    dark: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      newSelectedRadius: null as string | null,
      radii: [] as Radius[],
      disabled: false as boolean,
    };
  },
  watch: {
    newSelectedRadius(newValue: string | null): void {
      if (newValue !== null) {
        this.setSelectedRadius(newValue);
        this.$emit("input", newValue);
        this.newSelectedRadius = null;
      }
    },
  },
  computed: {
    ...mapState(["selectedRadius"]),
    ...mapGetters(["getInternational"]),
    getInternationalSelect(): boolean {
      return this.getInternational;
    },
  },
  mounted(): void {
    this.disableRadius(this.getInternationalSelect);
  },
  methods: {
    ...mapActions(["setSelectedRadius"]),
    disableRadius(disable: boolean): void {
      if (disable) {
        this.disabled = true;
        this.setSelectedRadius("");
      } else {
        this.disabled = false;
      }
    },
  },
});
</script>
