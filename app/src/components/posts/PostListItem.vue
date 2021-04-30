<template>
  <v-card class="post-list-item mb-3">
    <v-list-item
      :ripple="false"
      three-line
      :class="{ active: active }"
      @click="onClick"
    >
      <v-list-item-content>
        <v-list-item-title
          class="headline mb-1"
          :class="{ 'full-text': active }"
        >
          {{ post.title }}
        </v-list-item-title>
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
    <!-- TODO: Refactor this or use PostCard ... -->
    <v-card
      v-if="active && showDetail"
      class="details-smartphone"
      :class="{
        'details-smartphone-visible': active,
        'details-smartphone-hidden': !active,
      }"
    >
      <v-card-text>
        <div v-if="post.location">
          <h3>Einsatzort</h3>
          <p v-html="post.location"></p>
        </div>
        <div v-if="post.task">
          <h3>Aufgabe</h3>
          <p v-html="post.task"></p>
        </div>
        <div v-if="post.contact">
          <h3>Ansprechpartner</h3>
          <p v-html="post.contact"></p>
        </div>
        <div v-if="post.organization">
          <h3>Organisation</h3>
          <p v-html="post.organization"></p>
        </div>
        <div v-if="post.target_group">
          <h3>Zielgruppe</h3>
          <p v-html="post.target_group"></p>
        </div>
        <div v-if="post.timing">
          <h3>Einstiegsdatum / Beginn</h3>
          <p v-html="post.timing"></p>
        </div>
        <div v-if="post.effort">
          <h3>Zeitaufwand</h3>
          <p v-html="post.effort"></p>
        </div>
        <div v-if="post.opportunities">
          <h3>Möglichkeiten</h3>
          <p v-html="post.opportunities"></p>
        </div>
        <div v-if="post.prerequisites">
          <h3>Anforderungen</h3>
          <p v-html="post.prerequisites"></p>
        </div>
        <div v-if="post.language_skills">
          <h3>Sprachen</h3>
          <p v-html="post.language_skills"></p>
        </div>
        <div v-if="post.link">
          <h3>Quelle</h3>
          <p>
            <a :href="post.link" target="_blank">{{ post.source }}</a>
          </p>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-flex md12 sm12>
          <v-container style="margin-bottom: 10px">
            <template v-for="(category, i) in post.categories">
              <v-chip :key="i" class="mr-2 mt-2">{{ category }}</v-chip>
            </template>
          </v-container>
          <v-spacer></v-spacer>
          <v-container style="display: flex; justify-content: center">
            <v-btn
              class="my-2"
              dark
              large
              color="#054C66"
              :href="post.link"
              target="_blank"
            >
              Zum Angebot
            </v-btn>
          </v-container>
        </v-flex>
      </v-card-actions>
    </v-card>
  </v-card>
</template>

<script lang="ts">
import Vue from "vue";
import Post from "@/models/post";
import { mapState } from "vuex";

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
  },
  computed: {
    /** TODO: remove store variables from this component */
    ...mapState("searchModule", [
      "selectedLocation",
      "selectedRadius",
      "alternateRadius",
    ]),
  },
  methods: {
    onClick() {
      this.$emit("click", this.post);
    },
    postDistance(post: Post): string {
      if (!this.selectedLocation || !post.geo_location) {
        return "";
      }

      const distance = this.haversineDistance(
        [post.geo_location.lat, post.geo_location.lon],
        [this.selectedLocation.lat, this.selectedLocation.lon]
      );

      if (distance) {
        return Math.round(distance) + " km";
      } else {
        return "";
      }
    },
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
.post-list-item {
  &.active {
    background-color: #c4e0ff !important;
  }

  .post-subtitle {
    display: -webkit-box !important;
  }

  .details-smartphone {
    display: none;
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
    }
    .details-smartphone-visible {
      max-height: 10000px;
      transition: max-height 0.4s ease;
    }
    .details-smartphone-hidden {
      max-height: 0;
      transition: max-height 0.4s ease;
    }
    .details-smartphone p,
    .details-smartphone h3 {
      color: rgba(0, 0, 0, 0.87) !important;
    }
  }
}
</style>
