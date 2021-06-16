<!-- The list item of a post. It contains the title and location of a post. In the mobile view it also contains the details of the post. -->

<template>
  <v-card class="post mb-3">
    <v-list-item
      :ripple="false"
      three-line
      class="post-list-item"
      :class="{ active: active }"
      @click="onClick"
    >
      <v-list-item-content>
        <v-list-item-title
          class="headline mb-1"
          :class="{ 'full-text': active }"
          v-html="post.title"
        />
        <v-list-item-subtitle
          :set="(distance = postDistance(post))"
          :class="{
            'post-subtitle-hidden': active,
            'post-subtitle': !active,
          }"
        >
          <strong>
            <span v-if="post.post_struct.location.country === 'Deutschland'">
              {{ post.post_struct.location.zipcode }}
            </span>
            <span> {{ post.post_struct.location.city }} </span>
            <span v-if="post.post_struct.location.country !== 'Deutschland'">
              {{ post.post_struct.location.country }}
            </span>
            <em
              v-if="
                distance && post.post_struct.location.country === 'Deutschland'
              "
            >
              (in {{ distance }})
            </em>
          </strong>
          &mdash;
          <span v-html="post.task" />
        </v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>
    <!-- Detail Card -->
    <v-card
      v-if="showDetail"
      class="details-smartphone"
      :class="{
        'details-smartphone-visible': active,
        'details-smartphone-hidden': !active,
      }"
    >
      <v-card-text>
        <template v-for="column in columns">
          <div v-if="post[column.key]" :key="column.key">
            <h3>{{ column.label }}</h3>
            <p v-if="column.link">
              <a :href="post[column.link]" target="_blank">
                {{ post[column.key] }}
              </a>
            </p>
            <p v-else v-html="post[column.key]" />
          </div>
        </template>
      </v-card-text>
      <v-card-actions class="actions">
        <div class="tags">
          <template v-for="(category, index) in post.categories">
            <v-chip :key="index" class="mr-2 mt-2">{{ category }}</v-chip>
          </template>
        </div>
        <v-spacer></v-spacer>
        <div class="my-2 mt-6">
          <v-btn dark large color="#054C66" :href="post.link" target="_blank">
            Zum Angebot
          </v-btn>
        </div>
      </v-card-actions>
    </v-card>
  </v-card>
</template>

<script lang="ts">
import Vue from "vue";
import Post from "@/models/post";
import Location from "@/models/location";

export default Vue.extend({
  name: "PostListItem",
  props: {
    post: {
      type: Object as () => Post,
      required: true,
    },
    active: {
      type: Boolean,
      default: false,
    },
    showDetail: {
      type: Boolean,
      default: false,
    },
    location: {
      type: Object as () => Location,
      default: undefined,
    },
  },
  data: function () {
    return {
      columns: [
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
    onClick() {
      this.$emit("click", this.post);
    },
    /**
     * Calculates the haversine distance of the post to the search location.
     *
     * @return {string}: A string containing the rounded distance + km or an empty string if no search location
     * or no geo location of the post ist given.
     */
    postDistance(post: Post): string {
      if (!this.location || !post.geo_location) {
        return "";
      }

      const distance = this.haversineDistance(
        [post.geo_location.lat, post.geo_location.lon],
        [this.location.lat, this.location.lon]
      );

      if (distance) {
        return Math.round(distance) + " km";
      } else {
        return "";
      }
    },
    /**
     * Haversine formula to calculate the distance between two points on a sphere based on longitude and latitude.
     */
    haversineDistance([lat1, lon1], [lat2, lon2]): number {
      const toRadian = (angle) => (Math.PI / 180) * angle;
      const distance = (a, b) => (Math.PI / 180) * (a - b);
      const RADIUS_OF_EARTH_IN_KM = 6371;

      const dLat = distance(lat2, lat1);
      const dLon = distance(lon2, lon1);

      lat1 = toRadian(lat1);
      lat2 = toRadian(lat2);

      // Haversine Formula
      const h =
        Math.pow(Math.sin(dLat / 2), 2) +
        Math.pow(Math.sin(dLon / 2), 2) * Math.cos(lat1) * Math.cos(lat2);
      const c = 2 * Math.asin(Math.sqrt(h));

      return RADIUS_OF_EARTH_IN_KM * c;
    },
  },
});
</script>

<style lang="scss" scoped>
.post {
  .post-list-item.active {
    background-color: #c4e0ff !important;
  }

  .post-subtitle {
    display: -webkit-box !important;
  }

  .details-smartphone {
    display: none;
  }

  .actions {
    flex-direction: column;

    .tags {
      align-self: flex-start;
      margin: 0px 10px;
    }
  }

  @media only screen and (max-width: 960px) {
    .full-text {
      white-space: normal;
    }
    .post-subtitle-hidden {
      max-height: 0;
      opacity: 0;
      position: absolute;
    }
    .post-subtitle {
      max-height: 40px;
      opacity: 1;
      transition: all 0.4s 0.2s;
    }

    .details-smartphone {
      display: block;
      overflow: hidden;
      transition: max-height 0.4s ease-in-out;
    }
    .details-smartphone-visible {
      max-height: 10000px;
    }
    .details-smartphone-hidden {
      max-height: 0;
    }
    .details-smartphone p,
    .details-smartphone h3 {
      color: rgba(0, 0, 0, 0.87) !important;
    }
  }
}
</style>
