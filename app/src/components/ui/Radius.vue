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
            selectedRadius: string,
        } {
            return {
                radius: [
                    {
                        text: 'Überall',
                        value: '',
                    },
                    {
                        text: '5 km',
                        value: '5km',
                    },
                    {
                        text: '10 km',
                        value: '10km',
                    },
                    {
                        text: '25 km',
                        value: '25km',
                    },
                    {
                        text: '50 km',
                        value: '50km',
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
                        ...this.$route.query,
                        radius: newValue,
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
