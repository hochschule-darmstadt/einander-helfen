<template>
  <div>
    <Header />
    <div class="mt-3">
      <div style="width: 70%; margin: auto;">
        <v-row justify="center">
          <v-col cols="12" md="10">
            <div>
              <v-card-title class="headline mb-1">einander-helfen.org</v-card-title>
              <hr />
              <v-card-subtitle>
                <h2>einander-helfen.org ist das schnelle Suchportal für Freiwilligenarbeit und ehrenamtliche Tätigkeiten: Mit einer Fülle von unterschiedlichen Angeboten im deutschsprachigen Raum.</h2>
              </v-card-subtitle>
            </div>
            <div>
              <v-card-subtitle>
                <h3>Und so funktioniert's :</h3>
              </v-card-subtitle>
              <v-card-text>Einfach die Postleitzahl des eigenen Standorts und Umkreis in km eingeben und dann ein Stichwort im Suchen-Feld. Sofort werden alle Angebote in der Karte (rechts) und in der Liste (links) angezeigt. Ein Angebot auswählen (in der Liste oder auf der Karte) und schon werden Details angezeigt. Mit einem weiteren Klick ist man auf der Seite des Anbieters - mit weiteren Informationen.</v-card-text>
              <v-card-text>einander-helfen.org fasst Angebote von mehreren Anbietern im deutschsprachigen Raum zusammen und erlaubt es, bequem über alle zu suchen. Aktuell werden folgende Anbieter abgedeckt:</v-card-text>
              <v-card-text>
                Weitere Anbieter folgen. Fehlt Ihnen etwas? Dann kontaktieren Sie uns gerne unter
                <a
                  href="mailto:info@einander-helfen.org"
                >info@einander-helfen.org</a>.
              </v-card-text>
            </div>
            <div>
              <v-card-subtitle>
                <h3>Wer wir sind:</h3>
              </v-card-subtitle>
              <v-card-text>
                Wir sind ein ehrenamtliches Team und haben die Seite mit viel Initiative und Eigenarbeit entwickelt. Die Software ist Open Source
                <a
                  href="https://github.com/hochschule-darmstadt/einander-helfen"
                >https://github.com/hochschule-darmstadt/einander-helfen</a> und wurde initial von einem Team von Studierenden programmiert.
                <br />
                <br />Wir freuen uns auf Anregungen und Verbesserungsvorschläge unter
                <a
                  href="mailto:info@einander-helfen.org"
                >info@einander-helfen.org</a>
              </v-card-text>
              <v-card-text>
                <strong>THIS WILL BE ADDED LATER</strong>
              </v-card-text>
            </div>
          </v-col>
        </v-row>
      </div>
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
