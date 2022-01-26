<!-- The page 'Über uns'. It describes einander-helfen.org and how it works.-->

<template>
  <div class="about">
    <Header />
    <section class="container pt-6">
      <div>
        <h1>einander-helfen.org</h1>
        <p>
          <strong>einander-helfen.org</strong> is the fast search portal for
          Volunteering and voluntary activities: With a wealth of different
          offers around the world.
        </p>
      </div>
      <div>
        <h2>And this is how it works:"</h2>
        <p>
          Are you looking for a job offer for volunteering or honorary work
          within Germany? Then enter a keyword on the search. Don't forget to
          limit the radius! All offers are immediately displayed on the map and
          in the list. Select an offer (in the list or on the map) and the
          corresponding details are displayed. Another click takes you to the
          provider's page - with further information. You can also limit the
          search by several keywords
        </p>
        <p>
          Are you looking for a job offer for international voluntary service?
          Then click on the Germany flag and select \"International\" instead.
          Now enter your desired country and a keyword in the search field. All
          offers are immediately displayed on the map and in the list. Select an
          offer (in the list or on the map) and the corresponding details are
          displayed. Another click takes you to the provider's page - with
          further information. You can also narrow down the search by using
          several keywords.
        </p>
        <p>
          <strong>einander-helfen.org</strong> brings together offers from
          multiple providers around the world and allows you to conveniently
          search across all of them. Currently the following providers are
          covered:
        </p>
        <ul>
          <li>
            <a
              href="https://www.volunteermatch.org/"
              target="_blank"
              rel="noopener"
              >https://www.volunteermatch.org/</a
            >
          </li>
        </ul>
        <p>
          <br />
          More providers will follow. <br />
          Do you have any suggestions for improvement or is something missing?
          Then please contact us at
          <a href="mailto:info@einander-helfen.org">
            info@einander-helfen.org </a
          >.
        </p>
      </div>
      <div>
        <h2>Who we are:</h2>
        <p>
          We are a team of volunteers and have developed the site with a lot of
          initiative and passion. The software is open source
          <a
            href="https://github.com/hochschule-darmstadt/einander-helfen"
            target="_blank"
          >
            https://github.com/hochschule-darmstadt/einander-helfen
          </a>
          and was originally programmed by a team of students. We look forward
          to your suggestions and ideas for improvement at
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
