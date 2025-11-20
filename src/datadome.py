"""
DataDome bypass strategies and anti-detection techniques.

This module implements various strategies to evade DataDome's bot detection,
including human-like behavior simulation, timing randomization, and fingerprint
management.
"""

import random
import time
from typing import Optional


class DataDomeBypass:
    """Handles DataDome detection evasion strategies."""

    def __init__(self):
        """Initialize DataDome bypass handler."""
        self.cookies = {}
        self.last_request_time = 0

    def random_delay(self, min_seconds: float = 1.0, max_seconds: float = 3.0) -> None:
        """
        Introduce random delays between actions to mimic human behavior.

        Args:
            min_seconds: Minimum delay in seconds
            max_seconds: Maximum delay in seconds
        """
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)

    def human_like_mouse_movement(self, page) -> None:
        """
        Simulate human-like mouse movements on the page.

        Args:
            page: Camoufox page object
        """
        try:
            # Random mouse movements
            for _ in range(random.randint(2, 5)):
                x = random.randint(100, 800)
                y = random.randint(100, 600)
                page.mouse.move(x, y)
                time.sleep(random.uniform(0.1, 0.3))
        except Exception as e:
            print(f"Mouse movement simulation failed: {e}")

    def random_scroll(self, page) -> None:
        """
        Perform random scrolling to simulate human browsing.

        Args:
            page: Camoufox page object
        """
        try:
            # Random scroll down
            scroll_amount = random.randint(200, 600)
            page.evaluate(f"window.scrollBy(0, {scroll_amount})")
            self.random_delay(0.5, 1.5)

            # Sometimes scroll back up a bit
            if random.random() > 0.5:
                scroll_back = random.randint(50, 200)
                page.evaluate(f"window.scrollBy(0, -{scroll_back})")
                self.random_delay(0.3, 0.8)
        except Exception as e:
            print(f"Scroll simulation failed: {e}")

    def wait_for_page_load(self, page, timeout: int = 30000) -> bool:
        """
        Wait for page to load completely, checking for DataDome challenges.

        Args:
            page: Camoufox page object
            timeout: Maximum time to wait in milliseconds

        Returns:
            True if page loaded successfully, False if DataDome challenge detected
        """
        try:
            # Wait for network idle
            page.wait_for_load_state("networkidle", timeout=timeout)

            # Check for DataDome challenge
            is_blocked = self.check_datadome_challenge(page)
            if is_blocked:
                print("DataDome challenge detected, attempting to solve...")
                return self.handle_datadome_challenge(page)

            return True
        except Exception as e:
            print(f"Page load error: {e}")
            return False

    def check_datadome_challenge(self, page) -> bool:
        """
        Check if page contains DataDome challenge.

        Args:
            page: Camoufox page object

        Returns:
            True if DataDome challenge detected
        """
        try:
            # Check for common DataDome indicators
            indicators = [
                "geo.captcha-delivery.com",
                "datadome.co",
                "dd-captcha",
                "DataDome",
                "Checking your browser"
            ]

            page_content = page.content()
            for indicator in indicators:
                if indicator in page_content:
                    return True

            # Check for DataDome JavaScript
            scripts = page.query_selector_all("script")
            for script in scripts:
                src = script.get_attribute("src")
                if src and "datadome" in src.lower():
                    return True

            return False
        except Exception as e:
            print(f"Error checking DataDome challenge: {e}")
            return False

    def handle_datadome_challenge(self, page, max_wait: int = 60) -> bool:
        """
        Attempt to handle DataDome challenge automatically.

        Args:
            page: Camoufox page object
            max_wait: Maximum time to wait for challenge resolution in seconds

        Returns:
            True if challenge was resolved
        """
        try:
            print("Waiting for DataDome challenge to resolve...")

            # Simulate human behavior while waiting
            start_time = time.time()
            while time.time() - start_time < max_wait:
                # Small random movements and scrolls
                self.human_like_mouse_movement(page)
                self.random_scroll(page)
                self.random_delay(2, 4)

                # Check if challenge is still present
                if not self.check_datadome_challenge(page):
                    print("DataDome challenge resolved!")
                    return True

            print("Failed to resolve DataDome challenge within timeout")
            return False

        except Exception as e:
            print(f"Error handling DataDome challenge: {e}")
            return False

    def get_stealth_config(self) -> dict:
        """
        Get recommended Camoufox configuration for maximum stealth.

        Returns:
            Dictionary of Camoufox configuration options
        """
        return {
            # Randomize fingerprint
            "humanize": True,
            # Add random delays
            "geoip": True,
            # Mimic real browser behavior
            "exclude_addons": [],
            # Custom headers
            "default_args": [
                "--disable-blink-features=AutomationControlled"
            ]
        }

    def add_realistic_headers(self, page) -> None:
        """
        Add realistic browser headers to requests.

        Args:
            page: Camoufox page object
        """
        try:
            headers = {
                "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1"
            }

            page.set_extra_http_headers(headers)
        except Exception as e:
            print(f"Error setting headers: {e}")
