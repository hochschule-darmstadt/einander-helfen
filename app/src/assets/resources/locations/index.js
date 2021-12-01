import { Locale } from "../../../i18n";

console.log("locale is: " + Locale());

const locations =
  Locale() === "de"
    ? require("./de_plz_ort_state_lat_lon_rank.csv")
    : require("./en_plz_ort_state_lat_lon_rank.csv");

console.log("locations coming up");
console.log(locations);

export default locations;
