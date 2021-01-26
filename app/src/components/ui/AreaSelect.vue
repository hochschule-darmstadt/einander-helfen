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
      @change="$emit('change')">
      <template v-slot:item="{ item }">
        <img id="areaImage" :src="item.img">
        <v-space></v-space>
        <span>{{item.title}}</span>
      </template>
      <template v-slot:selection="{ item }">
        <img id="areaImageSelected" :src="item.img">
      </template>
    </v-select>
  </v-row>
</template>

<script lang="ts">
  import { createNamespacedHelpers } from 'vuex';

  const { mapState, mapActions, mapGetters } = createNamespacedHelpers('locationSearchModule');
  import Vue from 'vue';
  import Component from 'vue-class-component';
import { Prop } from 'vue-property-decorator';

  type Item = {
    title: string;
    img: string;
  };

  @Component
  export default class AreaSelect extends Vue {
    @Prop({default: false})
    public dark!: boolean;

    @Prop({default: ''})
    public attachTo!: string;

    public items: Item[] = [
      {
        title: 'Deutschland',
        img: 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Flag_of_Germany.svg/320px-Flag_of_Germany.svg.png'
      },
      {
        title: 'International',
        img: 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Earth_icon_2.png/240px-Earth_icon_2.png'
      }
    ];

    public selection: string = 'Deutschland';
  }
</script>

<style>
#areaImage, #areaImageSelected {
  height: 1.5em;
  width: 1.5em;
  object-fit: cover;
  border-radius: 50%;
}

#areaImage {
  margin-right: 1em;
}
</style>





