<template>
  <v-card class="post" tile>
    <v-btn class="button-close" icon @click="closePost()">
      <v-icon>close</v-icon>
    </v-btn>
    <v-card-title class="heading">
      <v-tooltip top v-if="post.geo_location === null">
        <template v-slot:activator="{ on }">
          <div class="d-inline-block" v-on="on">
            <v-btn class="button-map disabled" dark disabled>
              <v-icon class="button-icon">map</v-icon> Karte
            </v-btn>
          </div>
        </template>
        <span>
          Der Pin für dieses Angebot kann auf der Karte nicht angezeigt werden,
          da keine Geodaten hinterlegt sind.
        </span>
      </v-tooltip>

      <v-btn v-else class="button-map" dark @click="openMap()">
        <v-icon>map</v-icon> Karte
      </v-btn>

      <!--display title, subtitle and image on the right side-->
      <div class="headline">
        {{ post.title }}
      </div>
    </v-card-title>
    <v-card-text class="content">
      <v-simple-table dense>
        <tbody>
          <template v-for="el in headers">
            <tr v-if="post[el.key]" :key="el.key">
              <td>{{ el.label }}</td>
              <td v-if="el.link">
                <a
                  :href="post[el.link]"
                  target="_blank"
                  v-html="post[el.key]"
                />
              </td>
              <td v-else v-html="post[el.key]" />
            </tr>
          </template>
        </tbody>
      </v-simple-table>
    </v-card-text>

    <v-card-actions class="actions">
      <div class="tags">
        <template v-for="(category, i) in post.categories">
          <v-chip :key="i" class="mr-2 mt-2">{{ category }}</v-chip>
        </template>
      </div>
      <v-spacer />
      <div class="my-2">
        <v-btn dark large color="#054C66" :href="post.link" target="_blank">
          Zum Angebot
        </v-btn>
      </div>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import Vue from "vue";
import Post from "@/models/post";

/**
 * Emits @openMap click on button to Map
 * Emits @close close this card
 */
export default Vue.extend({
  name: "PostCard",
  props: {
    post: {
      type: Object as () => Post,
      required: true,
    },
  },
  data: function () {
    return {
      headers: [
        { key: "location", label: "Einsatzort" },
        { key: "task", label: "Aufgabe" },
        { key: "contact", label: "Ansprechpartner" },
        { key: "organization", label: "Organisation" },
        { key: "target_group", label: "Zielgruppe" },
        { key: "timing", label: "Einstiegsdatum / Beginn" },
        { key: "effort", label: "Zeitaufwand" },
        { key: "opportunities", label: "Möglichkeiten" },
        { key: "prerequisites", label: "Anforderungen" },
        { key: "language_skills", label: "Sprachen" },
        { key: "source", label: "Quelle", link: "link" },
      ],
    };
  },
  methods: {
    openMap(): void {
      this.$emit("openMap", this.post);
    },
    closePost(): void {
      this.$emit("close");
    },
  },
});
</script>

<style lang="scss" scoped>
.post {
  padding: 20px 0px;

  .button-close {
    position: absolute;
    top: 3px;
    right: 3px;
  }
  .heading {
    align-items: center;
    flex-wrap: unset;
    .button-map {
      margin-left: 20px;
      margin-right: 20px;
      background-color: rgb(5, 76, 102) !important;

      &.disabled {
        background-color: #e0e0e0;
        color: rgb(174, 168, 168) !important;
        .button-icon {
          color: rgb(174, 168, 168) !important;
        }
      }
    }
    .headline {
      padding-right: 20px;
      word-break: break-word;
    }
  }

  .content {
    padding: 0 10px;
    table {
      border-spacing: 0 20px !important;
    }
    tr:not(:first-child) {
      padding-top: 4px;
    }
    tr:hover {
      background: unset !important;
    }
    td {
      vertical-align: top;
    }
    tr:not(:last-child) td:not(.v-data-table__mobile-row) {
      border: 0 !important;
    }
  }

  .actions {
    flex-direction: column;

    .tags {
      align-self: flex-start;
      margin: 0px 10px;
    }
  }
}

@media only screen and (max-width: 960px) {
  .headline {
    font-size: 1.3rem !important;
  }
}
@media only screen and (max-width: 500px) {
  .button-map,
  .button-close {
    display: none;
  }
}
</style>
