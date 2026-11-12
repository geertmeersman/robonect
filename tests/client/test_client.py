"""Tests for RobonectClient."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.robonect.client.client import RobonectClient, RobonectException
from custom_components.robonect.client.const import SAFE_COMMANDS


def make_client(is_sleeping=None):
    """Create a RobonectClient with a mocked hass."""
    hass = MagicMock()
    client = RobonectClient(hass, "192.168.1.1", "user", "pass")
    client.is_sleeping = is_sleeping
    client.scheme = ["http"]
    return client


def make_response(status_code=200, text='{"successful": true}'):
    """Create a mock httpx response."""
    response = MagicMock()
    response.status_code = status_code
    response.text = text
    return response


# ---------------------------------------------------------------------------
# async_cmd — sleeping guard
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_async_cmd_skips_unsafe_command_when_sleeping():
    """Unsafe commands are skipped when mower is sleeping."""
    client = make_client(is_sleeping=True)
    result = await client.async_cmd("hour")
    assert result is None


@pytest.mark.asyncio
async def test_async_cmd_allows_safe_command_when_sleeping():
    """SAFE_COMMANDS are always allowed, even when sleeping."""
    client = make_client(is_sleeping=True)
    with patch.object(client, "_async_cmd_impl", new_callable=AsyncMock) as mock_impl:
        mock_impl.return_value = {"successful": True}
        for cmd in SAFE_COMMANDS:
            result = await client.async_cmd(cmd)
            assert result == {"successful": True}, f"Safe command '{cmd}' was blocked"


@pytest.mark.asyncio
async def test_async_cmd_bypass_sleeping_sends_unsafe_command():
    """bypass_sleeping=True allows unsafe commands through."""
    client = make_client(is_sleeping=True)
    with patch.object(client, "_async_cmd_impl", new_callable=AsyncMock) as mock_impl:
        mock_impl.return_value = {"successful": True}
        result = await client.async_cmd("hour", bypass_sleeping=True)
        assert result == {"successful": True}
        mock_impl.assert_called_once_with("hour", None)


@pytest.mark.asyncio
async def test_async_cmd_sends_command_when_not_sleeping():
    """Commands are sent normally when mower is not sleeping."""
    client = make_client(is_sleeping=False)
    with patch.object(client, "_async_cmd_impl", new_callable=AsyncMock) as mock_impl:
        mock_impl.return_value = {"status": 0}
        result = await client.async_cmd("hour")
        assert result == {"status": 0}


@pytest.mark.asyncio
async def test_async_cmd_sends_command_when_sleeping_unknown():
    """Commands are sent when is_sleeping is None (unknown state)."""
    client = make_client(is_sleeping=None)
    with patch.object(client, "_async_cmd_impl", new_callable=AsyncMock) as mock_impl:
        mock_impl.return_value = {"status": 0}
        result = await client.async_cmd("hour")
        assert result == {"status": 0}


@pytest.mark.asyncio
async def test_async_cmd_missing_command_returns_error():
    """Missing command returns error dict."""
    client = make_client()
    result = await client.async_cmd(None)
    assert result == {"successful": False, "error": "missing_command"}


# ---------------------------------------------------------------------------
# state() — is_sleeping detection
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_state_sets_is_sleeping_true_on_status_17():
    """state() sets is_sleeping=True when status is 17."""
    client = make_client(is_sleeping=False)
    with patch.object(client, "_async_cmd_impl", new_callable=AsyncMock) as mock_impl:
        mock_impl.return_value = {"status": {"status": 17}, "sync_time": None}
        await client.state()
    assert client.is_sleeping is True


@pytest.mark.asyncio
async def test_state_sets_is_sleeping_false_on_other_status():
    """state() sets is_sleeping=False when status is not 17."""
    client = make_client(is_sleeping=True)
    with patch.object(client, "_async_cmd_impl", new_callable=AsyncMock) as mock_impl:
        mock_impl.return_value = {"status": {"status": 4}, "sync_time": None}
        await client.state()
    assert client.is_sleeping is False


@pytest.mark.asyncio
async def test_state_handles_flat_status_status():
    """state() handles flattened 'status.status' key from transform_json."""
    client = make_client()
    with patch.object(client, "_async_cmd_impl", new_callable=AsyncMock) as mock_impl:
        mock_impl.return_value = {"status.status": 17, "sync_time": None}
        await client.state()
    assert client.is_sleeping is True


# ---------------------------------------------------------------------------
# async_cmds — command filtering
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_async_cmds_filters_unsafe_commands_when_sleeping():
    """async_cmds skips unsafe commands when sleeping."""
    client = make_client()
    with patch.object(
        client, "state", new_callable=AsyncMock
    ) as mock_state, patch.object(
        client, "async_cmd", new_callable=AsyncMock
    ) as mock_cmd:
        mock_state.return_value = {"status": {"status": 17}}
        client.is_sleeping = True
        mock_cmd.return_value = {"successful": True}

        await client.async_cmds(["hour", "battery", "status"])

        called_cmds = [call.args[0] for call in mock_cmd.call_args_list]
        assert "hour" not in called_cmds
        assert "battery" not in called_cmds
        assert "status" in called_cmds


@pytest.mark.asyncio
async def test_async_cmds_bypass_sleeping_sends_all_commands():
    """async_cmds with bypass_sleeping=True sends all commands."""
    client = make_client()
    with patch.object(
        client, "state", new_callable=AsyncMock
    ) as mock_state, patch.object(
        client, "async_cmd", new_callable=AsyncMock
    ) as mock_cmd:
        mock_state.return_value = {"status": {"status": 17}}
        client.is_sleeping = True
        mock_cmd.return_value = {"successful": True}

        await client.async_cmds(["hour", "battery", "status"], bypass_sleeping=True)

        called_cmds = [call.args[0] for call in mock_cmd.call_args_list]
        assert "hour" in called_cmds
        assert "battery" in called_cmds
        assert "status" in called_cmds


# ---------------------------------------------------------------------------
# RobonectException
# ---------------------------------------------------------------------------


def test_robonect_exception_message():
    """RobonectException formats message correctly."""
    exc = RobonectException("status", ValueError("timeout"), "no response")
    assert "status" in exc.message
    assert "no response" in exc.message
