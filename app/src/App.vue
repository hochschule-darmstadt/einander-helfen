<template>
  <v-app>
    <Header/>
    <v-content >
      <router-view></router-view>
    </v-content>
    <Footer />
  </v-app>
</template>

<script lang="ts">
import { Vue } from 'vue-property-decorator';
import Toolbar from '@/components/layout/Toolbar.vue';
import Footer from '@/components/layout/Footer.vue';

export default Vue.extend({
  components: {
    Footer,
    Toolbar
  }
});
</script>


