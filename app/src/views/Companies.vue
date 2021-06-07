<!-- The page 'Organisationen'. It provides links to other companies that offer voluntary work.-->

<template>
  <div>
    <Header />
    <div class="companies">
      <v-container justify="center" class="containerWithContent">
        <h1>Organisationen</h1>
        Sie haben nicht das gefunden, wonach Sie gesucht haben? Kein Problem!
        Die untensetehende Liste enthält weiterführende Links zu anderen
        Organisationen, die ebenfalls nationale und internationale ehrenamtliche
        Tätigkeiten zur Verfügung stellen.
        <div class="urlList mt-4">
          <div
            class="letterBox mb-4"
            v-for="letter in alphabet"
            :key="letter"
            v-show="getLetterCompanies(letter).length > 0"
          >
            <h2>{{ letter }}</h2>
            <div
              v-for="company in getLetterCompanies(letter)"
              :key="company.title"
            >
              <a class="companyLink" :href="company.url">
                {{ company.title }}
              </a>
              <br />
            </div>
          </div>
        </div>
      </v-container>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import Header from "@/components/layout/SearchHeader.vue";
import Company from "@/models/company";
import companies from "@/resources/companies";

export default Vue.extend({
  name: "Companies",
  components: {
    Header,
  },
  data() {
    return {
      alphabet: "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ".split(""),
    };
  },
  computed: {
    companiesArray(): Company[] {
      return companies;
    },
  },
  methods: {
    /**
     * Provides a caseinsensitive sorted list of all companies of the given letter.
     *
     * @param {string} letter: The letter that the company's title must begin with. Caseinsensitive.
     * @return {Company[]}: A sorted array with all companies that start with the given letter.
     */
    getLetterCompanies(letter: string): Company[] {
      // Filter companies starting with the given letter
      var letterCompanies = companies.filter((company) =>
        company.title.toUpperCase().startsWith(letter)
      );
      // Sort companies caseinsensitive
      return letterCompanies.sort(function (a, b) {
        return a.title.toLowerCase() < b.title.toLowerCase() ? -1 : 1;
      });
    },
  },
});
</script>

<style>
@import "./../styles/ContainerWithContent.css";

.letterBox {
  display: inline-block;
  width: 100%;
}
.companyLink {
  text-decoration: none;
}
.urlList {
  column-count: 3;
}

@media (max-width: 960px) {
  .urlList {
    column-count: 2;
  }
}

@media (max-width: 599px) {
  .urlList {
    column-count: 1;
  }
}
</style>
