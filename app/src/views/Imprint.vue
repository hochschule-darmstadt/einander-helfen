<!-- The page 'Impressum'. It contains contact details, sources and information about liability -->

<template>
  <div>
    <Header />
    <div class="imprint">
      <v-container justify="center" class="containerWithContent">
        <h1>Impressum (legal notice, in German)</h1>

        <h2>Angaben gemäß § 5 TMG</h2>
        Roland Humm <br />
        Pragelatostr. 113 <br />
        D-64372 <br />
        Ober Ramstadt <br />

        <h2>Kontakt</h2>
        <p>
          Email:
          <a href="mailto:info@einander-helfen.org">info@einander-helfen.org</a>
        </p>

        <h3>Haftung für Inhalte</h3>
        <p>
          Als Diensteanbieter sind wir gemäß § 7 Abs.1 TMG für eigene Inhalte
          auf diesen Seiten nach den allgemeinen Gesetzen verantwortlich. Nach
          §§ 8 bis 10 TMG sind wir als Diensteanbieter jedoch nicht
          verpflichtet, übermittelte oder gespeicherte fremde Informationen zu
          überwachen oder nach Umständen zu forschen, die auf eine rechtswidrige
          Tätigkeit hinweisen.
        </p>
        <p>
          Verpflichtungen zur Entfernung oder Sperrung der Nutzung von
          Informationen nach den allgemeinen Gesetzen bleiben hiervon unberührt.
          Eine diesbezügliche Haftung ist jedoch erst ab dem Zeitpunkt der
          Kenntnis einer konkreten Rechtsverletzung möglich. Bei Bekanntwerden
          von entsprechenden Rechtsverletzungen werden wir diese Inhalte
          umgehend entfernen.
        </p>

        <h3>Haftung für Links</h3>
        <p>
          Unser Angebot enthält Links zu externen Websites Dritter, auf deren
          Inhalte wir keinen Einfluss haben. Deshalb können wir für diese
          fremden Inhalte auch keine Gewähr übernehmen. Für die Inhalte der
          verlinkten Seiten ist stets der jeweilige Anbieter oder Betreiber der
          Seiten verantwortlich. Die verlinkten Seiten wurden zum Zeitpunkt der
          Verlinkung auf mögliche Rechtsverstöße überprüft. Rechtswidrige
          Inhalte waren zum Zeitpunkt der Verlinkung nicht erkennbar.
        </p>
        <p>
          Eine permanente inhaltliche Kontrolle der verlinkten Seiten ist jedoch
          ohne konkrete Anhaltspunkte einer Rechtsverletzung nicht zumutbar. Bei
          Bekanntwerden von Rechtsverletzungen werden wir derartige Links
          umgehend entfernen.
        </p>

        <h3>Urheberrecht</h3>
        <p>
          Die durch die Seitenbetreiber erstellten Inhalte und Werke auf diesen
          Seiten unterliegen dem deutschen Urheberrecht. Die Vervielfältigung,
          Bearbeitung, Verbreitung und jede Art der Verwertung außerhalb der
          Grenzen des Urheberrechtes bedürfen der schriftlichen Zustimmung des
          jeweiligen Autors bzw. Erstellers. Downloads und Kopien dieser Seite
          sind nur für den privaten, nicht kommerziellen Gebrauch gestattet.
        </p>
        <p>
          Soweit die Inhalte auf dieser Seite nicht vom Betreiber erstellt
          wurden, werden die Urheberrechte Dritter beachtet. Insbesondere werden
          Inhalte Dritter als solche gekennzeichnet. Sollten Sie trotzdem auf
          eine Urheberrechtsverletzung aufmerksam werden, bitten wir um einen
          entsprechenden Hinweis. Bei Bekanntwerden von Rechtsverletzungen
          werden wir derartige Inhalte umgehend entfernen.
        </p>
        <p>
          Quelle:
          <a href="https://www.e-recht24.de/impressum-generator.html"
            >https://www.e-recht24.de/impressum-generator.html
          </a>
        </p>

        <h1>Quellenangabe / Bildquellen</h1>
        <ul class="mt-2 mb-5">
          <li v-for="item in items" :key="item" class="mb-2">
            <strong>{{ item.author }}</strong> - <i>{{ item.position }}</i>
            <br />
            <a class="wordbreak" :href="item.source">{{ item.source }}</a
            >,
            <p class="wordbreak">{{ item.license }}</p>
          </li>
        </ul>
      </v-container>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import Header from "@/components/layout/SearchHeader.vue";

