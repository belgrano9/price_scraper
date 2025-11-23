"""Tests for location disambiguation."""

import pytest
from src.verify.location import disambiguate_location, get_all_stations_for_city


class TestLocationDisambiguation:
    """Test location disambiguation."""

    def test_single_station_city(self):
        """City with single station has high confidence."""
        match = disambiguate_location("Sevilla")
        assert match.name == "Sevilla-Santa Justa"
        assert match.confidence == 1.0
        assert not match.is_ambiguous

    def test_multi_station_city(self):
        """City with multiple stations is flagged."""
        match = disambiguate_location("Madrid")
        assert "Atocha" in match.name or "Madrid" in match.name
        assert match.is_ambiguous
        assert match.alternatives is not None
        assert len(match.alternatives) > 0

    def test_barcelona_stations(self):
        """Barcelona has multiple stations."""
        match = disambiguate_location("Barcelona")
        assert match.is_ambiguous
        assert "Sants" in match.name  # Primary station

    def test_case_insensitive(self):
        """Location matching is case insensitive."""
        match1 = disambiguate_location("MADRID")
        match2 = disambiguate_location("madrid")
        match3 = disambiguate_location("Madrid")
        assert match1.name == match2.name == match3.name

    def test_unknown_city(self):
        """Unknown city has low confidence."""
        match = disambiguate_location("Atlantis")
        assert match.confidence < 0.5
        assert match.is_ambiguous

    def test_accented_city(self):
        """Handle accented city names."""
        match = disambiguate_location("Málaga")
        assert "Málaga" in match.name or "Malaga" in match.name
        assert match.confidence >= 0.7


class TestGetAllStations:
    """Test getting all stations for a city."""

    def test_madrid_stations(self):
        """Get all Madrid stations."""
        stations = get_all_stations_for_city("Madrid")
        assert len(stations) >= 2  # At least 2 stations

    def test_single_station_city(self):
        """City with one station."""
        stations = get_all_stations_for_city("Granada")
        assert len(stations) == 1

    def test_unknown_city(self):
        """Unknown city returns empty list."""
        stations = get_all_stations_for_city("Nowhere")
        assert stations == []
