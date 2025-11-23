"""Match user intent to available train bookings."""

from datetime import datetime
from typing import Optional

from ..models import (
    UserIntent,
    TrainBooking,
    VerificationResult,
    VerificationWarning,
)
from .location import disambiguate_location
from .datetime_parser import parse_datetime, is_time_in_preference


def match_intent_to_bookings(
    intent: UserIntent,
    available_bookings: list[TrainBooking],
) -> VerificationResult:
    """
    Match a user intent to available train bookings.

    Args:
        intent: Parsed user intent
        available_bookings: List of available train bookings

    Returns:
        VerificationResult with confidence, warnings, and matched bookings
    """
    warnings: list[VerificationWarning] = []
    suggestions: list[str] = []
    confidence = 1.0

    # Validate destination
    if not intent.destination:
        warnings.append(VerificationWarning(
            type="location",
            message="No destination specified",
            severity="high",
        ))
        confidence *= 0.3
        suggestions.append("Please specify a destination city")
    else:
        dest_match = disambiguate_location(intent.destination)
        if dest_match.is_ambiguous and dest_match.alternatives:
            warnings.append(VerificationWarning(
                type="location",
                message=f"Multiple stations in {intent.destination}: {', '.join(dest_match.alternatives[:2])}",
                severity="medium",
            ))
            confidence *= 0.8
            suggestions.append(f"Confirm destination: {dest_match.name}?")

        if dest_match.confidence < 0.5:
            warnings.append(VerificationWarning(
                type="location",
                message=f"Unknown destination: {intent.destination}",
                severity="high",
            ))
            confidence *= 0.5

    # Validate origin
    if not intent.origin:
        warnings.append(VerificationWarning(
            type="location",
            message="No origin specified - using context or default",
            severity="low",
        ))
        confidence *= 0.9
        suggestions.append("Confirm departure city")
    else:
        origin_match = disambiguate_location(intent.origin)
        if origin_match.is_ambiguous and origin_match.alternatives:
            warnings.append(VerificationWarning(
                type="location",
                message=f"Multiple stations in {intent.origin}",
                severity="medium",
            ))
            confidence *= 0.85

    # Validate date
    if not intent.date:
        warnings.append(VerificationWarning(
            type="time",
            message="No date specified - assuming today",
            severity="low",
        ))
        confidence *= 0.9
    else:
        parsed_date = parse_datetime(intent.date)
        if not parsed_date:
            warnings.append(VerificationWarning(
                type="time",
                message=f"Could not parse date: {intent.date}",
                severity="high",
            ))
            confidence *= 0.5
        elif parsed_date < datetime.now():
            warnings.append(VerificationWarning(
                type="time",
                message="Date is in the past",
                severity="high",
            ))
            confidence *= 0.3

    # Validate time preference
    if intent.time_preference:
        if intent.time_preference in ("morning", "afternoon", "evening"):
            warnings.append(VerificationWarning(
                type="time",
                message=f"'{intent.time_preference}' is ambiguous - multiple trains may match",
                severity="low",
            ))
            confidence *= 0.95

    # Filter and score bookings
    matched_bookings: list[tuple[TrainBooking, float]] = []

    for booking in available_bookings:
        score = 1.0

        # Check time preference match
        time_matches, time_confidence = is_time_in_preference(
            booking.departure_time,
            intent.time_preference
        )

        if not time_matches:
            continue  # Skip bookings that don't match time preference

        score *= time_confidence

        # Check availability
        if not booking.available:
            score *= 0.1  # Heavy penalty for unavailable

        matched_bookings.append((booking, score))

    # Sort by score
    matched_bookings.sort(key=lambda x: x[1], reverse=True)

    # Extract just the bookings
    final_bookings = [b for b, _ in matched_bookings]
    recommended = final_bookings[0] if final_bookings else None

    # Determine if safe to book
    safe_to_book = (
        confidence >= 0.7
        and len([w for w in warnings if w.severity == "high"]) == 0
        and recommended is not None
        and recommended.available
    )

    return VerificationResult(
        confidence=round(confidence, 2),
        safe_to_book=safe_to_book,
        intent=intent,
        warnings=warnings,
        suggestions=suggestions,
        matched_bookings=final_bookings[:5],  # Top 5 matches
        recommended_booking=recommended,
    )


def quick_verify(
    intent_text: str,
    bookings: list[TrainBooking],
    context: Optional[dict] = None,
) -> VerificationResult:
    """
    Quick verification helper that parses intent and matches in one call.

    Args:
        intent_text: Raw intent text
        bookings: Available bookings
        context: Optional context

    Returns:
        VerificationResult
    """
    from .intent_parser import parse_intent

    intent = parse_intent(intent_text, context)
    return match_intent_to_bookings(intent, bookings)
