"""Definitions for Robonect sensors added to MQTT."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.components.sensor import SensorStateClass
from homeassistant.const import ELECTRIC_POTENTIAL_VOLT
from homeassistant.const import PERCENTAGE
from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import EntityCategory

from .utils import unix_to_datetime
from .utils import wifi_signal_to_percentage


@dataclass
class RobonectSensorEntityDescription(SensorEntityDescription):
    """Sensor entity description for Robonect."""

    state: Callable | None = None
    rest: str | None = None
    rest_attrs: dict | None = None
    rest_category: str | None = None


BUTTONS: tuple[RobonectSensorEntityDescription, ...] = (
    RobonectSensorEntityDescription(
        key="mower/battery/charge",
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:battery",
    ),
)

SENSORS: tuple[RobonectSensorEntityDescription, ...] = (
    RobonectSensorEntityDescription(
        key="$.status.status.battery",
        name="Battery",
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:battery",
        rest_category="status",
    ),
)

SENSORS: tuple[RobonectSensorEntityDescription, ...] = (
    RobonectSensorEntityDescription(
        key="mower/battery/charge",
        rest="$.status.status.battery",
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:battery",
        rest_category="status",
    ),
    RobonectSensorEntityDescription(
        key="device/serial",
        rest="$.version.serial",
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:tag",
        rest_category="version",
    ),
    RobonectSensorEntityDescription(
        key="mower/distance",
        rest="$.status.status.distance",
        icon="mdi:map-marker-distance",
        device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement="m",
        entity_category=EntityCategory.DIAGNOSTIC,
        rest_category="status",
    ),
    RobonectSensorEntityDescription(
        key="device/name",
        rest="$.status.name",
        icon="mdi:robot-mower",
        entity_category=EntityCategory.DIAGNOSTIC,
        rest_category="status",
    ),
    RobonectSensorEntityDescription(
        key="health/climate/temperature",
        rest="$.status.health.temperature",
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=TEMP_CELSIUS,
        entity_category=EntityCategory.DIAGNOSTIC,
        rest_category="status",
    ),
    RobonectSensorEntityDescription(
        key="health/climate/humidity",
        rest="$.status.health.humidity",
        icon="mdi:water-percent",
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        entity_category=EntityCategory.DIAGNOSTIC,
        rest_category="status",
    ),
    RobonectSensorEntityDescription(
        key="mower/blades/quality",
        rest="$.status.blades.quality",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:terraform",
        entity_category=EntityCategory.DIAGNOSTIC,
        rest_category="status",
    ),
    RobonectSensorEntityDescription(
        key="mower/blades/days",
        rest="$.status.blades.days",
        icon="mdi:terraform",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement="d",
        entity_category=EntityCategory.DIAGNOSTIC,
        rest_category="status",
    ),
    RobonectSensorEntityDescription(
        key="mower/blades/hours",
        rest="$.status.blades.hours",
        icon="mdi:terraform",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement="h",
        entity_category=EntityCategory.DIAGNOSTIC,
        rest_category="status",
    ),
    RobonectSensorEntityDescription(
        key="mower/stopped",
        rest="$.status.status.stopped",
        icon="mdi:stop",
        entity_category=EntityCategory.DIAGNOSTIC,
        rest_category="status",
    ),
    RobonectSensorEntityDescription(
        key="wlan/rssi",
        rest="$.status.wlan.signal",
        rest_attrs="$.status.wlan",
        state=wifi_signal_to_percentage,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:wifi",
        entity_category=EntityCategory.DIAGNOSTIC,
        rest_category="status",
    ),
    RobonectSensorEntityDescription(
        key="mower/mode",
        rest="$.status.status.mode",
        icon="mdi:auto-mode",
        entity_category=EntityCategory.DIAGNOSTIC,
        rest_category="status",
    ),
    RobonectSensorEntityDescription(
        key="mower/statistic/hours",
        rest="$.status.status.hours",
        icon="mdi:clock-star-four-points",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement="h",
        entity_category=EntityCategory.DIAGNOSTIC,
        rest_category="status",
    ),
    RobonectSensorEntityDescription(
        key="mower/error/code",
        rest="$.error.errors.0.error_code",
        rest_attrs="$.error.errors.0",
        icon="mdi:alert-circle",
        entity_category=EntityCategory.DIAGNOSTIC,
        rest_category="error",
    ),
    RobonectSensorEntityDescription(
        key="mower/error/message",
        rest="$.error.errors.0.error_message",
        rest_attrs="$.error.errors.0",
        icon="mdi:alert-circle",
        entity_category=EntityCategory.DIAGNOSTIC,
        rest_category="error",
    ),
    RobonectSensorEntityDescription(
        key="mower/substatus",
        rest="$.none",
        icon="mdi:crosshairs-question",
        entity_category=EntityCategory.DIAGNOSTIC,
        rest_category="NONE",
    ),
    RobonectSensorEntityDescription(
        key="mower/substatus/plain",
        rest="$.none",
        icon="mdi:crosshairs-question",
        entity_category=EntityCategory.DIAGNOSTIC,
        rest_category="NONE",
    ),
    RobonectSensorEntityDescription(
        key="mower/timer/next/unix",
        rest="$.status.timer.next.unix",
        rest_attrs="$.status.timer.next",
        icon="mdi:calendar-clock",
        device_class=SensorDeviceClass.TIMESTAMP,
        state=unix_to_datetime,
        entity_category=EntityCategory.DIAGNOSTIC,
        rest_category="status",
    ),
    RobonectSensorEntityDescription(
        key="weather/data/break",
        rest="$.none",
        icon="mdi:stop",
        entity_category=EntityCategory.DIAGNOSTIC,
        rest_category="NONE",
    ),
    RobonectSensorEntityDescription(
        key="mower/status",
        rest="$.status.status.status",
        icon="mdi:crosshairs-question",
        entity_category=EntityCategory.DIAGNOSTIC,
        rest_category="status",
    ),
    RobonectSensorEntityDescription(
        key="mower/status/plain",
        rest="$.none",
        icon="mdi:crosshairs-question",
        entity_category=EntityCategory.DIAGNOSTIC,
        rest_category="NONE",
    ),
    RobonectSensorEntityDescription(
        key="mower/status/duration",
        rest="$.status.status.duration",
        icon="mdi:timer-sand",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement="min",
        rest_category="status",
    ),
    RobonectSensorEntityDescription(
        key="health/voltage/int33",
        rest="$.health.health.voltages.int3v3",
        icon="mdi:flash",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        entity_category=EntityCategory.DIAGNOSTIC,
        rest_category="health",
    ),
    RobonectSensorEntityDescription(
        key="health/voltage/ext33",
        rest="$.health.health.voltages.ext3v3",
        icon="mdi:flash",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        entity_category=EntityCategory.DIAGNOSTIC,
        rest_category="health",
    ),
    RobonectSensorEntityDescription(
        key="health/voltage/batt",
        rest="$.health.health.voltages.batt",
        icon="mdi:flash",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        entity_category=EntityCategory.DIAGNOSTIC,
        rest_category="health",
    ),
    RobonectSensorEntityDescription(
        key="gps/latitude",
        rest="$.gps.latitude",
        rest_attrs="$.gps",
        icon="mdi:crosshairs-gps",
        entity_category=EntityCategory.DIAGNOSTIC,
        rest_category="gps",
    ),
    RobonectSensorEntityDescription(
        key="gps/longitude",
        rest="$.gps.longitude",
        rest_attrs="$.gps",
        icon="mdi:crosshairs-gps",
        entity_category=EntityCategory.DIAGNOSTIC,
        rest_category="gps",
    ),
    RobonectSensorEntityDescription(
        key="passage/open",
        rest="$.door.open",
        rest_attrs="$.door",
        icon="mdi:gate-open",
        entity_category=EntityCategory.DIAGNOSTIC,
        rest_category="door",
    ),
    RobonectSensorEntityDescription(
        key=".clock/time",
        rest="$.status.clock.unix",
        rest_attrs="$.status.clock",
        icon="mdi:clock-time-eight-outline",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_category=EntityCategory.DIAGNOSTIC,
        rest_category="status",
    ),
)