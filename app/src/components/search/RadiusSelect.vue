<!-- Part of the SearchComponent to limit the search by the distance of the results to the given location -->

template>
  <v-select
    class="radius_select"
    label="Umkreis"
    :items="radiiArray"
    :dark="dark"
    :disabled="disabled"
    :attach="attachTo"
    :value="radius"
    @change="onChange"
    @keydown.enter="onEnter"
  />
</template>

<script lang="ts">
import Vue from "vue";
import Radius from "@/models/radius";
import radii from "@/resources/radii";

export default Vue.extend({
  name: "RadiusSelect",
  props: {
    value: {
      type: String,
    },
    isInternational: {
      type: Boolean,
      default: true,
    },
    dark: {
      type: Boolean,
      default: false,
    },
    attachTo: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      radius: {} as Radius,
    };
  },
  watch: {
    /** change selection on value change */
    value(): void {
      this.setRadius();
    },
  },
  computed: {
    disabled(): boolean {
      return this.isInternational;
    },
    radiiArray(): Radius[] {
      return radii;
    },
  },
  mounted(): void {
    this.setRadius();
  },
  methods: {
    setRadius() {
      if (this.radius.value != this.value) {
        this.radius = this.getRadiusObject();
      }
    },
    onChange(inputValue) {
      if (this.value != inputValue) {
        this.$emit("input", inputValue);
      }
    },
    onEnter(): void {
      this.$emit("input", this.radius.value);
      this.$emit("enter");
    },
    getRadiusObject() {
      return (
        radii.find((radius: Radius) => radius.value == this.value) || radii[0]
      );
    },
  },
});
</script>

<style lang="scss" scoped>
@media (min-width: 600px) {
  .radius_select {
    width: 100px;
  }
}
</style>
