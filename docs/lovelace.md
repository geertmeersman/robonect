# Robonect — Lovelace Examples

## Extra sensor for daily mowing time

Add the following to your `configuration.yaml`:

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

## Extra template sensors (used for the mower card)

Add the following to your `template.yaml`:

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

---

## Mower card with buttons

![Lovelace mower card](https://raw.githubusercontent.com/geertmeersman/robonect/main/images/screenshots/lovelace_card.png)

<details><summary>Show YAML code</summary>

Required custom cards:
- [custom:button-card](https://github.com/custom-cards/button-card)
- [custom:mini-graph-card](https://github.com/kalkih/mini-graph-card)

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
