<!-- eslint-disable prettier/prettier -->
<!-- The page 'Impressum'. It contains contact details, sources and information about liability -->

<template>
  <div class="imprint">
    <Header />
    <section class="container pt-6">
      <h1>{{ $t("imprint.imprintHeadline") }}</h1>

      <h2>{{ $t("imprint.informationAccordingTo") }}</h2>
      Roland Humm <br />
      Pragelatostr. 113 <br />
      D-64372 <br />
      Ober Ramstadt <br />

      <h2>{{ $t("imprint.contact") }}</h2>
      <p>
        Email:
        <a href="mailto:info@einander-helfen.org">info@einander-helfen.org</a>
      </p>

      <h3>{{ $t("imprint.liabilityForContentsHeadline") }}</h3>
      <p>
        {{ $t("imprint.liabilityForContentsDescription1") }}
      </p>
      <p>
        {{ $t("imprint.liabilityForContentsDescription2") }}
      </p>

      <h3>{{ $t("imprint.liabilityForLinksHeadline") }}</h3>
      <p>
        {{ $t("imprint.liabilityForLinksDescription1") }}
      </p>
      <p>
        {{ $t("imprint.liabilityForLinksDescription2") }}
      </p>

      <h3>{{ $t("imprint.copyrightHeadline") }}</h3>
      <p>
        {{ $t("imprint.copyrightHeadlineDescription1") }}
      </p>
      <p>
        {{ $t("imprint.copyrightHeadlineDescription2") }}
      </p>
      <p>
        {{ $t("imprint.source") }}
        <a href="https://www.e-recht24.de/impressum-generator.html"
          >https://www.e-recht24.de/impressum-generator.html
        </a>
      </p>

      <h1>{{ $t("imprint.sourceReference") }}</h1>
      <ul class="mt-2 mb-5">
        <li v-for="(item, index) in items" :key="index" class="mb-2">
          -
          <!--use i18n translation if exists
          
            <strong v-if='$te("imprint.sourceReferenceItems."+item.i18nKey+".author")'>{{ $t("imprint.sourceReferenceItems."+item.i18nKey+".author") }}</strong>
          <strong v-else>{{ item.author }}</strong>
          -->
           <strong>{{ item.author }}</strong>
           - <!--use i18n translation if exists
          <i v-if='$te("imprint.sourceReferenceItems."+item.i18nKey+".position")'>{{ $t("imprint.sourceReferenceItems."+item.i18nKey+".position") }}</i> 
          <i v-else>{{ item.position }}</i> -->
          <i>{{ item.position }}</i> - 
          <br />
          <!--use i18n translation if exists
          <p class="wordbreak" v-if='$te("imprint.sourceReferenceItems."+item.i18nKey+".license")'>{{ $t("imprint.sourceReferenceItems."+item.i18nKey+".license") }}</p>
          <p class="wordbreak" v-else>{{ item.license }}</p>
          -->
          <p class="wordbreak">{{ item.license }}</p>
        </li>
      </ul>
    </section>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import Header from "@/components/layout/SearchHeader.vue";

