<template>
    <v-autocomplete
            label="Umkreis"
            :items="kms"
            v-model="kms[0]">
    </v-autocomplete>
</template>

<script>
export default {
    data: () => ({
        kms: ['Überall', '5 km', '10 km', '25 km', '50 km']
    })
};
</script>

<style scoped>

</style>