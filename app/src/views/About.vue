<template>
  <div>
    <Header />
    <div class="about">
      <v-container justify="center" class="containerWithContent">
        <div>
          <h1>einander-helfen.org</h1>
          <p>
            <strong>einander-helfen.org</strong> ist das schnelle Suchportal für Freiwilligenarbeit und ehrenamtliche Tätigkeiten: Mit einer Fülle von unterschiedlichen Angeboten auf der ganzen Welt.
          </p>
        </div>
        <div>
          <h2>Und so funktioniert's:</h2>
          <p>Sie suchen ein Ehrenamtangebot innerhalb Deutschlands? Dann tragen Sie ein Stichwort im Suchen-Feld ein und geben die Postleitzahl oder den Ortsnamen des eigenen Standorts an. Vergessen Sie dabei nicht den Umkreis einzuschränken! Sofort werden alle Angebote in der Karte und in der Liste angezeigt. Ein Angebot auswählen (in der Liste oder auf der Karte) und schon werden die dazughörigen Details angezeigt. Mit einem weiteren Klick ist man auf der Seite des Anbieters - mit weiteren Informationen.</p>
          <p>Sie suchen ein Ehrenamtangebot im internationalen Raum? Dann klicken Sie auf die Deutschlandflagge und wählen stattdessen "International" aus. Geben Sie nun Ihr gewünschtes Land an und tragen ein Stichwort im Suchen-Feld ein. Sofort werden alle Angebote in der Karte und in der Liste angezeigt. Ein Angebot auswählen (in der Liste oder auf der Karte) und schon werden die dazughörigen Details angezeigt. Mit einem weiteren Klick ist man auf der Seite des Anbieters - mit weiteren Informationen.</p>
          <p>
            <strong>einander-helfen.org</strong> fasst Angebote von mehreren Anbietern auf der ganzen Welt zusammen und erlaubt es, bequem über alle zu suchen. Aktuell werden folgende Anbieter abgedeckt:
          </p>
          <ul>
            <li><a href="https://www.ehrenamtssuche-hessen.de/" target="_blank" rel="noopener">www.ehrenamtssuche-hessen.de</a></li>
            <li><a href="https://www.gute-tat.de/" target="_blank" rel="noopener">www.gute-tat.de</a></li>
            <li><a href="https://www.weltwaerts.de" target="_blank" rel="noopener">www.weltwaerts.de</a></li>
            <li><a href="https://ein-jahr-freiwillig.de" target="_blank" rel="noopener">www.ein-jahr-freiwillig.de</a></li>
            <li><a href="https://www.bundesfreiwilligendienst.de" target="_blank" rel="noopener">www.bundesfreiwilligendienst.de</a></li>
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
              href="https://github.com/hochschule-darmstadt/einander-helfen" target="_blank"
            >https://github.com/hochschule-darmstadt/einander-helfen</a> und wurde initial von einem Team von Studierenden programmiert. Wir freuen uns auf Anregungen und Verbesserungsvorschläge unter
            <a
              href="mailto:info@einander-helfen.org"
            >info@einander-helfen.org</a>
          </p>
        </div>
      </v-container>
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

<style>
  @import './../styles/ContainerWithContent.css';
</style>