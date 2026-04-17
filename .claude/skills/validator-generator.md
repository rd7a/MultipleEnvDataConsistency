# Skill: Validator Generator

## Trigger
Use this skill when given a sample JSON response body from an API endpoint.

## Output
A typed validator module in `src/validators/<name>_validator.py` with:
- A `REQUIRED_FIELDS` constant listing all top-level required keys
- A `validate_<name>_schema(data)` function returning a list of missing fields
- Per-field type-check helpers where the type is non-trivial (nested object, list, numeric range)
- Type hints on all functions using built-in generics

## Template

```python
from typing import Any

# All fields the API response must contain
REQUIRED_FIELDS: list[str] = ["field1", "field2", "field3"]


def validate_<name>_schema(data: dict[str, Any]) -> list[str]:
    """Returns list of missing required fields."""
    return [f for f in REQUIRED_FIELDS if f not in data]


def validate_<field>_range(value: float) -> bool:
    """Returns True if value is within the acceptable range."""
    return MIN_VALUE <= value <= MAX_VALUE


def validate_<field>_type(data: dict[str, Any]) -> bool:
    """Returns True if <field> is the expected type."""
    return isinstance(data.get("<field>"), expected_type)
```

## Rules
- Validators must return data — never raise exceptions or call assert internally
- One validator file per API resource (e.g. countries_validator.py, weather_validator.py)
- Constants (ranges, required fields) at module top in UPPER_SNAKE_CASE
- Tests import from validators — validators never import from tests
