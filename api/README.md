# API

This is the backend component of `zimit-frontend` which is responsible to serve the API for the frontend UI and process notification webhooks.

## Download Size Limiting (Security)

Downloads of user-provided URLs are strictly limited in size for security and infrastructure protection. Both a soft and hard cap are enforced:

- The backend enforces a `sizeHardLimit` on every user-initiated download task, with the limit set by the environment variable `ZIMIT_SIZE_LIMIT` (defaults to 4 GiB unless configured otherwise).
- The offliner/crawler job receives BOTH `sizeSoftLimit` and `sizeHardLimit` so it must stop the download immediately as the cap is hit, not just after the file is written.

If the offliner attempts to download more than this hard cap, the process is aborted and an error/partial result will be reported in the backend, frontend, and notification email.

### Configuration

You can customize the hard limit via environment variable for the backend API:

```
ZIMIT_SIZE_LIMIT=<bytes>  # defaults to 4294967296 (4 GiB)
```

## Browsertrix Crawler Block Rules

The UI allows users to specify `block_rules` as an advanced option. These rules are passed directly to the Browsertrix Crawler to control which URLs are blocked from being loaded during the crawl. This helps mitigate security and privacy risks by preventing the loading of unwanted resources (e.g., analytics scripts, internal IP addresses, or metadata endpoints).

### Usage

The `block_rules` should be provided as a JSON array of objects, conforming to the Browsertrix Crawler's `--blockRules` option format. Each object in the array defines a rule with properties like `url` (a regex to match the URL), `type` (`block` or `allowOnly`), `inFrameUrl`, and `frameTextMatch`.

**Example:**

```json
[
  { "url": "google-analytics\\.com", "type": "block" },
  { "url": "internal\\.ip", "type": "block" }
]
```

---
See https://github.com/openzim/zimit-frontend/issues/67 for background.
