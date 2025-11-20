"""
SNCF Price Scraper package.

This package provides tools for scraping train ticket prices from SNCF Connect
while bypassing DataDome anti-bot protection.
"""

from .scraper import SNCFScraper
from .datadome import DataDomeBypass
from .parser import PriceParser

__version__ = "0.1.0"
__all__ = ["SNCFScraper", "DataDomeBypass", "PriceParser"]
