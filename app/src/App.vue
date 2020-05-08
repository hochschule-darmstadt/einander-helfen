<template>
  <v-app>
    <Navigation />
    <v-content>
      <router-view></router-view>
    </v-content>
    <Footer />
  </v-app>
</template>

<script lang="ts">
import { Vue } from 'vue-property-decorator';
import Component from 'vue-class-component';
import Navigation from '@/components/layout/Navigation.vue';
import Footer from '@/components/layout/Footer.vue';

@Component({
  components: {
    Footer,
    Navigation
  }
})
export default class Counter extends Vue {}
</script>


