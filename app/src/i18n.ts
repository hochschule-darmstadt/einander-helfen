import Vue from "vue";
import VueI18n, { LocaleMessages } from "vue-i18n";

Vue.use(VueI18n);

//GLOBALE LOCALE
type RegisteredLocales = "de" | "en";
const GLOBALLOCALE: RegisteredLocales = process.env.VUE_APP_I18N_EH_LOCALE;
const FALLBACKLOCALE: RegisteredLocales = process.env.VUE_APP_I18N_EH_FALLBACK_LOCALE;
//WILL BE USED THROUGHOUT THE APP

export const getLocale = (): RegisteredLocales => {
  return GLOBALLOCALE;
};

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
  fallbackLocale: FALLBACKLOCALE,
  silentFallbackWarn: true,
  messages: loadLocaleMessages(),
});
