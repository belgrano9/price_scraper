# Usage Guide - SNCF Price Scraper

This guide provides detailed instructions on how to install, configure, and use the SNCF price scraper.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection
- ~500MB free disk space (for Camoufox browser)

## Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd price_scraper
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: The first time you run the scraper, Camoufox will automatically download a Firefox browser binary (~200MB). This is normal and only happens once.

## Quick Start

The easiest way to get started is to run the example script:

```bash
python example.py
```

This will:
1. Open a Firefox browser window (visible, not headless)
2. Navigate to SNCF Connect website
3. Search for trains from Paris to Lyon for tomorrow
4. Extract and display price information
5. Save results to `data/prices.json`

## Basic Usage

### Import the Scraper

```python
from src.scraper import SNCFScraper

# Initialize scraper
scraper = SNCFScraper(headless=False, debug=True)
```

### Run a Search

```python
results = scraper.scrape(
    origin="Paris",
    destination="Lyon",
    date="2024-12-15",  # Format: YYYY-MM-DD
    passengers=1
)
```

### Process Results

```python
for train in results:
    print(f"Departure: {train['departure_time']}")
    print(f"Arrival: {train['arrival_time']}")
    print(f"Price: {train['price']}€")
    print(f"Duration: {train['duration']}")
    print()
```

## Configuration Options

### SNCFScraper Parameters

```python
scraper = SNCFScraper(
    headless=False,  # Set to True to hide browser window (not recommended for DataDome)
    debug=True       # Enable detailed logging and screenshots
)
```

**Important**:
- `headless=False` is recommended as DataDome can more easily detect headless browsers
- `debug=True` helps troubleshoot issues and saves screenshots to `data/` directory

## Understanding DataDome

DataDome is an advanced bot detection service that protects SNCF's website. It uses:

- **Browser fingerprinting**: Analyzes browser characteristics
- **Behavioral analysis**: Monitors mouse movements, scrolling, timing
- **TLS fingerprinting**: Checks network connection patterns
- **JavaScript challenges**: Tests browser automation detection

### How This Scraper Handles DataDome

1. **Camoufox Browser**: Uses a patched Firefox with anti-fingerprinting features
2. **Human Simulation**: Adds random delays, mouse movements, and scrolling
3. **Realistic Headers**: Sets proper browser headers and user agent
4. **Challenge Detection**: Automatically detects and waits for DataDome challenges
5. **Behavioral Mimicking**: Simulates realistic human browsing patterns

## Troubleshooting

### Issue: "DataDome challenge detected"

**Solution**:
- The scraper will automatically wait up to 60 seconds for the challenge to resolve
- Keep the browser window visible (headless=False)
- Ensure you have a stable internet connection
- Try increasing delays between actions

### Issue: No prices extracted

**Possible causes**:
1. SNCF website structure changed
2. DataDome blocked the request
3. Invalid search parameters
4. No trains available for the selected route/date

**Solutions**:
- Check `data/screenshot_*.png` files to see what the page looked like
- Enable debug mode: `SNCFScraper(debug=True)`
- Try a different route or date
- Check if the website is accessible in a normal browser

### Issue: Browser doesn't open

**Solution**:
```bash
# Reinstall Camoufox
pip uninstall camoufox
pip install camoufox

# Or force browser reinstall
python -c "from camoufox.sync_api import Camoufox; Camoufox()"
```

### Issue: Import errors

**Solution**:
```bash
# Make sure you're in the project root directory
cd price_scraper

# Verify Python can find the src module
python -c "from src.scraper import SNCFScraper; print('OK')"

# If it fails, add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

## Advanced Usage

### Custom Search Parameters

```python
from datetime import datetime, timedelta

# Search for next week
next_week = datetime.now() + timedelta(days=7)
date_str = next_week.strftime("%Y-%m-%d")

scraper = SNCFScraper(headless=False, debug=True)
results = scraper.scrape(
    origin="Marseille",
    destination="Lille",
    date=date_str,
    passengers=2
)
```

### Using Individual Components

You can use the DataDome bypass and parser modules independently:

```python
from src.datadome import DataDomeBypass
from src.parser import PriceParser

# Use DataDome bypass strategies
bypass = DataDomeBypass()
bypass.random_delay(1, 3)

# Parse HTML content
parser = PriceParser()
prices = parser.parse_prices(html_content)
```

### Saving Results to Different Format

```python
import csv

# After scraping
results = scraper.scrape(...)

# Save to CSV
with open('data/prices.csv', 'w', newline='') as f:
    if results:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
```

## Best Practices

### 1. Rate Limiting
Don't make too many requests in a short time:

```python
import time

routes = [("Paris", "Lyon"), ("Lyon", "Marseille")]

for origin, destination in routes:
    results = scraper.scrape(origin, destination, date)
    # Wait between searches
    time.sleep(60)  # Wait 1 minute between searches
```

### 2. Error Handling

```python
try:
    results = scraper.scrape(origin, destination, date)
    if results:
        print(f"Found {len(results)} trains")
    else:
        print("No results - check debug output")
except Exception as e:
    print(f"Error: {e}")
    # Handle error appropriately
```

### 3. Debug Mode During Development

Always use debug mode when testing:

```python
scraper = SNCFScraper(headless=False, debug=True)
```

This provides:
- Detailed console logging
- Screenshots saved to `data/` directory
- Visible browser for monitoring

## Legal and Ethical Considerations

⚠️ **Important Reminders**:

1. **Educational Use Only**: This tool is for learning web scraping techniques
2. **Respect robots.txt**: Check SNCF's robots.txt file
3. **Rate Limiting**: Don't overload SNCF's servers
4. **Terms of Service**: Review SNCF Connect's terms of service
5. **Personal Use**: Don't use scraped data commercially
6. **GDPR Compliance**: Be aware of data protection regulations

## Performance Tips

1. **Use headless=False**: Better success rate against DataDome
2. **Enable debug mode**: Helps identify issues quickly
3. **Stable internet**: Use a reliable connection
4. **Be patient**: DataDome checks can take 10-30 seconds
5. **Regular updates**: Keep Camoufox updated for latest anti-detection features

## Common Routes to Test

Here are some popular routes to test the scraper:

```python
test_routes = [
    ("Paris", "Lyon"),
    ("Paris", "Marseille"),
    ("Lyon", "Nice"),
    ("Paris", "Bordeaux"),
    ("Lille", "Paris"),
]
```

## Output Format

Results are saved in JSON format:

```json
{
  "scrape_time": "2024-11-20T10:30:00",
  "total_results": 5,
  "results": [
    {
      "departure_time": "08:30",
      "arrival_time": "10:45",
      "duration": "2h15",
      "price": 45.50,
      "train_type": "TGV",
      "train_number": "6701",
      "connections": 0,
      "fare_class": "2nd class"
    }
  ]
}
```

## Getting Help

If you encounter issues:

1. Check this USAGE.md guide
2. Enable debug mode and review output
3. Check screenshot files in `data/` directory
4. Review error messages carefully
5. Ensure all dependencies are installed correctly

## Next Steps

- Experiment with different routes and dates
- Customize the parser for additional data extraction
- Implement proxy rotation for larger scale scraping
- Add retry logic for failed requests
- Export data to different formats (CSV, Excel, database)
