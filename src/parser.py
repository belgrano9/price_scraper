"""
Parser module for extracting price data from SNCF website HTML.

This module contains logic to parse train schedules, prices, and other relevant
information from the SNCF Connect search results.
"""

import re
from typing import Dict, List, Optional
from bs4 import BeautifulSoup


class PriceParser:
    """Parser for SNCF train price data."""

    def __init__(self):
        """Initialize the parser."""
        pass

    def parse_prices(self, html_content: str) -> List[Dict]:
        """
        Parse price information from HTML content.

        Args:
            html_content: HTML content of search results page

        Returns:
            List of dictionaries containing price and schedule information
        """
        try:
            soup = BeautifulSoup(html_content, "lxml")
            results = []

            # Try to find train proposals/results
            # SNCF Connect uses various class names and structures
            train_cards = self._find_train_cards(soup)

            for card in train_cards:
                train_info = self._parse_train_card(card)
                if train_info:
                    results.append(train_info)

            return results

        except Exception as e:
            print(f"Error parsing prices: {e}")
            return []

    def _find_train_cards(self, soup: BeautifulSoup) -> List:
        """
        Find train card elements in the page.

        Args:
            soup: BeautifulSoup object

        Returns:
            List of train card elements
        """
        # Try multiple selectors as SNCF may change their HTML structure
        selectors = [
            "div[class*='train-card']",
            "div[class*='proposal']",
            "div[class*='journey']",
            "li[class*='train']",
            "article[class*='train']",
            "div[data-testid*='train']",
            "div[data-testid*='proposal']",
        ]

        for selector in selectors:
            cards = soup.select(selector)
            if cards:
                return cards

        # If no specific cards found, try to find any containers with price info
        price_containers = soup.find_all(
            lambda tag: tag.name in ['div', 'article', 'li', 'section'] and
            (tag.find(string=re.compile(r'€|EUR', re.IGNORECASE)) or
             tag.find(class_=re.compile(r'price|tarif', re.IGNORECASE)))
        )

        return price_containers if price_containers else []

    def _parse_train_card(self, card) -> Optional[Dict]:
        """
        Parse individual train card element.

        Args:
            card: BeautifulSoup element representing a train card

        Returns:
            Dictionary with train information or None
        """
        try:
            info = {}

            # Extract departure time
            info['departure_time'] = self._extract_time(card, ['departure', 'depart', 'start'])

            # Extract arrival time
            info['arrival_time'] = self._extract_time(card, ['arrival', 'arrivee', 'arrive', 'end'])

            # Extract duration
            info['duration'] = self._extract_duration(card)

            # Extract price
            price = self._extract_price(card)
            if price:
                info['price'] = price
            else:
                # If no price found, skip this card
                return None

            # Extract train type (TGV, Intercités, TER, etc.)
            info['train_type'] = self._extract_train_type(card)

            # Extract train number
            info['train_number'] = self._extract_train_number(card)

            # Extract number of connections
            info['connections'] = self._extract_connections(card)

            # Extract fare class if available
            info['fare_class'] = self._extract_fare_class(card)

            return info

        except Exception as e:
            print(f"Error parsing train card: {e}")
            return None

    def _extract_time(self, element, keywords: List[str]) -> Optional[str]:
        """
        Extract time from element using keywords.

        Args:
            element: BeautifulSoup element
            keywords: List of keywords to search for

        Returns:
            Time string or None
        """
        # Try to find time by class names containing keywords
        for keyword in keywords:
            time_elem = element.find(class_=re.compile(keyword, re.IGNORECASE))
            if time_elem:
                # Look for time pattern HH:MM
                time_text = time_elem.get_text(strip=True)
                time_match = re.search(r'\b(\d{1,2}[h:]\d{2})\b', time_text)
                if time_match:
                    return time_match.group(1).replace('h', ':')

        # Try to find any time pattern in the element
        text = element.get_text()
        times = re.findall(r'\b(\d{1,2}[h:]\d{2})\b', text)
        if times:
            # Return first found time (could be improved with position logic)
            return times[0].replace('h', ':')

        return None

    def _extract_duration(self, element) -> Optional[str]:
        """
        Extract journey duration.

        Args:
            element: BeautifulSoup element

        Returns:
            Duration string or None
        """
        # Look for duration patterns like "2h30", "3h 45min", etc.
        text = element.get_text()

        # Pattern for duration
        duration_patterns = [
            r'(\d+h\s*\d*\s*(?:min)?)',
            r'(\d+\s*h\s*\d*)',
            r'Durée[:\s]*(\d+h\d+)',
        ]

        for pattern in duration_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return None

    def _extract_price(self, element) -> Optional[float]:
        """
        Extract price from element.

        Args:
            element: BeautifulSoup element

        Returns:
            Price as float or None
        """
        # Look for price elements
        price_elem = element.find(class_=re.compile(r'price|tarif|amount', re.IGNORECASE))

        if price_elem:
            text = price_elem.get_text(strip=True)
        else:
            text = element.get_text()

        # Extract price patterns
        # Match formats like: 25€, €25, 25.50€, 25,50 €, EUR 25
        price_patterns = [
            r'(\d+[,.]?\d*)\s*€',
            r'€\s*(\d+[,.]?\d*)',
            r'EUR\s*(\d+[,.]?\d*)',
            r'(\d+[,.]?\d*)\s*EUR',
        ]

        for pattern in price_patterns:
            match = re.search(pattern, text)
            if match:
                price_str = match.group(1).replace(',', '.')
                try:
                    return float(price_str)
                except ValueError:
                    continue

        return None

    def _extract_train_type(self, element) -> Optional[str]:
        """
        Extract train type (TGV, TER, etc.).

        Args:
            element: BeautifulSoup element

        Returns:
            Train type string or None
        """
        text = element.get_text()

        train_types = ['TGV', 'INOUI', 'OUIGO', 'TER', 'Intercités', 'INTERCITES']

        for train_type in train_types:
            if train_type.lower() in text.lower():
                return train_type

        return None

    def _extract_train_number(self, element) -> Optional[str]:
        """
        Extract train number.

        Args:
            element: BeautifulSoup element

        Returns:
            Train number or None
        """
        text = element.get_text()

        # Pattern for train numbers (e.g., "TGV 6701", "6701")
        number_match = re.search(r'(?:TGV|TER|INOUI)?\s*(\d{4,5})', text)
        if number_match:
            return number_match.group(1)

        return None

    def _extract_connections(self, element) -> int:
        """
        Extract number of connections/transfers.

        Args:
            element: BeautifulSoup element

        Returns:
            Number of connections
        """
        text = element.get_text().lower()

        # Direct train
        if 'direct' in text or 'sans correspondance' in text:
            return 0

        # Look for number of connections
        connection_patterns = [
            r'(\d+)\s*correspondance',
            r'(\d+)\s*changement',
            r'(\d+)\s*transfer',
        ]

        for pattern in connection_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))

        return 0

    def _extract_fare_class(self, element) -> Optional[str]:
        """
        Extract fare class (1st class, 2nd class, etc.).

        Args:
            element: BeautifulSoup element

        Returns:
            Fare class string or None
        """
        text = element.get_text().lower()

        fare_classes = [
            ('1ère classe', '1st class'),
            ('1ere classe', '1st class'),
            ('2ème classe', '2nd class'),
            ('2eme classe', '2nd class'),
            ('première classe', '1st class'),
            ('premiere classe', '1st class'),
            ('seconde classe', '2nd class'),
        ]

        for french, english in fare_classes:
            if french in text:
                return english

        return None
