<!-- The page 'Anbieter'. It provides links to other organizations that offer voluntary work.-->

<template>
  <div class="organizations">
    <Header />
    <section class="container pt-6">
      <h1>{{ $t("organizations.organizationsHeadline") }}</h1>
      {{ $t("organizations.organizationsDescription1") }}
      <div class="organizationList mt-4">
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
            <a class="link" :href="organization.url" target="blank">
              {{ organization.title }}
            </a>
            <br />
          </div>
        </div>
      </div>
    </section>
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
.organizationList {
  column-width: 20em;
  column-gap: 6em;
}

.letterBox {
  display: inline-block;
  width: 100%;
}

.link {
  text-decoration: none;
  &:hover {
    text-decoration: underline;
  }
}
</style>
