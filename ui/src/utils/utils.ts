import constants from '../constants'

/**
 * Convert the user-provided block rules (one regular expression per line) into
 * the single URL regex string expected by zimit's --blockRules option.
 *
 * Browsertrix also accepts structured rules through its YAML config, but zimit
 * only forwards a plain string to the crawler, so multiple simple rules are
 * combined here using an alternation.
 */
export const normalizeBlockRules = (value: unknown): string | undefined => {
  if (typeof value !== 'string') {
    return undefined
  }
  const rules = value
    .split(/\r?\n/)
    .map((rule) => rule.trim())
    .filter((rule) => rule !== '')
  if (rules.length === 0) {
    return undefined
  }
  if (rules.length === 1) {
    return rules[0]
  }
  return rules.map((rule) => `(?:${rule})`).join('|')
}

export const getRulesFromFieldType = (
  type: string,
  required: boolean
): Array<(value: string) => string | boolean> => {
  const rules = []
  switch (type) {
    case 'email':
      rules.push(constants.rules.email)
      break
    case 'url':
      rules.push(constants.rules.url)
      break
    case 'integer':
      rules.push(constants.rules.integer)
      break
    case 'float':
      rules.push(constants.rules.number)
      break
  }
  if (required) {
    rules.push(constants.rules.required)
  }
  return rules
}
