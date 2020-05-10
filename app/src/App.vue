<template>
  <v-app>
    <v-content >
      <router-view></router-view>
    </v-content>
    <Footer />
  </v-app>
</template>

<script lang="ts">
import { Vue } from 'vue-property-decorator';
import Component from 'vue-class-component';
import Footer from '@/components/layout/Footer.vue';

@Component({
  components: {
    Footer
  }
})
export default class Counter extends Vue {}
</script>


