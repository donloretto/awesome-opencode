"""
Geo-pricing simulation module.
Analyzes how flight prices vary across different countries, currencies, and regional markets.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from .utils import FlightLogger, CurrencyConverter


class GeoPricingAnalyzer:
    """
    Analyzes and simulates geo-pricing differences.

    Airlines often charge different prices for the same flight depending on:
    - Booking country/region
    - Currency used
    - Local market conditions
    - Point of sale location
    - User's IP address location
    """

    # Regional pricing multipliers (relative to EU baseline)
    REGIONAL_MULTIPLIERS = {
        'DE': 1.0,   # Germany (baseline)
        'FR': 1.02,  # France
        'GB': 1.15,  # UK - often more expensive
        'US': 1.12,  # USA
        'CH': 1.25,  # Switzerland - typically highest
        'ES': 0.92,  # Spain - often cheaper
        'IT': 0.95,  # Italy
        'NL': 1.05,  # Netherlands
        'PL': 0.85,  # Poland - often cheapest in EU
        'TR': 0.80,  # Turkey
        'IN': 0.75,  # India
        'TH': 0.82,  # Thailand
        'AE': 1.10,  # UAE
        'SG': 1.08,  # Singapore
        'AU': 1.18,  # Australia
        'BR': 0.88,  # Brazil
        'MX': 0.83,  # Mexico
        'AR': 0.79,  # Argentina
    }

    # Currency-specific pricing patterns
    CURRENCY_ADJUSTMENTS = {
        'EUR': 1.0,
        'USD': 0.98,  # Sometimes slightly cheaper when priced in USD
        'GBP': 1.02,  # Often rounded up
        'CHF': 1.01,
        'PLN': 0.96,  # Eastern European currencies often better deals
        'TRY': 0.93,
        'INR': 0.94,
        'THB': 0.95,
        'AED': 1.01,
        'AUD': 1.00,
    }

    def __init__(self, logger: Optional[FlightLogger] = None):
        self.logger = logger or FlightLogger("GeoPricing")
        self.currency_converter = CurrencyConverter()

    def simulate_regional_pricing(
        self,
        base_price: float,
        base_currency: str,
        origin: str,
        destination: str,
        departure_date: datetime
    ) -> List[Dict[str, Any]]:
        """
        Simulate how the same flight is priced in different countries.

        Returns list of prices from different booking locations.
        """
        self.logger.info("Simulating regional pricing differences")

        regional_prices = []

        for country, multiplier in self.REGIONAL_MULTIPLIERS.items():
            # Apply regional multiplier
            regional_price = base_price * multiplier

            # Apply currency-specific adjustment
            local_currency = self._get_country_currency(country)
            currency_adj = self.CURRENCY_ADJUSTMENTS.get(local_currency, 1.0)
            regional_price *= currency_adj

            # Convert to local currency
            price_in_local = self.currency_converter.convert(
                regional_price,
                base_currency,
                local_currency
            )

            # Convert back to EUR for comparison
            price_in_eur = self.currency_converter.convert(
                price_in_local,
                local_currency,
                'EUR'
            )

            regional_prices.append({
                'country': country,
                'country_name': self._get_country_name(country),
                'currency': local_currency,
                'price_local': round(price_in_local, 2),
                'price_eur': round(price_in_eur, 2),
                'price_formatted': self.currency_converter.format_price(price_in_local, local_currency),
                'multiplier': multiplier,
                'vpn_recommended': self._should_use_vpn(country),
                'savings_vs_germany': round(base_price - price_in_eur, 2),
                'savings_percentage': round(((base_price - price_in_eur) / base_price * 100), 2)
            })

        # Sort by EUR price
        regional_prices.sort(key=lambda x: x['price_eur'])

        return regional_prices

    def find_cheapest_market(
        self,
        base_price: float,
        base_currency: str,
        origin: str,
        destination: str,
        departure_date: datetime
    ) -> Dict[str, Any]:
        """
        Identify the cheapest market to book from.

        Returns detailed analysis of best booking location.
        """
        regional_prices = self.simulate_regional_pricing(
            base_price, base_currency, origin, destination, departure_date
        )

        cheapest = regional_prices[0]
        most_expensive = regional_prices[-1]

        # Calculate maximum possible savings
        max_savings = most_expensive['price_eur'] - cheapest['price_eur']
        max_savings_pct = (max_savings / most_expensive['price_eur'] * 100)

        return {
            'cheapest_market': cheapest,
            'most_expensive_market': most_expensive,
            'all_markets': regional_prices,
            'max_savings': round(max_savings, 2),
            'max_savings_percentage': round(max_savings_pct, 2),
            'recommendation': self._generate_recommendation(cheapest, regional_prices),
            'price_spread': {
                'min': cheapest['price_eur'],
                'max': most_expensive['price_eur'],
                'average': round(sum(p['price_eur'] for p in regional_prices) / len(regional_prices), 2)
            }
        }

    def explain_geo_pricing(self, country1: str, country2: str) -> Dict[str, Any]:
        """
        Explain why prices differ between two countries.
        """
        reasons = []

        mult1 = self.REGIONAL_MULTIPLIERS.get(country1, 1.0)
        mult2 = self.REGIONAL_MULTIPLIERS.get(country2, 1.0)

        if mult1 != mult2:
            diff_pct = abs(mult1 - mult2) / min(mult1, mult2) * 100
            reasons.append({
                'factor': 'Regional Market Pricing',
                'impact': f"{diff_pct:.1f}% difference",
                'explanation': f"Airlines price differently based on local market conditions, competition, and purchasing power."
            })

        curr1 = self._get_country_currency(country1)
        curr2 = self._get_country_currency(country2)

        if curr1 != curr2:
            reasons.append({
                'factor': 'Currency Pricing Strategy',
                'impact': 'Variable',
                'explanation': f"Prices in {curr1} vs {curr2} may be rounded differently and have currency-specific adjustments."
            })

        # Add general factors
        reasons.extend([
            {
                'factor': 'Local Competition',
                'impact': 'High',
                'explanation': 'Markets with more competition (like Poland, Spain) often have lower prices.'
            },
            {
                'factor': 'Purchasing Power',
                'impact': 'Medium',
                'explanation': 'Airlines adjust prices based on average income levels in each country.'
            },
            {
                'factor': 'Local Taxes & Fees',
                'impact': 'Medium',
                'explanation': 'Different countries have different aviation taxes and airport fees.'
            },
            {
                'factor': 'Point of Sale Rules',
                'impact': 'Medium',
                'explanation': 'Airlines segment markets and apply different pricing rules per region.'
            }
        ])

        return {
            'country1': {'code': country1, 'name': self._get_country_name(country1)},
            'country2': {'code': country2, 'name': self._get_country_name(country2)},
            'reasons': reasons,
            'price_difference_multiplier': abs(mult1 - mult2)
        }

    def legal_access_methods(self, target_country: str) -> Dict[str, Any]:
        """
        Outline legal ways to access pricing from different countries.

        IMPORTANT: This is for educational purposes. Always comply with
        airline terms of service and local laws.
        """
        methods = [
            {
                'method': 'VPN Service',
                'legality': 'Gray Area',
                'description': 'Use VPN to appear to browse from target country',
                'risks': [
                    'May violate airline Terms of Service',
                    'Booking might be cancelled if detected',
                    'Payment card address might not match'
                ],
                'tips': [
                    'Clear cookies before connecting to VPN',
                    'Use incognito/private browsing',
                    'Consider using local payment method if possible'
                ]
            },
            {
                'method': 'Local Travel Agency',
                'legality': 'Fully Legal',
                'description': 'Contact travel agency in target country to book',
                'risks': ['Service fees may offset savings'],
                'tips': [
                    'Find agencies that serve international clients',
                    'Ask for quote before committing',
                    'Ensure they provide proper documentation'
                ]
            },
            {
                'method': 'Local Credit Card',
                'legality': 'Fully Legal',
                'description': 'Use credit card issued in target country',
                'risks': ['Need to have legitimate card from that country'],
                'tips': [
                    'Some international banks issue cards in multiple countries',
                    'Transferwise/Revolut cards may help'
                ]
            },
            {
                'method': 'Book While Physically Present',
                'legality': 'Fully Legal',
                'description': 'Book while actually in the target country',
                'risks': ['Need to travel there first'],
                'tips': [
                    'Good for future bookings if you visit frequently',
                    'Use local SIM card for extra authenticity'
                ]
            },
            {
                'method': 'Multi-Currency Booking Sites',
                'legality': 'Fully Legal',
                'description': 'Use OTAs that allow currency/region selection',
                'risks': ['Limited options, may have fees'],
                'tips': [
                    'Compare prices in different currencies',
                    'Check if card charges foreign transaction fees'
                ]
            }
        ]

        warnings = [
            'Always read airline Terms of Service',
            'Misrepresenting your location may lead to booking cancellation',
            'Ensure payment card billing address matches',
            'Some countries have laws against VPN usage',
            'Consider tax implications of international bookings'
        ]

        return {
            'target_country': self._get_country_name(target_country),
            'methods': methods,
            'warnings': warnings,
            'recommended_approach': self._get_recommended_approach(target_country)
        }

    def _get_country_currency(self, country_code: str) -> str:
        """Get primary currency for country."""
        currency_map = {
            'DE': 'EUR', 'FR': 'EUR', 'IT': 'EUR', 'ES': 'EUR', 'NL': 'EUR',
            'GB': 'GBP', 'US': 'USD', 'CH': 'CHF', 'PL': 'PLN', 'TR': 'TRY',
            'IN': 'INR', 'TH': 'THB', 'AE': 'AED', 'SG': 'USD', 'AU': 'AUD',
            'BR': 'USD', 'MX': 'USD', 'AR': 'USD'
        }
        return currency_map.get(country_code, 'EUR')

    def _get_country_name(self, country_code: str) -> str:
        """Get country name from code."""
        names = {
            'DE': 'Germany', 'FR': 'France', 'GB': 'United Kingdom',
            'US': 'United States', 'CH': 'Switzerland', 'ES': 'Spain',
            'IT': 'Italy', 'NL': 'Netherlands', 'PL': 'Poland',
            'TR': 'Turkey', 'IN': 'India', 'TH': 'Thailand',
            'AE': 'UAE', 'SG': 'Singapore', 'AU': 'Australia',
            'BR': 'Brazil', 'MX': 'Mexico', 'AR': 'Argentina'
        }
        return names.get(country_code, country_code)

    def _should_use_vpn(self, country: str) -> bool:
        """Determine if VPN would help access this market."""
        # Countries where geo-pricing differences are significant
        significant_diff = ['PL', 'TR', 'IN', 'TH', 'AR', 'MX', 'BR']
        return country in significant_diff

    def _generate_recommendation(
        self,
        cheapest: Dict[str, Any],
        all_prices: List[Dict[str, Any]]
    ) -> str:
        """Generate recommendation based on analysis."""
        savings = abs(cheapest['savings_vs_germany'])
        savings_pct = abs(cheapest['savings_percentage'])

        if savings < 20:
            return f"Price difference is minimal (€{savings:.2f}). Stick with your local market for simplicity."
        elif savings < 50:
            return f"Moderate savings possible (€{savings:.2f}, {savings_pct:.1f}%). Consider if you have legal access to {cheapest['country_name']} market."
        else:
            return f"Significant savings (€{savings:.2f}, {savings_pct:.1f}%)! Worth exploring legal methods to book from {cheapest['country_name']}."

    def _get_recommended_approach(self, target_country: str) -> str:
        """Get recommended approach for accessing market."""
        if target_country in ['PL', 'ES', 'IT']:
            return "These are EU countries. Consider using a local EU travel agency or booking while visiting."
        elif target_country in ['TR', 'IN', 'TH']:
            return "Significant savings possible, but consider using reputable local travel agency rather than VPN."
        else:
            return "Evaluate if savings justify the complexity. Local travel agency is safest approach."


def compare_markets_for_route(
    origin: str,
    destination: str,
    base_price: float,
    markets_to_compare: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Compare specific markets for a route.

    Convenience function for quick market comparison.
    """
    analyzer = GeoPricingAnalyzer()

    if markets_to_compare is None:
        markets_to_compare = ['DE', 'PL', 'TR', 'IN', 'GB', 'US']

    results = analyzer.simulate_regional_pricing(
        base_price=base_price,
        base_currency='EUR',
        origin=origin,
        destination=destination,
        departure_date=datetime.now()
    )

    # Filter to requested markets
    filtered = [r for r in results if r['country'] in markets_to_compare]

    return {
        'markets': filtered,
        'cheapest': min(filtered, key=lambda x: x['price_eur']),
        'most_expensive': max(filtered, key=lambda x: x['price_eur'])
    }
