<template>
    <v-autocomplete
            filled
            rounded
            color="white"
            label="z.B. MacherIn"
            append-icon="search"
            :items="volunteerTags">
    </v-autocomplete>
</template>

<script>
export default {
    data: () => ({
        volunteerTags: [
            'MacherIn',
            'DenkerIn',
            'Jugend Arbeit',
            'Soziales'
        ]
    })
};
</script>

<style scoped>

</style>