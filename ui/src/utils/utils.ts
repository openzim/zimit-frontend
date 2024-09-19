import constants from '../constants'

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
