<img src="https://github.com/geertmeersman/robonect/raw/main/images/brand/logo.png"
     alt="Robonect"
     align="right"
     style="width: 200px;margin-right: 10px;" />

# Robonect for Home Assistant

A Home Assistant integration to monitor and control your Robonect-equipped robotic lawn mower via MQTT and/or REST API.

**MQTT sensors** (when enabled) take priority over REST sensors, as they update faster.

**REST sensors** update on a configurable scan interval. When the mower is sleeping, only `status`-category sensors are updated to avoid waking the mower on every scan.

---

<!-- [START BADGES] -->
<!-- Please keep comment here to allow auto update -->

[![maintainer](https://img.shields.io/badge/maintainer-Geert%20Meersman-green?style=for-the-badge&logo=github)](https://github.com/geertmeersman)
[![buyme_coffee](https://img.shields.io/badge/Buy%20me%20an%20Omer-donate-yellow?style=for-the-badge&logo=buymeacoffee)](https://www.buymeacoffee.com/geertmeersman)
[![discord](https://img.shields.io/discord/1104706338111627385?style=for-the-badge&logo=discord)](https://discord.gg/wZHsA4aGvS)

[![discord](http://invidget.switchblade.xyz/wZHsA4aGvS)](https://discord.gg/wZHsA4aGvS)

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
[![Downloads (latest release)](https://img.shields.io/github/downloads/geertmeersman/robonect/latest/total)](https://github.com/geertmeersman/robonect/releases/latest)
[![github last-commit](https://img.shields.io/github/last-commit/geertmeersman/robonect)](https://github.com/geertmeersman/robonect/commits)
[![github contributors](https://img.shields.io/github/contributors/geertmeersman/robonect)](https://github.com/geertmeersman/robonect/graphs/contributors)
[![github commit activity](https://img.shields.io/github/commit-activity/y/geertmeersman/robonect?logo=github)](https://github.com/geertmeersman/robonect/commits/main)

<!-- [END BADGES] -->

## Features

| Platform | Entities |
| --- | --- |
| `lawn_mower` | Robotic Lawn Mower with full state, attributes and commands |
| `sensor` | Battery, blades, status, mode, distance, temperature, humidity, Wi-Fi, motors, GPS, timers, errors, versions, ... |
| `binary_sensor` | Health alarm, error, stopped, weather break, GPIO/OUT states |
| `button` | Start, Stop, Home, End of day, Auto, Manual, Reboot, Shutdown, Sleep, Reset error, Reset blades, Sync clock |
| `switch` | Timers 1–14, GPIO/OUT channels, Winter mode |
| `device_tracker` | GPS position of the mower |

- → Full entity reference: [docs/entities.md](docs/entities.md)
- → Available services: [docs/services.md](docs/services.md)
- → Lovelace examples: [docs/lovelace.md](docs/lovelace.md)
- → Blueprints: [docs/blueprints.md](docs/blueprints.md)
- → Troubleshooting: [docs/troubleshooting.md](docs/troubleshooting.md)
- → Screenshots: [docs/screenshots.md](docs/screenshots.md)

## Installation

### Using [HACS](https://hacs.xyz/) (recommended)

**Click on this button:**

[![Open your Home Assistant instance and open the repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg?style=flat-square)](https://my.home-assistant.io/redirect/hacs_repository/?owner=geertmeersman&repository=robonect&category=integration)

**or follow these steps:**

1. Simply search for `Robonect` in HACS and install it easily.
2. Restart Home Assistant
3. Add the 'Robonect' integration via HA Settings > 'Devices and Services' > 'Integrations'
4. Provide your Robonect configuration details

### Manual

1. Copy the `custom_components/robonect` directory of this repository as `config/custom_components/robonect` in your Home Assistant installation.
2. Restart Home Assistant
3. Add the 'Robonect' integration via HA Settings > 'Devices and Services' > 'Integrations'
4. Provide your Robonect configuration details

| Platform         | Description                                                                 |
| ---------------- | --------------------------------------------------------------------------- |
| `lawn_mower`     | Lawn mower entity with state, commands and attributes                       |
| `sensor`         | All Robonect sensors (MQTT takes priority over REST when both are enabled)  |
| `binary_sensor`  | Health, error, weather and GPIO/OUT binary sensors                          |
| `button`         | Control buttons (start, stop, modes, reboot, reset, ...)                   |
| `switch`         | Timer switches, GPIO/OUT switches, winter mode                              |
| `device_tracker` | GPS location tracker                                                        |

## Contributions are welcome

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

## Troubleshooting

[![discord](http://invidget.switchblade.xyz/wZHsA4aGvS)](https://discord.gg/wZHsA4aGvS)

→ Full troubleshooting guide: [docs/troubleshooting.md](docs/troubleshooting.md)

## Screenshots

→ Screenshots: [docs/screenshots.md](docs/screenshots.md)

## License

[MIT](LICENSE) © [Geert Meersman](https://github.com/geertmeersman)
