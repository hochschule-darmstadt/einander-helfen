<template>
    <v-app-bar flat color="#00254f">
        <v-layout justify-space-between no-gutters color="#00254f">
                <v-container>
                    <v-row>
                        <v-col>
                            <v-layout>
                                <v-toolbar-side-icon>
                                <v-img class="mt-1" width=80px height=75px src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Heart-hand-shake.svg/256px-Heart-hand-shake.svg.png"></v-img>
                                </v-toolbar-side-icon>
                                <div class="pl-5 mt-5 headline font-weight-light white--text">einander-helfen.org/div>
                            </v-layout>
                        </v-col>
                        <v-col>
                            <div class="font-weight-bold d-none d-sm-flex pl-5 mt-5 title font-weight-light white--text">
                                Das schnelle Suchportal für Freiwilligenarbeit
                            </div>
                        </v-col>
                        <v-col>
                            <div align="right">
                                <v-menu>
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-btn
                                        v-bind="attrs"
                                        v-on="on"
                                        dark
                                        style="margin-top: 1vh"
                                        icon
                                        >
                                        <v-icon>more_vert</v-icon>
                                        </v-btn>
                                    </template>
                                    <v-list>
                                        <v-list-item
                                        v-for="(link, index) in links"
                                        :key="index"
                                        router
                                        :to="link.route"
                                        >
                                        <v-list-item-title>{{ link.text }}</v-list-item-title>
                                        </v-list-item>
                                    </v-list>
                                </v-menu>
                            </div>
                        </v-col>
                    </v-row>
                </v-container>

        </v-layout>
    </v-app-bar>
</template>

<script>
export default {
  data: () => ({
    links: [
      { text: 'Home', route: '/'},
      { text: 'Über uns', route: '/about' },
      { text: 'Impressum', route: '/imprint' },
      { text: 'Datenschutzerklärung', route: '/privacy' }
    ]
  })
};
</script>
