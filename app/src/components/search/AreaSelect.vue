<!-- Component to select the area of the search (national or international) -->

<template>
  <v-select
    class="areaSelect"
    :items="items"
    v-model="selection"
    label=""
    :dark="dark"
    :attach="attachTo"
    @change="onInputChange"
  >
    <template v-slot:item="{ item }">
      <img class="areaImage" :alt="item.alt" :src="item.img" />
      <v-spacer />
      <span>{{ item.text }}</span>
    </template>
    <template v-slot:selection="{ item }">
      <img class="areaImageSelected" :alt="item.alt" :src="item.img" />
    </template>
  </v-select>
</template>

<script lang="ts">
import Vue from "vue";

interface AreaItem {
  alt: string;
  text: string;
  value: string;
  img: string;
}

/**
 * Emits @Input for v-model value
 */
export default Vue.extend({
  name: "AreaSelect",
  props: {
    /**
     * value is used for v-model implementation.
     * It defines if the area is international (true) or national/germany (false)
     */
    value: {
      type: Boolean,
      required: true,
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
  data: function () {
    return {
      items: [
        {
          alt: "Flagge-Deutschland",
          text: "Deutschland",
          value: "germany",
          img: require("@/assets/images/area/240px-Flag_of_Germany.png"),
        },
        {
          alt: "Flagge-International",
          text: "International",
          value: "international",
          img: require("@/assets/images/area/240px-Earth_icon_2.png"),
        },
      ] as AreaItem[],
      selection: "",
    };
  },
  mounted(): void {
    this.setSelection();
  },
  watch: {
    /** change selection on value change */
    value(): void {
      this.setSelection();
    },
  },
  computed: {
    isInternational(): boolean {
      return this.selection == this.items[1].value;
    },
  },
  methods: {
    setSelection(): void {
      this.selection = this.value ? this.items[1].value : this.items[0].value;
      this.$emit("input", this.isInternational);
    },
    onInputChange() {
      this.$emit("input", this.isInternational);
    },
  },
});
</script>

<style lang="scss" scoped>
.areaSelect {
  max-width: fit-content;
  margin-top: 8px;

  ::v-deep .v-select__selections input {
    display: none;
    visibility: hidden;
  }
}

.areaImage,
.areaImageSelected {
  height: 1.5em;
  width: 1.5em;
  object-fit: cover;
  border-radius: 50%;
}

.areaImage {
  margin-right: 1em;
}

::v-deep .v-menu__content {
  display: inline-table;
}
</style>
