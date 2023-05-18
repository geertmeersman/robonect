<img src="https://github.com/geertmeersman/robonect/raw/main/images/brand/logo.png"
     alt="Robonect"
     align="right"
     style="width: 200px;margin-right: 10px;" />

# Robonect for Home Assistant

A Home Assistant integration to monitor Robonect

### Features

- All possible Robonect sensors
- Service calls to Robonect actions

---

<!-- [START BADGES] -->
<!-- Please keep comment here to allow auto update -->

[![maintainer](https://img.shields.io/badge/maintainer-Geert%20Meersman-green?style=for-the-badge&logo=github)](https://github.com/geertmeersman)
[![buyme_coffee](https://img.shields.io/badge/Buy%20me%20a%20Duvel-donate-yellow?style=for-the-badge&logo=buymeacoffee)](https://www.buymeacoffee.com/geertmeersman)
[![discord](https://img.shields.io/discord/1094198226493636638?style=for-the-badge&logo=discord)](https://discord.gg/f6qxuMA4)

[![MIT License](https://img.shields.io/github/license/geertmeersman/robonect?style=flat-square)](https://github.com/geertmeersman/robonect/blob/master/LICENSE)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=flat-square)](https://github.com/hacs/integration)

[![Open your Home Assistant instance and open the repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg?style=flat-square)](https://my.home-assistant.io/redirect/hacs_repository/?owner=geertmeersman&repository=robonect&category=integration)

[![GitHub issues](https://img.shields.io/github/issues/geertmeersman/robonect)](https://github.com/geertmeersman/robonect/issues)
[![Average time to resolve an issue](http://isitmaintained.com/badge/resolution/geertmeersman/robonect.svg)](http://isitmaintained.com/project/geertmeersman/robonect)
[![Percentage of issues still open](http://isitmaintained.com/badge/open/geertmeersman/robonect.svg)](http://isitmaintained.com/project/geertmeersman/robonect)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)](https://github.com/geertmeersman/robonect/pulls)

[![Hacs and Hassfest validation](https://github.com/geertmeersman/robonect/actions/workflows/validate.yml/badge.svg)](https://github.com/geertmeersman/robonect/actions/workflows/validate.yml)
[![Python](https://img.shields.io/badge/Python-FFD43B?logo=python)](https://github.com/geertmeersman/robonect/search?l=python)

[![manifest version](https://img.shields.io/github/manifest-json/v/geertmeersman/robonect/master?filename=custom_components%2Frobonect%2Fmanifest.json)](https://github.com/geertmeersman/robonect)
[![github release](https://img.shields.io/github/v/release/geertmeersman/robonect?logo=github)](https://github.com/geertmeersman/robonect/releases)
[![github release date](https://img.shields.io/github/release-date/geertmeersman/robonect)](https://github.com/geertmeersman/robonect/releases)
[![github last-commit](https://img.shields.io/github/last-commit/geertmeersman/robonect)](https://github.com/geertmeersman/robonect/commits)
[![github contributors](https://img.shields.io/github/contributors/geertmeersman/robonect)](https://github.com/geertmeersman/robonect/graphs/contributors)
[![github commit activity](https://img.shields.io/github/commit-activity/y/geertmeersman/robonect?logo=github)](https://github.com/geertmeersman/robonect/commits/main)

<!-- [END BADGES] -->

## Installation

The Pull request is still pending merge for the hacs-default repository. So until that time, add my repository as a custom repository in hacs and the integration will show up.

Explanation: https://hacs.xyz/docs/faq/custom_repositories/

```
Repository: geertmeersman/robonect
Category: Integration
```

### Using [HACS](https://hacs.xyz/) (recommended)

1. Simply search for `Robonect` in HACS and install it easily.
2. Restart Home Assistant
3. Add the 'Robonect' integration via HA Settings > 'Devices and Services' > 'Integrations'
4. Provide your Robonect username and password

### Manual

1. Copy the `custom_components/robonect` directory of this repository as `config/custom_components/robonect` in your Home Assistant instalation.
2. Restart Home Assistant
3. Add the 'robonect' integration via HA Settings > 'Devices and Services' > 'Integrations'
4. Provide your robonect username and password

This integration will set up the following platforms.

| Platform   | Description                                       |
| ---------- | ------------------------------------------------- |
| `robonect` | Home Assistant component for Robonect             |

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

## Troubleshooting

1. You can enable logging for this integration specifically and share your logs, so I can have a deep dive investigation. To enable logging, update your `configuration.yaml` like this, we can get more information in Configuration -> Logs page

```
logger:
  default: warning
  logs:
    custom_components.robonect: debug
```

## Screenshots
