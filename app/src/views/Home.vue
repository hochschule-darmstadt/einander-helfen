<template>
  <div class="home">
    <h1>Einander Helfen</h1>
    <v-card
            color="red lighten-2"
            dark
    >
      <v-card-text>
        <v-autocomplete
                v-model="model"
                :items="items"
                :loading="isLoading"
                :search-input.sync="query"
                color="white"
                hide-no-data
                hide-selected
                item-text="Description"
                item-value="API"
                label="Public APIs"
                placeholder="Start typing to Search"
                prepend-icon="mdi-database-search"
                return-object
        ></v-autocomplete>
      </v-card-text>
      <v-divider></v-divider>
      <v-expand-transition>
        <v-list v-if="model" class="red lighten-3">
          <v-list-item
                  v-for="(field, i) in fields"
                  :key="i"
          >
            <v-list-item-content>
              <v-list-item-title v-text="field.value"></v-list-item-title>
              <v-list-item-subtitle v-text="field.key"></v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-expand-transition>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
                :disabled="!model"
                color="grey darken-3"
                @click="model = null"
        >
          Clear
          <v-icon right>mdi-close-circle</v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';

interface Entry {
  API: string;
  Description: string;
  Auth: string;
  HTTPS: boolean;
  Cors: string;
  Link: URL;
  Category: string;
}

export default Vue.extend({
  data(): {
    query: string,
    isLoading: boolean,
    model?: Entry
    count: number,
    entries: Entry[],
    descriptionLimit: number,
  } {
    return {
      query: '',
      isLoading: false,
      model: undefined,
      count: 0,
      entries: [],
      descriptionLimit: 60,
    };
  },

  watch: {
    query(val): void {
      // Items have already been loaded
      if (this.items.length > 0) {
        return;
      }

      // Items have already been requested
      if (this.isLoading) {
        return;
      }

      this.isLoading = true;

      // Lazily load input items
      fetch('https://api.publicapis.org/entries')
              .then((res) => res.json())
              .then((res) => {
                const { count, entries } = res;
                this.count = count;
                this.entries = entries;
              })
              .catch((err) => {
                console.log(err);
              })
              .finally(() => (this.isLoading = false));
    },
  },

  computed: {
    fields(): object {
      if (!this.model) {
        return [];
      }

      return Object.keys(this.model).map((key) => {
        if (this.isValidKey(key, this.model)) {
          return {
            key,
            value: this.model ? this.model[key] || 'n/a' : 'n/a',
          };
        }
      });
    },
    items(): Entry[] {
      return this.entries.map((entry) => {

        const Description = entry.Description.length > this.descriptionLimit
                ? entry.Description.slice(0, this.descriptionLimit) + '...'
                : entry.Description;

        return Object.assign({}, entry, { Description });
      });
    },
  },

  methods: {
    isValidKey(prop: string, obj: Entry | undefined): prop is keyof Entry {
      return (obj && (prop in obj)) as boolean;
    }
  }

});
</script>
