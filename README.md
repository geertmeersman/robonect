<img src="https://github.com/geertmeersman/robonect/raw/main/images/brand/logo.png"
     alt="Robonect"
     align="right"
     style="width: 200px;margin-right: 10px;" />

# Robonect for Home Assistant

A Home Assistant integration to monitor Robonect

## Features

- MQTT listener
- REST API client
- All Robonect sensors (if MQTT enabled priority to MQTT sensors over REST)
- Automower lawn mower entity
- Buttons (change mode, start, stop, return home, ...)
- Service calls to Robonect actions, like scheduling a job, modifying a timer

**MQTT sensors** (when enabled) are enabled prior to the REST sensors, as they update faster.

The **REST sensors**, are updated on a configurable scan interval. When the mower is sleeping, only the status sensors are being updated (since the others have no activity and updating them would wake up the mower, resulting in a beep every time a scan happens). Example here: [Rest sensor and the REST category](#rest-sensor-and-the-rest-category)

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
[![github last-commit](https://img.shields.io/github/last-commit/geertmeersman/robonect)](https://github.com/geertmeersman/robonect/commits)
[![github contributors](https://img.shields.io/github/contributors/geertmeersman/robonect)](https://github.com/geertmeersman/robonect/graphs/contributors)
[![github commit activity](https://img.shields.io/github/commit-activity/y/geertmeersman/robonect?logo=github)](https://github.com/geertmeersman/robonect/commits/main)

<!-- [END BADGES] -->

## Table of contents

- [Robonect for Home Assistant](#robonect-for-home-assistant)
  - [Features](#features)
  - [Table of contents](#table-of-contents)
  - [Installation](#installation)
    - [Using HACS (recommended)](#using-hacs-recommended)
    - [Manual](#manual)
  - [Contributions are welcome](#contributions-are-welcome)
  - [Troubleshooting](#troubleshooting)
    - [Frequently asked questions](#frequently-asked-questions)
    - [Enable debug logging](#enable-debug-logging)
    - [Disable debug logging and download logs](#disable-debug-logging-and-download-logs)
  - [Extra sensor for daily mowing time](#extra-sensor-for-daily-mowing-time)
  - [Extra sensors templates, used for lovelace card](#extra-sensors-templates-used-for-lovelace-card)
  - [Lovelace examples](#lovelace-examples)
    - [Mower card with some nice buttons](#mower-card-with-some-nice-buttons)
  - [Available Services](#available-services)
    - [Start the Mower](#start-the-mower)
    - [Stop the Mower](#stop-the-mower)
    - [Reboot the Mower](#reboot-the-mower)
    - [Shutdown the Mower](#shutdown-the-mower)
    - [Sleep Mode](#sleep-mode)
    - [Set Operation Mode](#set-operation-mode)
    - [Place a Mowing Job](#place-a-mowing-job)
    - [Modify a Timer](#modify-a-timer)
    - [Control Equipment](#control-equipment)
    - [Direct the Mower](#direct-the-mower)
  - [Screenshots](#screenshots)
    - [Integration page](#integration-page)
    - [Mowing job](#mowing-job)
    - [Timer](#timer)
    - [Config flow](#config-flow)
    - [REST sensor and the REST category](#rest-sensor-and-the-rest-category)

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
3. Add the 'robonect' integration via HA Settings > 'Devices and Services' > 'Integrations'
4. Provide your Robonect configuration details

This integration will set up the following platforms.

| Platform   | Description                           |
| ---------- | ------------------------------------- |
| `robonect` | Home Assistant component for Robonect |

## Extra sensor for daily mowing time

Define a daily mowing time sensor by adding the followinng lines to your configuration.yaml:

```yaml
sensor:
  - platform: history_stats
    name: Daily mowing time
    entity_id: sensor.automower_mower_status
    state: 2
    type: time
    start: "{{ now().replace(hour=0, minute=0, second=0) }}"
    end: "{{ now() }}"
```

## Extra sensors templates, used for lovelace card

In template.yaml, add the following:

```yaml
- sensor:
    - name: "Automower Battery Current"
      unique_id: "sensor.automower_battery_current"
      unit_of_measurement: "mA"
      state: "{{ state_attr('sensor.automower_battery_0', 'current') | replace(' mA', '') | int(0) }}"
      icon: "mdi:current-dc"
    - name: "Automower Battery Voltage"
      unique_id: "sensor.automower_battery_voltage"
      unit_of_measurement: "V"
      state: "{{ state_attr('sensor.automower_battery_0', 'voltage') | replace(' V', '') | float(0) }}"
      icon: "mdi:sine-wave"
    - name: "Automower Battery Temperature"
      unique_id: "sensor.automower_battery_temperature"
      unit_of_measurement: "°C"
      state: "{{ state_attr('sensor.automower_battery_0', 'temperature') | replace(' °C', '') | float(0) }}"
      icon: "mdi:temperature-celsius"
    - name: "Automower Battery Capacity"
      unique_id: "sensor.automower_battery_capacity"
      unit_of_measurement: "mAh"
      state: "{{ state_attr('sensor.automower_battery_0', 'capacity').remaining | replace(' mAh', '') | int(0) }}"
      icon: "mdi:battery-charging-medium"
```

## Lovelace examples

### Mower card with some nice buttons

![Lovelace mower card](https://raw.githubusercontent.com/geertmeersman/robonect/main/images/screenshots/lovelace_card.png)

<details><summary>Show markdown code</summary>

The example uses the following custom lovelace cards:

- custom:button-card: <https://github.com/custom-cards/button-card>
- custom:mini-graph-card: <https://github.com/kalkih/mini-graph-card>

```yaml
type: vertical-stack
cards:
  - card:
      content: " "
      card_mod:
        style: |
          ha-card {
            color: white;
            font-variant: small-caps;
            background-color: red;
            text-align: center
          }
      title: Automower needs help
      type: markdown
    conditions:
      - entity: sensor.automower_mower_status
        state: "7"
    type: conditional
  - type: conditional
    conditions:
      - condition: state
        entity: binary_sensor.automower_winter_mode
        state: "off"
    card:
      type: custom:stack-in-card
      mode: vertical
      keep:
        border_radius: true
      cards:
        - type: horizontal-stack
          cards:
            - entity: sensor.automower_mower_status_duration
              show_entity_picture: true
              show_name: false
              font-size: 11px
              show_state: true
              show_label: true
              styles:
                card:
                  - height: 40px
                  - padding: 5px
                  - margin-top: 10px
                  - border-top: 1px solid var(--state-icon-color)
                  - border: 0px solid var(--primary-background-color)
                  - font-size: 11px
              type: custom:button-card
            - entity: sensor.automower_mower_blades_quality
              show_entity_picture: true
              show_name: false
              font-size: 11px
              show_state: true
              show_label: true
              styles:
                card:
                  - height: 40px
                  - padding: 5px
                  - margin-top: 10px
                  - border-top: 1px solid var(--state-icon-color)
                  - border: 0px solid var(--primary-background-color)
                  - font-size: 11px
              type: custom:button-card
            - entity: binary_sensor.automower_health_alarm
              show_entity_picture: true
              show_name: false
              font-size: 11px
              show_state: true
              show_label: true
              styles:
                card:
                  - height: 40px
                  - padding: 5px
                  - margin-top: 10px
                  - border-top: 1px solid var(--state-icon-color)
                  - border: 0px solid var(--primary-background-color)
                  - font-size: 11px
              type: custom:button-card
            - entity: sensor.automower_mower_distance
              show_entity_picture: true
              show_name: false
              font-size: 11px
              show_state: true
              show_label: true
              styles:
                card:
                  - height: 40px
                  - padding: 5px
                  - margin-top: 10px
                  - border-top: 1px solid var(--state-icon-color)
                  - border: 0px solid var(--primary-background-color)
                  - font-size: 11px
              type: custom:button-card
            - entity: sensor.automower_mower_battery_charge
              show_entity_picture: true
              show_name: false
              font-size: 11px
              show_state: true
              show_label: true
              styles:
                card:
                  - height: 40px
                  - padding: 5px
                  - margin-top: 10px
                  - border-top: 1px solid var(--state-icon-color)
                  - border: 0px solid var(--primary-background-color)
                  - font-size: 11px
              type: custom:button-card
            - entity: sensor.automower_wlan_rssi
              show_entity_picture: true
              show_name: false
              font-size: 11px
              show_state: true
              show_label: true
              styles:
                card:
                  - height: 40px
                  - padding: 5px
                  - margin-top: 10px
                  - border-top: 1px solid var(--state-icon-color)
                  - border: 0px solid var(--primary-background-color)
                  - font-size: 11px
              type: custom:button-card
            - entity: sensor.automower_health_climate_temperature
              show_entity_picture: true
              show_name: false
              font-size: 11px
              show_state: true
              show_label: true
              styles:
                card:
                  - height: 40px
                  - padding: 5px
                  - margin-top: 10px
                  - border-top: 1px solid var(--state-icon-color)
                  - border: 0px solid var(--primary-background-color)
                  - font-size: 11px
              type: custom:button-card
            - entity: sensor.automower_health_climate_humidity
              show_entity_picture: true
              show_name: false
              font-size: 11px
              show_state: true
              show_label: true
              styles:
                card:
                  - height: 40px
                  - padding: 5px
                  - margin-top: 10px
                  - border-top: 1px solid var(--state-icon-color)
                  - border: 0px solid var(--primary-background-color)
                  - font-size: 11px
              type: custom:button-card
        - type: conditional
          conditions:
            - entity: binary_sensor.automower_mower_stopped
              state: "on"
          card:
            show_name: false
            label: Automower is currently stopped.<br> Click here to start.
            show_label: true
            show_icon: true
            layout: icon_label
            type: custom:button-card
            tap_action:
              action: call-service
              service: button.press
              service_data:
                entity_id: button.automower_start
            entity: button.automower_start
            styles:
              icon:
                - height: 30px
              card:
                - border: 0px solid var(--primary-background-color)
                - background: var(--warning-color)
                - font-size: 11px
                - border-radius: 10px
                - "--keep-background": "true"
        - type: conditional
          conditions:
            - entity: sensor.automower_mower_timer_next_unix
              state_not: unknown
          card:
            type: markdown
            content: >
              {% set time = states.sensor.automower_mower_timer_next_unix.state|as_datetime %}
              {% if time is not none %}
                  {% set day = as_timestamp(time)|timestamp_custom('%d', true)|int %}
                  {% set weekday = as_timestamp(time)|timestamp_custom('%w', true)|int %}
                  {% set month = as_timestamp(time)|timestamp_custom('%m', true)|int -1 %}
                  {% set weekday = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"][weekday] %}
                  {% set month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"][month] %}
                  Next start scheduled on {{weekday}} {{day}} {{month}} at {{ as_timestamp(time)|timestamp_custom('%H:%M', true) }}
              {% else %}
                  No scheduled start time available.
              {% endif %}
            card_mod:
              style: |
                ha-card {
                  border-width: 0;
                  text-align: center;
                }
        - type: conditional
          conditions:
            - entity: binary_sensor.automower_weather_data_break
              state: "on"
          card:
            type: markdown
            content: >
              {% set data = {'toorainy': 'teveel regen', 'toocold': 'te koud',
              'toowarm': 'te warm', 'toodry': 'te droog', 'toowet': 'te nat',
              'day': 'overdag', 'night': '\'s nachts'} -%} Botje is gestopt
              omwille van het weer: {% for condition,value in
              state_attr('binary_sensor.automower_weather_service',
              'weather').condition.items() -%} {% if value -%}
              {{data[condition]}} {% endif -%} {% endfor -%}
            card_mod:
              style: |
                ha-card {
                  border-width: 0;
                  text-align: center;
                }
        - type: tile
          entity: lawn_mower.automower_robonect
          show_entity_picture: true
          vertical: true
          features:
            - type: lawn-mower-commands
              commands:
                - start_pause
                - dock
          card_mod:
            style: |
              ha-card {
                border-width: 0;
              }
        - type: horizontal-stack
          style: |
            ha-card {
              margin-left: 10px;
            }
          cards:
            - show_name: false
              show_icon: true
              type: custom:button-card
              tap_action:
                action: call-service
                service: button.press
                service_data:
                  entity_id: button.automower_auto
              entity: button.automower_auto
              styles:
                card:
                  - height: 40px
                  - border: 0px solid var(--primary-background-color)
                  - background: |
                      [[[
                        if (states['sensor.automower_mower_mode'].state == '0' )
                          return 'var(--state-vacuum-17-color, var(--state-vacuum-active-color, var(--state-active-color)))'
                        return ''
                      ]]]
                  - font-size: 11px
                  - border-radius: 10px
                  - "--keep-background": "true"
            - show_name: false
              show_icon: true
              type: custom:button-card
              entity: button.automower_man
              tap_action:
                action: call-service
                service: button.press
                service_data:
                  entity_id: button.automower_man
              styles:
                card:
                  - height: 40px
                  - border: 0px solid var(--primary-background-color)
                  - background: |
                      [[[
                        if (states['sensor.automower_mower_mode'].state == '1' )
                          return 'var(--state-vacuum-17-color, var(--state-vacuum-active-color, var(--state-active-color)))'
                        return ''
                      ]]]
                  - font-size: 11px
                  - "--keep-background": "true"
            - show_name: false
              show_icon: true
              type: custom:button-card
              tap_action:
                action: call-service
                service: button.press
                service_data:
                  entity_id: button.automower_eod
              entity: button.automower_eod
              styles:
                card:
                  - height: 40px
                  - border: 0px solid var(--primary-background-color)
                  - background: |
                      [[[
                        if (states['sensor.automower_mower_mode'].state == '2' )
                          return 'var(--state-vacuum-17-color, var(--state-vacuum-active-color, var(--state-active-color)))'
                        return ''
                      ]]]
                  - font-size: 11px
                  - "--keep-background": "true"
        - type: horizontal-stack
          cards:
            - type: gauge
              entity: sensor.automower_battery_current
              needle: true
              min: -1500
              max: 1500
              segments:
                - from: -1500
                  color: var(--info-color)
                - from: 0
                  color: var(--success-color)
              name: Stroom
              card_mod:
                style: |
                  ha-card {
                    border-width: 0;
                    border-radius: 0
                  }
            - type: gauge
              entity: sensor.automower_battery_voltage
              needle: true
              min: 0
              max: 30
              segments:
                - from: 0
                  color: var(--error-color)
                - from: 17.2
                  color: var(--warning-color)
                - from: 19.3
                  color: var(--success-color)
              name: Spanning
              card_mod:
                style: |
                  ha-card {
                    border-width: 0;
                    border-radius: 0
                  }
            - type: gauge
              entity: sensor.automower_battery_capacity
              needle: true
              min: 0
              max: 1600
              segments:
                - from: 0
                  color: var(--error-color)
                - from: 200
                  color: var(--warning-color)
                - from: 800
                  color: var(--success-color)
              name: Capaciteit
              card_mod:
                style: |
                  ha-card {
                    border-width: 0;
                    border-radius: 0
                  }
            - type: gauge
              entity: sensor.automower_battery_temperature
              needle: true
              min: -10
              max: 50
              segments:
                - from: -10
                  color: var(--error-color)
                - from: 0
                  color: var(--warning-color)
                - from: 10
                  color: var(--success-color)
                - from: 30
                  color: var(--warning-color)
              name: Temp
              card_mod:
                style: |
                  ha-card {
                    border-width: 0;
                    border-radius: 0
                  }
  - type: conditional
    conditions:
      - condition: state
        entity: binary_sensor.automower_winter_mode
        state: "on"
    card:
      show_name: true
      show_icon: true
      type: button
      tap_action:
        action: more-info
      entity: binary_sensor.automower_winter_mode
      name: Wintermode
      hold_action:
        action: none
  - type: conditional
    conditions:
      - condition: state
        entity: binary_sensor.automower_winter_mode
        state: "off"
    card:
      aggregate_func: max
      entities:
        - entity: sensor.daily_mowing_time
      group_by: date
      hour24: true
      hours_to_show: 360
      line_color: green
      name: Dagelijkse maaitijd
      show:
        graph: bar
        icon: false
      type: custom:mini-graph-card
```

</details>

## Available Services

### Start the Mower

- **Name**: `start`
- **Description**: Starts the Robonect mower.

### Stop the Mower

- **Name**: `stop`
- **Description**: Stops the Robonect mower.

### Reboot the Mower

- **Name**: `reboot`
- **Description**: Reboots the Robonect mower.

### Shutdown the Mower

- **Name**: `shutdown`
- **Description**: Shuts the Robonect mower down.

### Sleep Mode

- **Name**: `sleep`
- **Description**: Sets the Robonect mower to sleep mode.

### Set Operation Mode

- **Name**: `operation_mode`
- **Description**: Sets the operation mode of the Robonect mower.
  - **Fields**:
    - `mode`: Operation mode of the mower.
      - **Example**: `"eod"`
      - **Default**: `"auto"`
      - **Options**:
        - `"man"`
        - `"auto"`
        - `"eod"`
        - `"home"`

### Place a Mowing Job

- **Name**: `job`
- **Description**: The mower performs a mowing job.
  - **Fields**:
    - `entity_id`: The entity ID of the Robonect mower.
      - **Example**: `lawn_mower.automower_robonect`
    - `start`: Start time in 'hh:mm'. If omitted, the job starts immediately.
      - **Example**: `"10:00"`
    - `end`: End time in 'hh:mm'.
      - **Example**: `"13:00"`
    - `duration`: Duration of the job in minutes. Omitted if the end is set.
      - **Example**: `145`
      - **Min**: `1`
      - **Max**: `10080`
    - `after`: Mode activated after the job is done.
      - **Example**: `"Auto"`
      - **Default**: `"Auto"`
      - **Options**:
        - `"Auto"`
        - `"Home"`
        - `"End of day"`
    - `corridor`: Corridor width. Defaults to "Normal" if omitted.
      - **Example**: `"Normal"`
      - **Options**:
        - `"Normal"`
        - `"0"` to `"9"`
    - `remotestart`: Remote mowing starting point.
      - **Default**: `"Normal"`
      - **Options**:
        - `"Normal"`
        - `"From charging station"`
        - `"Remote start 1"` to `"Remote start 5"`

### Modify a Timer

- **Name**: `timer`
- **Description**: Modify a Robonect timer.
  - **Fields**:
    - `entity_id`: The entity ID of the Robonect mower.
      - **Example**: `lawn_mower.automower_robonect`
    - `timer`: Timer ID.
      - **Example**: `"1"`
      - **Default**: `"1"`
      - **Options**: `"1"` to `"14"`
    - `enable`: Enable or disable the timer.
    - `start`: Start time in 'hh:mm'.
      - **Example**: `"10:00"`
    - `end`: End time in 'hh:mm'.
      - **Example**: `"13:00"`
    - `weekdays`: Select the weekdays for the timer.
      - **Options**:
        - `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday`, `Saturday`, `Sunday`

### Control Equipment

- **Name**: `ext`
- **Description**: Control GPIO or OUT channels, set modes, handle errors, and signal inversion.
  - **Fields**:
    - `entity_id`: The entity ID of the Robonect mower.
      - **Example**: `lawn_mower.automower_robonect`
    - `ext`: External equipment selection.
      - **Options**:
        - `GPIO1`, `GPIO2`, `OUT1`, `OUT2`
    - `gpioout`: Select the GPIO channel mode.
      - **Options**:
        - `[IN] Analog`, `[IN] Floating`, `[IN] PullDown`, `[IN] PullUp`, `[OUT] OpenDrain`, `[OUT] PushPull`
    - `gpiomode`: Select the mode for GPIO/OUT operation.
      - **Options**:
        - `Off`, `On`, `Night (19-7 o'clock)`, `Drive`, `Night drive (19-7 o'clock)`, `Searching/Way home`, `Park position`, `Brake light`, `Left Turn Signal`, `Right Turn Signal`, `API`
    - `gpioerr`: Checkbox to flash on fault.
    - `gpioinv`: Checkbox to set Low-activ signal.

### Direct the Mower

- **Name**: `direct`
- **Description**: Direct a Robonect mower by setting the speed percentage for each wheel and duration.
  - **Fields**:
    - `entity_id`: The entity ID of the Robonect mower.
      - **Example**: `lawn_mower.automower_robonect`
    - `left`: The speed percentage of the left wheel. Positive or negative.
      - **Example**: `50%`
    - `right`: The speed percentage of the right wheel. Positive or negative.
      - **Example**: `50%`
    - `timeout`: The timeout/duration in milliseconds.
      - **Example**: `3000 ms`

## Blueprints

### Syncing Robonect Time

Automatically press a Robonect clock sync button at a specific time each day to keep your mower’s internal clock accurate and aligned with Home Assistant time.

This blueprint allows you to configure the target button entity (e.g. button.automower_sync_clock) and choose the time of day when synchronization should occur.

The options that are sent are to sync automatically over the Internet with automatic summer/winter time adjustment active.

It’s a simple, reliable way to ensure your mower’s schedule and time-based automations stay precise — no manual syncing required. 🌱🕓

[![Import the blueprint.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fgeertmeersman%2Frobonect%2Fblob%2Fmain%2Fblueprints%2Fsync_robonect_time.yaml)

## Screenshots

### Integration page

![Integration device](https://raw.githubusercontent.com/geertmeersman/robonect/main/images/screenshots/integration_device.png)

![Diagnostic](https://raw.githubusercontent.com/geertmeersman/robonect/main/images/screenshots/diagnostic_1.png)
![Diagnostic](https://raw.githubusercontent.com/geertmeersman/robonect/main/images/screenshots/diagnostic_2.png)
![Diagnostic](https://raw.githubusercontent.com/geertmeersman/robonect/main/images/screenshots/diagnostic_3.png)

### Mowing job

![Mowing job](https://raw.githubusercontent.com/geertmeersman/robonect/main/images/screenshots/mowing_job.png)

### Timer

![Timer](https://raw.githubusercontent.com/geertmeersman/robonect/main/images/screenshots/timer.png)

### Config flow

![config_flow_1](https://raw.githubusercontent.com/geertmeersman/robonect/main/images/screenshots/config_flow_1.png)
![config_flow_1](https://raw.githubusercontent.com/geertmeersman/robonect/main/images/screenshots/config_flow_2.png)

**Options**

![options_1](https://raw.githubusercontent.com/geertmeersman/robonect/main/images/screenshots/options_1.png)
![options_2](https://raw.githubusercontent.com/geertmeersman/robonect/main/images/screenshots/options_2.png)
![options_3](https://raw.githubusercontent.com/geertmeersman/robonect/main/images/screenshots/options_3.png)
![options_4](https://raw.githubusercontent.com/geertmeersman/robonect/main/images/screenshots/options_4.png)
![options_5](https://raw.githubusercontent.com/geertmeersman/robonect/main/images/screenshots/options_5.png)
![options_6](https://raw.githubusercontent.com/geertmeersman/robonect/main/images/screenshots/options_6.png)
![options_7](https://raw.githubusercontent.com/geertmeersman/robonect/main/images/screenshots/options_7.png)

### REST sensor and the REST category

Note: if the sensor is a REST sensor and the category does not equal 'status', the sensor will only be updated during the non-sleeping phase of the mower

![rest_category](https://raw.githubusercontent.com/geertmeersman/robonect/main/images/screenshots/rest_category.png)

## Contributions are welcome

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

## Troubleshooting

[![discord](http://invidget.switchblade.xyz/wZHsA4aGvS)](https://discord.gg/wZHsA4aGvS)

### Frequently asked questions

- I am missing a lot of sensors: please check that the MQTT topic you have entered in the HA config flow equals the MQTT topic in Robonect
- If you would be expecting specific sensors and you don't see them, make sure your Robonect firmware is up to date.

### Enable debug logging

To enable debug logging, go to Settings -> Devices & Services and then click the triple dots for the Robonect integration and click Enable Debug Logging.

![enable-debug-logging](https://raw.githubusercontent.com/geertmeersman/robonect/main/images/screenshots/enable-debug-logging.gif)

### Disable debug logging and download logs

Once you enable debug logging, you ideally need to make the error happen. Run your automation, change up your device or whatever was giving you an error and then come back and disable Debug Logging. Disabling debug logging is the same as enabling, but now you will see Disable Debug Logging. After you disable debug logging, it will automatically prompt you to download your log file. Please provide this logfile.

![disable-debug-logging](https://raw.githubusercontent.com/geertmeersman/robonect/main/images/screenshots/disable-debug-logging.gif)
