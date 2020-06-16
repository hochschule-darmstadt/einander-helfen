<template>
    <v-app-bar flat absolute height="95vh" color="#00254f">
        <v-layout justify-space-between>

                <v-layout >
                    <v-toolbar-side-icon>
                    <v-img class="mt-1 ml-2" width=80px height=75px src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Heart-hand-shake.svg/256px-Heart-hand-shake.svg.png"></v-img>
                    </v-toolbar-side-icon> 
                    <div class="pl-5 mt-5 headline font-weight-light white--text">einander-helfen.de</div>
                    <v-spacer></v-spacer>
                    <div class="font-weight-bold d-none d-sm-flex pl-5 mt-5 title font-weight-light white--text">
                        das schnelle Suchportal für Freiwilligenarbeit
                    </div>
                    <v-spacer></v-spacer>
                    <v-menu offset-y>
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
                </v-layout>

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