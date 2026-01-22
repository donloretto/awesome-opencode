"""
Shared utility functions for the flight price analyzer.
Provides logging, currency conversion, formatting, and helper functions.
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import hashlib
import random
import time
from pathlib import Path
from urllib.parse import urlencode


class FlightLogger:
    """Custom logger for flight price analyzer."""

    def __init__(self, name: str = "FlightAnalyzer", log_file: str = "flight_analyzer.log"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # File handler
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def info(self, message: str):
        self.logger.info(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)


class CurrencyConverter:
    """Currency conversion utility."""

    # Exchange rates (sample rates - in production, fetch from API)
    RATES = {
        'EUR': 1.0,
        'USD': 1.08,
        'GBP': 0.86,
        'CHF': 0.94,
        'CAD': 1.46,
        'AUD': 1.66,
        'JPY': 158.50,
        'CNY': 7.82,
        'INR': 89.75,
        'AED': 3.97,
        'THB': 36.50,
    }

    @classmethod
    def convert(cls, amount: float, from_currency: str, to_currency: str = 'EUR') -> float:
        """Convert amount from one currency to another."""
        if from_currency not in cls.RATES or to_currency not in cls.RATES:
            return amount

        # Convert to EUR first, then to target currency
        eur_amount = amount / cls.RATES[from_currency]
        return eur_amount * cls.RATES[to_currency]

    @classmethod
    def format_price(cls, amount: float, currency: str = 'EUR') -> str:
        """Format price with currency symbol."""
        symbols = {
            'EUR': '€',
            'USD': '$',
            'GBP': '£',
            'CHF': 'CHF',
            'CAD': 'CAD',
            'AUD': 'AUD',
            'JPY': '¥',
            'CNY': '¥',
            'INR': '₹',
            'AED': 'AED',
            'THB': '฿',
        }
        symbol = symbols.get(currency, currency)
        return f"{symbol}{amount:.2f}"


class AirportHelper:
    """Airport and route utilities with comprehensive worldwide airport database."""

    AIRPORTS = None  # Will be loaded from JSON
    _airports_loaded = False

    # Nearby airports mapping
    NEARBY_AIRPORTS = {
        'FRA': ['MUC', 'STR', 'CGN', 'DUS'],
        'MUC': ['FRA', 'STR', 'VIE'],
        'BER': ['HAM', 'DUS', 'FRA'],
        'JFK': ['EWR', 'LGA'],
        'LHR': ['LGW', 'STN', 'LTN'],
        'CDG': ['ORY'],
        'DXB': ['AUH'],
        'IST': ['SAW'],
        'NYC': ['JFK', 'LGA', 'EWR'],
        'LON': ['LHR', 'LGW', 'STN', 'LTN', 'LCY'],
        'PAR': ['CDG', 'ORY'],
        'MIL': ['MXP', 'LIN'],
        'ROM': ['FCO', 'CIA'],
        'BER': ['BER', 'SXF', 'TXL'],
        'SHA': ['PVG', 'SHA'],
        'TOK': ['NRT', 'HND'],
        'BUE': ['EZE', 'AEP'],
    }

    @classmethod
    def _load_airports(cls):
        """Load airport database from JSON file."""
        if cls._airports_loaded:
            return

        try:
            # Try to load from data directory
            data_dir = Path(__file__).parent.parent / 'data'
            airports_file = data_dir / 'airports.json'

            if airports_file.exists():
                with open(airports_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    cls.AIRPORTS = data.get('airports', {})
                    cls._airports_loaded = True
            else:
                # Fallback to basic airports
                cls.AIRPORTS = {
                    'FRA': {'city': 'Frankfurt', 'country': 'DE', 'name': 'Frankfurt Airport', 'region': 'Europe'},
                    'JFK': {'city': 'New York', 'country': 'US', 'name': 'John F. Kennedy Intl', 'region': 'North America'},
                }
                cls._airports_loaded = True
        except Exception as e:
            # Fallback to basic airports
            cls.AIRPORTS = {
                'FRA': {'city': 'Frankfurt', 'country': 'DE', 'name': 'Frankfurt Airport', 'region': 'Europe'},
                'JFK': {'city': 'New York', 'country': 'US', 'name': 'John F. Kennedy Intl', 'region': 'North America'},
            }
            cls._airports_loaded = True

    @classmethod
    def get_airport_info(cls, code: str) -> Optional[Dict[str, str]]:
        """Get airport information."""
        cls._load_airports()
        return cls.AIRPORTS.get(code.upper())

    @classmethod
    def get_nearby_airports(cls, code: str) -> List[str]:
        """Get list of nearby airports."""
        return cls.NEARBY_AIRPORTS.get(code.upper(), [])

    @classmethod
    def get_all_airports(cls) -> Dict[str, Dict[str, str]]:
        """Get all airports in the database."""
        cls._load_airports()
        return cls.AIRPORTS

    @classmethod
    def search_airports(cls, query: str) -> List[Dict[str, Any]]:
        """Search airports by code, city, or name."""
        cls._load_airports()
        query = query.upper()
        results = []

        for code, info in cls.AIRPORTS.items():
            if (query in code or
                query in info.get('city', '').upper() or
                query in info.get('name', '').upper()):
                results.append({
                    'code': code,
                    **info
                })

        return results[:10]  # Return top 10 matches

    @classmethod
    def format_route(cls, origin: str, destination: str) -> str:
        """Format route as readable string."""
        origin_info = cls.get_airport_info(origin)
        dest_info = cls.get_airport_info(destination)

        origin_name = origin_info['city'] if origin_info else origin
        dest_name = dest_info['city'] if dest_info else destination

        return f"{origin_name} ({origin}) → {dest_name} ({destination})"


class DateHelper:
    """Date and time utilities."""

    @staticmethod
    def parse_date(date_str: str) -> datetime:
        """Parse date string to datetime object."""
        formats = ['%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y']
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        raise ValueError(f"Unable to parse date: {date_str}")

    @staticmethod
    def format_date(date_obj: datetime, format_str: str = '%Y-%m-%d') -> str:
        """Format datetime object to string."""
        return date_obj.strftime(format_str)

    @staticmethod
    def get_date_range(start_date: datetime, days: int = 7) -> List[datetime]:
        """Get list of dates in range."""
        return [start_date + timedelta(days=i) for i in range(days)]

    @staticmethod
    def get_optimal_booking_window(departure_date: datetime) -> Dict[str, Any]:
        """Calculate optimal booking window based on departure date."""
        today = datetime.now()
        days_until_departure = (departure_date - today).days

        # General rules for booking windows
        if days_until_departure > 180:
            return {
                'status': 'too_early',
                'recommendation': 'Wait until 2-3 months before departure',
                'optimal_days_before': [60, 90]
            }
        elif days_until_departure > 90:
            return {
                'status': 'good',
                'recommendation': 'Good time to book, prices stable',
                'optimal_days_before': [60, 90]
            }
        elif days_until_departure > 21:
            return {
                'status': 'optimal',
                'recommendation': 'Optimal booking window',
                'optimal_days_before': [21, 90]
            }
        elif days_until_departure > 7:
            return {
                'status': 'late',
                'recommendation': 'Book soon, prices may increase',
                'optimal_days_before': [7, 21]
            }
        else:
            return {
                'status': 'very_late',
                'recommendation': 'Last minute - expect high prices',
                'optimal_days_before': [0, 7]
            }


class RequestHelper:
    """HTTP request utilities for avoiding detection."""

    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    ]

    @classmethod
    def get_random_user_agent(cls) -> str:
        """Get random user agent string."""
        return random.choice(cls.USER_AGENTS)

    @staticmethod
    def generate_session_id() -> str:
        """Generate unique session ID."""
        timestamp = str(time.time())
        random_str = str(random.random())
        return hashlib.md5(f"{timestamp}{random_str}".encode()).hexdigest()

    @staticmethod
    def calculate_delay(base_delay: float = 2.0, jitter: float = 1.0) -> float:
        """Calculate random delay to avoid detection."""
        return base_delay + random.uniform(0, jitter)

    @classmethod
    def get_safe_headers(cls, referer: Optional[str] = None) -> Dict[str, str]:
        """Get headers that minimize tracking."""
        headers = {
            'User-Agent': cls.get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'de-DE,de;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        if referer:
            headers['Referer'] = referer
        return headers


class DataCache:
    """Simple in-memory cache for API responses."""

    def __init__(self, ttl: int = 3600):
        self.cache = {}
        self.ttl = ttl  # Time to live in seconds

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return data
            else:
                del self.cache[key]
        return None

    def set(self, key: str, value: Any):
        """Set value in cache."""
        self.cache[key] = (value, time.time())

    def clear(self):
        """Clear all cache."""
        self.cache.clear()

    def generate_key(self, *args) -> str:
        """Generate cache key from arguments."""
        key_str = '_'.join(str(arg) for arg in args)
        return hashlib.md5(key_str.encode()).hexdigest()


def format_duration(minutes: int) -> str:
    """Format flight duration."""
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m"


def calculate_price_difference(price1: float, price2: float) -> Dict[str, Any]:
    """Calculate price difference and percentage."""
    diff = price1 - price2
    percent = (diff / price2 * 100) if price2 > 0 else 0
    return {
        'absolute': diff,
        'percentage': percent,
        'cheaper': price1 < price2
    }


def validate_airport_code(code: str) -> bool:
    """Validate airport IATA code."""
    return len(code) == 3 and code.isalpha()


def validate_date_format(date_str: str) -> bool:
    """Validate date string format."""
    try:
        DateHelper.parse_date(date_str)
        return True
    except ValueError:
        return False


class BookingLinkGenerator:
    """Generate booking links for various flight search platforms."""

    @staticmethod
    def format_date_for_url(date_obj: datetime, format_type: str = 'standard') -> str:
        """Format date for URL based on platform requirements."""
        if format_type == 'standard':
            return date_obj.strftime('%Y-%m-%d')
        elif format_type == 'compact':
            return date_obj.strftime('%Y%m%d')
        else:
            return date_obj.strftime('%Y-%m-%d')

    @classmethod
    def google_flights(cls, origin: str, destination: str, departure_date: datetime,
                      return_date: Optional[datetime] = None) -> str:
        """Generate Google Flights search URL."""
        base_url = "https://www.google.com/travel/flights"

        # Format: /flights?q=Flights%20from%20FRA%20to%20JFK%20on%202026-03-15
        if return_date:
            date_str = f"{cls.format_date_for_url(departure_date)}%20return%20{cls.format_date_for_url(return_date)}"
        else:
            date_str = cls.format_date_for_url(departure_date)

        query = f"Flights from {origin} to {destination} on {date_str}"
        params = {'q': query}

        return f"{base_url}?{urlencode(params)}"

    @classmethod
    def skyscanner(cls, origin: str, destination: str, departure_date: datetime,
                   return_date: Optional[datetime] = None) -> str:
        """Generate Skyscanner search URL."""
        base_url = "https://www.skyscanner.com/transport/flights"

        dep_date = cls.format_date_for_url(departure_date, 'compact')

        if return_date:
            ret_date = cls.format_date_for_url(return_date, 'compact')
            # Format: /FRA/JFK/260315/260322
            url = f"{base_url}/{origin}/{destination}/{dep_date[2:]}/{ret_date[2:]}"
        else:
            # One-way: /FRA/JFK/260315
            url = f"{base_url}/{origin}/{destination}/{dep_date[2:]}"

        return url

    @classmethod
    def kayak(cls, origin: str, destination: str, departure_date: datetime,
             return_date: Optional[datetime] = None, adults: int = 1) -> str:
        """Generate Kayak search URL."""
        base_url = "https://www.kayak.com/flights"

        dep_date = cls.format_date_for_url(departure_date)

        if return_date:
            ret_date = cls.format_date_for_url(return_date)
            # Format: /FRA-JFK/2026-03-15/2026-03-22/1adults
            url = f"{base_url}/{origin}-{destination}/{dep_date}/{ret_date}/{adults}adults"
        else:
            # One-way: /FRA-JFK/2026-03-15/1adults
            url = f"{base_url}/{origin}-{destination}/{dep_date}/{adults}adults"

        return url

    @classmethod
    def momondo(cls, origin: str, destination: str, departure_date: datetime,
               return_date: Optional[datetime] = None) -> str:
        """Generate Momondo search URL."""
        base_url = "https://www.momondo.com/flight-search"

        dep_date = cls.format_date_for_url(departure_date)

        if return_date:
            ret_date = cls.format_date_for_url(return_date)
            url = f"{base_url}/{origin}-{destination}/{dep_date}/{ret_date}"
        else:
            url = f"{base_url}/{origin}-{destination}/{dep_date}"

        return url

    @classmethod
    def kiwi(cls, origin: str, destination: str, departure_date: datetime,
            return_date: Optional[datetime] = None) -> str:
        """Generate Kiwi.com search URL."""
        base_url = "https://www.kiwi.com/en/search"

        params = {
            'sort': 'price',
            'aTime': '00:00',
            'dTime': '00:00',
            'origin': origin,
            'destination': destination,
            'departure': cls.format_date_for_url(departure_date, 'compact')
        }

        if return_date:
            params['return'] = cls.format_date_for_url(return_date, 'compact')

        return f"{base_url}?{urlencode(params)}"

    @classmethod
    def expedia(cls, origin: str, destination: str, departure_date: datetime,
               return_date: Optional[datetime] = None) -> str:
        """Generate Expedia search URL."""
        base_url = "https://www.expedia.com/Flights-Search"

        params = {
            'trip': 'roundtrip' if return_date else 'oneway',
            'leg1': f'from:{origin},to:{destination},departure:{cls.format_date_for_url(departure_date, "compact")}'
        }

        if return_date:
            params['leg2'] = f'from:{destination},to:{origin},departure:{cls.format_date_for_url(return_date, "compact")}'

        return f"{base_url}?{urlencode(params)}"

    @classmethod
    def generate_all_links(cls, origin: str, destination: str, departure_date: datetime,
                          return_date: Optional[datetime] = None) -> Dict[str, str]:
        """Generate booking links for all supported platforms."""
        return {
            'google_flights': cls.google_flights(origin, destination, departure_date, return_date),
            'skyscanner': cls.skyscanner(origin, destination, departure_date, return_date),
            'kayak': cls.kayak(origin, destination, departure_date, return_date),
            'momondo': cls.momondo(origin, destination, departure_date, return_date),
            'kiwi': cls.kiwi(origin, destination, departure_date, return_date),
            'expedia': cls.expedia(origin, destination, departure_date, return_date)
        }

    @classmethod
    def get_platform_display_names(cls) -> Dict[str, str]:
        """Get user-friendly display names for platforms."""
        return {
            'google_flights': 'Google Flights',
            'skyscanner': 'Skyscanner',
            'kayak': 'Kayak',
            'momondo': 'Momondo',
            'kiwi': 'Kiwi.com',
            'expedia': 'Expedia'
        }
