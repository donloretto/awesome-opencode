#!/usr/bin/env python3
"""
Flight Price Analyzer - Main Entry Point

Comprehensive flight price analysis tool implementing 7 key strategies:
1. Hidden city tickets and alternative routing
2. Anti-price-inflation techniques
3. Geo-pricing simulation
4. Historical pricing analysis
5. Fare rules and ticket class breakdown
6. Platform comparison
7. Fare tracking strategy
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent))

from modules.utils import FlightLogger, DateHelper, AirportHelper
from modules.search import FlightSearchEngine
from modules.geo_pricing import GeoPricingAnalyzer
from modules.inflation import PriceInflationAnalyzer
from modules.historical import HistoricalPricingAnalyzer
from modules.fare_tracking import FareTrackingStrategy
from modules.platform_compare import PlatformComparator


class FlightPriceAnalyzer:
    """Main application class coordinating all analysis modules."""

    def __init__(self, config_path: str = 'config.json'):
        self.logger = FlightLogger("Main")
        self.config = self._load_config(config_path)

        # Initialize all modules
        self.search_engine = FlightSearchEngine(self.logger)
        self.geo_analyzer = GeoPricingAnalyzer(self.logger)
        self.inflation_analyzer = PriceInflationAnalyzer(self.logger)
        self.historical_analyzer = HistoricalPricingAnalyzer(self.logger)
        self.tracking_strategy = FareTrackingStrategy(self.logger)
        self.platform_comparator = PlatformComparator(self.logger)

        self.logger.info("Flight Price Analyzer initialized")

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            config_file = Path(__file__).parent / config_path
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.warning(f"Config file {config_path} not found, using defaults")
            return {}

    def comprehensive_analysis(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        return_date: Optional[str] = None,
        target_price: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Perform comprehensive analysis covering all 7 strategies.

        Args:
            origin: Origin airport code (e.g., 'FRA')
            destination: Destination airport code (e.g., 'JFK')
            departure_date: Departure date in YYYY-MM-DD format
            return_date: Optional return date
            target_price: Optional target price in EUR
        """
        self.logger.info(f"\n{'='*80}")
        self.logger.info(f"COMPREHENSIVE FLIGHT PRICE ANALYSIS")
        self.logger.info(f"{'='*80}")
        self.logger.info(f"Route: {origin} → {destination}")
        self.logger.info(f"Departure: {departure_date}")
        if return_date:
            self.logger.info(f"Return: {return_date}")
        self.logger.info(f"{'='*80}\n")

        # Parse dates
        dep_date = DateHelper.parse_date(departure_date)
        ret_date = DateHelper.parse_date(return_date) if return_date else None

        results = {
            'route_info': {
                'origin': origin,
                'destination': destination,
                'departure_date': departure_date,
                'return_date': return_date,
                'route_description': AirportHelper.format_route(origin, destination)
            }
        }

        # Strategy 1: Advanced Search (Hidden City, Nearby Airports, Multi-leg)
        if self.config.get('modules', {}).get('search', {}).get('enabled', True):
            self.logger.info("📍 [1/7] Analyzing Hidden City Tickets & Alternative Routing...")
            search_results = self.search_engine.comprehensive_search(
                origin, destination, dep_date, ret_date
            )
            results['advanced_search'] = search_results

        # Strategy 2: Anti-Price-Inflation
        if self.config.get('modules', {}).get('inflation', {}).get('enabled', True):
            self.logger.info("🛡️  [2/7] Analyzing Price Inflation Triggers & Avoidance...")
            results['price_inflation'] = {
                'tracking_methods': self.inflation_analyzer.analyze_tracking_methods(),
                'triggers': self.inflation_analyzer.explain_price_inflation_triggers(),
                'avoidance_strategy': self.inflation_analyzer.get_avoidance_strategy(),
                'search_protocol': self.inflation_analyzer.generate_search_protocol(
                    origin, destination, dep_date, search_number=1
                )
            }

        # Strategy 3: Geo-Pricing Simulation
        if self.config.get('modules', {}).get('geo_pricing', {}).get('enabled', True):
            self.logger.info("🌍 [3/7] Simulating Geo-Pricing Across Countries...")
            base_price = results.get('advanced_search', {}).get('direct_flight', {}).get('price', 450.0)
            results['geo_pricing'] = self.geo_analyzer.find_cheapest_market(
                base_price, 'EUR', origin, destination, dep_date
            )
            results['geo_pricing']['access_methods'] = self.geo_analyzer.legal_access_methods(
                results['geo_pricing']['cheapest_market']['country']
            )

        # Strategy 4: Historical Pricing Analysis
        if self.config.get('modules', {}).get('historical', {}).get('enabled', True):
            self.logger.info("📊 [4/7] Analyzing Historical Pricing Patterns...")
            results['historical_analysis'] = self.historical_analyzer.get_comprehensive_analysis(
                origin, destination, dep_date, ret_date
            )

        # Strategy 5: Fare Rules Analysis (integrated in search results)
        self.logger.info("📋 [5/7] Analyzing Fare Rules & Ticket Classes...")
        results['fare_rules'] = self._analyze_fare_rules()

        # Strategy 6: Platform Comparison
        if self.config.get('modules', {}).get('platform_compare', {}).get('enabled', True):
            self.logger.info("💰 [6/7] Comparing Booking Platforms...")
            base_price = results.get('advanced_search', {}).get('direct_flight', {}).get('price', 450.0)
            results['platform_comparison'] = self.platform_comparator.compare_platforms(
                base_price, origin, destination
            )

        # Strategy 7: Fare Tracking Strategy
        if self.config.get('modules', {}).get('fare_tracking', {}).get('enabled', True):
            self.logger.info("🔔 [7/7] Creating Fare Tracking Strategy...")
            results['tracking_strategy'] = self.tracking_strategy.create_tracking_strategy(
                origin, destination, dep_date, ret_date, target_price
            )
            results['tracking_example'] = self.tracking_strategy.get_practical_example(
                origin, destination, (dep_date - datetime.now()).days
            )

        # Generate final recommendations
        results['final_recommendations'] = self._generate_final_recommendations(results)

        self.logger.info(f"\n{'='*80}")
        self.logger.info("ANALYSIS COMPLETE")
        self.logger.info(f"{'='*80}\n")

        return results

    def _analyze_fare_rules(self) -> Dict[str, Any]:
        """Analyze fare rules and ticket classes."""
        return {
            'ticket_classes': {
                'economy_basic': {
                    'description': 'Cheapest option, most restrictions',
                    'typical_features': ['No changes', 'No refunds', 'Last to board', 'No seat selection'],
                    'cost_savings': '20-30% vs standard economy',
                    'recommendation': 'Good for certain travel, no flexibility needed'
                },
                'economy_standard': {
                    'description': 'Standard economy with moderate flexibility',
                    'typical_features': ['Paid changes allowed', 'Seat selection', 'Standard baggage'],
                    'cost_savings': 'Baseline',
                    'recommendation': 'Best balance of price and flexibility'
                },
                'economy_flex': {
                    'description': 'Flexible economy ticket',
                    'typical_features': ['Free changes', 'Refundable (with fee)', 'Priority boarding'],
                    'cost_increase': '30-50% vs standard',
                    'recommendation': 'Only if high chance of changes needed'
                },
                'premium_economy': {
                    'description': 'Enhanced comfort, moderate price increase',
                    'typical_features': ['More legroom', 'Better meals', 'Priority boarding', 'More baggage'],
                    'cost_increase': '50-100% vs economy',
                    'recommendation': 'Consider for long-haul (8+ hours)'
                }
            },
            'routing_logic': {
                'direct_flights': 'Most expensive but most convenient',
                'one_stop': '15-30% cheaper, reasonable for medium distances',
                'two_stops': '30-50% cheaper, only worthwhile for large savings',
                'self_transfer': 'Cheapest but highest risk, no protection'
            },
            'pricing_conditions': {
                'advance_purchase': 'Book 21-90 days ahead for best economy prices',
                'saturday_night_stay': 'Often required for cheap fares (legacy rule)',
                'minimum_stay': 'Some fares require 2-7 night minimum',
                'maximum_stay': 'Typically 1-12 months from departure'
            },
            'cost_reduction_tips': [
                'Choose basic economy if no baggage needed',
                'Bring own food to avoid inflated onboard prices',
                'Select free seats (usually middle seats)',
                'Join loyalty program even for one flight (better support)',
                'Book separate one-way tickets if cheaper than round-trip',
                'Consider nearby airports (may save 30%+)',
                'Fly Tuesday/Wednesday instead of Friday/Sunday (10-20% cheaper)',
                'Book on Tuesday afternoon for weekly low prices'
            ]
        }

    def _generate_final_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate prioritized final recommendations."""
        recommendations = []

        # Top cheapest option
        if 'advanced_search' in results:
            cheapest = results['advanced_search'].get('cheapest_option', {})
            recommendations.append(
                f"💰 CHEAPEST OPTION: {cheapest.get('route_type', 'Unknown')} route at "
                f"€{cheapest.get('price', 0):.2f}"
            )

        # Geo-pricing opportunity
        if 'geo_pricing' in results:
            geo = results['geo_pricing']
            if geo.get('max_savings', 0) > 30:
                recommendations.append(
                    f"🌍 GEO-PRICING: Save €{geo['max_savings']:.2f} by booking from "
                    f"{geo['cheapest_market']['country_name']}"
                )

        # Booking window
        if 'historical_analysis' in results:
            hist = results['historical_analysis'].get('booking_window_analysis', {})
            if hist.get('currently_optimal'):
                recommendations.append("✅ TIMING: You're in the optimal booking window - good time to book!")
            else:
                recommendations.append(f"⏰ TIMING: {hist.get('recommendation', '')}")

        # Price inflation warning
        recommendations.append(
            "🛡️  IMPORTANT: Use incognito mode, clear cookies, and limit searches to avoid price inflation"
        )

        # Platform recommendation
        if 'platform_comparison' in results:
            platform = results['platform_comparison'].get('cheapest_overall', {})
            recommendations.append(
                f"💻 PLATFORM: Book via {platform.get('platform', 'N/A')} for lowest total cost"
            )

        # Tracking strategy
        recommendations.append(
            "🔔 TRACKING: Set up Google Flights & Kayak price alerts instead of manual searching"
        )

        return recommendations

    def export_results(self, results: Dict[str, Any], format: str = 'json', filename: str = 'analysis_results'):
        """Export results to file."""
        output_path = Path(__file__).parent / f"{filename}.{format}"

        try:
            if format == 'json':
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2, ensure_ascii=False, default=str)
            else:
                self.logger.error(f"Unsupported format: {format}")
                return

            self.logger.info(f"Results exported to {output_path}")
        except Exception as e:
            self.logger.error(f"Export failed: {e}")

    def print_summary(self, results: Dict[str, Any]):
        """Print human-readable summary."""
        print("\n" + "="*80)
        print("FLIGHT PRICE ANALYSIS SUMMARY")
        print("="*80)

        # Route info
        route = results.get('route_info', {})
        print(f"\nRoute: {route.get('route_description', 'N/A')}")
        print(f"Departure: {route.get('departure_date', 'N/A')}")
        if route.get('return_date'):
            print(f"Return: {route.get('return_date')}")

        # Recommendations
        print("\n" + "-"*80)
        print("KEY RECOMMENDATIONS:")
        print("-"*80)
        for i, rec in enumerate(results.get('final_recommendations', []), 1):
            print(f"{i}. {rec}")

        # Price summary
        if 'advanced_search' in results:
            print("\n" + "-"*80)
            print("PRICE SUMMARY:")
            print("-"*80)
            direct = results['advanced_search'].get('direct_flight', {})
            cheapest = results['advanced_search'].get('cheapest_option', {})

            print(f"Direct Flight: €{direct.get('price', 0):.2f}")
            print(f"Cheapest Option: €{cheapest.get('price', 0):.2f} ({cheapest.get('route_type', 'N/A')})")

            if 'price_analysis' in results['advanced_search']:
                analysis = results['advanced_search']['price_analysis']
                print(f"Potential Savings: €{analysis.get('savings_amount', 0):.2f} "
                      f"({analysis.get('savings_percentage', 0):.1f}%)")

        print("\n" + "="*80 + "\n")


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description='Flight Price Analyzer - Find the cheapest flights using advanced strategies'
    )

    parser.add_argument('origin', help='Origin airport code (e.g., FRA)')
    parser.add_argument('destination', help='Destination airport code (e.g., JFK)')
    parser.add_argument('departure_date', help='Departure date (YYYY-MM-DD)')
    parser.add_argument('--return-date', '-r', help='Return date (YYYY-MM-DD)')
    parser.add_argument('--target-price', '-t', type=float, help='Target price in EUR')
    parser.add_argument('--output', '-o', default='json', choices=['json'], help='Output format')
    parser.add_argument('--export', '-e', help='Export results to file (without extension)')
    parser.add_argument('--config', '-c', default='config.json', help='Config file path')

    args = parser.parse_args()

    # Create analyzer
    analyzer = FlightPriceAnalyzer(config_path=args.config)

    # Run analysis
    results = analyzer.comprehensive_analysis(
        origin=args.origin.upper(),
        destination=args.destination.upper(),
        departure_date=args.departure_date,
        return_date=args.return_date,
        target_price=args.target_price
    )

    # Print summary
    analyzer.print_summary(results)

    # Export if requested
    if args.export:
        analyzer.export_results(results, format=args.output, filename=args.export)
    else:
        # Always export to default location
        analyzer.export_results(results, format=args.output)


if __name__ == '__main__':
    main()
