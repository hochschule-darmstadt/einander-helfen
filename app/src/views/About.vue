<template>
    <div>
        <Header />
        <p>Hier würde die Über-Seite stehen.</p>
    </div>
</template>


<script lang="ts">
import Header from '@/components/layout/Header.vue';
import Vue from 'vue';

export default Vue.extend({
  components: { Header },
});
</script>