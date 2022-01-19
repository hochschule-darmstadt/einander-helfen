import { getLocale } from "@/i18n";

const tags =
  getLocale() === "de"
    ? require("./de-Tags-einander-helfen.csv")
    : require("./us-Tags-einander-helfen.csv");

export default tags;
