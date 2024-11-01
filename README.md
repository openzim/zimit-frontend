# zimit-frontend

[![CodeFactor](https://www.codefactor.io/repository/github/openzim/zimit-frontend/badge)](https://www.codefactor.io/repository/github/openzim/zimit-frontend)
[![Docker](https://ghcr-badge.egpl.dev/openzim/zimit-ui/latest_tag?label=docker)](https://ghcr.io/openzim/zimit-ui)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

This project is a UI (and its API / backend-for-frontend) allowing any user to submit
Zimit requests to a Zimfarm instance. It is NOT a standalone tool allowing to run zimit
scraper. A Zimfarm instance and associated worker(s) is required for the system to be
functional.

You can see it live at https://zimit.kiwix.org.

`zimit-frontend` adheres to openZIM's [Contribution Guidelines](https://github.com/openzim/overview/wiki/Contributing).

`zimit-frontend` has implemented openZIM's [Python bootstrap, conventions and policies](https://github.com/openzim/_python-bootstrap/blob/main/docs/Policy.md) **v1.0.3**.

## How-to

### Run the project

This project is better deployed with its [Docker image](https://ghcr.io/openzim/zimit-ui) which is ready to use (you still need to deploy Zimfarm separately).

### Contribute

You can start a development stack with most required components in the `dev` folder. See [README](./dev/README.md) there.

## Internationalization (i18n)

This project supports internationalization, including RTL languages.

Strings to translate are hosted in the `locales` folder, but it is better to direct to
TranslateWiki to translate this project.

Should you want to add a new language, the new code must be declared at following locations:

- `supportedLanguages` constant in `ui/src/i18n.ts` to declare the code, associated label in the UI and LTR/RTL direction
- `rtl_language_codes` constant in `api/src/zimitfrontend/constants.py` to declare the LTR/RTL direction
