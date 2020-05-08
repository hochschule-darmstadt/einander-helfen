<template>
  <v-footer color="grey lighten-4" padless absolute>
    <v-row justify="center" no-gutters>
      <v-btn
        v-for="(link, index) in links"
        :key="index"
        color="grey"
        text
        rounded
        class="my-2"
        router
        :to="link.route"
      >{{ link.text }}</v-btn>
    </v-row>
  </v-footer>
</template>

<script>
export default {
  data: () => ({
    links: [
      { text: 'Über', route: '/about' },
      { text: 'Impressum', route: '/imprint' },
      { text: 'Datenschutzerklärung', route: '/privacy' }
    ]
  })
};
</script>
