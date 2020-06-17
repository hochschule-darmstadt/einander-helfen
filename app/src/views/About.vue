<template>
  <div>
    <Header />
    <div class="about">
      <v-row justify="center">
        <v-col cols="12" md="10">
          <p>
            Hier steht das 'Über uns'.
          </p>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Header from '@/components/layout/Header.vue';

@Component({
  components: {
      Header
  }
})
export default class About extends Vue {}
</script>