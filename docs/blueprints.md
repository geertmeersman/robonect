# Robonect — Blueprints

## Syncing Robonect Time

Automatically press the Robonect clock sync button at a specific time each day to keep your mower's internal clock accurate and aligned with Home Assistant time.

Configure the target button entity (e.g. `button.automower_sync_clock`) and the time of day when synchronization should occur. The sync uses automatic Internet time with summer/winter time adjustment.

[![Import the blueprint.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fgeertmeersman%2Frobonect%2Fblob%2Fmain%2Fblueprints%2Fsync_robonect_time.yaml)
