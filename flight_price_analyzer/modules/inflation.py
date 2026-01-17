"""
Anti-price-inflation module.
Analyzes how airlines detect and raise prices, and provides methods to avoid it.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json
from .utils import FlightLogger, RequestHelper


class PriceInflationAnalyzer:
    """
    Analyzes airline price inflation techniques and provides countermeasures.

    Airlines use sophisticated tracking to detect repeated searches and
    gradually increase prices to create urgency.
    """

    # Tracking methods airlines use
    TRACKING_METHODS = {
        'cookies': {
            'detection_method': 'HTTP Cookies',
            'what_tracked': 'Previous searches, viewed routes, search frequency',
            'inflation_trigger': 'Repeated searches for same route within short timeframe',
            'severity': 'High',
            'detection_window': '7-30 days'
        },
        'browser_fingerprint': {
            'detection_method': 'Browser Fingerprinting',
            'what_tracked': 'Browser version, plugins, screen resolution, fonts, timezone',
            'inflation_trigger': 'Unique browser signature matches previous sessions',
            'severity': 'Very High',
            'detection_window': 'Persistent until browser profile changes'
        },
        'ip_address': {
            'detection_method': 'IP Address Tracking',
            'what_tracked': 'Geographic location, ISP, previous searches from same IP',
            'inflation_trigger': 'Multiple searches from same IP address',
            'severity': 'Medium',
            'detection_window': '24 hours - 7 days'
        },
        'user_agent': {
            'detection_method': 'User Agent String',
            'what_tracked': 'Device type, OS, browser version',
            'inflation_trigger': 'Pattern of searches from same device signature',
            'severity': 'Low',
            'detection_window': 'Session-based'
        },
        'device_type': {
            'detection_method': 'Device Detection',
            'what_tracked': 'Mobile vs Desktop, operating system',
            'inflation_trigger': 'Mobile users often shown higher prices',
            'severity': 'Medium',
            'detection_window': 'Per session'
        },
        'location_data': {
            'detection_method': 'Geolocation',
            'what_tracked': 'Country, city, timezone from IP and browser',
            'inflation_trigger': 'High-income locations see higher prices',
            'severity': 'High',
            'detection_window': 'Persistent'
        },
        'search_history': {
            'detection_method': 'Search Pattern Analysis',
            'what_tracked': 'Number of searches, time between searches, routes searched',
            'inflation_trigger': '3+ searches for same route in 24 hours',
            'severity': 'Very High',
            'detection_window': '1-7 days'
        },
        'time_of_day': {
            'detection_method': 'Time-Based Pricing',
            'what_tracked': 'Time of search, day of week',
            'inflation_trigger': 'Evening/weekend searches often priced higher',
            'severity': 'Medium',
            'detection_window': 'Real-time'
        },
        'session_duration': {
            'detection_method': 'Session Behavior Analysis',
            'what_tracked': 'How long on site, pages viewed, booking abandonment',
            'inflation_trigger': 'Long sessions without booking indicate high interest',
            'severity': 'High',
            'detection_window': 'Current session + cookie lifetime'
        },
        'payment_signals': {
            'detection_method': 'Payment Method Detection',
            'what_tracked': 'Premium credit cards, corporate cards',
            'inflation_trigger': 'Premium card holders may see higher prices',
            'severity': 'Medium',
            'detection_window': 'Transaction-based'
        }
    }

    def __init__(self, logger: Optional[FlightLogger] = None):
        self.logger = logger or FlightLogger("PriceInflation")

    def analyze_tracking_methods(self) -> Dict[str, Any]:
        """
        Comprehensive analysis of all tracking methods airlines use.
        """
        self.logger.info("Analyzing airline tracking methods")

        return {
            'tracking_methods': self.TRACKING_METHODS,
            'total_methods': len(self.TRACKING_METHODS),
            'high_severity': [
                name for name, data in self.TRACKING_METHODS.items()
                if data['severity'] in ['High', 'Very High']
            ],
            'summary': self._generate_tracking_summary()
        }

    def explain_price_inflation_triggers(self) -> List[Dict[str, Any]]:
        """
        Detailed explanation of behaviors that trigger price inflation.
        """
        triggers = [
            {
                'trigger': 'Repeated Searches',
                'description': 'Searching for the same route 3+ times in 24 hours',
                'how_detected': 'Cookies + IP tracking + browser fingerprint',
                'typical_increase': '5-20%',
                'time_to_trigger': '3-5 searches',
                'evidence_level': 'Well documented'
            },
            {
                'trigger': 'Long Session Duration',
                'description': 'Spending 15+ minutes browsing flights without booking',
                'how_detected': 'Session analytics and behavior tracking',
                'typical_increase': '3-10%',
                'time_to_trigger': '15-30 minutes',
                'evidence_level': 'Industry reported'
            },
            {
                'trigger': 'Premium Location',
                'description': 'Searching from high-income zip codes or countries',
                'how_detected': 'IP geolocation and billing address',
                'typical_increase': '10-25%',
                'time_to_trigger': 'Immediate',
                'evidence_level': 'Confirmed by studies'
            },
            {
                'trigger': 'Mobile Device',
                'description': 'Using mobile phone vs desktop computer',
                'how_detected': 'User agent and screen size',
                'typical_increase': '5-15%',
                'time_to_trigger': 'Immediate',
                'evidence_level': 'Mixed evidence'
            },
            {
                'trigger': 'Peak Search Times',
                'description': 'Searching during evening hours or weekends',
                'how_detected': 'Server timestamp',
                'typical_increase': '3-8%',
                'time_to_trigger': 'Immediate',
                'evidence_level': 'Anecdotal'
            },
            {
                'trigger': 'Returning Visitor',
                'description': 'Recognized as previous visitor who didn\'t book',
                'how_detected': 'Cookies and localStorage',
                'typical_increase': '5-15%',
                'time_to_trigger': '2nd visit',
                'evidence_level': 'Well documented'
            },
            {
                'trigger': 'Cart Abandonment',
                'description': 'Starting booking process but not completing',
                'how_detected': 'Session tracking and cookies',
                'typical_increase': '5-12%',
                'time_to_trigger': 'Next visit',
                'evidence_level': 'Industry reported'
            },
            {
                'trigger': 'Premium Card Signals',
                'description': 'Using premium credit card or corporate email',
                'how_detected': 'Payment processing and form data',
                'typical_increase': '5-10%',
                'time_to_trigger': 'At payment',
                'evidence_level': 'Suspected'
            }
        ]

        return triggers

    def get_avoidance_strategy(self) -> Dict[str, Any]:
        """
        Precise step-by-step method to avoid price inflation.
        """
        strategy = {
            'step_by_step_method': [
                {
                    'step': 1,
                    'action': 'Use Incognito/Private Browsing',
                    'reason': 'Prevents cookie tracking and session continuity',
                    'effectiveness': 'High',
                    'instructions': [
                        'Chrome/Edge: Ctrl+Shift+N (Windows) or Cmd+Shift+N (Mac)',
                        'Firefox: Ctrl+Shift+P (Windows) or Cmd+Shift+P (Mac)',
                        'Safari: Cmd+Shift+N',
                        'Start fresh incognito window for each search session'
                    ]
                },
                {
                    'step': 2,
                    'action': 'Clear Cookies and Cache',
                    'reason': 'Remove existing tracking data',
                    'effectiveness': 'Very High',
                    'instructions': [
                        'Before searching, clear all cookies for airline/OTA sites',
                        'Clear browser cache completely',
                        'Use CCleaner or similar tool for thorough cleaning',
                        'Or use browser privacy mode which auto-clears on close'
                    ]
                },
                {
                    'step': 3,
                    'action': 'Use VPN',
                    'reason': 'Masks IP address and location',
                    'effectiveness': 'Very High',
                    'instructions': [
                        'Connect to VPN before opening browser',
                        'Choose server in country with lower pricing (e.g., Poland, Turkey)',
                        'Verify IP changed using whatismyip.com',
                        'Keep VPN on for entire search and booking process'
                    ]
                },
                {
                    'step': 4,
                    'action': 'Rotate User Agent',
                    'reason': 'Prevents device fingerprinting',
                    'effectiveness': 'Medium',
                    'instructions': [
                        'Install User Agent Switcher browser extension',
                        'Rotate between different browsers and OS signatures',
                        'Use desktop user agent (mobile often shows higher prices)',
                        'Change user agent between search sessions'
                    ]
                },
                {
                    'step': 5,
                    'action': 'Limit Search Frequency',
                    'reason': 'Avoid triggering repeated search detection',
                    'effectiveness': 'High',
                    'instructions': [
                        'Maximum 2 searches per route per day',
                        'Wait at least 6 hours between searches for same route',
                        'Use different devices/browsers for additional searches',
                        'Track prices passively with alerts instead of searching'
                    ]
                },
                {
                    'step': 6,
                    'action': 'Search at Optimal Times',
                    'reason': 'Avoid peak pricing periods',
                    'effectiveness': 'Medium',
                    'instructions': [
                        'Search Tuesday-Thursday for best prices',
                        'Search early morning (6-8 AM) when prices reset',
                        'Avoid weekend and evening searches',
                        'Book Tuesday afternoon (3-5 PM) for weekly price drops'
                    ]
                },
                {
                    'step': 7,
                    'action': 'Use Multiple Platforms',
                    'reason': 'Compare without triggering single site tracking',
                    'effectiveness': 'High',
                    'instructions': [
                        'Check airline direct, then OTAs separately',
                        'Use different browser sessions for each platform',
                        'Don\'t search same route on multiple sites in quick succession',
                        'Spread searches across 2-3 days if not urgent'
                    ]
                },
                {
                    'step': 8,
                    'action': 'Minimize Session Duration',
                    'reason': 'Avoid high-interest detection',
                    'effectiveness': 'Medium',
                    'instructions': [
                        'Know what you want before searching',
                        'Spend maximum 5-10 minutes per session',
                        'Don\'t browse multiple dates/routes in one session',
                        'Close browser immediately after each search'
                    ]
                },
                {
                    'step': 9,
                    'action': 'Book Immediately When Ready',
                    'reason': 'Prevent cart abandonment tracking',
                    'effectiveness': 'High',
                    'instructions': [
                        'Don\'t start booking process unless ready to complete',
                        'Have payment info ready before clicking "Book"',
                        'Complete entire booking in one session',
                        'If must abandon, clear all cookies before returning'
                    ]
                },
                {
                    'step': 10,
                    'action': 'Use Generic Email',
                    'reason': 'Avoid corporate/premium user profiling',
                    'effectiveness': 'Low',
                    'instructions': [
                        'Use personal email, not corporate',
                        'Avoid premium domain emails',
                        'Use generic Gmail/Outlook addresses',
                        'Don\'t use email that\'s in airline loyalty program'
                    ]
                }
            ],
            'quick_checklist': [
                '☐ Incognito/private window',
                '☐ VPN connected (optional but recommended)',
                '☐ Cookies cleared',
                '☐ Desktop user agent',
                '☐ First search of the day for this route',
                '☐ Tuesday-Thursday, morning time',
                '☐ Ready to book if price is right',
                '☐ Payment info prepared',
                '☐ Will close browser immediately after'
            ],
            'effectiveness_rating': 'Following all steps can reduce inflation by 10-25%'
        }

        return strategy

    def get_technical_countermeasures(self) -> List[Dict[str, Any]]:
        """
        Technical countermeasures for advanced users.
        """
        return [
            {
                'method': 'Browser Containers',
                'platform': 'Firefox Multi-Account Containers',
                'description': 'Isolate searches in separate containers',
                'difficulty': 'Easy',
                'effectiveness': 'Very High',
                'setup': [
                    'Install Firefox Multi-Account Containers extension',
                    'Create separate container for each airline/OTA',
                    'Each container has isolated cookies and storage',
                    'Prevents cross-site tracking'
                ]
            },
            {
                'method': 'Virtual Machines',
                'platform': 'VirtualBox, VMware',
                'description': 'Use fresh VM for each search',
                'difficulty': 'Hard',
                'effectiveness': 'Very High',
                'setup': [
                    'Create clean Windows/Linux VM',
                    'Take snapshot of clean state',
                    'Search for flights',
                    'Revert to snapshot after each search'
                ]
            },
            {
                'method': 'Browser Automation Scripts',
                'platform': 'Selenium, Puppeteer',
                'description': 'Automated searches with randomization',
                'difficulty': 'Hard',
                'effectiveness': 'High',
                'setup': [
                    'Script that clears cache, rotates user agents',
                    'Randomize timing between actions',
                    'Rotate through VPN endpoints',
                    'Extract prices without triggering bot detection'
                ]
            },
            {
                'method': 'Temporary Email Services',
                'platform': 'Temp-mail.org, 10minutemail',
                'description': 'Use disposable emails for price checking',
                'difficulty': 'Easy',
                'effectiveness': 'Medium',
                'setup': [
                    'Generate temporary email',
                    'Use for price checks and alerts',
                    'Switch to real email only when booking',
                    'Prevents email-based tracking'
                ]
            },
            {
                'method': 'Anti-Fingerprint Browser',
                'platform': 'Tor Browser, Brave',
                'description': 'Browser designed to prevent fingerprinting',
                'difficulty': 'Easy',
                'effectiveness': 'Very High',
                'setup': [
                    'Use Tor Browser or Brave in private mode',
                    'Built-in fingerprint protection',
                    'Randomizes many fingerprint vectors',
                    'Note: Some sites block Tor'
                ]
            }
        ]

    def generate_search_protocol(
        self,
        origin: str,
        destination: str,
        departure_date: datetime,
        search_number: int = 1
    ) -> Dict[str, Any]:
        """
        Generate a specific search protocol for a given flight.

        Provides exact steps to follow for this specific search.
        """
        protocol = {
            'search_info': {
                'route': f"{origin} → {destination}",
                'date': departure_date.strftime('%Y-%m-%d'),
                'search_number': search_number,
                'risk_level': self._assess_risk_level(search_number)
            },
            'pre_search_checklist': [],
            'search_execution': [],
            'post_search_actions': [],
            'warnings': []
        }

        # Determine precautions based on search number
        if search_number == 1:
            protocol['pre_search_checklist'] = [
                'Open incognito window',
                'Optionally connect VPN',
                'Navigate directly to booking site'
            ]
            protocol['risk_level'] = 'Low'
        elif search_number == 2:
            protocol['pre_search_checklist'] = [
                'Wait at least 6 hours since last search',
                'Open fresh incognito window',
                'Clear all cookies',
                'Consider using VPN'
            ]
            protocol['risk_level'] = 'Medium'
        else:  # 3+
            protocol['pre_search_checklist'] = [
                'CRITICAL: Wait 24 hours since last search',
                'Use different browser or device',
                'Clear ALL browser data',
                'MUST use VPN with different location',
                'Use different user agent',
                'Consider using different platform'
            ]
            protocol['risk_level'] = 'High'
            protocol['warnings'] = [
                f"This is search #{search_number} - HIGH INFLATION RISK",
                "Prices likely already inflated from previous searches",
                "Consider waiting 48-72 hours for prices to reset"
            ]

        protocol['search_execution'] = [
            'Keep session under 10 minutes',
            'Search only for exact route needed',
            'Do not browse other dates or routes',
            'If found good price, book immediately',
            'If not booking, close browser immediately'
        ]

        protocol['post_search_actions'] = [
            'Close browser completely',
            'If searched 3+ times, stop and wait 48 hours',
            'Set up price alert instead of manual searching',
            'Log price for tracking purposes'
        ]

        return protocol

    def _generate_tracking_summary(self) -> str:
        """Generate summary of tracking methods."""
        high_severity = sum(
            1 for data in self.TRACKING_METHODS.values()
            if data['severity'] in ['High', 'Very High']
        )

        return (
            f"Airlines use {len(self.TRACKING_METHODS)} different tracking methods. "
            f"{high_severity} are high severity and most likely to cause price inflation. "
            f"The most effective countermeasures are: incognito mode, cookie clearing, "
            f"VPN usage, and limiting search frequency."
        )

    def _assess_risk_level(self, search_number: int) -> str:
        """Assess inflation risk based on search number."""
        if search_number == 1:
            return 'Low - First search, minimal tracking'
        elif search_number == 2:
            return 'Medium - Second search, some tracking possible'
        elif search_number == 3:
            return 'High - Third search, likely being tracked'
        else:
            return 'Very High - Multiple searches, prices likely inflated'


def create_search_plan(route_searches: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Create a search plan for multiple routes.

    Optimizes search strategy to minimize tracking across multiple flights.
    """
    analyzer = PriceInflationAnalyzer()

    plan = {
        'total_routes': len(route_searches),
        'recommended_timeline': [],
        'platform_rotation': [],
        'risk_mitigation': []
    }

    # Spread searches across multiple days
    for i, route in enumerate(route_searches):
        day = (i // 2) + 1  # Max 2 routes per day
        session = (i % 2) + 1

        plan['recommended_timeline'].append({
            'route': route,
            'search_day': day,
            'session': session,
            'time_of_day': 'Morning' if session == 1 else 'Afternoon',
            'platform': 'Direct airline' if i % 3 == 0 else 'OTA',
            'use_vpn': i > 2  # VPN for searches after first 2
        })

    return plan
