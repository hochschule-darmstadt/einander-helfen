<template>
  <v-row justify="center">
    <v-select
      id="areaSelect"
      :items="items"
      v-model="selection"
      label=""
      item-text="title"
      item-value="title"
      :dark="dark"
      @change="$emit('change')"
    >
      <template v-slot:item="{ item }">
        <img id="areaImage" :src="item.img" />
        <v-spacer></v-spacer>
        <span>{{ item.title }}</span>
      </template>
      <template v-slot:selection="{ item }">
        <img id="areaImageSelected" :src="item.img" />
      </template>
    </v-select>
  </v-row>
</template>

<script lang="ts">
import Vue from "vue";

interface Item {
  title: string;
  img: string;
}

export default Vue.extend({
  name: "AreaSelect",
  props: {
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
          img: "/images/240px-Flag_of_Germany.png",
        },
        {
          title: "International",
          img: "/images/240px-Earth_icon_2.png",
        },
      ] as Item[],
      selection: "",
    };
  },
  mounted(): void {
    this.selection = this.items[0].title;
    this.setSelection(this.international);
  },
  computed: {
    getInternational(): any {
      return this.$store.getters.getInternational;
    },
    international(): boolean {
      return this.getInternational;
    },
  },
  watch: {
    selection(newValue: string): void {
      if (newValue === this.items[0].title) {
        this.setInternational(false);
      } else {
        this.setInternational(true);
      }
    },
  },
  methods: {
    setSelection(international: boolean): void {
      if (international) {
        this.selection = this.items[1].title;
      } else {
        this.selection = this.items[0].title;
      }
    },
    setInternational(obj: boolean) {
      this.$store.commit("setInternational", obj);
    },
  },
});
</script>

<style lang="scss">
#areaImage,
#areaImageSelected {
  height: 1.5em;
  width: 1.5em;
  object-fit: cover;
  border-radius: 50%;
}

#areaImage {
  margin-right: 1em;
}

#areaSelect .v-select__selections input {
  display: none;
  visibility: hidden;
}

#areaSelect {
  margin-top: 4px;
  max-width: fit-content;
  margin-right: 8px;
  margin-left: 0;
}
</style>
