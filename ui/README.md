# Zimit UI (Vue 3 + TypeScript + Vite)

This is the UI/frontend for Zimit.

## Recommended Setup

- [VS Code](https://code.visualstudio.com/) + [Vue - Official](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (previously Volar) and disable Vetur

- Use [vue-tsc](https://github.com/vuejs/language-tools/tree/master/packages/tsc) for performing the same type checking from the command line, or for generating d.ts files for SFCs.

## Browsertrix Crawler block rules

The advanced options contain a **Block Rules** textarea. Enter one URL regular
expression per line; the UI validates each expression and combines them into a
single alternation before sending the request to the API.

For example, the following input:

```text
google-analytics\.com
doubleclick\.net
```

is sent as the `blockRules` flag with value:

```text
(?:google-analytics\.com)|(?:doubleclick\.net)
```

`blockRules` is a string because zimit forwards it to Browsertrix Crawler as a
single `--blockRules` CLI value, and the crawler interprets that value as a URL
regex. Do not enter a JSON array/object: structured block rules are only supported
by Browsertrix through its YAML config, which is not exposed by zimit-frontend.
