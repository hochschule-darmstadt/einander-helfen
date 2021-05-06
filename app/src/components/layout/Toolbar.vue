<template>
  <v-app-bar flat height="100px" color="#00254f">
    <v-layout justify-space-between no-gutters color="#00254f">
      <v-row>
        <v-col class="column logoCol">
          <v-layout>
            <v-app-bar-nav-icon>
              <v-img
                class="mt-7"
                width="80px"
                height="75px"
                src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Heart-hand-shake.svg/256px-Heart-hand-shake.svg.png"
              ></v-img>
            </v-app-bar-nav-icon>
            <div
              id="logo"
              class="pl-5 mt-5 headline font-weight-light white--text"
            >
              einander-helfen.org
            </div>
          </v-layout>
        </v-col>
        <v-col id="sloganCol">
          <div
            id="slogan"
            class="font-weight-bold d-none d-sm-flex pl-5 mt-5 title font-weight-light white--text"
          >
            Das schnelle Suchportal für Freiwilligenarbeit
          </div>
        </v-col>
        <v-col class="column menuCol">
          <div align="right">
            <v-menu>
              <template v-slot:activator="{ on, attrs }">
                <v-btn id="menu" v-bind="attrs" v-on="on" dark icon>
                  <v-icon>menu</v-icon>
                </v-btn>
              </template>
              <v-list>
                <v-list-item
                  v-for="(link, index) in links"
                  :key="index"
                  router
                  :to="link.route"
                >
                  <v-list-item-title>{{ link.text }}</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </div>
        </v-col>
      </v-row>
    </v-layout>
  </v-app-bar>
</template>

<script>
import Vue from "vue";

export default Vue.extend({
  name: "Toolbar",
  data: function () {
    return {
      links: [
        { text: "Home", route: "/" },
        { text: "Über uns", route: "/about" },
        { text: "Impressum", route: "/imprint" },
        { text: "Datenschutzerklärung", route: "/privacy" },
      ],
    };
  },
});
</script>

<style lang="scss">
#menu {
  margin-top: 20px;
}

#slogan {
  text-align: center;
  justify-content: center;
  align-items: center;
  display: none;
}

#sloganCol {
  visibility: hidden !important;
  display: none !important;
}

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
