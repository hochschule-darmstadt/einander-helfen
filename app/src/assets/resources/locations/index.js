import { getLocale } from "@/i18n";

const locations =
  getLocale() === "de"
    ? require("./de_plz_ort_state_lat_lon_rank.csv")
    : require("./en_plz_ort_state_lat_lon_rank.csv");

export default locations;
