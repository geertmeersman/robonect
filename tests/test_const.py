"""Tests for Robonect constants."""

from custom_components.robonect.const import (
    SERVICE_JOB_AFTER_CODES,
    SERVICE_JOB_CORRIDOR_CODES,
    SERVICE_JOB_REMOTESTART_CODES,
    STATUS_MAPPING_LAWN_MOWER,
    WEEKDAYS_HEX,
    WEEKDAYS_SHORT,
)

# ---------------------------------------------------------------------------
# STATUS_MAPPING_LAWN_MOWER
# ---------------------------------------------------------------------------


def test_status_sleeping_is_docked():
    """Status 17 maps to docked."""
    assert STATUS_MAPPING_LAWN_MOWER[17] == "docked"


def test_status_mowing():
    """Status 2 maps to mowing."""
    assert STATUS_MAPPING_LAWN_MOWER[2] == "mowing"


def test_status_charging():
    """Status 4 maps to charging."""
    assert STATUS_MAPPING_LAWN_MOWER[4] == "charging"


def test_status_error():
    """Status 7 maps to error."""
    assert STATUS_MAPPING_LAWN_MOWER[7] == "error"


def test_status_unknown():
    """Status 99 maps to unknown."""
    assert STATUS_MAPPING_LAWN_MOWER[99] == "unknown"


def test_status_missing_key_returns_unknown():
    """Missing status key falls back to unknown."""
    assert STATUS_MAPPING_LAWN_MOWER.get(999, "unknown") == "unknown"


# ---------------------------------------------------------------------------
# SERVICE_JOB_AFTER_CODES
# ---------------------------------------------------------------------------


def test_job_after_codes_keys():
    """Job after codes contain expected keys."""
    assert set(SERVICE_JOB_AFTER_CODES.keys()) == {"Auto", "Home", "End of day"}


def test_job_after_auto_is_3():
    """Auto after code is 3."""
    assert SERVICE_JOB_AFTER_CODES["Auto"] == 3


def test_job_after_home_is_1():
    """Home after code is 1."""
    assert SERVICE_JOB_AFTER_CODES["Home"] == 1


# ---------------------------------------------------------------------------
# SERVICE_JOB_CORRIDOR_CODES
# ---------------------------------------------------------------------------


def test_corridor_normal_is_minus_one():
    """Normal corridor code is -1."""
    assert SERVICE_JOB_CORRIDOR_CODES["Normal"] == -1


def test_corridor_codes_range():
    """Numeric corridor codes are in range 0-9."""
    numeric = {k: v for k, v in SERVICE_JOB_CORRIDOR_CODES.items() if k != "Normal"}
    assert all(0 <= v <= 9 for v in numeric.values())


# ---------------------------------------------------------------------------
# SERVICE_JOB_REMOTESTART_CODES
# ---------------------------------------------------------------------------


def test_remotestart_normal_is_0():
    """Normal remotestart code is 0."""
    assert SERVICE_JOB_REMOTESTART_CODES["Normal"] == 0


def test_remotestart_codes_range():
    """All remotestart codes are in range 0-6."""
    assert all(0 <= v <= 6 for v in SERVICE_JOB_REMOTESTART_CODES.values())


# ---------------------------------------------------------------------------
# WEEKDAYS_HEX / WEEKDAYS_SHORT
# ---------------------------------------------------------------------------


def test_weekdays_hex_covers_all_days():
    """WEEKDAYS_HEX values match WEEKDAYS_SHORT."""
    assert set(WEEKDAYS_HEX.values()) == set(WEEKDAYS_SHORT)


def test_weekdays_hex_bits_are_powers_of_two():
    """WEEKDAYS_HEX keys are all powers of two (bitmask)."""
    assert all((k & (k - 1)) == 0 for k in WEEKDAYS_HEX)


def test_weekdays_short_count():
    """WEEKDAYS_SHORT contains 7 days."""
    assert len(WEEKDAYS_SHORT) == 7
