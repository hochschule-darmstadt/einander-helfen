<template>
  <div id="nav">
    <ul>
      <li>
        <router-link to="/">Home</router-link>
        <router-link to="/imprint">Impressum</router-link>
        <router-link to="/privacy">Datenschutz</router-link>
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { Vue } from 'vue-property-decorator';
import Component from 'vue-class-component';

@Component({
  components: {
  }
})
export default class Counter extends Vue {
}
</script>

<style scoped lang="scss">
#nav {
  background-color: #fff;
  width: 260px;
  padding: 100px 0 0 0;
  min-height: 100vh;
  position: fixed;
  box-shadow: 0 -5px 15px rgba(150,150,150,0.3);

  ul {
    padding: 0 20px;
    list-style: none;

    li {
      line-height: 40px;

      a {
        color: #000;
        text-decoration: none;
        display: block;
        transition: padding-left 0.2s;
        padding-left: 10px;

        &:hover {
          padding-left: 15px;
        }
        &.router-link-exact-active {
          background-color: rgba(25,118,210,0.5);
          color: #fff;
          border-radius: 3px;
        }
      }
      span {
        margin-top: 20px;
        padding-left: 10px;
        color: rgba(0,0,0,0.6);
        font-size: 0.8em;
        font-weight: bold;
        text-transform: uppercase;
      }

      ul {
        padding: 0;

        li {
          a {

          }
        }
      }
    }
  }
}
</style>
