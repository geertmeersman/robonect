"""Tests for RobonectEntity.async_send_command."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest


def make_entity(async_cmd_return=None):
    """Build a minimal RobonectEntity with a mocked coordinator."""
    from custom_components.robonect.entity import RobonectEntity

    hass = MagicMock()
    hass.loop = MagicMock()
    hass.loop.is_running.return_value = False
    hass.bus = MagicMock()
    hass.bus.async_fire = MagicMock()

    entry = MagicMock()
    entry.entry_id = "test"
    entry.data = {
        "mqtt_topic": "automower",
        "mqtt_enabled": False,
        "host": "192.168.1.1",
        "brand": "Husqvarna",
        "type": "310",
    }

    description = MagicMock()
    description.key = "test/key"
    description.category = "NONE"
    description.translation_key = None

    with patch(
        "custom_components.robonect.entity.dr.async_get", return_value=MagicMock()
    ):
        entity = RobonectEntity.__new__(RobonectEntity)
        entity.hass = hass
        entity.entry = entry
        entity.entity_description = description
        entity.base_topic = "automower"
        entity.topic = "automower/test/key"
        entity.slug = "automower_test_key"
        entity._attr_translation_key = "test_key"
        entity._attr_unique_id = "test-NONE-automower_test_key"
        entity.device_identifier = {("robonect", "automower")}
        entity.dev_reg = MagicMock()
        entity.dev_reg.async_get_device.return_value = MagicMock(id="device_id")

        client = MagicMock()
        client.async_cmd = AsyncMock(return_value=async_cmd_return)
        coordinator = MagicMock()
        coordinator.client = client
        entity.coordinator = coordinator

    return entity, client


# ---------------------------------------------------------------------------
# async_send_command — None response (sleeping guard)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_entity_async_send_command_handles_none_response():
    """entity.async_send_command does not crash when async_cmd returns None."""
    entity, client = make_entity(async_cmd_return=None)
    # Should not raise TypeError
    await entity.async_send_command("hour", {})
    client.async_cmd.assert_called_once_with("hour", {})


@pytest.mark.asyncio
async def test_entity_async_send_command_fires_event_on_success():
    """entity.async_send_command fires event when response is a dict."""
    entity, client = make_entity(async_cmd_return={"successful": True})
    await entity.async_send_command("status", {})
    entity.hass.bus.async_fire.assert_called_once()


@pytest.mark.asyncio
async def test_entity_async_send_command_no_command_logs_error():
    """entity.async_send_command logs error when command is empty."""
    entity, client = make_entity()
    with patch("custom_components.robonect.entity._LOGGER") as mock_logger:
        await entity.async_send_command("", {})
        mock_logger.error.assert_called_once()
