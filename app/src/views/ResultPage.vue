<template>
    <div>
        <Header/>
        <div class="grid">
            <div class="map" v-if="!postIsOpen">
                <v-card tile height="75vh">
                    <div id="map" :style="{height: map.height, width: map.width}">
                        <v-btn @click="closeMap()"
                               style="position: absolute; z-index: 9999; margin-left: 50px; margin-top: 20px;">Details
                        </v-btn>
                        <l-map ref="map" :center="map.center" :zoom="map.zoom">
                            <l-tile-layer :url="map.url" :attribution="map.attribution"></l-tile-layer>
                            <template v-for="(advertisement, i) in posts">
                                <l-marker v-if="i === currentPostId" :icon="map.markerRed"
                                          :lat-lng="[advertisement.lat, advertisement.lon]"
                                          @click="openAdvertisement(i)">
                                    <l-tooltip>{{ advertisement.title }}</l-tooltip>
                                </l-marker>
                                <l-marker v-else :icon="map.markerBlue"
                                          :lat-lng="[advertisement.lat, advertisement.lon]"
                                          @click="openAdvertisement(i)">
                                    <l-tooltip>{{ advertisement.title }}</l-tooltip>
                                </l-marker>
                            </template>
                        </l-map>
                    </div>
                </v-card>
            </div>
            <div class="detail" v-if="postIsOpen">
                <v-card
                        class="detailCard"
                        tile
                >
                    <v-list-item three-line>
                        <v-btn class="mr-3" text @click="closeAdvertisement()">
                            <v-icon>arrow_back</v-icon>
                        </v-btn>
                        <!--display title, subtitle and image on the left side-->
                        <v-list-item-content style="margin-top:2%">
                            <v-list-item-title class="headline mb-1">{{
                                currentPost.title
                                }}
                            </v-list-item-title>
                            <v-list-item-subtitle>{{
                                currentPost.task
                                }}
                            </v-list-item-subtitle>
                        </v-list-item-content>

                        <v-img
                                style="margin-top:2%"
                                max-width="80px"
                                height="80px"
                                contain
                                :src="currentPost.image"
                        ></v-img>
                    </v-list-item>

                    <!--display content on the right side-->
                    <v-card-text style="padding-left:5%; padding-right:5%">
                        <v-row v-if="currentPost.location">
                            <v-col cols="2">Einsatzort</v-col>
                            <v-col cols="8" v-html="currentPost.location"></v-col>
                        </v-row>
                        <v-row v-if="currentPost.target_group">
                            <v-col cols="2">Zielgruppe</v-col>
                            <v-col
                                    cols="8"
                                    v-html="currentPost.target_group"
                            ></v-col>
                        </v-row>
                        <v-row v-if="currentPost.timing">
                            <v-col cols="2">Einstiegsdatum / Beginn</v-col>
                            <v-col cols="8" v-html="currentPost.timing"></v-col>
                        </v-row>
                        <v-row v-if="currentPost.effort">
                            <v-col cols="2">Zeitaufwand</v-col>
                            <v-col cols="8" v-html="currentPost.effort"></v-col>
                        </v-row>
                        <v-row v-if="currentPost.opportunities">
                            <v-col cols="2">Möglichkeiten</v-col>
                            <v-col
                                    cols="8"
                                    v-html="currentPost.opportunities"
                            ></v-col>
                        </v-row>
                        <v-row v-if="currentPost.organization">
                            <v-col cols="2">Organisation</v-col>
                            <v-col
                                    cols="8"
                                    v-html="currentPost.organization"
                            ></v-col>
                        </v-row>
                        <v-row v-if="currentPost.contact">
                            <v-col cols="2">Kontakt</v-col>
                            <v-col cols="8" v-html="currentPost.contact"></v-col>
                        </v-row>
                    </v-card-text>

                    <v-card-actions>
                        <v-col>
                            <v-container style="margin-bottom: 10px">
                                <template
                                        v-for="(category, i) in currentPost.categories"
                                >
                                    <v-chip :key="i" class="mr-2">{{ category }}</v-chip>
                                </template>
                            </v-container>
                            <v-spacer></v-spacer>
                            <v-container style="display:flex;justify-content:center;">
                                <v-btn
                                        class="my-2"
                                        dark
                                        large
                                        color="#F29472"
                                        :href="currentPost.link"
                                        target="_blank"
                                >
                                    Zum Stellenangebot
                                </v-btn>
                            </v-container>
                        </v-col>
                    </v-card-actions>
                </v-card>
            </div>

            <div class="posts">
                <div ref="wrapperPosts">
                    <template v-for="(advertisement, i) in visiblePages">
                        <v-card class="mb-3" tile>
                            <v-list-item three-line @click="openAdvertisement(i)">
                                <v-list-item-content>
                                    <v-list-item-title class="headline mb-1">{{
                                        advertisement.title
                                        }}
                                    </v-list-item-title>
                                    <v-list-item-subtitle>{{
                                        advertisement.task
                                        }}
                                    </v-list-item-subtitle>
                                </v-list-item-content>

                                <v-img
                                        max-width="80px"
                                        height="80px"
                                        contain
                                        :src="advertisement.image"
                                ></v-img>
                            </v-list-item>
                        </v-card>
                    </template>
                </div>
                <!--pageination-->
                <div class="text-center" style="margin-top:2%">
                    <v-pagination v-model="page" :length="numberOfPages" color="#054C66"></v-pagination>

                </div>
            </div>
        </div>
    </div>
