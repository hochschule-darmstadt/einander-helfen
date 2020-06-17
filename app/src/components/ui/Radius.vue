<template>
    <v-select
            label="Umkreis"
            :items="radii"
            item-value="value"
            v-model="selectedRadius"
            :dark="dark"
            style="margin-left: 10px; margin-right: 10px;">
    </v-select>
</template>

<script lang="ts">
    import {mapActions, mapGetters, mapState} from 'vuex';
    declare var require: any;
    import Vue from 'vue';
    import QueryBuilder from 'es-query-builder/dist';
    import axios from 'axios';

    export default Vue.extend({
        props: {
            dark: {
                type: Boolean,
                default: false
            },
        },
        data(): {
            selectedRadius: string,
        } {
            return {
                selectedRadius: this.$store.state.radiusSearchValue || '',
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
        computed: {
            ...mapState(['radii'])
        }
    });
</script>

<style scoped>

</style>
