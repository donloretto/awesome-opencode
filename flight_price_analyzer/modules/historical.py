"""
Historical pricing analysis module.
Uses historical airline pricing behavior to identify optimal booking windows and price patterns.
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from .utils import FlightLogger, DateHelper
import calendar


class HistoricalPricingAnalyzer:
    """
    Analyzes historical pricing patterns to predict optimal booking times.

    Examines:
    - Best booking windows (days before departure)
    - Cheapest days of week to book
    - Cheapest days of week to fly
    - Seasonal price variations
    - Fare reset patterns
    - Inventory release cycles
    """

    # Historical data based on industry studies
    BOOKING_WINDOW_PATTERNS = {
        'domestic': {
            'optimal_days_before': [21, 60],
            'price_trend': 'Prices lowest 3-8 weeks before departure',
            'avoid_booking': [0, 7],  # Last week
            'avoid_reason': 'Last-minute premium up to 40%'
        },
        'international': {
            'optimal_days_before': [60, 120],
            'price_trend': 'Prices lowest 2-4 months before departure',
            'avoid_booking': [0, 14],
            'avoid_reason': 'Last-minute premium up to 50%'
        },
        'intercontinental': {
            'optimal_days_before': [90, 180],
            'price_trend': 'Prices lowest 3-6 months before departure',
            'avoid_booking': [0, 21],
            'avoid_reason': 'Last-minute premium up to 60%'
        }
    }

    DAY_OF_WEEK_PATTERNS = {
        'best_days_to_book': {
            'days': ['Tuesday', 'Wednesday', 'Thursday'],
            'reason': 'Airlines often release sales Monday evening, prices adjust Tuesday',
            'average_savings': '5-10%'
        },
        'worst_days_to_book': {
            'days': ['Friday', 'Saturday', 'Sunday'],
            'reason': 'Weekend leisure demand, fewer business sales',
            'average_markup': '5-15%'
        },
        'best_days_to_fly': {
            'days': ['Tuesday', 'Wednesday', 'Saturday'],
            'reason': 'Lower demand = lower prices',
            'average_savings': '10-20%'
        },
        'worst_days_to_fly': {
            'days': ['Friday', 'Sunday'],
            'reason': 'Business and weekend travelers create high demand',
            'average_markup': '15-30%'
        }
    }

    SEASONAL_PATTERNS = {
        'peak_seasons': [
            {
                'name': 'Summer (Jun-Aug)',
                'months': [6, 7, 8],
                'multiplier': 1.3,
                'booking_advance': 'Book 3-6 months ahead',
                'note': 'Highest demand, prices 30% above average'
            },
            {
                'name': 'Christmas/New Year (Dec 20 - Jan 5)',
                'months': [12, 1],
                'multiplier': 1.4,
                'booking_advance': 'Book 4-6 months ahead',
                'note': 'Peak holiday travel, prices 40% above average'
            },
            {
                'name': 'Easter Week',
                'months': [3, 4],
                'multiplier': 1.2,
                'booking_advance': 'Book 2-3 months ahead',
                'note': 'Spring break demand'
            }
        ],
        'off_peak_seasons': [
            {
                'name': 'Late Winter (Jan 15 - Mar 15)',
                'months': [1, 2, 3],
                'multiplier': 0.75,
                'booking_advance': 'Book 1-2 months ahead',
                'note': 'Lowest demand, best deals'
            },
            {
                'name': 'Fall (Sep - Nov)',
                'months': [9, 10, 11],
                'multiplier': 0.85,
                'booking_advance': 'Book 1-3 months ahead',
                'note': 'Good prices after summer rush'
            }
        ]
    }

    TIME_OF_DAY_PATTERNS = {
        'best_times_to_book': [
            {'time': '3:00 AM - 5:00 AM', 'reason': 'Automated fare resets', 'savings': 'Variable'},
            {'time': '3:00 PM - 6:00 PM Tuesday', 'reason': 'Post-sale adjustment period', 'savings': '5-10%'},
        ],
        'worst_times_to_book': [
            {'time': '7:00 PM - 11:00 PM', 'reason': 'High demand period', 'markup': '3-8%'},
            {'time': 'Weekends', 'reason': 'Leisure booking peak', 'markup': '5-10%'}
        ]
    }

    def __init__(self, logger: Optional[FlightLogger] = None):
        self.logger = logger or FlightLogger("HistoricalPricing")

    def analyze_booking_window(
        self,
        origin: str,
        destination: str,
        departure_date: datetime
    ) -> Dict[str, Any]:
        """
        Analyze optimal booking window for a specific route.
        """
        self.logger.info(f"Analyzing booking window for {origin} → {destination}")

        # Determine route type
        route_type = self._classify_route(origin, destination)
        pattern = self.BOOKING_WINDOW_PATTERNS[route_type]

        # Calculate current booking window
        today = datetime.now()
        days_until_departure = (departure_date - today).days

        # Determine if currently in optimal window
        in_optimal_window = (
            pattern['optimal_days_before'][0] <= days_until_departure <= pattern['optimal_days_before'][1]
        )

        # Calculate when optimal window opens/closes
        optimal_start = departure_date - timedelta(days=pattern['optimal_days_before'][1])
        optimal_end = departure_date - timedelta(days=pattern['optimal_days_before'][0])

        analysis = {
            'route_type': route_type,
            'departure_date': departure_date.strftime('%Y-%m-%d'),
            'days_until_departure': days_until_departure,
            'optimal_booking_window': {
                'start_date': optimal_start.strftime('%Y-%m-%d'),
                'end_date': optimal_end.strftime('%Y-%m-%d'),
                'days_before': pattern['optimal_days_before']
            },
            'currently_optimal': in_optimal_window,
            'recommendation': self._generate_booking_recommendation(
                days_until_departure, pattern, in_optimal_window
            ),
            'price_trend': pattern['price_trend'],
            'historical_pattern': self._get_historical_price_curve(route_type)
        }

        return analysis

    def analyze_day_of_week(
        self,
        departure_date: datetime,
        booking_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Analyze day of week patterns for booking and flying.
        """
        if booking_date is None:
            booking_date = datetime.now()

        departure_day = departure_date.strftime('%A')
        booking_day = booking_date.strftime('%A')

        # Check if departure day is optimal
        is_good_departure_day = departure_day in self.DAY_OF_WEEK_PATTERNS['best_days_to_fly']['days']
        is_bad_departure_day = departure_day in self.DAY_OF_WEEK_PATTERNS['worst_days_to_fly']['days']

        # Check if booking day is optimal
        is_good_booking_day = booking_day in self.DAY_OF_WEEK_PATTERNS['best_days_to_book']['days']
        is_bad_booking_day = booking_day in self.DAY_OF_WEEK_PATTERNS['worst_days_to_book']['days']

        # Find better alternative days
        better_departure_days = self._find_better_days(
            departure_date,
            self.DAY_OF_WEEK_PATTERNS['best_days_to_fly']['days']
        )

        analysis = {
            'departure_analysis': {
                'day': departure_day,
                'is_optimal': is_good_departure_day,
                'is_expensive': is_bad_departure_day,
                'expected_impact': self._get_day_price_impact(departure_day, 'fly'),
                'better_alternatives': better_departure_days
            },
            'booking_analysis': {
                'day': booking_day,
                'is_optimal': is_good_booking_day,
                'is_expensive': is_bad_booking_day,
                'expected_impact': self._get_day_price_impact(booking_day, 'book')
            },
            'patterns': self.DAY_OF_WEEK_PATTERNS,
            'recommendation': self._generate_day_recommendation(
                is_good_departure_day, is_good_booking_day, better_departure_days
            )
        }

        return analysis

    def analyze_seasonal_pricing(
        self,
        departure_date: datetime
    ) -> Dict[str, Any]:
        """
        Analyze seasonal pricing patterns.
        """
        month = departure_date.month

        # Find applicable seasonal pattern
        season_info = self._identify_season(month, departure_date)

        # Calculate price multiplier
        multiplier = season_info.get('multiplier', 1.0)

        # Estimate price impact
        base_price = 300  # Example base price
        seasonal_price = base_price * multiplier

        analysis = {
            'departure_date': departure_date.strftime('%Y-%m-%d'),
            'month': departure_date.strftime('%B'),
            'season': season_info,
            'price_impact': {
                'multiplier': multiplier,
                'vs_average': f"{((multiplier - 1) * 100):+.0f}%",
                'example_base': base_price,
                'example_seasonal': seasonal_price
            },
            'booking_advice': season_info.get('booking_advance', 'Book 2-3 months ahead'),
            'all_seasons': {
                'peak': self.SEASONAL_PATTERNS['peak_seasons'],
                'off_peak': self.SEASONAL_PATTERNS['off_peak_seasons']
            }
        }

        return analysis

    def identify_fare_reset_times(self) -> Dict[str, Any]:
        """
        Identify when airlines typically reset fares.
        """
        return {
            'daily_resets': [
                {
                    'time': '12:00 AM - 2:00 AM EST',
                    'frequency': 'Daily',
                    'what_happens': 'Automated fare updates, expired sales removed',
                    'opportunity': 'New inventory released at base fares'
                },
                {
                    'time': '3:00 AM - 5:00 AM Local',
                    'frequency': 'Daily',
                    'what_happens': 'Regional fare adjustments',
                    'opportunity': 'Catch pricing errors before correction'
                }
            ],
            'weekly_resets': [
                {
                    'time': 'Monday 5:00 PM - 11:59 PM EST',
                    'frequency': 'Weekly',
                    'what_happens': 'Airlines release weekend sales',
                    'opportunity': 'New sale fares available'
                },
                {
                    'time': 'Tuesday 3:00 PM EST',
                    'frequency': 'Weekly',
                    'what_happens': 'Competitors match Monday sales',
                    'opportunity': 'Best time to find matching lower prices'
                }
            ],
            'inventory_releases': [
                {
                    'timing': '330 days before departure',
                    'what_happens': 'Initial schedule release',
                    'opportunity': 'Early bird fares (not always cheapest)'
                },
                {
                    'timing': '90-120 days before departure',
                    'what_happens': 'Major inventory release',
                    'opportunity': 'Optimal pricing for most routes'
                },
                {
                    'timing': '21-30 days before departure',
                    'what_happens': 'Inventory assessment and repricing',
                    'opportunity': 'Last chance for good deals before last-minute surge'
                },
                {
                    'timing': '7 days before departure',
                    'what_happens': 'Last-minute premium pricing',
                    'opportunity': 'Only for unsold inventory on unpopular routes'
                }
            ],
            'best_search_times': [
                'Tuesday 3:00 PM EST (weekly low point)',
                'Wednesday 12:00 PM EST (mid-week stability)',
                'Sunday 5:00 AM EST (weekend fare updates)'
            ]
        }

    def analyze_demand_cycles(
        self,
        origin: str,
        destination: str,
        departure_date: datetime
    ) -> Dict[str, Any]:
        """
        Analyze demand cycles that influence pricing.
        """
        # Business vs leisure route
        route_character = self._classify_route_character(origin, destination)

        # Day of week demand
        day_demand = self._analyze_day_demand(departure_date)

        # Seasonal demand
        seasonal_demand = self._analyze_seasonal_demand(departure_date)

        # Event-based demand
        event_impact = self._check_event_impact(destination, departure_date)

        return {
            'route_character': route_character,
            'day_demand': day_demand,
            'seasonal_demand': seasonal_demand,
            'event_impact': event_impact,
            'overall_demand': self._calculate_overall_demand(
                route_character, day_demand, seasonal_demand, event_impact
            ),
            'pricing_recommendation': self._generate_demand_recommendation(
                route_character, day_demand, seasonal_demand
            )
        }

    def get_comprehensive_analysis(
        self,
        origin: str,
        destination: str,
        departure_date: datetime,
        return_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive historical analysis combining all factors.
        """
        self.logger.info(f"Performing comprehensive historical analysis")

        analysis = {
            'route': f"{origin} → {destination}",
            'departure_date': departure_date.strftime('%Y-%m-%d'),
            'return_date': return_date.strftime('%Y-%m-%d') if return_date else None,
            'booking_window_analysis': self.analyze_booking_window(origin, destination, departure_date),
            'day_of_week_analysis': self.analyze_day_of_week(departure_date),
            'seasonal_analysis': self.analyze_seasonal_pricing(departure_date),
            'fare_reset_times': self.identify_fare_reset_times(),
            'demand_cycle_analysis': self.analyze_demand_cycles(origin, destination, departure_date),
            'overall_recommendation': None
        }

        # Generate overall recommendation
        analysis['overall_recommendation'] = self._generate_overall_recommendation(analysis)

        return analysis

    # Helper methods

    def _classify_route(self, origin: str, destination: str) -> str:
        """Classify route as domestic, international, or intercontinental."""
        # Simplified - in production, use actual airport database
        from .utils import AirportHelper
        helper = AirportHelper()

        origin_info = helper.get_airport_info(origin)
        dest_info = helper.get_airport_info(destination)

        if not origin_info or not dest_info:
            return 'international'

        if origin_info['country'] == dest_info['country']:
            return 'domestic'

        # Check if same continent (simplified)
        eu_countries = ['DE', 'FR', 'IT', 'ES', 'NL', 'GB', 'PL', 'AT', 'CH']
        if origin_info['country'] in eu_countries and dest_info['country'] in eu_countries:
            return 'international'

        return 'intercontinental'

    def _generate_booking_recommendation(
        self,
        days_until: int,
        pattern: Dict,
        in_optimal: bool
    ) -> str:
        """Generate booking recommendation based on window analysis."""
        if in_optimal:
            return f"✓ BOOK NOW - You're in the optimal booking window ({days_until} days before departure)"
        elif days_until > pattern['optimal_days_before'][1]:
            days_to_wait = days_until - pattern['optimal_days_before'][1]
            return f"WAIT - Too early. Optimal window opens in {days_to_wait} days"
        elif days_until < pattern['optimal_days_before'][0]:
            return f"BOOK ASAP - Past optimal window. Prices likely increasing (only {days_until} days left)"
        else:
            return "MONITOR - Close to optimal window"

    def _get_historical_price_curve(self, route_type: str) -> List[Dict[str, Any]]:
        """Get historical price curve for route type."""
        curves = {
            'domestic': [
                {'days_before': 90, 'relative_price': 1.1},
                {'days_before': 60, 'relative_price': 0.95},
                {'days_before': 30, 'relative_price': 0.92},
                {'days_before': 21, 'relative_price': 0.90},  # Optimal
                {'days_before': 14, 'relative_price': 0.95},
                {'days_before': 7, 'relative_price': 1.15},
                {'days_before': 3, 'relative_price': 1.30},
                {'days_before': 1, 'relative_price': 1.40},
            ],
            'international': [
                {'days_before': 180, 'relative_price': 1.0},
                {'days_before': 120, 'relative_price': 0.92},
                {'days_before': 90, 'relative_price': 0.88},
                {'days_before': 60, 'relative_price': 0.85},  # Optimal
                {'days_before': 30, 'relative_price': 0.90},
                {'days_before': 14, 'relative_price': 1.10},
                {'days_before': 7, 'relative_price': 1.35},
                {'days_before': 1, 'relative_price': 1.50},
            ]
        }
        return curves.get(route_type, curves['international'])

    def _find_better_days(self, target_date: datetime, good_days: List[str]) -> List[Dict[str, str]]:
        """Find better alternative days near target date."""
        alternatives = []
        for offset in [-3, -2, -1, 1, 2, 3]:
            alt_date = target_date + timedelta(days=offset)
            if alt_date.strftime('%A') in good_days:
                alternatives.append({
                    'date': alt_date.strftime('%Y-%m-%d'),
                    'day': alt_date.strftime('%A'),
                    'offset': offset
                })
        return alternatives[:3]  # Top 3 alternatives

    def _get_day_price_impact(self, day: str, context: str) -> str:
        """Get price impact for specific day."""
        if context == 'fly':
            if day in self.DAY_OF_WEEK_PATTERNS['best_days_to_fly']['days']:
                return f"-{self.DAY_OF_WEEK_PATTERNS['best_days_to_fly']['average_savings']}"
            elif day in self.DAY_OF_WEEK_PATTERNS['worst_days_to_fly']['days']:
                return f"+{self.DAY_OF_WEEK_PATTERNS['worst_days_to_fly']['average_markup']}"
        else:  # book
            if day in self.DAY_OF_WEEK_PATTERNS['best_days_to_book']['days']:
                return f"-{self.DAY_OF_WEEK_PATTERNS['best_days_to_book']['average_savings']}"
            elif day in self.DAY_OF_WEEK_PATTERNS['worst_days_to_book']['days']:
                return f"+{self.DAY_OF_WEEK_PATTERNS['worst_days_to_book']['average_markup']}"
        return "0%"

    def _generate_day_recommendation(
        self,
        good_departure: bool,
        good_booking: bool,
        alternatives: List[Dict]
    ) -> str:
        """Generate day-of-week recommendation."""
        if good_departure and good_booking:
            return "✓ Optimal - Both departure and booking days are ideal"
        elif good_departure:
            return "✓ Good departure day, consider booking on Tuesday/Wednesday if possible"
        elif alternatives:
            alt = alternatives[0]
            return f"Consider flying on {alt['day']} ({alt['date']}) instead for better pricing"
        else:
            return "Current day has higher demand. Monitor prices and book during Tuesday-Thursday if possible"

    def _identify_season(self, month: int, date: datetime) -> Dict[str, Any]:
        """Identify which season the date falls into."""
        # Check peak seasons
        for season in self.SEASONAL_PATTERNS['peak_seasons']:
            if month in season['months']:
                return season

        # Check off-peak seasons
        for season in self.SEASONAL_PATTERNS['off_peak_seasons']:
            if month in season['months']:
                return season

        # Default shoulder season
        return {
            'name': 'Shoulder Season',
            'multiplier': 1.0,
            'booking_advance': 'Book 1-2 months ahead',
            'note': 'Moderate demand'
        }

    def _classify_route_character(self, origin: str, destination: str) -> Dict[str, Any]:
        """Classify if route is business or leisure oriented."""
        # Simplified logic
        business_hubs = ['FRA', 'LHR', 'JFK', 'DXB']

        is_business = origin in business_hubs and destination in business_hubs

        return {
            'type': 'business' if is_business else 'leisure',
            'description': 'Business route with weekday demand' if is_business else 'Leisure route with weekend demand'
        }

    def _analyze_day_demand(self, date: datetime) -> Dict[str, Any]:
        """Analyze demand based on day of week."""
        day = date.strftime('%A')
        is_weekend = day in ['Friday', 'Saturday', 'Sunday']

        return {
            'day': day,
            'demand_level': 'high' if is_weekend else 'moderate',
            'reason': 'Weekend leisure travel' if is_weekend else 'Weekday travel'
        }

    def _analyze_seasonal_demand(self, date: datetime) -> Dict[str, Any]:
        """Analyze seasonal demand."""
        season = self._identify_season(date.month, date)

        return {
            'season': season['name'],
            'demand_level': 'high' if season['multiplier'] > 1.1 else 'low',
            'multiplier': season['multiplier']
        }

    def _check_event_impact(self, destination: str, date: datetime) -> Dict[str, Any]:
        """Check for major events impacting demand."""
        # Simplified - in production, check events database
        return {
            'events_found': False,
            'description': 'No major events detected',
            'impact': 'none'
        }

    def _calculate_overall_demand(
        self,
        route_char: Dict,
        day_demand: Dict,
        seasonal_demand: Dict,
        event_impact: Dict
    ) -> str:
        """Calculate overall demand level."""
        demand_score = 0

        if route_char['type'] == 'business':
            demand_score += 1

        if day_demand['demand_level'] == 'high':
            demand_score += 2

        if seasonal_demand['demand_level'] == 'high':
            demand_score += 3

        if event_impact['impact'] != 'none':
            demand_score += 2

        if demand_score >= 5:
            return 'Very High'
        elif demand_score >= 3:
            return 'High'
        elif demand_score >= 1:
            return 'Moderate'
        else:
            return 'Low'

    def _generate_demand_recommendation(
        self,
        route_char: Dict,
        day_demand: Dict,
        seasonal_demand: Dict
    ) -> str:
        """Generate recommendation based on demand analysis."""
        if day_demand['demand_level'] == 'high' and seasonal_demand['demand_level'] == 'high':
            return "⚠️ Peak demand period. Book well in advance and expect high prices."
        elif seasonal_demand['demand_level'] == 'high':
            return "High season. Book 3-6 months ahead for better prices."
        elif day_demand['demand_level'] == 'high':
            return "Consider shifting travel dates to mid-week for lower prices."
        else:
            return "✓ Low demand period. Good opportunity for deals."

    def _generate_overall_recommendation(self, analysis: Dict[str, Any]) -> str:
        """Generate overall recommendation from all analyses."""
        recommendations = []

        # Booking window
        if analysis['booking_window_analysis']['currently_optimal']:
            recommendations.append("✓ In optimal booking window")
        else:
            recommendations.append(analysis['booking_window_analysis']['recommendation'])

        # Day of week
        if not analysis['day_of_week_analysis']['departure_analysis']['is_optimal']:
            alternatives = analysis['day_of_week_analysis']['departure_analysis']['better_alternatives']
            if alternatives:
                recommendations.append(f"Consider alternative date: {alternatives[0]['date']}")

        # Seasonal
        seasonal_impact = analysis['seasonal_analysis']['season']['multiplier']
        if seasonal_impact > 1.15:
            recommendations.append("⚠️ High season - expect elevated prices")
        elif seasonal_impact < 0.9:
            recommendations.append("✓ Off-peak season - good time for deals")

        return " | ".join(recommendations)
