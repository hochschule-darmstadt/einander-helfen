<template>
  <div>
    <Header />
    <div class="about">
      <v-container justify="center" class="containerWithContent">
        <div>
          <h1>einander-helfen.org</h1>
          <p>
            <strong>einander-helfen.org</strong> ist das schnelle Suchportal für
            Freiwilligenarbeit und ehrenamtliche Tätigkeiten: Mit einer Fülle
            von unterschiedlichen Angeboten auf der ganzen Welt.
          </p>
        </div>
        <div>
          <h2>Und so funktioniert's:</h2>
          <p>
            Sie suchen ein Stellenangebot für Freiwilligenarbeit oder Ehrenamt
            innerhalb Deutschlands? Dann tragen Sie ein Stichwort im Suchen-Feld
            ein und geben die Postleitzahl oder den Ortsnamen des eigenen
            Standorts an. Vergessen Sie dabei nicht den Umkreis einzuschränken!
            Sofort werden alle Angebote in der Karte und in der Liste angezeigt.
            Ein Angebot auswählen (in der Liste oder auf der Karte) und schon
            werden die dazugehörigen Details angezeigt. Mit einem weiteren Klick
            ist man auf der Seite des Anbieters - mit weiteren Informationen.
            Sie können die Suche auch durch mehrere Stichworte einschränken.
          </p>
          <p>
            Sie suchen ein Stellenangebot für internationalen
            Freiwilligendienst? Dann klicken Sie auf die Deutschlandflagge und
            wählen stattdessen "International" aus. Geben Sie nun Ihr
            gewünschtes Land an und tragen ein Stichwort im Suchen-Feld ein.
            Sofort werden alle Angebote in der Karte und in der Liste angezeigt.
            Ein Angebot auswählen (in der Liste oder auf der Karte) und schon
            werden die dazugehörigen Details angezeigt. Mit einem weiteren Klick
            ist man auf der Seite des Anbieters - mit weiteren Informationen.
            Sie können die Suche auch durch mehrere Stichworte einschränken.
          </p>
          <p>
            <strong>einander-helfen.org</strong> fasst Angebote von mehreren
            Anbietern auf der ganzen Welt zusammen und erlaubt es, bequem über
            alle zu suchen. Aktuell werden folgende Anbieter abgedeckt:
          </p>
          <ul>
            <li>
              <a
                href="https://www.ehrenamtssuche-hessen.de/"
                target="_blank"
                rel="noopener"
                >www.ehrenamtssuche-hessen.de</a
              >
            </li>
            <li>
              <a href="https://www.gute-tat.de/" target="_blank" rel="noopener"
                >www.gute-tat.de</a
              >
            </li>
            <li>
              <a href="https://www.weltwaerts.de" target="_blank" rel="noopener"
                >www.weltwaerts.de</a
              >
            </li>
            <li>
              <a
                href="https://ein-jahr-freiwillig.de"
                target="_blank"
                rel="noopener"
                >www.ein-jahr-freiwillig.de</a
              >
            </li>
            <li>
              <a
                href="https://www.bundesfreiwilligendienst.de"
                target="_blank"
                rel="noopener"
              >
                www.bundesfreiwilligendienst.de
              </a>
            </li>
            <li>
              <a
                href="https://www.europa.eu/youth/home_de"
                target="_blank"
                rel="noopener"
              >
                www.europa.eu/youth
              </a>
            </li>
            <li>
              <a
                href="https://www.betterplace.org"
                target="_blank"
                rel="noopener"
                >www.betterplace.org</a
              >
            </li>
            <li>
              <a
                href="https://www.ehrenamt.sachsen.de"
                target="_blank"
                rel="noopener"
                >www.ehrenamt.sachsen.de</a
              >
            </li>
            <li>
              <a href="https://www.dksb.de" target="_blank" rel="noopener"
                >www.dksb.de</a
              >
            </li>
          </ul>
          <p>
            <br />
            Weitere Anbieter folgen. <br />
            Haben Sie Verbesserungsvorschläge oder fehlt Ihnen etwas? Dann
            kontaktieren Sie uns gerne unter
            <a href="mailto:info@einander-helfen.org">
              info@einander-helfen.org </a
            >.
          </p>
        </div>
        <div>
          <h2>Wer wir sind:</h2>
          <p>
            Wir sind ein ehrenamtliches Team und haben die Seite mit viel
            Initiative und Eigenarbeit entwickelt. Die Software ist Open Source
            <a
              href="https://github.com/hochschule-darmstadt/einander-helfen"
              target="_blank"
            >
              https://github.com/hochschule-darmstadt/einander-helfen
            </a>
            und wurde initial von einem Team von Studierenden programmiert. Wir
            freuen uns auf Anregungen und Verbesserungsvorschläge unter
            <a href="mailto:info@einander-helfen.org">
              info@einander-helfen.org
            </a>
          </p>
        </div>
      </v-container>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import Header from "@/components/layout/SearchHeader.vue";

export default Vue.extend({
  name: "About",
  components: {
    Header,
  },
});
</script>

<style>
@import "./../styles/ContainerWithContent.css";
</style>
