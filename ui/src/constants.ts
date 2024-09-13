import type { InjectionKey } from 'vue'
import type { Config } from './config'

export default {
  not_set_magic_value: 'Not set',
  config: Symbol() as InjectionKey<Config>,
  rules: {
    required: (value: string) => !!value || 'Required.',
    email: (value: string) => !value || /.+@.+\..+/.test(value) || 'E-mail must be valid.',
    number: (value: string) => !value || !isNaN(Number(value)) || 'Must be a number.',
    url: (value: string) =>
      !value ||
      value.startsWith('http://') ||
      value.startsWith('https://') ||
      'Must be an HTTP(S) URL',
    integer: (value: string) =>
      !value || Number.isInteger(Number(value)) || 'Must be an integer value'
  }
}