</template>

<!-- test content -->
<script lang="ts">
    import Header from '@/components/layout/Header.vue';
    import Advertisement from '@/models/advertisement';

    import Vue from 'vue';
    import {mapActions, mapState} from 'vuex';

    import L, {LatLngTuple} from 'leaflet';
    import {LMap, LTileLayer, LMarker, LTooltip, LIcon} from 'vue2-leaflet';
    import 'leaflet/dist/leaflet.css';

    export default Vue.extend({
        components: {Header, LMap, LTileLayer, LMarker, LTooltip},
        data(): {
            postIsOpen: boolean;
            currentPostId: number;
            page: number;
            perPage: number;
            map: any;
        } {
            return {
                postIsOpen: false,
                currentPostId: 0,
                page: 1,
                perPage: 7,
                map: {
                    url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
                    center: [51.5000, 10.5000],
                    zoom: 12,
                    width: '100%',
                    height: '100%',
                    markerBlue: L.icon({
                        iconUrl: require('../../public/images/marker/marker-icon.png'),
                        iconSize: [25, 41]
                    }),
                    markerRed: L.icon({
                        iconUrl: require('../../public/images/marker/marker-icon-red.png'),
                        iconSize: [25, 41]
                    })
                }
            };
        },
        computed: {
            ...mapState(['posts']),
            visiblePages(): Advertisement[] {
                return this.posts.slice(
                    (this.page - 1) * this.perPage,
                    this.page * this.perPage
                );
            },
            currentPost(): Advertisement | null {
                return this.postIsOpen
                    ? this.posts[this.currentPostId]
                    : null;
            },
            numberOfPages(): number {
                return Math.ceil(this.posts.length / this.perPage);
            }
        },
        created(): void {
            this.hydrateStateFromURIParams(this.$route.query);
        },
        watch: {
            posts(val: Advertisement[], oldVal: Advertisement[]): void {
                if (val.length === 1) {
                    this.openAdvertisement(0);
                }
                const markers = val.map((post) => [post.lat, post.lon] as LatLngTuple);
                (this.$refs.map as LMap).fitBounds(markers);
            }
        },
        methods: {
            ...mapActions(['hydrateStateFromURIParams']),
            openAdvertisement(index: number): void {
                this.postIsOpen = true;
                this.currentPostId = index + ((this.page - 1) * this.perPage);
            },
            closeAdvertisement(): void {
                this.postIsOpen = false;
                const currentPost = this.posts[this.currentPostId];
                const location = [currentPost.lat, currentPost.lon] as LatLngTuple;
                this.$nextTick(() => {
                    (this.$refs.map as LMap).setCenter(location);
                })
            },
            numberOfPages(): number {
                return Math.ceil(this.posts.length / this.perPage);
            },
            closeMap(): void {
                this.postIsOpen = true;
            }
        }
    });
</script>

<style scoped>
    .grid {
        width: 100%;
        display: grid;
        grid-template-columns: 50% 50%;
        grid-template-areas: "posts detail";
    }

    .map,
    .detail {
        grid-area: detail;
        height: 75vh;
    }

    .posts {
        grid-area: posts;
        height: 75vh;
        overflow: auto
    }

    @media (max-width: 500px) {
        .grid {
            grid-template-columns: 100%;
            grid-row-gap: 10px;
            grid-template-areas: "detail" "posts";
        }

        .posts {
            height: auto;
        }
    }
</style>
