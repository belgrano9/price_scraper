"""Tests for intent-booking matcher."""

import pytest
from datetime import datetime, timedelta

from src.models import UserIntent, TrainBooking
from src.verify.matcher import match_intent_to_bookings


def make_booking(
    departure_hour: int,
    price: float = 100.0,
    available: bool = True,
) -> TrainBooking:
    """Helper to create test bookings."""
    tomorrow = datetime.now() + timedelta(days=1)
    base = datetime.combine(tomorrow.date(), datetime.min.time())

    return TrainBooking(
        train_type="AVE",
        origin="Madrid Pta.Atocha",
        destination="Barcelona-Sants",
        departure_time=base.replace(hour=departure_hour),
        arrival_time=base.replace(hour=departure_hour + 3),
        duration_minutes=180,
        price=price,
        available=available,
    )


class TestMatcher:
    """Test intent to booking matching."""

    def test_morning_preference(self):
        """Morning preference matches early trains."""
        intent = UserIntent(
            destination="Barcelona",
            origin="Madrid",
            date="tomorrow",
            time_preference="morning",
        )

        bookings = [
            make_booking(6),   # 06:00 - morning
            make_booking(9),   # 09:00 - morning
            make_booking(14),  # 14:00 - afternoon
            make_booking(18),  # 18:00 - evening
        ]

        result = match_intent_to_bookings(intent, bookings)

        # Should only match morning trains
        assert len(result.matched_bookings) == 2
        assert all(b.departure_time.hour < 12 for b in result.matched_bookings)

    def test_afternoon_preference(self):
        """Afternoon preference matches midday trains."""
        intent = UserIntent(
            destination="Barcelona",
            time_preference="afternoon",
        )

        bookings = [
            make_booking(9),   # morning
            make_booking(13),  # afternoon
            make_booking(16),  # afternoon
            make_booking(20),  # evening
        ]

        result = match_intent_to_bookings(intent, bookings)

        # Should match afternoon trains
        matched_hours = [b.departure_time.hour for b in result.matched_bookings]
        assert all(12 <= h < 18 for h in matched_hours)

    def test_no_time_preference(self):
        """No time preference matches all trains."""
        intent = UserIntent(
            destination="Barcelona",
            origin="Madrid",
        )

        bookings = [
            make_booking(6),
            make_booking(12),
            make_booking(18),
        ]

        result = match_intent_to_bookings(intent, bookings)

        # Should match all trains
        assert len(result.matched_bookings) == 3

    def test_unavailable_booking_low_priority(self):
        """Unavailable bookings are deprioritized."""
        intent = UserIntent(
            destination="Barcelona",
            time_preference="morning",
        )

        bookings = [
            make_booking(9, available=False),
            make_booking(10, available=True),
        ]

        result = match_intent_to_bookings(intent, bookings)

        # Available booking should be recommended
        assert result.recommended_booking is not None
        assert result.recommended_booking.available

    def test_missing_destination_warning(self):
        """Missing destination generates warning."""
        intent = UserIntent()  # Empty intent

        result = match_intent_to_bookings(intent, [])

        assert len(result.warnings) > 0
        assert any(w.type == "location" for w in result.warnings)
        assert result.confidence < 0.5

    def test_ambiguous_destination_warning(self):
        """Ambiguous destination generates warning."""
        intent = UserIntent(
            destination="Barcelona",  # Has multiple stations
        )

        result = match_intent_to_bookings(intent, [])

        # Should have location warning
        location_warnings = [w for w in result.warnings if w.type == "location"]
        assert len(location_warnings) > 0

    def test_safe_to_book_conditions(self):
        """Safe to book requires reasonable confidence and available booking."""
        intent = UserIntent(
            destination="Sevilla",  # Single station city = higher confidence
            origin="Granada",       # Single station city
            date="tomorrow",
            time_preference="09:00",
        )

        bookings = [make_booking(9)]

        result = match_intent_to_bookings(intent, bookings)

        # Should have reasonable confidence and a recommendation
        assert result.confidence >= 0.6
        assert result.recommended_booking is not None

    def test_not_safe_with_high_severity_warning(self):
        """Not safe to book with high severity warnings."""
        intent = UserIntent()  # Missing destination = high severity

        result = match_intent_to_bookings(intent, [])

        assert not result.safe_to_book
