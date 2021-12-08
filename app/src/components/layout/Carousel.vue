<!-- The carousel contains images that are shown alternately every few seconds.-->

<template>
  <VueSlickCarousel class="carousel"
    :dots="true"
    :infinite="true"
    :autoplay="true"
    :autoplaySpeed="30000"
  >
    <picture>
      <source media="(max-width: 768px)" srcset="/images/header/1_phone.jpg" />
      <img src="/images/header/1.jpg" />
    </picture>
    <picture>
      <source media="(max-width: 768px)" srcset="/images/header/2_phone.jpg" />
      <img src="/images/header/2.jpg" />
    </picture>
    <picture>
      <source media="(max-width: 768px)" srcset="/images/header/3_phone.jpg" />
      <img src="/images/header/3.jpg" />
    </picture>
  </VueSlickCarousel>
</template>

<script lang="ts">
import Vue from "vue";
import VueSlickCarousel from "vue-slick-carousel";
import "vue-slick-carousel/dist/vue-slick-carousel-theme.css";
import "vue-slick-carousel/dist/vue-slick-carousel.css";

export default Vue.extend({
  name: "Carousel",
  components: {
    VueSlickCarousel,
  },
});
</script>

<style lang="scss" scoped>
.carousel {
  cursor: pointer;
}
img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  pointer-events: none;
}
.slick-arrow {
  display: none !important ;
  visibility: hidden;
}
</style>
