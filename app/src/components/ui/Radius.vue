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
    import radii from '@/resources/radii';
    import Radius from '@/models/radius';

    export default Vue.extend({
        props: {
            dark: {
                type: Boolean,
                default: false
            },
        },
        data(): {
            newSelectedRadius: string,
            radii: Radius[]
        } {
            return {
                newSelectedRadius: '',
                radii
            };
        },
        watch: {
            newSelectedRadius(newValue): void {
                this.setSelectedRadius(newValue);
                this.$emit('input', newValue);
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
