//import { isInternalDeclaration } from 'typescript';
import { createI18n } from 'vue-i18n';

async function loadI18n() {
  
  // Detect browser language
  const simplifiedBrowserLanguage = navigator.language.split('-')[0];

  const supportedLanguages = ['en', 'fr']; // Add more supported languages here

  // Check if browser language is supported, otherwise fallback to English
  const defaultLanguage = supportedLanguages.includes(simplifiedBrowserLanguage)
    ? simplifiedBrowserLanguage
    : 'en';

  const i18n =  createI18n({
    legacy: false,
    locale: defaultLanguage, // set locale
    fallbackLocale: 'en', // set fallback locale for untranslated messages
    warnHtmlMessage: true, // we prefer to translate whole HTML blocks to ease translators work
  });

  // List of locales whose messages have been loaded
  const loadedLocales: string[] = [];

  async function setCurrentLocale(locale: string) {
    if (!loadedLocales.includes(locale)) {
      // load messages if they have not yet been loaded
      const localMessages = await import(`./locales/${locale}.json`);
      i18n.global.setLocaleMessage(locale, localMessages);
      loadedLocales.push(locale);
    }
    // set current locale
    i18n.global.locale.value = locale;
  }

  // // set locale to default language (and hence load its messages)
  // let pq = Promise.all([(async () => {await setCurrentLocale(defaultLanguage);})()]).catch(error => {

  // //let pq = Promise.all([setCurrentLocale(defaultLanguage)]).catch(error => {
  //   // TODO: do something more intelligent than simply logging something in the console
  //   console.error('Failed to load ' + defaultLanguage + ' locale:\n' + error);
  // })
  await setCurrentLocale(defaultLanguage)
  
  
  return {
    i18n: i18n,
    t: i18n.global.t,
    setCurrentLocale: setCurrentLocale
  }

}

export default loadI18n


//export const t = loadI18n().then((i18n) => i18n.t)
// await setCurrentLocale(defaultLanguage);

// export default i18n;

