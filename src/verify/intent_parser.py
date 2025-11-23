"""Parse user intent from natural language."""

import re
from typing import Optional
from ..models import UserIntent


# Common Spanish cities for train travel
SPANISH_CITIES = [
    "madrid", "barcelona", "valencia", "sevilla", "seville", "malaga", "málaga",
    "bilbao", "zaragoza", "alicante", "cordoba", "córdoba", "granada", "murcia",
    "valladolid", "vigo", "gijon", "gijón", "santander", "pamplona", "leon", "león",
    "toledo", "salamanca", "burgos", "san sebastian", "san sebastián", "donostia",
    "tarragona", "lleida", "girona", "cadiz", "cádiz", "almeria", "almería",
    "oviedo", "logroño", "vitoria", "huesca", "teruel", "cuenca", "segovia", "avila", "ávila"
]

# Time patterns
TIME_PATTERNS = {
    "morning": r"\b(morning|mañana|am|early)\b",
    "afternoon": r"\b(afternoon|tarde|pm|midday)\b",
    "evening": r"\b(evening|noche|night|late)\b",
    "specific": r"\b(\d{1,2})[:\.]?(\d{2})?\s*(am|pm|h|hours?)?\b",
}

# Date patterns
DATE_PATTERNS = {
    "tomorrow": r"\b(tomorrow|mañana)\b",
    "today": r"\b(today|hoy)\b",
    "day_of_week": r"\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday|lunes|martes|miércoles|jueves|viernes|sábado|domingo)\b",
    "specific_date": r"\b(\d{1,2})[/\-.](\d{1,2})[/\-.]?(\d{2,4})?\b",
}


def parse_intent(text: str, context: Optional[dict] = None) -> UserIntent:
    """
    Parse natural language booking intent into structured data.

    Args:
        text: Natural language intent (e.g., "Book me a train to Barcelona tomorrow morning")
        context: Optional context (user_location, conversation_history, etc.)

    Returns:
        UserIntent with extracted fields
    """
    text_lower = text.lower()
    context = context or {}

    # Extract destination (city after "to" or "a")
    destination = _extract_destination(text_lower)

    # Extract origin (city after "from" or "de", or from context)
    origin = _extract_origin(text_lower, context)

    # Extract date
    date = _extract_date(text_lower)

    # Extract time preference
    time_preference = _extract_time_preference(text_lower)

    return UserIntent(
        origin=origin,
        destination=destination,
        date=date,
        time_preference=time_preference,
    )


def _extract_destination(text: str) -> Optional[str]:
    """Extract destination city from text."""
    # Words that are not destinations
    non_destinations = {
        "train", "tren", "ticket", "billete", "book", "reservar", "me", "a",
        "train tomorrow", "train today", "tren mañana", "tren hoy"
    }

    # Pattern: "to <city>" or "a <city>"
    patterns = [
        r"\bto\s+([a-záéíóúñ]+)(?:\s|$)",  # Single word after "to"
        r"\ba\s+([a-záéíóúñ]+)(?:\s|$)",   # Single word after "a" (Spanish)
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            candidate = match.group(1).strip()

            # Skip common non-destination words
            if candidate.lower() in non_destinations:
                continue

            # Check if it's a known city
            for city in SPANISH_CITIES:
                if city == candidate.lower():
                    return city.title()

    # Fallback: look for any city mentioned in the text
    for city in SPANISH_CITIES:
        if re.search(rf"\b{city}\b", text, re.IGNORECASE):
            return city.title()

    return None


def _extract_origin(text: str, context: dict) -> Optional[str]:
    """Extract origin city from text or context."""
    # Pattern: "from <city>" or "de <city>" or "desde <city>"
    patterns = [
        r"\bfrom\s+([a-záéíóúñ\s]+?)(?:\s+to\b|\s*$)",
        r"\bde\s+([a-záéíóúñ\s]+?)(?:\s+a\b|\s*$)",
        r"\bdesde\s+([a-záéíóúñ\s]+?)(?:\s+a\b|\s*$)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            candidate = match.group(1).strip()
            for city in SPANISH_CITIES:
                if city in candidate.lower():
                    return city.title()
            if len(candidate) > 2:
                return candidate.title()

    # Use context if available
    if context.get("user_location"):
        return context["user_location"]

    return None


def _extract_date(text: str) -> Optional[str]:
    """Extract date from text."""
    # Check for relative dates first
    if re.search(DATE_PATTERNS["tomorrow"], text, re.IGNORECASE):
        return "tomorrow"

    if re.search(DATE_PATTERNS["today"], text, re.IGNORECASE):
        return "today"

    # Check for day of week
    match = re.search(DATE_PATTERNS["day_of_week"], text, re.IGNORECASE)
    if match:
        return match.group(1).lower()

    # Check for specific date
    match = re.search(DATE_PATTERNS["specific_date"], text)
    if match:
        day, month, year = match.groups()
        if year:
            return f"{day}/{month}/{year}"
        return f"{day}/{month}"

    return None


def _extract_time_preference(text: str) -> Optional[str]:
    """Extract time preference from text."""
    # Check for specific time first
    match = re.search(TIME_PATTERNS["specific"], text, re.IGNORECASE)
    if match:
        hour = int(match.group(1))
        minutes = match.group(2) or "00"
        period = match.group(3)

        # Handle 12-hour format
        if period and period.lower() == "pm" and hour < 12:
            hour += 12
        elif period and period.lower() == "am" and hour == 12:
            hour = 0

        return f"{hour:02d}:{minutes}"

    # Check for general time periods
    if re.search(TIME_PATTERNS["morning"], text, re.IGNORECASE):
        return "morning"

    if re.search(TIME_PATTERNS["afternoon"], text, re.IGNORECASE):
        return "afternoon"

    if re.search(TIME_PATTERNS["evening"], text, re.IGNORECASE):
        return "evening"

    return None
