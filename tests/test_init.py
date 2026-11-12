"""Tests for async_send_command in __init__.py."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.robonect import async_send_command


def make_hass_with_coordinator(async_cmd_return):
    """Build a minimal hass mock with a coordinator whose async_cmd returns the given value."""
    client = MagicMock()
    client.async_cmd = AsyncMock(return_value=async_cmd_return)

    coordinator = MagicMock()
    coordinator.client = client

    entry = MagicMock()
    entry.entry_id = "test_entry"
    entry.title = "Test Mower"

    hass = MagicMock()
    hass.data = {"robonect": {"test_entry": {"coordinator": coordinator}}}

    return hass, entry, client


# ---------------------------------------------------------------------------
# async_send_command — None response handling (fix for #436 TypeError)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_async_send_command_handles_none_response():
    """async_send_command does not crash when async_cmd returns None (sleeping guard)."""
    hass, entry, client = make_hass_with_coordinator(None)

    with patch(
        "custom_components.robonect.async_fire_event", new_callable=AsyncMock
    ) as mock_fire:
        await async_send_command(hass, entry, "hour")
        mock_fire.assert_not_called()


@pytest.mark.asyncio
async def test_async_send_command_fires_event_on_success():
    """async_send_command fires event when async_cmd returns a dict."""
    hass, entry, client = make_hass_with_coordinator({"successful": True})

    with patch(
        "custom_components.robonect.async_fire_event", new_callable=AsyncMock
    ) as mock_fire:
        await async_send_command(hass, entry, "status")
        mock_fire.assert_called_once()
        fired_response = mock_fire.call_args.args[2]
        assert fired_response["command"] == "status"


@pytest.mark.asyncio
async def test_async_send_command_passes_bypass_sleeping():
    """async_send_command passes bypass_sleeping to async_cmd."""
    hass, entry, client = make_hass_with_coordinator({"successful": True})

    with patch("custom_components.robonect.async_fire_event", new_callable=AsyncMock):
        await async_send_command(
            hass, entry, "mode", {"mode": "job"}, bypass_sleeping=True
        )
        client.async_cmd.assert_called_once_with("mode", {"mode": "job"}, True)


@pytest.mark.asyncio
async def test_async_send_command_handles_exception():
    """async_send_command handles exceptions from async_cmd gracefully."""
    hass, entry, client = make_hass_with_coordinator(None)
    client.async_cmd = AsyncMock(side_effect=Exception("connection error"))

    with patch(
        "custom_components.robonect.async_fire_event", new_callable=AsyncMock
    ) as mock_fire:
        await async_send_command(hass, entry, "status")
        mock_fire.assert_called_once()
        fired_response = mock_fire.call_args.args[2]
        assert fired_response["successful"] is False
        assert "connection error" in fired_response["exception"]
