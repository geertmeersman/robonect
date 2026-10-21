# Robonect — Services

## start

Starts the mower.

```yaml
service: robonect.start
target:
  entity_id: lawn_mower.automower_robonect
```

---

## stop

Stops the mower.

```yaml
service: robonect.stop
target:
  entity_id: lawn_mower.automower_robonect
```

---

## reboot

Reboots the Robonect module.

```yaml
service: robonect.reboot
target:
  entity_id: lawn_mower.automower_robonect
```

---

## shutdown

Shuts down the Robonect module.

```yaml
service: robonect.shutdown
target:
  entity_id: lawn_mower.automower_robonect
```

---

## sleep

Puts the Robonect module to sleep.

```yaml
service: robonect.sleep
target:
  entity_id: lawn_mower.automower_robonect
```

---

## operation_mode

Sets the operation mode of the mower.

| Field | Required | Options | Default |
| --- | --- | --- | --- |
| `mode` | yes | `auto`, `man`, `eod`, `home` | `auto` |

```yaml
service: robonect.operation_mode
data:
  mode: auto
```

---

## job

Places a one-off mowing job.

| Field | Required | Description | Example |
| --- | --- | --- | --- |
| `entity_id` | yes | Lawn mower entity | `lawn_mower.automower_robonect` |
| `start` | no | Start time `hh:mm` (omit to start immediately) | `10:00` |
| `end` | no | End time `hh:mm` | `13:00` |
| `duration` | no | Duration in minutes (ignored if `end` is set) | `145` |
| `after` | no | Mode after job: `Auto`, `Home`, `End of day` | `Auto` |
| `remotestart` | no | Starting point: `Normal`, `From charging station`, `Remote start 1–5` | `Normal` |
| `corridor` | no | Corridor width: `Normal`, `0`–`9` | `Normal` |

```yaml
service: robonect.job
data:
  entity_id: lawn_mower.automower_robonect
  start: "10:00"
  end: "13:00"
  after: Auto
  remotestart: Normal
```

---

## timer

Modifies a mowing timer (1–14).

| Field | Required | Description | Example |
| --- | --- | --- | --- |
| `entity_id` | yes | Lawn mower entity | `lawn_mower.automower_robonect` |
| `timer` | yes | Timer ID `1`–`14` | `1` |
| `enable` | yes | Enable or disable the timer | `true` |
| `start` | yes | Start time `hh:mm` | `08:00` |
| `end` | yes | End time `hh:mm` | `12:00` |
| `weekdays` | yes | List of weekdays: `mo`, `tu`, `we`, `th`, `fr`, `sa`, `su` | `[mo, tu, we]` |

```yaml
service: robonect.timer
data:
  entity_id: lawn_mower.automower_robonect
  timer: "1"
  enable: true
  start: "08:00"
  end: "12:00"
  weekdays:
    - mo
    - tu
    - we
    - th
    - fr
```

---

## ext (Control Equipment)

Controls GPIO or OUT channels.

| Field | Required | Description |
| --- | --- | --- |
| `entity_id` | yes | Lawn mower entity |
| `ext` | yes | Channel: `GPIO1`, `GPIO2`, `OUT1`, `OUT2` |
| `gpioout` | yes | Channel mode: `[IN] Analog`, `[IN] Floating`, `[IN] PullDown`, `[IN] PullUp`, `[OUT] OpenDrain`, `[OUT] PushPull` |
| `gpiomode` | yes | Operation mode: `Off`, `On`, `Night (19-7 o'clock)`, `Drive`, `Night drive (19-7 o'clock)`, `Searching/Way home`, `Park position`, `Brake light`, `Left Turn Signal`, `Right Turn Signal`, `API` |
| `gpioerr` | yes | Flash on fault (boolean) |
| `gpioinv` | yes | Low-active signal (boolean) |

```yaml
service: robonect.ext
data:
  entity_id: lawn_mower.automower_robonect
  ext: GPIO1
  gpioout: "[OUT] PushPull"
  gpiomode: "On"
  gpioerr: false
  gpioinv: false
```

---

## direct

Directly controls wheel speeds for manual driving.

| Field | Required | Description | Range |
| --- | --- | --- | --- |
| `entity_id` | yes | Lawn mower entity | — |
| `left` | yes | Left wheel speed % (positive = forward, negative = backward) | -100 to 100 |
| `right` | yes | Right wheel speed % | -100 to 100 |
| `timeout` | yes | Duration in milliseconds | 1–5000 |

```yaml
service: robonect.direct
data:
  entity_id: lawn_mower.automower_robonect
  left: 50
  right: 50
  timeout: 3000
```
