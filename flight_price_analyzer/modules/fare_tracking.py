"""
Fare tracking module.
Creates strategies to monitor price drops without triggering price inflation.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
from .utils import FlightLogger, DateHelper


class FareTrackingStrategy:
    """
    Creates and manages fare tracking strategies that avoid price inflation.

    Key principles:
    1. Minimize active searches
    2. Use passive monitoring where possible
    3. Randomize search timing
    4. Isolate tracking sessions
    5. Set up smart alerts
    """

    def __init__(self, logger: Optional[FlightLogger] = None):
        self.logger = logger or FlightLogger("FareTracking")
        self.tracked_routes = []

    def create_tracking_strategy(
        self,
        origin: str,
        destination: str,
        departure_date: datetime,
        return_date: Optional[datetime] = None,
        target_price: Optional[float] = None,
        flexibility_days: int = 3
    ) -> Dict[str, Any]:
        """
        Create comprehensive tracking strategy for a route.

        Returns strategy with search frequency, timing, and alert setup.
        """
        self.logger.info(f"Creating tracking strategy for {origin} → {destination}")

        # Calculate days until departure
        days_until = (departure_date - datetime.now()).days

        # Determine search frequency based on urgency
        frequency = self._calculate_search_frequency(days_until)

        # Generate search schedule
        schedule = self._generate_search_schedule(days_until, frequency)

        # Alert setup recommendations
        alerts = self._setup_alert_recommendations()

        # Behavioral rules
        behavioral_rules = self._get_behavioral_rules()

        strategy = {
            'route': f"{origin} → {destination}",
            'departure_date': departure_date.strftime('%Y-%m-%d'),
            'return_date': return_date.strftime('%Y-%m-%d') if return_date else None,
            'target_price': target_price,
            'flexibility_days': flexibility_days,
            'days_until_departure': days_until,
            'search_frequency': frequency,
            'search_schedule': schedule,
            'alert_setup': alerts,
            'behavioral_rules': behavioral_rules,
            'platform_rotation': self._create_platform_rotation(),
            'session_protocol': self._create_session_protocol(),
            'price_drop_thresholds': self._calculate_drop_thresholds(target_price)
        }

        # Add to tracked routes
        self.tracked_routes.append({
            'route': f"{origin}-{destination}",
            'created': datetime.now().isoformat(),
            'strategy': strategy
        })

        return strategy

    def _calculate_search_frequency(self, days_until: int) -> Dict[str, Any]:
        """
        Calculate optimal search frequency to avoid inflation.

        Rule of thumb: The closer to departure, the more frequently you can search,
        but never more than once per day for the same route.
        """
        if days_until > 90:
            return {
                'frequency': 'Once per week',
                'max_searches_per_week': 1,
                'min_hours_between': 168,  # 7 days
                'reason': 'Far from departure, prices stable, infrequent checking sufficient'
            }
        elif days_until > 30:
            return {
                'frequency': 'Twice per week',
                'max_searches_per_week': 2,
                'min_hours_between': 72,  # 3 days
                'reason': 'Entering optimal booking window, moderate monitoring'
            }
        elif days_until > 14:
            return {
                'frequency': 'Every other day',
                'max_searches_per_week': 3,
                'min_hours_between': 48,
                'reason': 'Close to departure, prices may fluctuate'
            }
        elif days_until > 7:
            return {
                'frequency': 'Daily',
                'max_searches_per_week': 7,
                'min_hours_between': 24,
                'reason': 'Last 2 weeks, daily monitoring recommended'
            }
        else:
            return {
                'frequency': 'Every 12 hours',
                'max_searches_per_week': 14,
                'min_hours_between': 12,
                'reason': 'Final week, frequent monitoring but be cautious of inflation'
            }

    def _generate_search_schedule(
        self,
        days_until: int,
        frequency: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """
        Generate specific search schedule with recommended times.
        """
        schedule = []
        current_date = datetime.now()

        # Generate next 7 days of searches
        for day in range(7):
            search_date = current_date + timedelta(days=day)

            # Determine if should search on this day
            if frequency['max_searches_per_week'] >= 7:
                should_search = True
            elif frequency['max_searches_per_week'] >= 3:
                should_search = day % 2 == 0  # Every other day
            else:
                should_search = day % 7 == 0  # Once per week

            if should_search:
                # Randomize time within optimal window
                optimal_times = ['06:00', '07:00', '15:00', '16:00']
                import random
                time = random.choice(optimal_times)

                schedule.append({
                    'date': search_date.strftime('%Y-%m-%d'),
                    'day': search_date.strftime('%A'),
                    'recommended_time': time,
                    'time_zone': 'Local',
                    'notes': 'Use incognito mode, clear cookies first'
                })

        return schedule

    def _setup_alert_recommendations(self) -> Dict[str, Any]:
        """
        Recommend alert services and setup.
        """
        return {
            'recommended_services': [
                {
                    'service': 'Google Flights Price Tracking',
                    'pros': ['Free', 'Reliable', 'No manual searching needed'],
                    'cons': ['Limited to Google Flights inventory'],
                    'setup': [
                        'Search flight on Google Flights',
                        'Click "Track prices" toggle',
                        'Receive email alerts on price changes',
                        'Check email instead of searching repeatedly'
                    ],
                    'effectiveness': 'Very High'
                },
                {
                    'service': 'Kayak Price Alerts',
                    'pros': ['Multi-platform comparison', 'Flexible date tracking'],
                    'cons': ['Can be slow to update'],
                    'setup': [
                        'Search on Kayak.com',
                        'Create free account',
                        'Click "Create Price Alert"',
                        'Set target price threshold'
                    ],
                    'effectiveness': 'High'
                },
                {
                    'service': 'Skyscanner Price Alerts',
                    'pros': ['Whole month view', 'Good for flexible dates'],
                    'cons': ['Alerts can be delayed'],
                    'setup': [
                        'Search on Skyscanner',
                        'Click "Get Price Alerts"',
                        'Enter email',
                        'Choose alert frequency'
                    ],
                    'effectiveness': 'High'
                },
                {
                    'service': 'Hopper App',
                    'pros': ['Predictive analytics', 'Buy/wait recommendations'],
                    'cons': ['Mobile only', 'Some features require subscription'],
                    'setup': [
                        'Download Hopper app',
                        'Search flight',
                        'Enable "Watch This Trip"',
                        'Get push notifications'
                    ],
                    'effectiveness': 'Very High'
                },
                {
                    'service': 'AirfareWatchdog',
                    'pros': ['Finds mistake fares', 'Manual deal hunting'],
                    'cons': ['US-focused'],
                    'setup': [
                        'Sign up on AirfareWatchdog.com',
                        'Set departure city',
                        'Receive weekly deal emails'
                    ],
                    'effectiveness': 'Medium'
                }
            ],
            'recommended_approach': 'Use 2-3 alert services simultaneously for best coverage',
            'alert_threshold': 'Set alerts for 10-15% below current price',
            'alert_frequency': 'Daily digest preferred over real-time to avoid spam'
        }

    def _get_behavioral_rules(self) -> List[Dict[str, str]]:
        """
        Get behavioral rules to maintain price stability.
        """
        return [
            {
                'rule': 'One Search Per Session',
                'description': 'Search for your specific route once, then close browser',
                'importance': 'Critical',
                'rationale': 'Multiple searches in one session strongly trigger inflation'
            },
            {
                'rule': 'Always Use Incognito Mode',
                'description': 'Never search in regular browser mode',
                'importance': 'Critical',
                'rationale': 'Prevents cookie tracking across sessions'
            },
            {
                'rule': 'Minimum 24-Hour Gap',
                'description': 'Wait at least 24 hours between manual searches',
                'importance': 'High',
                'rationale': 'Frequent searches detected even across incognito sessions via IP'
            },
            {
                'rule': 'Rotate Platforms',
                'description': 'Don\'t search same route on same platform twice in a row',
                'importance': 'High',
                'rationale': 'Platform-specific tracking can link sessions'
            },
            {
                'rule': 'Prefer Alerts Over Searches',
                'description': 'Set up alerts and wait, rather than searching actively',
                'importance': 'Very High',
                'rationale': 'Alerts are passive and don\'t trigger inflation'
            },
            {
                'rule': 'Clear All Data Between Sessions',
                'description': 'Clear cookies, cache, and localStorage',
                'importance': 'High',
                'rationale': 'Complete data cleanup prevents session linking'
            },
            {
                'rule': 'Randomize Search Times',
                'description': 'Don\'t search at the same time each day',
                'importance': 'Medium',
                'rationale': 'Pattern detection can link searches'
            },
            {
                'rule': 'Book Immediately If Target Met',
                'description': 'When target price is reached, book within 1 hour',
                'importance': 'Critical',
                'rationale': 'Prices can change quickly, hesitation causes missed opportunities'
            },
            {
                'rule': 'Don\'t Complete Booking Unless Committing',
                'description': 'Never enter passenger details unless ready to purchase',
                'importance': 'High',
                'rationale': 'Cart abandonment heavily tracked and can raise future prices'
            },
            {
                'rule': 'Use Different Devices',
                'description': 'Rotate between phone, tablet, computer',
                'importance': 'Medium',
                'rationale': 'Device fingerprinting can link searches'
            }
        ]

    def _create_platform_rotation(self) -> Dict[str, Any]:
        """
        Create platform rotation schedule.
        """
        platforms = [
            'Google Flights',
            'Airline Direct',
            'Kayak',
            'Skyscanner',
            'Momondo',
            'Expedia'
        ]

        return {
            'platforms': platforms,
            'rotation_schedule': [
                {'search_number': 1, 'platform': 'Google Flights', 'reason': 'Best for initial price discovery'},
                {'search_number': 2, 'platform': 'Airline Direct', 'reason': 'Check direct pricing'},
                {'search_number': 3, 'platform': 'Kayak', 'reason': 'Multi-platform comparison'},
                {'search_number': 4, 'platform': 'Skyscanner', 'reason': 'Alternative inventory'},
                {'search_number': 5, 'platform': 'Momondo', 'reason': 'Often finds hidden deals'},
            ],
            'rule': 'Never use same platform twice in a row',
            'max_platforms_per_day': 2
        }

    def _create_session_protocol(self) -> List[Dict[str, str]]:
        """
        Create detailed session protocol.
        """
        return [
            {
                'step': '1. Preparation',
                'actions': [
                    'Close all browser windows',
                    'Clear all cookies and cache',
                    'Optional: Connect to VPN',
                    'Wait at least 24 hours since last search'
                ]
            },
            {
                'step': '2. Session Start',
                'actions': [
                    'Open new incognito/private window',
                    'Navigate directly to booking site (don\'t use Google search)',
                    'Verify cookies are disabled/cleared',
                    'Start timer for session duration'
                ]
            },
            {
                'step': '3. Search Execution',
                'actions': [
                    'Enter flight details exactly once',
                    'Review results',
                    'Take screenshot of best prices',
                    'Do NOT search additional dates or routes',
                    'Complete session in under 10 minutes'
                ]
            },
            {
                'step': '4. Decision Point',
                'actions': [
                    'If price meets target: Book immediately',
                    'If price too high: Close browser without booking',
                    'Do NOT start booking process unless committing',
                    'Do NOT browse other options'
                ]
            },
            {
                'step': '5. Session End',
                'actions': [
                    'Close all browser windows',
                    'Clear cookies and cache again',
                    'Log price in tracking spreadsheet',
                    'Set reminder for next search time',
                    'Disconnect VPN if used'
                ]
            }
        ]

    def _calculate_drop_thresholds(
        self,
        target_price: Optional[float]
    ) -> Dict[str, Any]:
        """
        Calculate when to act on price drops.
        """
        if not target_price:
            return {
                'note': 'No target price set',
                'recommendation': 'Monitor for 10-15% drops from initial price'
            }

        return {
            'target_price': target_price,
            'excellent_price': target_price * 0.85,  # 15% below target
            'good_price': target_price * 0.95,  # 5% below target
            'acceptable_price': target_price,
            'overpriced': target_price * 1.10,  # 10% above target
            'actions': {
                'excellent': 'BOOK IMMEDIATELY - Exceptional deal',
                'good': 'BOOK SOON - Good opportunity',
                'acceptable': 'BOOK if in optimal window',
                'overpriced': 'WAIT - Above target, continue monitoring'
            }
        }

    def export_strategy(self, strategy: Dict[str, Any], filepath: str = 'tracking_strategy.json'):
        """
        Export tracking strategy to file for reference.
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(strategy, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Strategy exported to {filepath}")
            return {'success': True, 'filepath': filepath}
        except Exception as e:
            self.logger.error(f"Failed to export strategy: {e}")
            return {'success': False, 'error': str(e)}

    def get_practical_example(
        self,
        origin: str = 'FRA',
        destination: str = 'JFK',
        days_until: int = 45
    ) -> Dict[str, Any]:
        """
        Provide practical example of tracking strategy in action.
        """
        departure_date = datetime.now() + timedelta(days=days_until)

        example = {
            'scenario': {
                'route': f"{origin} → {destination}",
                'departure_date': departure_date.strftime('%Y-%m-%d'),
                'days_until_departure': days_until,
                'target_price': 450.00,
                'current_price': 520.00
            },
            'week_by_week_plan': [
                {
                    'week': 1,
                    'actions': [
                        'Set up Google Flights price alert',
                        'Set up Kayak price alert',
                        'Manual search on Google Flights (incognito)',
                        'Log baseline price: €520',
                        'Set calendar reminder for next search'
                    ],
                    'searches': 1,
                    'time_spent': '15 minutes setup + 5 minutes search'
                },
                {
                    'week': 2,
                    'actions': [
                        'Check alert emails (no manual search needed)',
                        'If no alerts, one manual search mid-week',
                        'Use different platform (Kayak)',
                        'Log any price changes'
                    ],
                    'searches': '0-1 (prefer 0)',
                    'time_spent': '5 minutes'
                },
                {
                    'week': 3,
                    'actions': [
                        'Monitor alerts daily',
                        'Manual search if 7+ days since last',
                        'Consider booking if price drops to €480',
                        'Research alternative airports'
                    ],
                    'searches': '1-2',
                    'time_spent': '10 minutes'
                },
                {
                    'week': 4,
                    'actions': [
                        'Daily alert monitoring',
                        'Manual search every 3 days',
                        'Book immediately if hits €450 target',
                        'Consider booking even if slight above target'
                    ],
                    'searches': '2-3',
                    'time_spent': '15 minutes'
                },
                {
                    'week': 5,
                    'actions': [
                        'Increase to daily monitoring',
                        'Book if any significant drop occurs',
                        'Consider that prices may only increase from here',
                        'Make final decision by end of week'
                    ],
                    'searches': '3-5',
                    'time_spent': '20 minutes'
                }
            ],
            'total_searches': '7-12 over 5 weeks',
            'total_time': '~1 hour over 5 weeks',
            'expected_outcome': 'Catch 10-20% price drop without triggering inflation',
            'comparison': {
                'without_strategy': '30+ searches, prices artificially inflated 10-15%',
                'with_strategy': '7-12 searches, prices remain stable'
            }
        }

        return example


def monitor_price_stability(
    search_history: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Monitor if prices are being inflated based on search history.

    Detects patterns that indicate price inflation.
    """
    if len(search_history) < 2:
        return {
            'status': 'insufficient_data',
            'message': 'Need at least 2 searches to detect inflation'
        }

    # Calculate price trend
    prices = [s['price'] for s in search_history]
    avg_increase = sum([
        prices[i] - prices[i-1]
        for i in range(1, len(prices))
    ]) / (len(prices) - 1)

    # Detect suspicious patterns
    warnings = []

    if avg_increase > 10:
        warnings.append('Prices increasing steadily - possible inflation detected')

    if len(search_history) > 5:
        warnings.append('High search frequency may be triggering inflation')

    # Check time between searches
    times = [datetime.fromisoformat(s['timestamp']) for s in search_history]
    min_gap = min([
        (times[i] - times[i-1]).total_seconds() / 3600
        for i in range(1, len(times))
    ])

    if min_gap < 6:
        warnings.append('Searches too close together (< 6 hours)')

    return {
        'status': 'warning' if warnings else 'ok',
        'average_price_change': round(avg_increase, 2),
        'total_searches': len(search_history),
        'warnings': warnings,
        'recommendation': _get_stability_recommendation(warnings, len(search_history))
    }


def _get_stability_recommendation(warnings: List[str], search_count: int) -> str:
    """Get recommendation based on stability analysis."""
    if not warnings:
        return "✓ No inflation detected. Continue current strategy."

    if search_count > 5:
        return "⚠️ STOP SEARCHING. Wait 48-72 hours for prices to reset. Use alerts only."

    if len(warnings) > 2:
        return "⚠️ Multiple warning signs. Reduce search frequency immediately."

    return "⚠️ Potential inflation detected. Switch to alert-based monitoring."
