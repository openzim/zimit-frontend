# API

This is the backend component of `zimit-frontend` which is responsible to serve the API for the frontend UI and process notification webhooks.

## Browsertrix Crawler block rules

The optional `blockRules` flag is forwarded unchanged to zimit, which passes it to
Browsertrix Crawler as the `--blockRules` option.

`--blockRules` is a crawler CLI option of type `array`, but zimit and Browsertrix
treat every CLI value as a URL regular expression. Therefore `blockRules` **must be
a string**, not a serialized JSON array or object. A JSON array is only supported by
Browsertrix when it is provided through a YAML `--config` file, which is not exposed
by zimit-frontend.

The UI lets users enter one regular expression per line and combines them into a
single alternation before submitting the request, for example:

```text
google-analytics\.com
doubleclick\.net
```

is submitted as:

```text
(?:google-analytics\.com)|(?:doubleclick\.net)
```

This makes all the simple `{"url": "<regex>", "type": "block"}` rules usable
without pretending that structured rules (`allowOnly`, `inFrameUrl`,
`frameTextMatch`, ...) are supported end-to-end.
