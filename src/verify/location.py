"""Location disambiguation for Spanish train stations."""

from dataclasses import dataclass


@dataclass
class StationMatch:
    """A matched station with confidence."""
    name: str
    code: str
    confidence: float
    is_ambiguous: bool = False
    alternatives: list[str] | None = None


# Known station mappings (city -> stations)
CITY_STATIONS = {
    "madrid": [
        ("Madrid Pta.Atocha - Almudena Grandes", "60000", True),  # Main station
        ("Madrid-Chamartín-Clara Campoamor", "17000", False),
        ("Madrid - Atocha Cercanías", "18000", False),
    ],
    "barcelona": [
        ("Barcelona-Sants", "71801", True),  # Main station
        ("Barcelona-Passeig de Gràcia", "71802", False),
        ("Barcelona-Estació de França", "71803", False),
    ],
    "valencia": [
        ("Valencia Joaquín Sorolla", "65000", True),
        ("Valencia Nord", "65001", False),
    ],
    "sevilla": [
        ("Sevilla-Santa Justa", "51003", True),
    ],
    "seville": [
        ("Sevilla-Santa Justa", "51003", True),
    ],
    "malaga": [
        ("Málaga María Zambrano", "31002", True),
    ],
    "málaga": [
        ("Málaga María Zambrano", "31002", True),
    ],
    "bilbao": [
        ("Bilbao-Abando Indalecio Prieto", "13002", True),
    ],
    "zaragoza": [
        ("Zaragoza-Delicias", "70002", True),
    ],
    "alicante": [
        ("Alicante Terminal", "69001", True),
    ],
    "cordoba": [
        ("Córdoba Central", "50001", True),
    ],
    "córdoba": [
        ("Córdoba Central", "50001", True),
    ],
    "granada": [
        ("Granada", "30001", True),
    ],
}


def disambiguate_location(city_name: str) -> StationMatch:
    """
    Disambiguate a city name to specific station(s).

    Args:
        city_name: City name from user intent (e.g., "Barcelona")

    Returns:
        StationMatch with best match and alternatives
    """
    city_lower = city_name.lower().strip()

    # Direct match
    if city_lower in CITY_STATIONS:
        stations = CITY_STATIONS[city_lower]
        primary = next((s for s in stations if s[2]), stations[0])  # Get primary station

        alternatives = [s[0] for s in stations if s[0] != primary[0]]

        return StationMatch(
            name=primary[0],
            code=primary[1],
            confidence=1.0 if len(stations) == 1 else 0.8,
            is_ambiguous=len(stations) > 1,
            alternatives=alternatives if alternatives else None,
        )

    # Fuzzy match - check if city is substring
    for city, stations in CITY_STATIONS.items():
        if city in city_lower or city_lower in city:
            primary = next((s for s in stations if s[2]), stations[0])
            alternatives = [s[0] for s in stations if s[0] != primary[0]]

            return StationMatch(
                name=primary[0],
                code=primary[1],
                confidence=0.7,
                is_ambiguous=True,
                alternatives=alternatives if alternatives else None,
            )

    # No match found
    return StationMatch(
        name=city_name,
        code="",
        confidence=0.3,
        is_ambiguous=True,
        alternatives=None,
    )


def get_all_stations_for_city(city_name: str) -> list[tuple[str, str]]:
    """
    Get all stations for a city.

    Args:
        city_name: City name

    Returns:
        List of (station_name, station_code) tuples
    """
    city_lower = city_name.lower().strip()

    if city_lower in CITY_STATIONS:
        return [(s[0], s[1]) for s in CITY_STATIONS[city_lower]]

    # Fuzzy match
    for city, stations in CITY_STATIONS.items():
        if city in city_lower or city_lower in city:
            return [(s[0], s[1]) for s in stations]

    return []
