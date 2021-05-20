<template>
  <v-app-bar flat height="100px" width="100%" color="#00254f">
    <v-row class="header">
      <v-col class="logo">
        <v-app-bar-nav-icon>
          <v-img
            class="mt-7"
            width="80px"
            height="75px"
            src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Heart-hand-shake.svg/256px-Heart-hand-shake.svg.png"
          />
        </v-app-bar-nav-icon>
        <div class="logo_text pl-5 mt-5 headline font-weight-light white--text">
          einander-helfen.org
        </div>
      </v-col>
      <v-col class="slogan">
        <div
          class="font-weight-bold d-none d-sm-flex pl-5 mt-5 title font-weight-light white--text"
        >
          Das Portal für Freiwilligenarbeit
        </div>
      </v-col>
      <v-col class="menu">
        <MenuButton />
      </v-col>
    </v-row>
  </v-app-bar>
</template>

<script>
import Vue from "vue";
import MenuButton from "@/components/layout/MenuButton.vue";

export default Vue.extend({
  name: "HeaderHome",
  components: {
    MenuButton,
  },
  data: function () {
    return {};
  },
});
</script>


<style lang="scss" scoped>
.header {
  margin-left: 16px;

  .logo {
    display: flex;
  }

  .slogan {
    text-align: center;
  }

  .menu {
    display: flex;
    justify-content: flex-end;
  }

  @media screen and (max-width: 765px) {
    .slogan {
      display: none;
    }
  }
}
</style>

<style lang="scss">
@media (max-width: 300px) {
  .column {
    padding-bottom: 19px !important ;
  }
  .logoCol {
    max-width: 70% !important ;
  }

  .menuCol {
    max-width: 30% !important;
  }

  #logo {
    margin-top: 6px;
    display: none;
    visibility: hidden;
  }
}

@media (min-width: 301px) and (max-width: 424px) {
  .column {
    padding-bottom: 19px !important;
  }
  .logoCol {
    max-width: 50% !important;
  }

  .menuCol {
    max-width: 50% !important;
  }

  #logo {
    margin-top: 12px !important;
  }
}

@media (min-width: 424px) and (max-width: 765px) {
  .column {
    padding-bottom: 19px !important;
  }
  .logoCol {
    max-width: 80% !important;
  }

  .menuCol {
    max-width: 20% !important;
  }
  #logo {
    margin-top: 24px !important;
  }
}

@media (min-width: 766px) {
  .column {
    max-width: 24% !important;
    padding-top: 6px !important;
  }

  #logo {
    margin-top: 6px !important;
  }

  #slogan {
    display: block;
    margin-top: 0px !important;
  }

  #sloganCol {
    visibility: visible !important;
    display: block !important;
  }
}

@media (min-width: 855px) and (max-width: 1003px) {
  .column {
    max-width: 40% !important;
    padding-top: 6px !important;
  }

  #logo {
    margin-top: 6px !important;
    max-width: 60%;
  }

  #sloganCol {
    max-width: 50% !important;
  }
}

@media (min-width: 1004px) and (max-width: 1477px) {
  .column {
    max-width: 80%;
    padding-top: 6px;
  }

  #logo {
    margin-top: 6px !important;
  }

  #sloganCol {
    visibility: visible;
  }

  #slogan {
    margin-top: 20px !important;
  }
}

@media (min-width: 1393px) {
  #logo {
    margin-top: 24px !important;
  }

  #sloganCol {
    visibility: visible;
  }

  #slogan {
    margin-top: 20px !important;
  }
}
</style>
