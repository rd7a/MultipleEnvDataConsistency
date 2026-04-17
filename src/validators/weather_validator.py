from typing import Any

TEMP_MIN: float = -80.0
TEMP_MAX: float = 60.0


def validate_temperature_range(temperatures: list[float | None]) -> list[float]:
    """Returns temperatures that fall outside the acceptable range."""
    return [t for t in temperatures if t is not None and not (TEMP_MIN <= t <= TEMP_MAX)]


def validate_hourly_count(data: dict[str, Any]) -> bool:
    """Returns True if hourly temperature entries are present."""
    return len(data.get("hourly", {}).get("temperature_2m", [])) > 0


def validate_timezone(data: dict[str, Any]) -> bool:
    """Returns True if timezone field is present and non-empty."""
    return bool(data.get("timezone"))
