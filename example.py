#!/usr/bin/env python3
"""
Example script demonstrating how to use the SNCF price scraper.

This script shows basic usage of the scraper to search for train tickets
between two cities and extract price information.
"""

import sys
from datetime import datetime, timedelta
from src.scraper import SNCFScraper


def main():
    """Run example scraping session."""
    print("=" * 70)
    print("SNCF Price Scraper - Example Usage")
    print("=" * 70)
    print()
    print("This example will:")
    print("1. Initialize a browser with anti-detection features")
    print("2. Navigate to SNCF Connect website")
    print("3. Search for train tickets")
    print("4. Extract and display price information")
    print()
    print("⚠️  Note: The browser will open in visible mode (not headless)")
    print("    This helps bypass DataDome detection.")
    print()
    print("=" * 70)
    print()

    # Configuration
    # You can customize these values
    origin = "Paris"
    destination = "Lyon"

    # Search for tomorrow's date
    tomorrow = datetime.now() + timedelta(days=1)
    travel_date = tomorrow.strftime("%Y-%m-%d")

    passengers = 1

    print(f"Search Parameters:")
    print(f"  Origin:      {origin}")
    print(f"  Destination: {destination}")
    print(f"  Date:        {travel_date}")
    print(f"  Passengers:  {passengers}")
    print()
    print("=" * 70)
    print()

    # Initialize scraper
    # headless=False: Browser window will be visible
    # debug=True: Detailed logging and screenshot capture
    scraper = SNCFScraper(headless=False, debug=True)

    # Run scraper
    try:
        results = scraper.scrape(
            origin=origin,
            destination=destination,
            date=travel_date,
            passengers=passengers
        )

        # Display results
        print()
        print("=" * 70)
        print("RESULTS")
        print("=" * 70)
        print()

        if results:
            print(f"Found {len(results)} train options:\n")

            for i, train in enumerate(results, 1):
                print(f"{i}. Train Option")
                print(f"   Departure:    {train.get('departure_time', 'N/A')}")
                print(f"   Arrival:      {train.get('arrival_time', 'N/A')}")
                print(f"   Duration:     {train.get('duration', 'N/A')}")
                print(f"   Price:        {train.get('price', 'N/A')}€")
                print(f"   Train Type:   {train.get('train_type', 'N/A')}")
                print(f"   Connections:  {train.get('connections', 'N/A')}")
                if train.get('train_number'):
                    print(f"   Train Number: {train.get('train_number')}")
                if train.get('fare_class'):
                    print(f"   Class:        {train.get('fare_class')}")
                print()

            print(f"Results saved to: data/prices.json")
            print()
        else:
            print("No results found.")
            print()
            print("Possible reasons:")
            print("- DataDome blocked the request")
            print("- Website structure has changed")
            print("- Network connectivity issues")
            print("- Invalid search parameters")
            print()
            print("Check the debug output above for more details.")
            print()

    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError during scraping: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("=" * 70)
    print("Scraping completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
