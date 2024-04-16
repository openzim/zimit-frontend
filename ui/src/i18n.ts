import { createI18n } from 'vue-i18n';

// Detect browser language
const simplifiedBrowserLanguage = navigator.language.split('-')[0];

const supportedLanguages = ['en', 'fr']; // Add more supported languages here

// Check if browser language is supported, otherwise fallback to English
const defaultLanguage = supportedLanguages.includes(simplifiedBrowserLanguage)
  ? simplifiedBrowserLanguage
  : 'en';

const i18n = createI18n({
  legacy: false,
  locale: defaultLanguage, // set locale
  fallbackLocale: 'en', // set fallback locale for untranslated messages
  warnHtmlMessage: false, // we prefer to translate whole HTML blocks to ease translators work
});

// List of locales whose messages have been loaded
const loadedLocales: string[] = [];

export async function setCurrentLocale(locale: string) {
  if (!loadedLocales.includes(locale)) {
    // load messages if they have not yet been loaded
    const localMessages = await import(`./locales/${locale}.json`);
    i18n.global.setLocaleMessage(locale, localMessages);
    loadedLocales.push(locale);
  }
  // set current locale
  i18n.global.locale.value = locale;
}

// set locale to default language (and hence load its messages)
await setCurrentLocale(defaultLanguage);

export default i18n;
