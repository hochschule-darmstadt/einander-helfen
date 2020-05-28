<template>
  <div>
    <Header />
    <div class="imprint">
      <v-row justify="center">
        <v-col cols="12" md="10">
          <h1>Impressum (legal notice, in German)</h1>

          <h2>Angaben gemäß § 5 TMG</h2>
          Roland Humm <br />
          Pragelatostr. 113 <br />
          D-64372  <br />
          Ober Ramstadt <br />

          <h2>Kontakt</h2>
          <p>
            Email:
            <a href="mailto:info@einander-helfen.org"
              >info@einander-helfen.org</a
            >
          </p>

          <h3>Haftung für Inhalte</h3>
          <p>
            Als Diensteanbieter sind wir gemäß § 7 Abs.1 TMG für eigene Inhalte
            auf diesen Seiten nach den allgemeinen Gesetzen verantwortlich. Nach
            §§ 8 bis 10 TMG sind wir als Diensteanbieter jedoch nicht
            verpflichtet, übermittelte oder gespeicherte fremde Informationen zu
            überwachen oder nach Umständen zu forschen, die auf eine
            rechtswidrige Tätigkeit hinweisen.
          </p>
          <p>
            Verpflichtungen zur Entfernung oder Sperrung der Nutzung von
            Informationen nach den allgemeinen Gesetzen bleiben hiervon
            unberührt. Eine diesbezügliche Haftung ist jedoch erst ab dem
            Zeitpunkt der Kenntnis einer konkreten Rechtsverletzung möglich. Bei
            Bekanntwerden von entsprechenden Rechtsverletzungen werden wir diese
            Inhalte umgehend entfernen.
          </p>

          <h3>Haftung für Links</h3>
          <p>
            Unser Angebot enthält Links zu externen Websites Dritter, auf deren
            Inhalte wir keinen Einfluss haben. Deshalb können wir für diese
            fremden Inhalte auch keine Gewähr übernehmen. Für die Inhalte der
            verlinkten Seiten ist stets der jeweilige Anbieter oder Betreiber
            der Seiten verantwortlich. Die verlinkten Seiten wurden zum
            Zeitpunkt der Verlinkung auf mögliche Rechtsverstöße überprüft.
            Rechtswidrige Inhalte waren zum Zeitpunkt der Verlinkung nicht
            erkennbar.
          </p>
          <p>
            Eine permanente inhaltliche Kontrolle der verlinkten Seiten ist
            jedoch ohne konkrete Anhaltspunkte einer Rechtsverletzung nicht
            zumutbar. Bei Bekanntwerden von Rechtsverletzungen werden wir
            derartige Links umgehend entfernen.
          </p>

          <h3>Urheberrecht</h3>
          <p>
            Die durch die Seitenbetreiber erstellten Inhalte und Werke auf
            diesen Seiten unterliegen dem deutschen Urheberrecht. Die Vervielfä
            ltigung, Bearbeitung, Verbreitung und jede Art der Verwertung
            außerhalb der Grenzen des Urheberrechtes bedürfen der schriftlichen
            Zustimmung des jeweiligen Autors bzw. Erstellers. Downloads und
            Kopien dieser Seite sind nur für den privaten, nicht kommerziellen
            Gebrauch gestattet.
          </p>
          <p>
            Soweit die Inhalte auf dieser Seite nicht vom Betreiber erstellt
            wurden, werden die Urheberrechte Dritter beachtet. Insbesondere
            werden Inhalte Dritter als solche gekennzeichnet. Sollten Sie
            trotzdem auf eine Urheberrechtsverletzung aufmerksam werden, bitten
            wir um einen entsprechenden Hinweis. Bei Bekanntwerden von
            Rechtsverletzungen werden wir derartige Inhalte umgehend entfernen.
          </p>
          <p>
            Quelle:
            <a href="https://www.e-recht24.de/impressum-generator.html"
              >https://www.e-recht24.de/impressum-generator.html
            </a>
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
export default class Imprint extends Vue {}
</script>
