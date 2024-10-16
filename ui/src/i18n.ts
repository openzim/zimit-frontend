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
export const supportedLanguages: Language[] = [
  { code: 'en', display: 'English', rtl: false }, // Keep default first in array
  { code: 'fa', display: 'Persian', rtl: true }
]

// Check if browser language is supported, otherwise fallback to English
const defaultLanguage: Language =
  supportedLanguages.find((lang) => lang.code == simplifiedBrowserLanguage) || supportedLanguages[0]

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
