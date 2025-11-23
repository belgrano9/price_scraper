"""Date and time parsing for travel verification."""

from datetime import datetime, timedelta
from typing import Optional, Tuple
from dateutil import parser as date_parser


# Time ranges for general preferences
TIME_RANGES = {
    "morning": (6, 12),    # 06:00 - 12:00
    "afternoon": (12, 18), # 12:00 - 18:00
    "evening": (18, 23),   # 18:00 - 23:00
    "night": (20, 24),     # 20:00 - 00:00
    "early": (5, 9),       # 05:00 - 09:00
    "late": (18, 24),      # 18:00 - 00:00
}


def parse_datetime(date_str: Optional[str], base_date: Optional[datetime] = None) -> Optional[datetime]:
    """
    Parse a date string into a datetime object.

    Args:
        date_str: Date string (e.g., "tomorrow", "25/12", "2025-01-15")
        base_date: Base date for relative dates (defaults to now)

    Returns:
        Parsed datetime or None if parsing fails
    """
    if not date_str:
        return None

    base = base_date or datetime.now()
    date_lower = date_str.lower().strip()

    # Handle relative dates
    if date_lower in ("tomorrow", "mañana"):
        return base + timedelta(days=1)

    if date_lower in ("today", "hoy"):
        return base

    # Handle day of week
    days_of_week = {
        "monday": 0, "lunes": 0,
        "tuesday": 1, "martes": 1,
        "wednesday": 2, "miércoles": 2, "miercoles": 2,
        "thursday": 3, "jueves": 3,
        "friday": 4, "viernes": 4,
        "saturday": 5, "sábado": 5, "sabado": 5,
        "sunday": 6, "domingo": 6,
    }

    if date_lower in days_of_week:
        target_day = days_of_week[date_lower]
        current_day = base.weekday()
        days_ahead = target_day - current_day
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        return base + timedelta(days=days_ahead)

    # Try parsing with dateutil
    try:
        # European date format (day first)
        parsed = date_parser.parse(date_str, dayfirst=True)

        # If year not specified, use current year (or next year if date passed)
        if parsed.year == 1900:  # dateutil default when year not specified
            parsed = parsed.replace(year=base.year)
            if parsed < base:
                parsed = parsed.replace(year=base.year + 1)

        return parsed
    except (ValueError, date_parser.ParserError):
        return None


def parse_time_preference(time_pref: Optional[str]) -> Tuple[Optional[int], Optional[int]]:
    """
    Parse a time preference into hour range.

    Args:
        time_pref: Time preference (e.g., "morning", "09:00", "afternoon")

    Returns:
        Tuple of (min_hour, max_hour) or (None, None) if no preference
    """
    if not time_pref:
        return (None, None)

    time_lower = time_pref.lower().strip()

    # Check for general time periods
    if time_lower in TIME_RANGES:
        return TIME_RANGES[time_lower]

    # Check for specific time (HH:MM format)
    if ":" in time_pref:
        try:
            parts = time_pref.split(":")
            hour = int(parts[0])
            # Return a 2-hour window around the specific time
            return (max(0, hour - 1), min(23, hour + 1))
        except ValueError:
            pass

    # Try parsing as just an hour
    try:
        hour = int(time_pref.replace("h", "").replace("H", ""))
        return (max(0, hour - 1), min(23, hour + 1))
    except ValueError:
        pass

    return (None, None)


def is_time_in_preference(
    departure_time: datetime,
    time_preference: Optional[str]
) -> Tuple[bool, float]:
    """
    Check if a departure time matches a time preference.

    Args:
        departure_time: The departure datetime
        time_preference: User's time preference

    Returns:
        Tuple of (matches, confidence)
    """
    if not time_preference:
        return (True, 1.0)  # No preference means all times match

    min_hour, max_hour = parse_time_preference(time_preference)

    if min_hour is None:
        return (True, 0.5)  # Couldn't parse preference

    hour = departure_time.hour

    if min_hour <= hour <= max_hour:
        # Calculate how close to the center of the range
        center = (min_hour + max_hour) / 2
        distance = abs(hour - center)
        max_distance = (max_hour - min_hour) / 2
        confidence = 1.0 - (distance / max_distance) * 0.3  # Max 30% penalty

        return (True, confidence)

    return (False, 0.0)
