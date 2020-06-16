<template>
    <v-select
            label="Umkreis"
            :items="radius"
            v-model="selectedRadius"
            style="margin-left: 10px; margin-right: 10px;">       
    </v-select>
</template>

<script lang="ts">
    import {mapActions, mapGetters, mapState} from 'vuex';
    declare var require: any;
    import Vue from 'vue';
    import QueryBuilder from 'es-query-builder/dist';
    import axios from 'axios';

    export default Vue.extend(
    {
        data(): {
            radius: object[],
            selectedRadius: number,
        } {
            return {
                radius: [
                    {
                        text: 'Überall',
                        value: 0,
                    },
                    {
                        text: '5 km',
                        value: 5,
                    },
                    {
                        text: '10 km',
                        value: 10,
                    },
                    {
                        text: '25 km',
                        value: 25,
                    },
                    {
                        text: '50 km',
                        value: 50,
                    },
                ],
                selectedRadius: this.$store.state.radiusSearchValue || 0,
            };
        },
        watch: {
            selectedRadius(newValue, oldValue): void {
                this.setRadiusSearchValue(newValue);
                if (this.$route.name === 'resultPage') {
                    this.$router.push({
                    name: 'resultPage',
                    query: {
                        q: this.$route.query.q,
                        location: this.$route.query.location,
                        radius: newValue + '',
                    }
                    });
                }
            },
        },
        methods: {
            ...mapActions(['setRadiusSearchValue']),
        },
    });
</script>

<style scoped>

</style>