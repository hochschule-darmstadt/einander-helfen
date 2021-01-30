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
        <v-spacer></v-spacer>
        <span>{{item.title}}</span>
      </template>
      <template v-slot:selection="{ item }">
        <img id="areaImageSelected" :src="item.img">
      </template>
    </v-select>
  </v-row>
</template>

<script lang="ts">
  import { createNamespacedHelpers, mapActions as mapStateActions, mapGetters } from 'vuex';
  const { mapState, mapActions } = createNamespacedHelpers('locationSearchModule');
  import Vue from 'vue';
  import Component from 'vue-class-component';
  import { Prop, Watch } from 'vue-property-decorator';
  import { Getter, Mutation } from 'vuex-class';

  type Item = {
    title: string;
    img: string;
  };

  @Component
  export default class AreaSelect extends Vue {
    @Getter('getInternational') getInternational;
    @Mutation('setInternational') setInternational;

    @Watch('selection')
    onPropertyChanged(newValue: string): void {
      if (newValue === this.items[0].title) {
        this.setInternational(false);
      } else {
        this.setInternational(true);
      }
    }

    get international(): boolean {
      return this.getInternational;
    }

    mounted(): void {
      this.setSelection(this.international);
    }

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

    public selection: string = this.items[0].title;

    public setSelection(international: boolean): void {
      if(international) {
        this.selection = this.items[1].title;
      } else {
        this.selection = this.items[0].title;
      }
    }
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

#areaSelect .v-select__selections input {
  display: none;
  visibility: hidden;
}

#areaSelect{
  margin-top: 4px;
  max-width: fit-content;
  margin-right: 8px;
  margin-left: 0;
}

</style>





