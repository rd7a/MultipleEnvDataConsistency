from typing import Any

# Fields every country object must contain for schema validation
REQUIRED_FIELDS: list[str] = ["name", "capital", "population", "currencies", "languages"]


def validate_country_schema(country: dict[str, Any]) -> list[str]:
    """Returns a list of field names missing from the country object."""
    return [field for field in REQUIRED_FIELDS if field not in country]


def validate_population(country: dict[str, Any]) -> bool:
    """Returns True if population is a non-negative integer.
    Uninhabited territories legitimately report population 0."""
    return isinstance(country.get("population"), int) and country["population"] >= 0
