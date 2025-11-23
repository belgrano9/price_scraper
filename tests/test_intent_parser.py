"""Tests for intent parser."""

import pytest
from src.verify.intent_parser import parse_intent


class TestIntentParser:
    """Test intent parsing from natural language."""

    def test_simple_destination(self):
        """Parse simple destination."""
        intent = parse_intent("Book me a train to Barcelona")
        assert intent.destination == "Barcelona"

    def test_destination_with_origin(self):
        """Parse origin and destination."""
        intent = parse_intent("Train from Madrid to Barcelona")
        assert intent.origin == "Madrid"
        assert intent.destination == "Barcelona"

    def test_destination_with_date(self):
        """Parse destination with tomorrow."""
        intent = parse_intent("Train to Barcelona tomorrow")
        assert intent.destination == "Barcelona"
        assert intent.date == "tomorrow"

    def test_destination_with_time(self):
        """Parse destination with time preference."""
        intent = parse_intent("Train to Valencia in the morning")
        assert intent.destination == "Valencia"
        assert intent.time_preference == "morning"

    def test_specific_time(self):
        """Parse specific time."""
        intent = parse_intent("Train to Sevilla at 9am")
        assert intent.destination == "Sevilla"
        assert intent.time_preference == "09:00"

    def test_full_intent(self):
        """Parse complete intent."""
        intent = parse_intent("Book a train from Madrid to Barcelona tomorrow morning")
        assert intent.origin == "Madrid"
        assert intent.destination == "Barcelona"
        assert intent.date == "tomorrow"
        assert intent.time_preference == "morning"

    def test_context_origin(self):
        """Use context for origin when not specified."""
        intent = parse_intent(
            "Train to Barcelona",
            context={"user_location": "Valencia"}
        )
        assert intent.destination == "Barcelona"
        assert intent.origin == "Valencia"

    def test_afternoon_time(self):
        """Parse afternoon time preference."""
        intent = parse_intent("Train to Malaga in the afternoon")
        assert intent.destination == "Malaga"
        assert intent.time_preference == "afternoon"

    def test_european_date(self):
        """Parse European date format."""
        intent = parse_intent("Train to Barcelona on 25/12")
        assert intent.destination == "Barcelona"
        assert intent.date == "25/12"


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_no_destination(self):
        """Handle missing destination."""
        intent = parse_intent("Book me a train tomorrow")
        assert intent.destination is None
        assert intent.date == "tomorrow"

    def test_empty_intent(self):
        """Handle empty intent."""
        intent = parse_intent("")
        assert intent.destination is None
        assert intent.origin is None

    def test_gibberish(self):
        """Handle nonsense input."""
        intent = parse_intent("asdf jkl qwerty")
        assert intent.destination is None
