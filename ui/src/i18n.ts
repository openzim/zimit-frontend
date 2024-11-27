//import { isInternalDeclaration } from 'typescript';
import type { PiniaPluginContext } from 'pinia'
import { createI18n, type ComposerTranslation } from 'vue-i18n'

// Detect browser language
const simplifiedBrowserLanguage = navigator.language.split('-')[0]

export type Language = {
  code: string
  display: string
  rtl: boolean
}

// Vite-specific instruction to load locales from outside the `ui` folder and
// still bundle them in the application and still be able to lazy-import them
// when needed
const localesFiles = import.meta.glob('../../locales/*.json')

// Add more supported languages here
// Do not mind about ordering, it is done in UI
// If language is RTL, do not forget to also update `rtl_language_codes` constant in `api/src/zimitfrontend/constants.py`
// Some languages below are commented out because they have started but not yet completed (we target close to 100% translated before using the translation)
// You can check this at https://translatewiki.net/w/i.php?title=Special:MessageGroupStats/kiwix-zimit-frontend&suppresscomplete=0#sortable:3=desc
// Display name must be in native language. Display name must start with an upper-character.
// It should be provided by the translator under `language` key. If not, you might source proper values from https://w.wiki/C7AQ since Translate Wiki uses IETF codes
export const supportedLanguages: Language[] = [
  { code: 'en', display: 'English', rtl: false },
  { code: 'es', display: 'Español', rtl: false },
  { code: 'fa', display: 'فارسی', rtl: true },
  { code: 'fr', display: 'Français', rtl: false },
  { code: 'id', display: 'Bahasa Indonesia', rtl: false },
  //  { code: 'ko', display: '한국어', rtl: false },
  //  { code: 'lb', display: 'Lëtzebuergesch', rtl: false },
  //  { code: 'mk', display: 'македонски', rtl: false }
  //  { code: 'sq', display: 'shqip', rtl: false },
  { code: 'zh-hans', display: '简体中文', rtl: false }
]

// Check if browser language is supported, otherwise fallback to English
const defaultLanguage: Language =
  supportedLanguages.find((lang) => lang.code == simplifiedBrowserLanguage) ||
  supportedLanguages.find((lang) => lang.code == 'en') ||
  supportedLanguages[0]

// Create the i18n system
const i18n = createI18n({
  legacy: false,
  locale: defaultLanguage.code, // set locale
  fallbackLocale: 'en', // set fallback locale for untranslated messages
  warnHtmlMessage: true // we prefer to translate whole HTML blocks to ease translators work
})

// List of locales whose messages have been loaded
const loadedLocales: string[] = []

// Helper function to change the locale
export async function setCurrentLocale(locale: Language) {
  if (!loadedLocales.includes(locale.code)) {
    // load messages if they have not yet been loaded
    const localeMessages = await localesFiles[`../../locales/${locale.code}.json`]()
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-expect-error
    i18n.global.setLocaleMessage(locale.code, localeMessages)
    loadedLocales.push(locale.code)
  }
  // set current locale
  //i18n.locale = locale.code
  i18n.global.locale.value = locale.code
  // change document direction
  document.documentElement.setAttribute('dir', locale.rtl ? 'rtl' : 'ltr')
}

export function getCurrentLocale() {
  return i18n.global.locale.value
}

async function loadI18n() {
  await setCurrentLocale(defaultLanguage)
  return i18n
}

// pinia declaration of additional property
declare module 'pinia' {
  export interface PiniaCustomProperties {
    t: ComposerTranslation
  }
}

// definition of pinia plugin
export function i18nPlugin({ store }: PiniaPluginContext) {
  store.t = i18n.global.t
}

export default loadI18n
