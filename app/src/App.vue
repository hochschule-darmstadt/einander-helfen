<template>
  <v-app>
    <div id="app">
      <Navigation></Navigation>
      <div id="content">
        <div id="content2">
          <router-view/>
        </div>
      </div>
    </div>
  </v-app>
</template>

<script lang="ts">
import { Vue } from 'vue-property-decorator';
import Component from 'vue-class-component';
import Navigation from '@/components/layout/Navigation.vue';

@Component({
  components: {
    Navigation
  }
})
export default class Counter extends Vue {
}
</script>

<style scoped lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;

  #content {
    padding: 0 40px;
    min-height: 100vh;
    margin-left: 260px;
    background-color: #F8F8F8;

    #content2 {
      padding: 30px 0 0 0;
    }
  }
}
</style>
