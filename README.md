# SNCF Price Scraper

A web scraping project designed to extract train ticket prices from SNCF's website while bypassing DataDome anti-bot protection.

> **⚠️ EDUCATIONAL PURPOSES ONLY**
>
> This project is intended solely for educational and research purposes to understand web scraping techniques and anti-bot detection mechanisms. Users must comply with all applicable laws and terms of service.

## Overview

This project aims to scrape train ticket prices from the SNCF (French National Railway Company) website. The main challenge is defeating DataDome, a sophisticated bot detection and mitigation service that protects the SNCF website.

## Objective

**Primary Goal**: Successfully scrape train ticket prices from SNCF's web platform while evading DataDome's detection mechanisms.

### Challenges

- **DataDome Protection**: SNCF uses DataDome as a proxy/WAF to detect and block automated requests
- **Advanced Detection**: DataDome employs multiple detection techniques including:
  - Browser fingerprinting
  - Behavioral analysis
  - TLS fingerprinting
  - JavaScript challenges
  - Device profiling

## Technology Stack

### Camoufox

This project uses **Camoufox**, a Python library that provides Firefox-based browser automation with built-in anti-detection features.

**Why Camoufox?**

- Built on Firefox with anti-fingerprinting patches
- Randomizes browser fingerprints
- Mimics human-like behavior
- Better stealth compared to standard Selenium/Playwright
- Actively maintained anti-detection capabilities

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd price_scrapper

# Install dependencies
pip install camoufox

# Additional dependencies (if needed)
pip install -r requirements.txt
```

## Usage

```python
# Example usage (to be implemented)
from camoufox.sync_api import Camoufox

with Camoufox() as browser:
    page = browser.new_page()
    page.goto('https://www.sncf-connect.com')
    # Scraping logic here
```

## Project Structure

```text
price_scrapper/
├── README.md
├── requirements.txt
├── src/
│   ├── scraper.py       # Main scraping logic
│   ├── datadome.py      # DataDome bypass strategies
│   └── parser.py        # Price data parsing
└── data/
    └── prices.json      # Scraped price data
```

## Features (Planned)

- [ ] Initialize Camoufox browser with anti-detection settings
- [ ] Navigate to SNCF website
- [ ] Bypass DataDome challenges
- [ ] Search for train routes
- [ ] Extract price information
- [ ] Store data in structured format
- [ ] Implement retry logic for failed requests
- [ ] Add proxy rotation support

## Legal Disclaimer

⚠️ **Important**: Web scraping may violate the Terms of Service of websites. This project is for educational and research purposes only. Users are responsible for ensuring compliance with:

- SNCF's Terms of Service
- Applicable data protection laws (GDPR, etc.)
- Computer fraud and abuse laws

Always respect:

- robots.txt directives
- Rate limiting
- Website resources

## Contributing

Contributions are welcome! Please ensure all scraping activities are ethical and legal.

## License

This project is for educational purposes only.

## Resources

- [Camoufox Documentation](https://github.com/daijro/camoufox)
- [DataDome Documentation](https://docs.datadome.co/)
- [SNCF Connect](https://www.sncf-connect.com)

## Status

🚧 **Project Status**: In Development

This is an active research project exploring anti-bot detection bypass techniques.