export default Vue.extend({
  components: { Header },
  watch: {
    title: {
      immediate: true,
      handler() {
        document.title = "Impressum - Einander Helfen";
      },
    },
  },
  data(): {
    items: any;
  } {
    return {
      items: [
        {
          //i18nKey:"iitBombay",
          position: this.$t("imprint.sourceReferenceItems.iitBombay.position"),
          author: "IIT Bombay",
          source:
            "https://commons.wikimedia.org/wiki/File:Heart-hand-shake.svg",
          license: this.$t("imprint.sourceReferenceItems.iitBombay.license"),
          //"The copyright holder of this file, IIT Bombay, allows anyone to use it for any purpose, provided that the copyright holder is properly attributed. Redistribution, derivative work, commercial use, and all other use is permitted.",
        },
        {
          //i18nKey:"sKopp",
          position: this.$t("imprint.sourceReferenceItems.sKopp.position"),
          author: this.$t("imprint.sourceReferenceItems.sKopp.author"),
          source: "https://commons.wikimedia.org/wiki/File:Flag_of_Germany.svg",
          license: this.$t("imprint.sourceReferenceItems.sKopp.license"),
          //"This image of simple geometry is ineligible for copyright and therefore in the public domain, because it consists entirely of information that is common property and contains no original authorship.",
        },
        {
          //i18nKey:"tommasoSansone",
          position: this.$t(
            "imprint.sourceReferenceItems.tommasoSansone.position"
          ),
          author: "Tommaso.sansone91",
          source: "https://commons.wikimedia.org/wiki/File:Earth_icon_2.png",
          license: this.$t(
            "imprint.sourceReferenceItems.tommasoSansone.license"
          ),
          //"This file is made available under the Creative Commons CC0 1.0 Universal Public Domain Dedication. The person who associated a work with this deed has dedicated the work to the public domain by waiving all of their rights to the work worldwide under copyright law, including all related and neighboring rights, to the extent allowed by law. You can copy, modify, distribute and perform the work, even for commercial purposes, all without asking permission.",
        },
        {
          //i18nKey:"truthseeker",
          position: this.$t(
            "imprint.sourceReferenceItems.truthseeker.position"
          ),
          author: "truthseeker08",
          source:
            "https://pixabay.com/de/photos/hospiz-pflege-krankenpflege-1797305/",
          license: "https://pixabay.com/de/service/terms/#license",
        },
        {
          //i18nKey:"timkraaijvanger",
          position: this.$t(
            "imprint.sourceReferenceItems.timkraaijvanger.position"
          ),
          author: "timkraaijvanger",
          source:
            "https://pixabay.com/de/photos/kind-kleinkind-süß-blondine-blume-3089906/",
          license: "https://pixabay.com/de/service/terms/#license",
        },
        {
          //i18nKey:"anemone",
          position: this.$t("imprint.sourceReferenceItems.anemone.position"),
          author: "Anemone123",
          source:
            "https://pixabay.com/de/photos/teamgeist-zusammenhalt-gemeinsam-2447163/",
          license: "https://pixabay.com/de/service/terms/#license",
        },
        {
          //i18nKey:"cottonbro",
          position: this.$t("imprint.sourceReferenceItems.cottonbro.position"),
          author: "cottonbro",
          source:
            "https://www.pexels.com/de-de/foto/lebensmittel-hande-liebe-menschen-3992383/",
          license: "https://www.pexels.com/de-de/lizenz/",
        },
        {
          //i18nKey:"andreaPiacquadio",
          position: this.$t(
            "imprint.sourceReferenceItems.andreaPiacquadio.position"
          ),
          author: "Andrea Piacquadio",
          source:
            "https://www.pexels.com/de-de/foto/mann-menschen-frau-schreibtisch-3769981/",
          license: "https://www.pexels.com/de-de/lizenz/",
        },
        {
          //i18nKey:"fauxels",
          position: this.$t("imprint.sourceReferenceItems.fauxels.position"),
          author: "fauxels",
          source:
            "https://www.pexels.com/de-de/foto/mann-menschen-frau-schreibtisch-3184357/",
          license: "https://www.pexels.com/de-de/lizenz/",
        },
        {
          //i18nKey:"andreaPiacquadio2",
          position: this.$t(
            "imprint.sourceReferenceItems.andreaPiacquadio2.position"
          ),
          author: "Andrea Piacquadio",
          source:
            "https://www.pexels.com/de-de/foto/lebensmittel-mann-menschen-frau-3772534/",
          license: "https://www.pexels.com/de-de/lizenz/",
        },
        {
          //i18nKey:"freepik",
          position: this.$t("imprint.sourceReferenceItems.freepik.position"),
          author: "https://www.freepik.com",
          source: "https://www.flaticon.com/free-icon/robot_3398613",
          license: "https://www.freepikcompany.com/legal",
        },
        {
          //i18nKey:"dbenbenn",
          position: this.$t("imprint.sourceReferenceItems.dbenbenn.position"),
          author: "Dbenbenn, Zscout370, Jacobolus, Indolences, Technion.",
          source:
            "https://commons.wikimedia.org/wiki/File:Flag_of_the_United_States.svg",
          license: this.$t("imprint.sourceReferenceItems.dbenbenn.license"),
          //"This image is ineligible for copyright and therefore is in the public domain, because it consists entirely of information that is common property and contains no original authorship.",
        },
      ],
    };
  },
});
</script>

<style lang="scss" scoped></style>
