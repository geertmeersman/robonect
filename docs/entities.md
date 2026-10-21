# Robonect — Entities

## Lawn Mower

| Entity | States |
| --- | --- |
| Robotic Lawn Mower | `mowing`, `charging`, `docked`, `returning`, `paused`, `error`, `off`, `detecting_status`, `lost_cable_signal`, `waiting_for_garage_door`, `offline_cannot_bind`, `unknown` |

Attributes: battery, blades quality, distance from base, operating hours, time in current status, mode, status, sub-status, next start time.

---

## Sensors

| Sensor | Description | Unit | Category |
| --- | --- | --- | --- |
| Battery | Battery charge level | % | status |
| Battery (detailed) | Charge, voltage, current, temperature, capacity | % | battery |
| Blade quality | Quality of the blades | % | status |
| Blade age | Days since last blade reset | d | status |
| Blade operating hours | Hours of blade usage | h | status |
| Distance | Distance from base | m | status |
| Mode | Current mowing mode: Auto, Manual, Home, Demo, End of day, Mowing task | — | status |
| Status | Numeric mower status code | — | status |
| Simple status | Human-readable status | — | MQTT |
| Substatus | Detailed sub-status code | — | MQTT |
| Simple substatus | Human-readable sub-status | — | MQTT |
| Time in current status | Duration in current status | min | status |
| Operating hours | Total mowing hours | h | status |
| Next start time | Timestamp of next scheduled start | timestamp | status |
| Clock | Internal mower clock | timestamp | status |
| Internal temperature | Temperature inside the mower | °C | status |
| Internal humidity | Humidity inside the mower | % | status |
| Wi-Fi signal strength | WLAN signal as percentage | % | status |
| Name | Device name | — | status |
| Serial number | Device serial number | — | version |
| Application version | Robonect firmware version | — | version |
| Last error code | Most recent error code | — | error |
| Last error message | Most recent error message | — | error |
| Current error | Active error code from status | — | status |
| Motor drive left | Left drive motor power | % | motor |
| Motor drive right | Right drive motor power | % | motor |
| Motor blades | Blade motor speed | RPM | motor |
| Wire quality | Lowest boundary wire signal quality | % | wire |
| GPS Latitude | GPS latitude coordinate | — | gps |
| GPS Longitude | GPS longitude coordinate | — | gps |
| Passage open | Garage door / passage state | — | door |
| Robonect supply voltage | Battery supply voltage | V | health |
| Mower operating voltage | External 3.3V operating voltage | V | health |
| Robonect operating voltage | Internal 3.3V operating voltage | V | health |

> **Note:** Sensors marked with a REST category only update during the non-sleeping phase of the mower (except `status`, `clock`, `door`, `ext`, `gps`, `health`, `portal`, `push`, `timer`, `wlan`). See [REST sensor and the REST category](../README.md#rest-sensor-and-the-rest-category).

---

## Binary Sensors

| Sensor | Description | Category |
| --- | --- | --- |
| Health alarm | Safety alarm triggered | health |
| Error | Active mower error | status |
| Stopped | Mower is stopped | status |
| Stopped due to weather | Weather service triggered a stop | weather |
| Weather service | Weather service enabled | weather |
| GPIO 1 | External GPIO 1 status | ext |
| GPIO 2 | External GPIO 2 status | ext |
| OUT 1 | External OUT 1 status | ext |
| OUT 2 | External OUT 2 status | ext |

---

## Buttons

| Button | Description |
| --- | --- |
| Start | Start the mower |
| Stop | Stop the mower |
| Go back home | Send mower to charging station |
| End of day | Activate end-of-day mode |
| Automatic | Switch to automatic mode |
| Manual | Switch to manual mode |
| Reboot | Reboot the Robonect module |
| Shutdown | Shut down the Robonect module |
| Sleep | Put the Robonect module to sleep |
| Reset error | Reset the current error |
| Reset blades | Reset the blade usage counter |
| Sync clock | Synchronize the mower clock with Home Assistant |

---

## Switches

| Switch | Description | Category |
| --- | --- | --- |
| Timer 1–14 | Enable/disable individual mowing timers | timer |
| GPIO 1 | Toggle external GPIO 1 output | ext |
| GPIO 2 | Toggle external GPIO 2 output | ext |
| OUT 1 | Toggle external OUT 1 output | ext |
| OUT 2 | Toggle external OUT 2 output | ext |
| Winter mode | Pause all REST polling during winter storage | config |

---

## Device Tracker

| Entity | Description |
| --- | --- |
| GPS Tracker | Real-time GPS position of the mower based on the latest MQTT or REST data |