export default Vue.extend({
  components: { Header },
  data(): {
    items: any;
  } {
    return {
      items: [
        {
          position: "Logo von einander-helfen.org",
          author: "IIT Bombay",
          source:
            "https://commons.wikimedia.org/wiki/File:Heart-hand-shake.svg",
          license:
            "The copyright holder of this file, IIT Bombay, allows anyone to use it for any purpose, provided that the copyright holder is properly attributed. Redistribution, derivative work, commercial use, and all other use is permitted.",
        },
        {
          position:
            'Im Dropdownmenü links neben "Deutschland" (Deutschlandflagge)',
          author: "SKopp, Madden und andere User",
          source: "https://commons.wikimedia.org/wiki/File:Flag_of_Germany.svg",
          license:
            "This image of simple geometry is ineligible for copyright and therefore in the public domain, because it consists entirely of information that is common property and contains no original authorship.",
        },
        {
          position: 'Im Dropdownmenü links neben "International" (Weltkugel)',
          author: "Tommaso.sansone91",
          source: "https://commons.wikimedia.org/wiki/File:Earth_icon_2.png",
          license:
            "This file is made available under the Creative Commons CC0 1.0 Universal Public Domain Dedication. The person who associated a work with this deed has dedicated the work to the public domain by waiving all of their rights to the work worldwide under copyright law, including all related and neighboring rights, to the extent allowed by law. You can copy, modify, distribute and perform the work, even for commercial purposes, all without asking permission.",
        },
        {
          position: "Auf der Startseite erstes Bild im Karussel",
          author: "truthseeker08",
          source:
            "https://pixabay.com/de/photos/hospiz-pflege-krankenpflege-1797305/",
          license: "https://pixabay.com/de/service/terms/#license",
        },
        {
          position: "Auf der Startseite zweites Bild im Karussel",
          author: "geralt",
          source:
            "https://pixabay.com/de/photos/hilfe-hand-anbieten-verzweiflung-3049553/",
          license: "https://pixabay.com/de/service/terms/#license",
        },
        {
          position: "Auf der Startseite drittes Bild im Karussel",
          author: "Anemone123",
          source:
            "https://pixabay.com/de/photos/teamgeist-zusammenhalt-gemeinsam-2447163/",
          license: "https://pixabay.com/de/service/terms/#license",
        },
        {
          position: "Auf der Startseite unten das Bild auf der ersten Kachel",
          author: "cottonbro",
          source:
            "https://www.pexels.com/de-de/foto/lebensmittel-hande-liebe-menschen-3992383/",
          license: "https://www.pexels.com/de-de/lizenz/",
        },
        {
          position: "Auf der Startseite unten das Bild auf der zweiten Kachel",
          author: "Andrea Piacquadio",
          source:
            "https://www.pexels.com/de-de/foto/mann-menschen-frau-schreibtisch-3769981/",
          license: "https://www.pexels.com/de-de/lizenz/",
        },
        {
          position: "Auf der Startseite unten das Bild auf der vierten Kachel",
          author: "fauxels",
          source:
            "https://www.pexels.com/de-de/foto/mann-menschen-frau-schreibtisch-3184357/",
          license: "https://www.pexels.com/de-de/lizenz/",
        },
        {
          position: "Auf der Startseite unten das Bild auf der dritten Kachel",
          author: "Andrea Piacquadio",
          source:
            "https://www.pexels.com/de-de/foto/lebensmittel-mann-menschen-frau-3772534/",
          license: "https://www.pexels.com/de-de/lizenz/",
        },
      ],
    };
  },
});
</script>

<style>
@import "./../styles/ContainerWithContent.css";
</style>
