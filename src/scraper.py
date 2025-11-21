"""
Main web scraper for SNCF train ticket prices.

This module implements the core scraping functionality using Camoufox to bypass
DataDome protection and extract price information from SNCF Connect website.
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, List, Optional

from camoufox.sync_api import Camoufox

from datadome import DataDomeBypass
from datadome_advanced import AdvancedDataDomeBypass
from parser import PriceParser


class SNCFScraper:
    """Main scraper class for SNCF train ticket prices."""

    def __init__(self, headless: bool = False, debug: bool = False, use_advanced: bool = True,
                 session_name: str = "default", proxy: Optional[str] = None):
        """
        Initialize the SNCF scraper.

        Args:
            headless: Run browser in headless mode (not recommended for DataDome)
            debug: Enable debug logging
            use_advanced: Use advanced DataDome bypass techniques (recommended)
            session_name: Name for session persistence
            proxy: Proxy server URL (e.g., "http://proxy:port")
        """
        self.base_url = "https://www.sncf-connect.com"
        self.headless = headless
        self.debug = debug
        self.use_advanced = use_advanced
        self.session_name = session_name
        self.proxy = proxy

        # Choose bypass strategy
        if use_advanced:
            self.datadome_bypass = AdvancedDataDomeBypass()
        else:
            self.datadome_bypass = DataDomeBypass()

        self.parser = PriceParser()
        self.results = []

    def log(self, message: str) -> None:
        """
        Log debug messages.

        Args:
            message: Message to log
        """
        if self.debug:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] {message}")

    def initialize_browser(self) -> Camoufox:
        """
        Initialize Camoufox browser with advanced anti-detection settings.

        Returns:
            Configured Camoufox browser instance
        """
        self.log("🚀 Initializing Camoufox browser with advanced stealth...")

        # Get stealth configuration
        if self.use_advanced:
            config = self.datadome_bypass.get_advanced_stealth_config()
        else:
            config = self.datadome_bypass.get_stealth_config()

        # Build browser arguments
        browser_args = {
            "headless": self.headless,
            "humanize": config.get("humanize", True),
            "geoip": config.get("geoip", True),
        }

        # Add proxy if configured
        if self.proxy:
            browser_args["proxy"] = {"server": self.proxy}
            self.log(f"  Using proxy: {self.proxy}")

        # Initialize browser with anti-detection features
        browser = Camoufox(**browser_args)

        self.log("✓ Browser initialized successfully")
        return browser

    def navigate_to_homepage(self, page) -> bool:
        """
        Navigate to SNCF Connect homepage with advanced anti-detection.

        Args:
            page: Camoufox page object

        Returns:
            True if navigation successful
        """
        try:
            self.log(f"🌐 Navigating to {self.base_url}...")

            # Inject fingerprint spoofing (advanced mode only)
            if self.use_advanced:
                self.log("  Injecting fingerprint spoofing scripts...")
                self.datadome_bypass.inject_fingerprint_spoofing(page)

            # Try to load cookies from previous session
            if self.use_advanced:
                if self.datadome_bypass.load_cookies(page, self.session_name):
                    self.log("  Loaded cookies from previous session")

            # Add realistic headers
            if self.use_advanced:
                headers = self.datadome_bypass.get_realistic_headers()
                page.set_extra_http_headers(headers)
            else:
                self.datadome_bypass.add_realistic_headers(page)

            # Set randomized viewport (advanced mode only)
            if self.use_advanced:
                viewport = self.datadome_bypass.randomize_viewport()
                page.set_viewport_size(viewport)
                self.log(f"  Viewport: {viewport['width']}x{viewport['height']}")

            # Navigate to homepage
            page.goto(self.base_url, wait_until="domcontentloaded", timeout=30000)

            # Wait for page to load and check for DataDome
            if not self.datadome_bypass.wait_for_page_load(page):
                self.log("✗ Failed to bypass DataDome on homepage")
                return False

            # Simulate human behavior
            if self.use_advanced:
                self.datadome_bypass.gaussian_delay(2, 4)
                self.datadome_bypass.human_like_mouse_movement(page)
                self.datadome_bypass.random_scroll_with_inertia(page)
            else:
                self.datadome_bypass.random_delay(2, 4)
                self.datadome_bypass.human_like_mouse_movement(page)
                self.datadome_bypass.random_scroll(page)

            # Save cookies for future sessions
            if self.use_advanced:
                self.datadome_bypass.save_cookies(page, self.session_name)

            self.log("✓ Successfully loaded homepage")
            return True

        except Exception as e:
            self.log(f"✗ Error navigating to homepage: {e}")
            return False

    def search_route(
        self,
        page,
        origin: str,
        destination: str,
        date: str,
        passengers: int = 1
    ) -> bool:
        """
        Search for train routes between origin and destination.

        Args:
            page: Camoufox page object
            origin: Departure station
            destination: Arrival station
            date: Travel date (format: YYYY-MM-DD)
            passengers: Number of passengers

        Returns:
            True if search successful
        """
        try:
            self.log(f"Searching route: {origin} -> {destination} on {date}")

            # Wait for search form to be visible
            page.wait_for_selector("input[placeholder*='Départ'], input[placeholder*='départ'], input[name='origin']", timeout=10000)

            # Fill origin
            self.log("Filling origin field...")
            origin_input = page.query_selector("input[placeholder*='Départ'], input[placeholder*='départ'], input[name='origin']")
            if origin_input:
                origin_input.click()
                if self.use_advanced:
                    self.datadome_bypass.gaussian_delay(0.5, 1)
                    # Type character by character with realistic timing
                    for char in origin:
                        page.keyboard.type(char)
                        time.sleep(self.datadome_bypass.human_typing_delay())
                else:
                    self.datadome_bypass.random_delay(0.5, 1)
                    origin_input.fill(origin)

                if self.use_advanced:
                    self.datadome_bypass.gaussian_delay(1, 2)
                else:
                    self.datadome_bypass.random_delay(1, 2)

                # Wait for autocomplete and select first option
                page.wait_for_selector("li[role='option'], .autocomplete-item", timeout=5000)
                if self.use_advanced:
                    self.datadome_bypass.gaussian_delay(0.5, 1)
                else:
                    self.datadome_bypass.random_delay(0.5, 1)
                page.keyboard.press("ArrowDown")
                time.sleep(self.datadome_bypass.human_typing_delay() if self.use_advanced else random.uniform(0.3, 0.6))
                page.keyboard.press("Enter")

            # Fill destination
            self.log("Filling destination field...")
            if self.use_advanced:
                self.datadome_bypass.gaussian_delay(1, 2)
            else:
                self.datadome_bypass.random_delay(1, 2)

            dest_input = page.query_selector("input[placeholder*='Arrivée'], input[placeholder*='arrivée'], input[name='destination']")
            if dest_input:
                dest_input.click()
                if self.use_advanced:
                    self.datadome_bypass.gaussian_delay(0.5, 1)
                    # Type character by character with realistic timing
                    for char in destination:
                        page.keyboard.type(char)
                        time.sleep(self.datadome_bypass.human_typing_delay())
                else:
                    self.datadome_bypass.random_delay(0.5, 1)
                    dest_input.fill(destination)

                if self.use_advanced:
                    self.datadome_bypass.gaussian_delay(1, 2)
                else:
                    self.datadome_bypass.random_delay(1, 2)

                # Wait for autocomplete and select first option
                page.wait_for_selector("li[role='option'], .autocomplete-item", timeout=5000)
                if self.use_advanced:
                    self.datadome_bypass.gaussian_delay(0.5, 1)
                else:
                    self.datadome_bypass.random_delay(0.5, 1)
                page.keyboard.press("ArrowDown")
                time.sleep(self.datadome_bypass.human_typing_delay() if self.use_advanced else random.uniform(0.3, 0.6))
                page.keyboard.press("Enter")

            # Fill date if date picker is available
            self.log("Setting travel date...")
            self.datadome_bypass.random_delay(1, 2)

            # Submit search
            self.log("Submitting search...")
            search_button = page.query_selector("button[type='submit'], button:has-text('Rechercher'), button:has-text('Chercher')")
            if search_button:
                self.datadome_bypass.random_delay(0.5, 1.5)
                search_button.click()

                # Wait for results to load
                self.log("Waiting for search results...")
                if not self.datadome_bypass.wait_for_page_load(page, timeout=45000):
                    self.log("Failed to load search results (possible DataDome block)")
                    return False

                # Additional wait for results to render
                self.datadome_bypass.random_delay(3, 5)
                return True
            else:
                self.log("Could not find search button")
                return False

        except Exception as e:
            self.log(f"Error during search: {e}")
            return False

    def extract_prices(self, page) -> List[Dict]:
        """
        Extract price information from search results.

        Args:
            page: Camoufox page object

        Returns:
            List of price dictionaries
        """
        try:
            self.log("Extracting prices from page...")

            # Get page content
            html_content = page.content()

            # Parse prices using parser module
            prices = self.parser.parse_prices(html_content)

            self.log(f"Extracted {len(prices)} price entries")
            return prices

        except Exception as e:
            self.log(f"Error extracting prices: {e}")
            return []

    def save_results(self, filename: str = "prices.json") -> None:
        """
        Save scraped results to JSON file.

        Args:
            filename: Output filename
        """
        try:
            # Create data directory if it doesn't exist
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
            os.makedirs(data_dir, exist_ok=True)

            # Full path to output file
            filepath = os.path.join(data_dir, filename)

            # Add metadata
            output = {
                "scrape_time": datetime.now().isoformat(),
                "total_results": len(self.results),
                "results": self.results
            }

            # Write to file
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2, ensure_ascii=False)

            self.log(f"Results saved to {filepath}")

        except Exception as e:
            self.log(f"Error saving results: {e}")

    def scrape(
        self,
        origin: str,
        destination: str,
        date: str,
        passengers: int = 1
    ) -> List[Dict]:
        """
        Main scraping method.

        Args:
            origin: Departure station
            destination: Arrival station
            date: Travel date (format: YYYY-MM-DD)
            passengers: Number of passengers

        Returns:
            List of scraped price data
        """
        self.log("=" * 60)
        self.log("Starting SNCF price scraper")
        self.log("=" * 60)

        try:
            with self.initialize_browser() as browser:
                page = browser.new_page()

                # Navigate to homepage
                if not self.navigate_to_homepage(page):
                    self.log("Failed to load homepage, aborting...")
                    return []

                # Search for route
                if not self.search_route(page, origin, destination, date, passengers):
                    self.log("Failed to search route, aborting...")
                    return []

                # Extract prices
                prices = self.extract_prices(page)
                self.results = prices

                # Save screenshot for debugging
                if self.debug:
                    screenshot_path = os.path.join(
                        os.path.dirname(os.path.dirname(__file__)),
                        "data",
                        f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    )
                    page.screenshot(path=screenshot_path)
                    self.log(f"Screenshot saved to {screenshot_path}")

                # Save results
                self.save_results()

                self.log("=" * 60)
                self.log(f"Scraping completed! Found {len(prices)} results")
                self.log("=" * 60)

                return prices

        except Exception as e:
            self.log(f"Fatal error during scraping: {e}")
            import traceback
            if self.debug:
                traceback.print_exc()
            return []


def main():
    """Main entry point for the scraper."""
    # Example usage
    scraper = SNCFScraper(headless=False, debug=True)

    # Example search: Paris to Lyon
    results = scraper.scrape(
        origin="Paris",
        destination="Lyon",
        date="2024-12-01",
        passengers=1
    )

    print(f"\nFound {len(results)} train options")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result}")


if __name__ == "__main__":
    main()
