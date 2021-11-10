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
          <strong>{{ item.author }}</strong> - <!--use i18n translation if exists-->
                                               <i v-if='$t("imprint.sourceReferenceItems."+item.i18nKey+".position")==""'>{{ item.position }}</i> 
                                               <i v-else>{{ $t("imprint.sourceReferenceItems."+item.i18nKey+".position") }}</i> - 
          <br />
          <a class="wordbreak" :href="item.source">{{ item.source }}</a
          >,
          <!--use i18n translation if exists-->
          <p class="wordbreak" v-if='$t("imprint.sourceReferenceItems."+item.i18nKey+".license")==""'>{{ item.license }}</p>
          <p class="wordbreak" v-else>{{ $t("imprint.sourceReferenceItems."+item.i18nKey+".license") }}</p>
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
  data(): {
    items: any;
  } {
    return {
      items: [
        {
          i18nKey:"iitBombay",
          position: "Logo von einander-helfen.org",
          author: "IIT Bombay",
          source:
            "https://commons.wikimedia.org/wiki/File:Heart-hand-shake.svg",
          license:
            "The copyright holder of this file, IIT Bombay, allows anyone to use it for any purpose, provided that the copyright holder is properly attributed. Redistribution, derivative work, commercial use, and all other use is permitted.",
        },
        {
          i18nKey:"sKopp",
          position:
            'Im Dropdownmenü links neben "Deutschland" (Deutschlandflagge)',
          author: "SKopp, Madden und andere User",
          source: "https://commons.wikimedia.org/wiki/File:Flag_of_Germany.svg",
          license:
            "This image of simple geometry is ineligible for copyright and therefore in the public domain, because it consists entirely of information that is common property and contains no original authorship.",
        },
        {
          i18nKey:"tommasoSansone",
          position: 'Im Dropdownmenü links neben "International" (Weltkugel)',
          author: "Tommaso.sansone91",
          source: "https://commons.wikimedia.org/wiki/File:Earth_icon_2.png",
          license:
            "This file is made available under the Creative Commons CC0 1.0 Universal Public Domain Dedication. The person who associated a work with this deed has dedicated the work to the public domain by waiving all of their rights to the work worldwide under copyright law, including all related and neighboring rights, to the extent allowed by law. You can copy, modify, distribute and perform the work, even for commercial purposes, all without asking permission.",
        },
        {
          i18nKey:"truthseeker",
          position: "Auf der Startseite erstes Bild im Karussel",
          author: "truthseeker08",
          source:
            "https://pixabay.com/de/photos/hospiz-pflege-krankenpflege-1797305/",
          license: "https://pixabay.com/de/service/terms/#license",
        },
        {
          i18nKey:"timkraaijvanger",
          position: "Auf der Startseite zweites Bild im Karussel",
          author: "timkraaijvanger",
          source:
            "https://pixabay.com/de/photos/kind-kleinkind-süß-blondine-blume-3089906/",
          license: "https://pixabay.com/de/service/terms/#license",
        },
        {
          i18nKey:"anemone",
          position: "Auf der Startseite drittes Bild im Karussel",
          author: "Anemone123",
          source:
            "https://pixabay.com/de/photos/teamgeist-zusammenhalt-gemeinsam-2447163/",
          license: "https://pixabay.com/de/service/terms/#license",
        },
        {
          i18nKey:"cottonbro",
          position: "Auf der Startseite unten das Bild auf der ersten Kachel",
          author: "cottonbro",
          source:
            "https://www.pexels.com/de-de/foto/lebensmittel-hande-liebe-menschen-3992383/",
          license: "https://www.pexels.com/de-de/lizenz/",
        },
        {
          i18nKey:"andreaPiacquadio",
          position: "Auf der Startseite unten das Bild auf der zweiten Kachel",
          author: "Andrea Piacquadio",
          source:
            "https://www.pexels.com/de-de/foto/mann-menschen-frau-schreibtisch-3769981/",
          license: "https://www.pexels.com/de-de/lizenz/",
        },
        {
          i18nKey:"fauxels",
          position: "Auf der Startseite unten das Bild auf der vierten Kachel",
          author: "fauxels",
          source:
            "https://www.pexels.com/de-de/foto/mann-menschen-frau-schreibtisch-3184357/",
          license: "https://www.pexels.com/de-de/lizenz/",
        },
        {
          i18nKey:"andreaPiacquadio2",
          position: "Auf der Startseite unten das Bild auf der dritten Kachel",
          author: "Andrea Piacquadio",
          source:
            "https://www.pexels.com/de-de/foto/lebensmittel-mann-menschen-frau-3772534/",
          license: "https://www.pexels.com/de-de/lizenz/",
        },
        {
          i18nKey:"freepik",
          position: "Icon auf der PageNotFound Seite",
          author: "https://www.freepik.com",
          source: "https://www.flaticon.com/free-icon/robot_3398613",
          license: "https://www.freepikcompany.com/legal",
        },
      ],
    };
  },
});
</script>

<style lang="scss" scoped></style>
