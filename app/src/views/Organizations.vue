<!-- The page 'Organisationen'. It provides links to other organizations that offer voluntary work.-->

<template>
  <div>
    <Header />
    <div class="organizations">
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
            v-show="getLetterOrganizations(letter).length > 0"
          >
            <h2>{{ letter }}</h2>
            <div
              v-for="organization in getLetterOrganizations(letter)"
              :key="organization.title"
            >
              <a class="organizationLink" :href="organization.url">
                {{ organization.title }}
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
import Organization from "@/models/organization";
import organizations from "@/resources/organizations";

export default Vue.extend({
  name: "Organizations",
  components: {
    Header,
  },
  data() {
    return {
      alphabet: "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ".split(""),
    };
  },
  computed: {
    organizationsArray(): Organization[] {
      return organizations;
    },
  },
  methods: {
    /**
     * Provides a caseinsensitive sorted list of all organizations of the given letter.
     *
     * @param {string} letter: The letter that the organization's title must begin with. Caseinsensitive.
     * @return {Organization[]}: A sorted array with all organizations that start with the given letter.
     */
    getLetterOrganizations(letter: string): Organization[] {
      // Filter organizations starting with the given letter
      var letterOrganizations = organizations.filter((organization) =>
        organization.title.toUpperCase().startsWith(letter)
      );
      // Sort organizations caseinsensitive
      return letterOrganizations.sort(function (a, b) {
        return a.title.toLowerCase() < b.title.toLowerCase() ? -1 : 1;
      });
    },
  },
});
</script>

<style lang="scss" scoped>
@import "./../styles/ContainerWithContent.css";

.letterBox {
  display: inline-block;
  width: 100%;
}
.organizationLink {
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
