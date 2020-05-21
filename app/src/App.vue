<template>
  <v-app>
    <Header/>
    <div id="app">
      <Navigation></Navigation>
      <router-view/>
    </div>
    <Footer />
  </v-app>
</template>

<script lang="ts">
import { Vue } from 'vue-property-decorator';
import Component from 'vue-class-component';
import Header from '@/components/layout/Header.vue';
import Navigation from '@/components/layout/Navigation.vue';

@Component({
  components: {
    /*Navigation,*/
    Header,
  }
})
export default class Counter extends Vue {
}
</script>
/*
<style scoped lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;

  #content {
    padding: 0 40px;
    min-height: 78vh;
 /* margin-left: 260px;*/
    background-color: #F8F8F8;

    #content2 {
      padding: 30px 0 0 0;
    }
  }
}
</style>
