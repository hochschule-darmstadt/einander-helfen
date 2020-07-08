<template>
  <div>
    <Header />
    <div class="about">
      <v-row justify="center">
        <v-col cols="12" md="10">
          <div>
            <h1>einander-helfen.org</h1>
            <p>
              <strong>einander-helfen.org</strong> ist das schnelle Suchportal für Freiwilligenarbeit und ehrenamtliche Tätigkeiten: Mit einer Fülle von unterschiedlichen Angeboten im deutschsprachigen Raum.
            </p>
          </div>
          <div>
            <h2>Und so funktioniert's :</h2>
            <p>Einfach die Postleitzahl des eigenen Standorts und Umkreis in km eingeben und dann ein Stichwort im Suchen-Feld. Sofort werden alle Angebote in der Karte (rechts) und in der Liste (links) angezeigt. Ein Angebot auswählen (in der Liste oder auf der Karte) und schon werden Details angezeigt. Mit einem weiteren Klick ist man auf der Seite des Anbieters - mit weiteren Informationen.</p>
            <p>
              <strong>einander-helfen.org</strong> fasst Angebote von mehreren Anbietern im deutschsprachigen Raum zusammen und erlaubt es, bequem über alle zu suchen. Aktuell werden folgende Anbieter abgedeckt:
            </p>
            <ul>
              <li><a href="https://www.ehrenamtssuche-hessen.de/" target="_blank" rel="noopener">www.ehrenamtssuche-hessen.de</a></li>
            </ul>
            <p>
              <br />
              Weitere Anbieter folgen. <br />
              Fehlt Ihnen etwas? Dann kontaktieren Sie uns gerne unter
              <a href="mailto:info@einander-helfen.org">info@einander-helfen.org</a>.
            </p>
          </div>
          <div>
            <h2>Wer wir sind:</h2>
            <p>
              Wir sind ein ehrenamtliches Team und haben die Seite mit viel Initiative und Eigenarbeit entwickelt. Die Software ist Open Source
              <a
                href="https://github.com/hochschule-darmstadt/einander-helfen"
              >https://github.com/hochschule-darmstadt/einander-helfen</a> und wurde initial von einem Team von Studierenden programmiert. Wir freuen uns auf Anregungen und Verbesserungsvorschläge unter
              <a
                href="mailto:info@einander-helfen.org"
              >info@einander-helfen.org</a>
            </p>
          </div>
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
