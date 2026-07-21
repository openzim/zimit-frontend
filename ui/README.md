# Zimit UI (Vue 3 + TypeScript + Vite)

This is the UI/frontend for Zimit.

## Download Size Limit Security

All user-submitted website downloads are strictly limited in size. The backend and offliner components enforce a hard maximum size per request (default: 4 GiB; see backend docs for `ZIMIT_SIZE_LIMIT` env var). If a download exceeds this limit, the task is stopped and the user will see a clear partial/incomplete result or error, in the interface and notification email.

You can customize how the UI communicates this to users via translations (see `locales/en.json`, FAQ, etc). For advanced options, `sizeHardLimit` can be set but the backend will always enforce the global hard maximum cap.

## Browsertrix Crawler Block Rules

The UI now includes an "Advanced Options" section where users can specify `blockRules`. These rules are passed to the backend and then to the Browsertrix Crawler to block specific URLs from being loaded during the archiving process. This feature enhances security and privacy by allowing users to prevent unwanted resources (e.g., analytics scripts, internal IPs, or tracking elements) from being included in their ZIM files.

### Usage

`blockRules` should be provided as a JSON array of objects. Each object defines a blocking rule. The UI includes helper text with an example to guide users.

**Example (blocking Google Analytics):**

```json
[
  { "url": "google-analytics\\.com", "type": "block" }
]
```
