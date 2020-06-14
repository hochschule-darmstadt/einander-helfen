<template>
    <v-autocomplete
            label="Standort"
            :items="cities"
            v-model="cities[0]"
            prepend-inner-icon="place">
    </v-autocomplete>
</template>

<script>
export default {
    data: () => ({
        cities: [
            'Main Standort',
            'Darmstadt',
            'Frankfurt am Main',
            'Wiesbaden',
            'Mainz'
        ]
    })
};
</script>

<style scoped>

</style>