<template>
  <v-select
    class="areaSelect"
    :items="items"
    v-model="selection"
    label=""
    item-text="title"
    item-value="value"
    :dark="dark"
    :attach="attachTo"
    @change="onInputChange"
  >
    <template v-slot:item="{ item }">
      <img class="areaImage" :src="item.img" />
      <v-spacer />
      <span>{{ item.title }}</span>
    </template>
    <template v-slot:selection="{ item }">
      <img class="areaImageSelected" :src="item.img" />
    </template>
  </v-select>
</template>

<script lang="ts">
import Vue from "vue";

interface Item {
  title: string;
  value: string;
  img: string;
}

/**
 * Emits @Input for v-model value
 */
export default Vue.extend({
  name: "AreaSelect",
  props: {
    value: {
      type: String,
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
          title: "Deutschland",
          value: "germany",
          img: require("@/assets/images/240px-Flag_of_Germany.png"),
        },
        {
          title: "International",
          value: "international",
          img: require("@/assets/images/240px-Earth_icon_2.png"),
        },
      ] as Item[],
      selection: "" as Item["value"],
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
  methods: {
    setSelection(): void {
      // find object to value
      const itemToValue = this.items.find((item) => item.value == this.value);
      // if object found
      if (itemToValue?.title) {
        // set selected object
        this.selection = itemToValue.title;
      }
      // else set default object and emit change
      else {
        this.selection = this.items[0].title;
        this.onChange();
      }
    },
    onInputChange() {
      this.$emit("input", this.selection);
    },
  },
});
</script>

<style lang="scss" scoped>
.areaSelect {
  margin-top: 4px;
  max-width: fit-content;
  margin-right: 8px;
  margin-left: 0;
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

.areaSelect .v-select__selections input {
  display: none;
  visibility: hidden;
}
</style>
