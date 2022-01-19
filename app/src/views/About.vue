<!-- The page 'Über uns'. It describes einander-helfen.org and how it works.-->

<template>
  <div class="about">
    <Header />
    <section class="container pt-6">
      <div>
        <h1>{{ $t("home.title") }}</h1>
        <p>
          <strong>{{ $t("home.title") }}</strong> {{ $t("about.description1") }}
        </p>
      </div>
      <div>
        <h2>{{ $t("about.howItWorksHeadline") }}</h2>
        <p>{{ $t("about.howItWorksDescription1") }}</p>
        <p>{{ $t("about.howItWorksDescription2") }}</p>
        <p>
          <strong>{{ $t("home.title") }}</strong>
          {{ $t("about.providerDescription1") }}
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
            <a href="https://www.betterplace.org" target="_blank" rel="noopener"
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
          <li>
            <a
              href="https://www.sozialeinsatz.de"
              target="_blank"
              rel="noopener"
              >www.sozialeinsatz.de</a
            >
          </li>
        </ul>
        <p>
          <br />
          {{ $t("about.moreProvidersFollow") }} <br />
          {{ $t("about.suggestionsForImprovement") }}
          <a href="mailto:info@einander-helfen.org">
            info@einander-helfen.org </a
          >.
        </p>
      </div>
      <div>
        <h2>{{ $t("about.whoWeAre") }}</h2>
        <p>
          {{ $t("about.whoWeAreDescription1") }}
          <a
            href="https://github.com/hochschule-darmstadt/einander-helfen"
            target="_blank"
          >
            https://github.com/hochschule-darmstadt/einander-helfen
          </a>
          {{ $t("about.whoWeAreDescription2") }}
          <a href="mailto:info@einander-helfen.org">
            info@einander-helfen.org
          </a>
        </p>
      </div>
    </section>
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
  metaInfo: {
    title: "Über uns - Einander Helfen",
    link: [{ rel: "canonical", href: "https://einander-helfen.org/about" }],
  },
});
</script>

<style lang="scss" scoped></style>
