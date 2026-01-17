"""
Platform comparison module.
Compares pricing between airlines, OTAs, and booking sites to find the best deals.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from .utils import FlightLogger, CurrencyConverter


class BookingPlatform:
    """Represents a booking platform with its characteristics."""

    def __init__(
        self,
        name: str,
        platform_type: str,
        base_fee: float = 0.0,
        percentage_markup: float = 0.0,
        hidden_fees: Optional[List[str]] = None,
        pros: Optional[List[str]] = None,
        cons: Optional[List[str]] = None,
        reliability_score: int = 5
    ):
        self.name = name
        self.platform_type = platform_type  # 'airline', 'major_ota', 'regional', 'meta_search'
        self.base_fee = base_fee
        self.percentage_markup = percentage_markup
        self.hidden_fees = hidden_fees or []
        self.pros = pros or []
        self.cons = cons or []
        self.reliability_score = reliability_score  # 1-10

    def calculate_total_price(self, base_price: float) -> float:
        """Calculate total price including fees and markup."""
        price = base_price * (1 + self.percentage_markup / 100)
        price += self.base_fee
        return round(price, 2)


class PlatformComparator:
    """
    Compares pricing across different booking platforms.

    Analyzes:
    - Direct airline pricing
    - Major OTA pricing (Expedia, Booking.com, etc.)
    - Regional booking sites
    - Meta-search engines
    - Service fees and hidden costs
    """

    # Platform database
    PLATFORMS = {
        'lufthansa_direct': BookingPlatform(
            name='Lufthansa Direct',
            platform_type='airline',
            base_fee=0.0,
            percentage_markup=0.0,
            hidden_fees=['Seat selection fee', 'Baggage fee'],
            pros=['No booking fees', 'Direct customer service', 'Loyalty points', 'Flexible cancellation'],
            cons=['May not show cheapest options', 'Limited price comparison'],
            reliability_score=10
        ),
        'ryanair_direct': BookingPlatform(
            name='Ryanair Direct',
            platform_type='airline',
            base_fee=0.0,
            percentage_markup=0.0,
            hidden_fees=['Card payment fee', 'Priority boarding', 'Baggage fee', 'Seat selection'],
            pros=['Often lowest base fare', 'Direct booking'],
            cons=['Many hidden fees', 'Strict policies'],
            reliability_score=9
        ),
        'expedia': BookingPlatform(
            name='Expedia',
            platform_type='major_ota',
            base_fee=12.99,
            percentage_markup=2.5,
            hidden_fees=['Service fee'],
            pros=['Package deals', 'Rewards program', 'Good customer service'],
            cons=['Service fees', 'Markup on base fare'],
            reliability_score=9
        ),
        'booking_com': BookingPlatform(
            name='Booking.com',
            platform_type='major_ota',
            base_fee=0.0,
            percentage_markup=3.0,
            hidden_fees=['Sometimes higher base prices'],
            pros=['No visible fees', 'Easy cancellation'],
            cons=['Markup built into price', 'Limited flight inventory'],
            reliability_score=8
        ),
        'kayak': BookingPlatform(
            name='Kayak',
            platform_type='meta_search',
            base_fee=0.0,
            percentage_markup=0.0,
            hidden_fees=[],
            pros=['Price comparison', 'No fees (redirects to booking site)', 'Price alerts'],
            cons=['Redirects to other sites', 'Prices may differ on final site'],
            reliability_score=9
        ),
        'skyscanner': BookingPlatform(
            name='Skyscanner',
            platform_type='meta_search',
            base_fee=0.0,
            percentage_markup=0.0,
            hidden_fees=[],
            pros=['Best for comparison', 'Whole month view', 'Flexible dates'],
            cons=['Redirects to other sites', 'Some partners unreliable'],
            reliability_score=8
        ),
        'google_flights': BookingPlatform(
            name='Google Flights',
            platform_type='meta_search',
            base_fee=0.0,
            percentage_markup=0.0,
            hidden_fees=[],
            pros=['Fast', 'Accurate', 'Great UI', 'Price tracking'],
            cons=['Redirects to other sites', 'Limited to partner airlines'],
            reliability_score=10
        ),
        'momondo': BookingPlatform(
            name='Momondo',
            platform_type='meta_search',
            base_fee=0.0,
            percentage_markup=0.0,
            hidden_fees=[],
            pros=['Often finds cheapest options', 'Good for flexible dates'],
            cons=['Can show outdated prices', 'Some sketchy partners'],
            reliability_score=7
        ),
        'opodo': BookingPlatform(
            name='Opodo',
            platform_type='regional',
            base_fee=8.99,
            percentage_markup=1.5,
            hidden_fees=['Service fee', 'Prime membership push'],
            pros=['European focus', 'Multi-city options'],
            cons=['Service fees', 'Aggressive upselling'],
            reliability_score=6
        ),
        'edreams': BookingPlatform(
            name='eDreams',
            platform_type='regional',
            base_fee=9.99,
            percentage_markup=2.0,
            hidden_fees=['Service fee', 'Prime membership'],
            pros=['European inventory', 'Package deals'],
            cons=['High fees', 'Poor customer service reputation'],
            reliability_score=5
        ),
        'kiwi_com': BookingPlatform(
            name='Kiwi.com',
            platform_type='regional',
            base_fee=0.0,
            percentage_markup=1.0,
            hidden_fees=['Guarantee fee'],
            pros=['Virtual interlining', 'Creative routing'],
            cons=['Self-transfer risks', 'Limited support if things go wrong'],
            reliability_score=6
        ),
        'lastminute_com': BookingPlatform(
            name='Lastminute.com',
            platform_type='regional',
            base_fee=6.99,
            percentage_markup=1.5,
            hidden_fees=['Service fee'],
            pros=['Good for last-minute deals', 'Package options'],
            cons=['Fees', 'Not always cheapest'],
            reliability_score=7
        )
    }

    def __init__(self, logger: Optional[FlightLogger] = None):
        self.logger = logger or FlightLogger("PlatformComparator")
        self.currency_converter = CurrencyConverter()

    def compare_platforms(
        self,
        base_price: float,
        origin: str,
        destination: str,
        platforms_to_check: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Compare prices across multiple platforms.

        Returns comparison with fees, total costs, and recommendations.
        """
        self.logger.info(f"Comparing platforms for {origin} → {destination}")

        if platforms_to_check is None:
            platforms_to_check = list(self.PLATFORMS.keys())

        comparisons = []

        for platform_key in platforms_to_check:
            if platform_key not in self.PLATFORMS:
                continue

            platform = self.PLATFORMS[platform_key]

            # Simulate price variation (in reality, would query actual APIs)
            simulated_base = self._simulate_platform_price(base_price, platform)

            total_price = platform.calculate_total_price(simulated_base)

            comparisons.append({
                'platform': platform.name,
                'type': platform.platform_type,
                'base_price': simulated_base,
                'fees': platform.base_fee,
                'markup_percentage': platform.percentage_markup,
                'total_price': total_price,
                'hidden_fees': platform.hidden_fees,
                'pros': platform.pros,
                'cons': platform.cons,
                'reliability_score': platform.reliability_score,
                'value_score': self._calculate_value_score(total_price, platform)
            })

        # Sort by total price
        comparisons.sort(key=lambda x: x['total_price'])

        # Find cheapest in each category
        by_type = self._group_by_type(comparisons)

        return {
            'all_platforms': comparisons,
            'cheapest_overall': comparisons[0],
            'most_expensive': comparisons[-1],
            'price_difference': round(comparisons[-1]['total_price'] - comparisons[0]['total_price'], 2),
            'by_platform_type': by_type,
            'recommendations': self._generate_recommendations(comparisons),
            'fee_analysis': self._analyze_fees(comparisons)
        }

    def analyze_hidden_costs(
        self,
        platform_name: str
    ) -> Dict[str, Any]:
        """
        Deep dive into hidden costs for a specific platform.
        """
        if platform_name not in self.PLATFORMS:
            return {'error': 'Platform not found'}

        platform = self.PLATFORMS[platform_name]

        # Comprehensive fee breakdown
        fee_breakdown = {
            'visible_fees': {
                'booking_fee': platform.base_fee,
                'percentage_markup': f"{platform.percentage_markup}%"
            },
            'hidden_fees': platform.hidden_fees,
            'typical_extras': self._get_typical_extras(platform.platform_type),
            'total_potential_fees': self._estimate_total_fees(platform),
            'fee_avoidance_tips': self._get_fee_avoidance_tips(platform_name)
        }

        return fee_breakdown

    def identify_best_platform(
        self,
        route_type: str,
        booking_class: str = 'economy',
        priorities: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Recommend best platform based on route type and priorities.

        Route types: 'domestic', 'european', 'international', 'budget'
        Priorities: 'price', 'reliability', 'flexibility', 'customer_service'
        """
        if priorities is None:
            priorities = ['price', 'reliability']

        recommendations = []

        if route_type == 'budget':
            recommendations = [
                {
                    'platform': 'Google Flights + Airline Direct',
                    'reason': 'Use Google to find, book direct with airline to avoid OTA fees',
                    'expected_savings': '€10-30'
                },
                {
                    'platform': 'Skyscanner',
                    'reason': 'Shows budget airlines that others miss',
                    'expected_savings': '€20-50'
                },
                {
                    'platform': 'Ryanair/EasyJet Direct',
                    'reason': 'Budget airlines rarely on OTAs, must book direct',
                    'expected_savings': 'Base fare often 50%+ cheaper'
                }
            ]
        elif route_type == 'domestic':
            recommendations = [
                {
                    'platform': 'Airline Direct',
                    'reason': 'No OTA fees, best for domestic routes',
                    'expected_savings': '€10-20'
                },
                {
                    'platform': 'Google Flights',
                    'reason': 'Quick comparison, then book direct',
                    'expected_savings': 'Time saving'
                }
            ]
        elif route_type == 'european':
            recommendations = [
                {
                    'platform': 'Skyscanner',
                    'reason': 'Best European coverage including low-cost carriers',
                    'expected_savings': '€15-40'
                },
                {
                    'platform': 'Momondo',
                    'reason': 'Often finds deals others miss in Europe',
                    'expected_savings': '€20-60'
                },
                {
                    'platform': 'Kiwi.com',
                    'reason': 'Creative routing with self-transfers',
                    'expected_savings': '€30-100 (with risk)'
                }
            ]
        else:  # international
            recommendations = [
                {
                    'platform': 'Google Flights',
                    'reason': 'Best for long-haul comparison',
                    'expected_savings': 'Research tool'
                },
                {
                    'platform': 'Airline Direct',
                    'reason': 'Book direct for international for better support',
                    'expected_savings': '€20-50 in fees avoided'
                },
                {
                    'platform': 'Kayak',
                    'reason': 'Good international coverage',
                    'expected_savings': '€25-75'
                }
            ]

        return {
            'route_type': route_type,
            'priorities': priorities,
            'top_recommendations': recommendations,
            'general_strategy': self._get_general_strategy(route_type, priorities)
        }

    def _simulate_platform_price(
        self,
        base_price: float,
        platform: BookingPlatform
    ) -> float:
        """
        Simulate how platform might price the ticket differently.

        In reality, different platforms may show different base prices
        due to their contracts with airlines.
        """
        import random

        # Meta-search engines show actual prices
        if platform.platform_type == 'meta_search':
            return base_price

        # Airlines direct might be slightly higher or lower
        if platform.platform_type == 'airline':
            return base_price * random.uniform(0.95, 1.05)

        # OTAs often have slightly different pricing
        if platform.platform_type == 'major_ota':
            return base_price * random.uniform(0.98, 1.08)

        # Regional sites can vary more
        return base_price * random.uniform(0.95, 1.12)

    def _calculate_value_score(
        self,
        total_price: float,
        platform: BookingPlatform
    ) -> float:
        """
        Calculate value score combining price and reliability.

        Score from 1-10, higher is better value.
        """
        # Normalize price (assume 500 is average)
        price_score = max(1, min(10, 10 - (total_price - 400) / 50))

        # Combine with reliability (60% price, 40% reliability)
        value_score = (price_score * 0.6) + (platform.reliability_score * 0.4)

        return round(value_score, 1)

    def _group_by_type(
        self,
        comparisons: List[Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """Group platforms by type and find cheapest in each."""
        by_type = {}

        for comp in comparisons:
            ptype = comp['type']
            if ptype not in by_type:
                by_type[ptype] = {
                    'platforms': [],
                    'cheapest': None
                }

            by_type[ptype]['platforms'].append(comp)

            if not by_type[ptype]['cheapest'] or comp['total_price'] < by_type[ptype]['cheapest']['total_price']:
                by_type[ptype]['cheapest'] = comp

        return by_type

    def _generate_recommendations(
        self,
        comparisons: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate platform recommendations."""
        recommendations = []

        cheapest = comparisons[0]
        most_reliable = max(comparisons, key=lambda x: x['reliability_score'])
        best_value = max(comparisons, key=lambda x: x['value_score'])

        recommendations.append(
            f"💰 Cheapest: {cheapest['platform']} at €{cheapest['total_price']:.2f}"
        )

        recommendations.append(
            f"⭐ Most Reliable: {most_reliable['platform']} (score: {most_reliable['reliability_score']}/10)"
        )

        recommendations.append(
            f"🎯 Best Value: {best_value['platform']} (value score: {best_value['value_score']}/10)"
        )

        # Price difference warning
        price_range = comparisons[-1]['total_price'] - comparisons[0]['total_price']
        if price_range > 50:
            recommendations.append(
                f"⚠️ Price range is €{price_range:.2f} - shop around!"
            )

        # Meta-search recommendation
        meta_search = [c for c in comparisons if c['type'] == 'meta_search']
        if meta_search:
            recommendations.append(
                f"💡 Use {meta_search[0]['platform']} to compare, then book direct to avoid fees"
            )

        return recommendations

    def _analyze_fees(
        self,
        comparisons: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze fee patterns across platforms."""
        total_fees = sum(c['fees'] for c in comparisons)
        platforms_with_fees = [c for c in comparisons if c['fees'] > 0]

        return {
            'platforms_with_fees': len(platforms_with_fees),
            'total_fees_across_all': round(total_fees, 2),
            'average_fee': round(total_fees / len(comparisons), 2) if comparisons else 0,
            'highest_fee_platform': max(comparisons, key=lambda x: x['fees'])['platform'] if comparisons else None,
            'fee_free_platforms': [c['platform'] for c in comparisons if c['fees'] == 0],
            'recommendation': 'Use fee-free meta-search, then book direct with airline'
        }

    def _get_typical_extras(self, platform_type: str) -> List[Dict[str, str]]:
        """Get typical extra fees by platform type."""
        extras = {
            'airline': [
                {'item': 'Checked baggage', 'typical_cost': '€25-50'},
                {'item': 'Seat selection', 'typical_cost': '€5-30'},
                {'item': 'Priority boarding', 'typical_cost': '€10-20'},
                {'item': 'Meals', 'typical_cost': '€8-15'}
            ],
            'major_ota': [
                {'item': 'Service fee', 'typical_cost': '€10-20'},
                {'item': 'Credit card fee', 'typical_cost': '€5-10'},
                {'item': 'Insurance (pushed)', 'typical_cost': '€15-30'}
            ],
            'regional': [
                {'item': 'Service fee', 'typical_cost': '€8-15'},
                {'item': 'Membership fee', 'typical_cost': '€30-60/year'},
                {'item': 'SMS confirmation', 'typical_cost': '€2-5'}
            ],
            'meta_search': [
                {'item': 'None (redirects)', 'typical_cost': '€0'}
            ]
        }
        return extras.get(platform_type, [])

    def _estimate_total_fees(self, platform: BookingPlatform) -> str:
        """Estimate total potential fees."""
        base = platform.base_fee
        typical_extras = 20  # Average extras

        total = base + typical_extras
        return f"€{base:.2f} booking fee + ~€{typical_extras:.2f} potential extras = ~€{total:.2f} total fees"

    def _get_fee_avoidance_tips(self, platform_name: str) -> List[str]:
        """Get tips to avoid fees on specific platform."""
        tips_db = {
            'expedia': [
                'Book as a "member" for reduced fees',
                'Avoid phone bookings (higher fees)',
                'Decline insurance and extras at checkout'
            ],
            'ryanair_direct': [
                'Use Mastercard debit to avoid card fee',
                'Check in online to avoid airport fee',
                'Don\'t pay for seat selection unless needed',
                'Stick to cabin bag only'
            ],
            'edreams': [
                'Decline Prime membership (often pre-selected)',
                'Use debit card to reduce payment fees',
                'Opt out of all insurance offers'
            ],
            'default': [
                'Use price comparison sites to find, book direct',
                'Read all checkboxes carefully',
                'Decline optional services',
                'Use incognito mode to avoid price inflation'
            ]
        }
        return tips_db.get(platform_name, tips_db['default'])

    def _get_general_strategy(
        self,
        route_type: str,
        priorities: List[str]
    ) -> str:
        """Get general booking strategy."""
        if 'price' in priorities:
            return (
                "1. Use Google Flights or Skyscanner to find best price\n"
                "2. Note the airline and exact flight\n"
                "3. Go to airline's website and book directly\n"
                "4. This avoids OTA fees while getting best price"
            )
        elif 'flexibility' in priorities:
            return (
                "1. Book directly with airline for better flexibility\n"
                "2. OTAs often have stricter cancellation policies\n"
                "3. Airline credits are easier to use than OTA vouchers"
            )
        else:
            return (
                "1. Compare on meta-search engines\n"
                "2. Check both OTAs and airline direct\n"
                "3. Consider total cost including all fees\n"
                "4. Factor in reliability and customer service"
            )


def quick_platform_comparison(base_price: float = 450.0) -> Dict[str, Any]:
    """
    Quick comparison showing typical price differences.

    Useful for understanding general platform pricing.
    """
    comparator = PlatformComparator()

    comparison = comparator.compare_platforms(
        base_price=base_price,
        origin='FRA',
        destination='JFK'
    )

    return {
        'base_price': base_price,
        'comparison': comparison,
        'key_insight': f"Price range: €{comparison['cheapest_overall']['total_price']:.2f} - €{comparison['most_expensive']['total_price']:.2f}",
        'savings_potential': f"Save up to €{comparison['price_difference']:.2f} by choosing the right platform"
    }
