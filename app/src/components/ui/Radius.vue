<template>
    <v-select
            label="Umkreis"
            :items="radii"
            item-value="value"
            @input="newSelectedRadius = $event"
            v-bind:value="selectedRadius"
            :dark="dark"
            style="margin-left: 10px; margin-right: 10px;">
    </v-select>
</template>

<script lang="ts">
    import { createNamespacedHelpers } from 'vuex';
    const { mapActions, mapState } = createNamespacedHelpers('locationSearchModule');

    import Vue from 'vue';

    export default Vue.extend({
        props: {
            dark: {
                type: Boolean,
                default: false
            },
        },
        data(): {
            newSelectedRadius: string,
            radii: Array<{text: string, value: string}>
        } {
            return {
                newSelectedRadius: '',
                radii: [
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
                ]
            };
        },
        watch: {
            newSelectedRadius(newValue, oldValue): void {
                this.setSelectedRadius(newValue);
                if (this.$route.name === 'resultPage') {
                   this.$store.dispatch('updateURIFromState');
                }
            },
        },
        computed: {
            ...mapState(['selectedRadius'])
        },
        methods: {
            ...mapActions(['setSelectedRadius']),
        }
    });
</script>

<style scoped>

</style>
