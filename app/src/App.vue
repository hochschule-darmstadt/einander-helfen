<template>
  <v-app>
    <Toolbar />
    <v-content >
      <router-view></router-view>
    </v-content>
    <Footer />
  </v-app>
</template>

<script lang="ts">
import { Vue } from 'vue-property-decorator';
import Component from 'vue-class-component';
import Toolbar from '@/components/layout/Toolbar.vue';
import Footer from '@/components/layout/Footer.vue';

@Component({
  components: {
    Footer,
    Toolbar
  }
})
export default class Counter extends Vue {}
</script>


