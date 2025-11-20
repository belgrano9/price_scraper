#!/usr/bin/env python3
"""
Advanced example script demonstrating cutting-edge DataDome bypass techniques.

This script showcases the most advanced anti-detection methods including:
- Bezier curve mouse movements
- Canvas/WebGL/Audio fingerprint spoofing
- Gaussian timing delays
- Character-by-character typing with realistic delays
- Cookie/session persistence
- Viewport randomization
"""

import sys
from datetime import datetime, timedelta
from src.scraper import SNCFScraper


def print_header():
    """Print fancy header."""
    print("=" * 80)
    print("🚀 SNCF Price Scraper - ADVANCED MODE")
    print("=" * 80)
    print()
    print("This advanced mode includes state-of-the-art DataDome bypass techniques:")
    print()
    print("✓ Bezier curve mouse movements (human-like paths)")
    print("✓ Canvas/WebGL/Audio fingerprint spoofing")
    print("✓ Gaussian distribution timing (realistic delays)")
    print("✓ Character-by-character typing simulation")
    print("✓ Cookie and session persistence")
    print("✓ Randomized viewport dimensions")
    print("✓ Advanced behavioral patterns (scrolling with inertia)")
    print("✓ Enhanced DataDome challenge detection")
    print()
    print("=" * 80)
    print()


def print_config(config: dict):
    """Print configuration."""
    print("Configuration:")
    print(f"  Origin:       {config['origin']}")
    print(f"  Destination:  {config['destination']}")
    print(f"  Date:         {config['date']}")
    print(f"  Passengers:   {config['passengers']}")
    print(f"  Advanced:     {config['advanced']}")
    print(f"  Session:      {config['session_name']}")
    print(f"  Proxy:        {config['proxy'] or 'None'}")
    print()
    print("=" * 80)
    print()


def main():
    """Run advanced scraping session."""
    print_header()

    # ==================== CONFIGURATION ====================

    # Search parameters
    config = {
        "origin": "Paris",
        "destination": "Lyon",
        "date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "passengers": 1,
        "advanced": True,  # Enable advanced bypass techniques
        "session_name": "sncf_session_1",  # Session name for cookie persistence
        "proxy": None,  # Set to "http://proxy:port" if using a proxy
    }

    print_config(config)

    # ==================== INITIALIZATION ====================

    print("🔧 Initializing scraper with advanced settings...")
    print()

    try:
        scraper = SNCFScraper(
            headless=False,  # Keep visible for better success rate
            debug=True,  # Enable detailed logging
            use_advanced=config["advanced"],  # Use advanced bypass techniques
            session_name=config["session_name"],  # Session for cookie persistence
            proxy=config["proxy"]  # Optional proxy
        )

        print("✓ Scraper initialized")
        print()
        print("=" * 80)
        print()

        # ==================== SCRAPING ====================

        print("🎯 Starting scraping process...")
        print()
        print("The browser will:")
        print("  1. Open with randomized fingerprints")
        print("  2. Navigate to SNCF Connect")
        print("  3. Inject anti-detection scripts")
        print("  4. Load cookies from previous sessions (if any)")
        print("  5. Search for trains using human-like behavior")
        print("  6. Extract and save price data")
        print()
        print("⏱️  This may take 30-90 seconds depending on DataDome checks...")
        print()
        print("=" * 80)
        print()

        results = scraper.scrape(
            origin=config["origin"],
            destination=config["destination"],
            date=config["date"],
            passengers=config["passengers"]
        )

        # ==================== RESULTS ====================

        print()
        print("=" * 80)
        print("📊 RESULTS")
        print("=" * 80)
        print()

        if results:
            print(f"✓ Successfully found {len(results)} train options!")
            print()

            # Sort by price
            sorted_results = sorted(results, key=lambda x: x.get('price', float('inf')))

            for i, train in enumerate(sorted_results, 1):
                print(f"🚄 Option {i}")
                print(f"   {'─' * 60}")
                print(f"   Departure:    {train.get('departure_time', 'N/A')}")
                print(f"   Arrival:      {train.get('arrival_time', 'N/A')}")
                print(f"   Duration:     {train.get('duration', 'N/A')}")
                print(f"   💶 Price:     {train.get('price', 'N/A')}€")
                print(f"   Train Type:   {train.get('train_type', 'N/A')}")

                connections = train.get('connections', 'N/A')
                if connections == 0:
                    print(f"   ✓ Direct train (no changes)")
                else:
                    print(f"   Connections:  {connections}")

                if train.get('train_number'):
                    print(f"   Train #:      {train.get('train_number')}")
                if train.get('fare_class'):
                    print(f"   Class:        {train.get('fare_class')}")
                print()

            # Show cheapest option
            cheapest = sorted_results[0]
            print("=" * 80)
            print("💰 BEST DEAL")
            print("=" * 80)
            print(f"Cheapest option: {cheapest.get('price', 'N/A')}€")
            print(f"  {cheapest.get('departure_time', 'N/A')} → {cheapest.get('arrival_time', 'N/A')}")
            print(f"  Duration: {cheapest.get('duration', 'N/A')}")
            print(f"  Train: {cheapest.get('train_type', 'N/A')}")
            print()

            # Data saved location
            print("=" * 80)
            print("💾 Data saved to: data/prices.json")
            print("🍪 Cookies saved for next session!")
            print("=" * 80)
            print()

        else:
            print("✗ No results found")
            print()
            print("Possible reasons:")
            print("  • DataDome challenge not resolved")
            print("  • Website structure changed")
            print("  • Network issues")
            print("  • Invalid search parameters")
            print("  • No trains available for this route/date")
            print()
            print("📸 Check debug screenshots in data/ directory")
            print()
            print("💡 Tips to improve success rate:")
            print("  • Make sure you have a stable internet connection")
            print("  • Try using a residential proxy")
            print("  • Run the script multiple times (cookies help!)")
            print("  • Increase timeout values if your connection is slow")
            print()
            print("=" * 80)
            print()

    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user")
        print("=" * 80)
        sys.exit(0)

    except Exception as e:
        print(f"\n\n✗ Error during scraping: {e}")
        print()
        import traceback
        traceback.print_exc()
        print()
        print("=" * 80)
        sys.exit(1)

    print()
    print("=" * 80)
    print("✓ Scraping completed successfully!")
    print("=" * 80)
    print()
    print("Next steps:")
    print("  • Run again to test cookie persistence")
    print("  • Try different routes and dates")
    print("  • Integrate into your price monitoring system")
    print()


if __name__ == "__main__":
    main()
