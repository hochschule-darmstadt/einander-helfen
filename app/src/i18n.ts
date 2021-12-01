import Vue from "vue";
import VueI18n, { LocaleMessages } from "vue-i18n";

Vue.use(VueI18n);

//GLOBALE LOCALE
type RegisteredLocales = "de" | "en";
const GLOBALLOCALE: RegisteredLocales = "de";
//WILL BE USED THROUGHOUT THE APP


function loadLocaleMessages(): LocaleMessages {
  const locales = require.context(
    "./locales",
    true,
    /[A-Za-z0-9-_,\s]+\.json$/i
  );
  const messages: LocaleMessages = {};
  locales.keys().forEach((key) => {
    const matched = key.match(/([A-Za-z0-9-_]+)\./i);
    if (matched && matched.length > 1) {
      const locale = matched[1];
      messages[locale] = locales(key);
    }
  });
  return messages;
}

export default new VueI18n({
  locale: GLOBALLOCALE,
  fallbackLocale: "de",
  silentFallbackWarn: true,
  messages: loadLocaleMessages(),
});

export const getLocale = (): RegisteredLocales => {
  return GLOBALLOCALE;
};
