"""
SNCF Price Scraper package.

This package provides tools for scraping train ticket prices from SNCF Connect
while bypassing DataDome anti-bot protection using advanced anti-detection techniques.
"""

from .scraper import SNCFScraper
from .datadome import DataDomeBypass
from .datadome_advanced import AdvancedDataDomeBypass
from .parser import PriceParser

__version__ = "0.2.0"
__all__ = ["SNCFScraper", "DataDomeBypass", "AdvancedDataDomeBypass", "PriceParser"]
