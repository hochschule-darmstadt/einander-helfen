<template>
  <v-select
    class="languageSelection"
    :items="langs"
    v-model="$i18n.locale"
    v-bind:label="this.$t('languageSelection.languageChoice')"
    :dark="dark"
    :attach="attachTo"
    @change="onChange"
    @keydown.enter="onEnter"
  >
    <template v-slot:item="{ item }">
      <img class="languageImage" :src="item.img" />
      <v-spacer />
      <span>{{ item.text }}</span>
    </template>
    <template v-slot:selection="{ item }">
      <img class="languageImageSelected" :src="item.img" />
    </template>
  </v-select>
</template>

<script lang="ts">
import Vue from "vue";

interface Language {
  text: string;
  value: string;
  img: string;
}

export default Vue.extend({
  name: 'LanguageSelection',
  data: function () {
    return {
      langs: [
        {
          text: this.$t("languageSelection.german"),
          value: "de",
          img: require("@/assets/images/area/240px-Flag_of_Germany.png"),
        },
        {
          text: this.$t("languageSelection.english"),
          value: "en",
          img: require("@/assets/images/language/320px-Flag_of_the_United_States.svg.png"),
        },
      ] as Language[]
    };
  }
});
</script>

<style lang="scss" scoped>
.languageSelection {
  max-width: fit-content;
  margin-top: 8px;
  display: flex;
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;

  ::v-deep .v-select__selections input {
    display: none;
    visibility: hidden;
  }
}

.languageImage,
.languageImageSelected {
  height: 1.5em;
  width: 1.5em;
  object-fit: cover;
  border-radius: 50%;
}

.languageImage {
  margin-right: 1em;
}

::v-deep .v-menu__content {
  display: inline-table;
}
</style>

