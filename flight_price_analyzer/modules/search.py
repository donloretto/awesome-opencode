"""
Flight search module with advanced routing strategies.
Implements hidden city ticketing, nearby airports, and multi-leg combinations.
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import itertools
from .utils import (
    FlightLogger, AirportHelper, DateHelper,
    format_duration, calculate_price_difference, BookingLinkGenerator
)


class FlightRoute:
    """Represents a flight route with pricing and details."""

    def __init__(
        self,
        origin: str,
        destination: str,
        departure_date: datetime,
        return_date: Optional[datetime] = None,
        price: float = 0.0,
        currency: str = 'EUR',
        legs: Optional[List[Dict]] = None,
        route_type: str = 'direct',
        booking_link: Optional[str] = None,
        booking_links: Optional[Dict[str, str]] = None
    ):
        self.origin = origin
        self.destination = destination
        self.departure_date = departure_date
        self.return_date = return_date
        self.price = price
        self.currency = currency
        self.legs = legs or []
        self.route_type = route_type
        self.booking_link = booking_link
        self.booking_links = booking_links or self._generate_booking_links()

    def _generate_booking_links(self) -> Dict[str, str]:
        """Generate booking links for all platforms."""
        return BookingLinkGenerator.generate_all_links(
            self.origin,
            self.destination,
            self.departure_date,
            self.return_date
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert route to dictionary."""
        return {
            'origin': self.origin,
            'destination': self.destination,
            'departure_date': self.departure_date.isoformat(),
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'price': self.price,
            'currency': self.currency,
            'legs': self.legs,
            'route_type': self.route_type,
            'booking_link': self.booking_link or self.booking_links.get('google_flights'),
            'booking_links': self.booking_links,
            'route_description': AirportHelper.format_route(self.origin, self.destination)
        }


class FlightSearchEngine:
    """
    Advanced flight search engine.

    Implements strategies for finding cheaper flights:
    1. Hidden city ticketing
    2. Nearby airport combinations
    3. Multi-leg route optimization
    4. Split ticket analysis
    """

    def __init__(self, logger: Optional[FlightLogger] = None):
        self.logger = logger or FlightLogger("FlightSearch")
        self.airport_helper = AirportHelper()

    def search_direct_flight(
        self,
        origin: str,
        destination: str,
        departure_date: datetime,
        return_date: Optional[datetime] = None
    ) -> FlightRoute:
        """
        Simulate direct flight search.
        In production, this would query actual flight APIs.
        """
        self.logger.info(f"Searching direct flight: {origin} → {destination}")

        # Simulate flight data (in production, query real APIs)
        base_price = self._calculate_base_price(origin, destination, departure_date)

        legs = [{
            'origin': origin,
            'destination': destination,
            'departure': departure_date.isoformat(),
            'arrival': departure_date.isoformat(),
            'airline': 'Sample Airline',
            'flight_number': 'XX1234',
            'duration': 120  # minutes
        }]

        if return_date:
            legs.append({
                'origin': destination,
                'destination': origin,
                'departure': return_date.isoformat(),
                'arrival': return_date.isoformat(),
                'airline': 'Sample Airline',
                'flight_number': 'XX5678',
                'duration': 120
            })
            base_price *= 1.8  # Round trip pricing

        return FlightRoute(
            origin=origin,
            destination=destination,
            departure_date=departure_date,
            return_date=return_date,
            price=base_price,
            currency='EUR',
            legs=legs,
            route_type='direct'
        )

    def search_hidden_city(
        self,
        origin: str,
        destination: str,
        departure_date: datetime
    ) -> List[FlightRoute]:
        """
        Find hidden city ticket opportunities.

        Hidden city ticketing: Booking a flight to a city beyond your
        actual destination, getting off at the layover point.

        Example: FRA → NYC costs $800, but FRA → NYC → BOS costs $600.
        You book to Boston but get off in NYC.

        WARNING: This violates most airline terms of service.
        Only for educational/analytical purposes.
        """
        self.logger.info(f"Analyzing hidden city opportunities for {origin} → {destination}")

        hidden_city_routes = []

        # Major hub cities that could be beyond the destination
        potential_hidden_cities = self._get_cities_beyond(destination)

        for hidden_dest in potential_hidden_cities:
            # Check if route goes through actual destination
            route = self._simulate_layover_route(origin, hidden_dest, destination, departure_date)

            if route and route.price < self.search_direct_flight(origin, destination, departure_date).price:
                route.route_type = 'hidden_city'
                hidden_city_routes.append(route)

        return hidden_city_routes

    def search_nearby_airports(
        self,
        origin: str,
        destination: str,
        departure_date: datetime,
        return_date: Optional[datetime] = None
    ) -> List[FlightRoute]:
        """
        Search flights from/to nearby airports.

        Often flights to/from alternative airports are significantly cheaper.
        """
        self.logger.info(f"Searching nearby airport combinations")

        nearby_routes = []

        # Get nearby airports
        origin_airports = [origin] + self.airport_helper.get_nearby_airports(origin)
        dest_airports = [destination] + self.airport_helper.get_nearby_airports(destination)

        # Try all combinations
        for orig, dest in itertools.product(origin_airports, dest_airports):
            if orig == origin and dest == destination:
                continue  # Skip the original route

            route = self.search_direct_flight(orig, dest, departure_date, return_date)
            route.route_type = 'nearby_airport'
            nearby_routes.append(route)

        return sorted(nearby_routes, key=lambda r: r.price)

    def search_multi_leg(
        self,
        origin: str,
        destination: str,
        departure_date: datetime,
        return_date: Optional[datetime] = None
    ) -> List[FlightRoute]:
        """
        Find multi-leg combinations that airlines don't surface.

        Sometimes booking separate tickets for different legs is cheaper
        than a single through ticket.
        """
        self.logger.info(f"Analyzing multi-leg route combinations")

        multi_leg_routes = []

        # Find potential hub cities
        hubs = self._get_potential_hubs(origin, destination)

        for hub in hubs:
            # Split into two separate bookings
            leg1_price = self.search_direct_flight(origin, hub, departure_date).price
            leg2_price = self.search_direct_flight(hub, destination, departure_date).price

            total_price = leg1_price + leg2_price

            legs = [
                {
                    'origin': origin,
                    'destination': hub,
                    'departure': departure_date.isoformat(),
                    'price': leg1_price,
                    'booking_type': 'separate'
                },
                {
                    'origin': hub,
                    'destination': destination,
                    'departure': departure_date.isoformat(),
                    'price': leg2_price,
                    'booking_type': 'separate'
                }
            ]

            if return_date:
                leg3_price = self.search_direct_flight(destination, hub, return_date).price
                leg4_price = self.search_direct_flight(hub, origin, return_date).price
                total_price += leg3_price + leg4_price

                legs.extend([
                    {
                        'origin': destination,
                        'destination': hub,
                        'departure': return_date.isoformat(),
                        'price': leg3_price,
                        'booking_type': 'separate'
                    },
                    {
                        'origin': hub,
                        'destination': origin,
                        'departure': return_date.isoformat(),
                        'price': leg4_price,
                        'booking_type': 'separate'
                    }
                ])

            route = FlightRoute(
                origin=origin,
                destination=destination,
                departure_date=departure_date,
                return_date=return_date,
                price=total_price,
                currency='EUR',
                legs=legs,
                route_type='multi_leg_split'
            )
            multi_leg_routes.append(route)

        return sorted(multi_leg_routes, key=lambda r: r.price)

    def comprehensive_search(
        self,
        origin: str,
        destination: str,
        departure_date: datetime,
        return_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Perform comprehensive search with all strategies.

        Returns ranked results with price gap analysis.
        """
        self.logger.info(f"Starting comprehensive search: {origin} → {destination}")

        all_routes = []

        # 1. Direct flight
        direct = self.search_direct_flight(origin, destination, departure_date, return_date)
        all_routes.append(direct)

        # 2. Hidden city opportunities
        hidden_city_routes = self.search_hidden_city(origin, destination, departure_date)
        all_routes.extend(hidden_city_routes)

        # 3. Nearby airports
        nearby_routes = self.search_nearby_airports(origin, destination, departure_date, return_date)
        all_routes.extend(nearby_routes[:5])  # Top 5 nearby combinations

        # 4. Multi-leg combinations
        multi_leg_routes = self.search_multi_leg(origin, destination, departure_date, return_date)
        all_routes.extend(multi_leg_routes[:3])  # Top 3 multi-leg options

        # Sort by price
        all_routes.sort(key=lambda r: r.price)

        # Analyze price gaps
        analysis = self._analyze_price_gaps(all_routes, direct.price)

        return {
            'direct_flight': direct.to_dict(),
            'cheapest_option': all_routes[0].to_dict() if all_routes else None,
            'all_options': [route.to_dict() for route in all_routes[:10]],
            'price_analysis': analysis,
            'total_options_found': len(all_routes)
        }

    def _calculate_base_price(self, origin: str, destination: str, date: datetime) -> float:
        """Simulate base price calculation."""
        # Simple simulation based on route distance and date
        import random

        base = 150.0

        # Adjust for international vs domestic
        origin_info = self.airport_helper.get_airport_info(origin)
        dest_info = self.airport_helper.get_airport_info(destination)

        if origin_info and dest_info:
            if origin_info['country'] != dest_info['country']:
                base *= 2.5  # International multiplier

        # Add some randomness
        base *= random.uniform(0.8, 1.3)

        # Adjust for booking window
        booking_window = DateHelper.get_optimal_booking_window(date)
        if booking_window['status'] == 'very_late':
            base *= 1.5
        elif booking_window['status'] == 'late':
            base *= 1.2

        return round(base, 2)

    def _get_cities_beyond(self, destination: str) -> List[str]:
        """Get cities that could be beyond the destination for hidden city tickets."""
        # Simplified logic - in production, use geographic data
        beyond_cities = {
            'JFK': ['BOS', 'YUL', 'YYZ'],  # Beyond NYC
            'LHR': ['DUB', 'MAN', 'EDI'],  # Beyond London
            'CDG': ['AMS', 'BRU', 'LUX'],  # Beyond Paris
            'FRA': ['MUC', 'VIE', 'ZRH'],  # Beyond Frankfurt
            'DXB': ['DOH', 'AUH', 'MCT'],  # Beyond Dubai
        }
        return beyond_cities.get(destination, [])

    def _get_potential_hubs(self, origin: str, destination: str) -> List[str]:
        """Get potential hub cities between origin and destination."""
        # Major European and international hubs
        hubs = ['FRA', 'AMS', 'CDG', 'LHR', 'MUC', 'IST', 'DXB', 'DOH']

        # Filter out origin and destination
        return [h for h in hubs if h not in [origin, destination]]

    def _simulate_layover_route(
        self,
        origin: str,
        final_dest: str,
        layover: str,
        date: datetime
    ) -> Optional[FlightRoute]:
        """Simulate a route with a specific layover."""
        # Check if this routing makes geographic sense
        # In production, verify actual flight availability

        price = self._calculate_base_price(origin, final_dest, date) * 0.85  # Hidden city often cheaper

        legs = [
            {
                'origin': origin,
                'destination': layover,
                'departure': date.isoformat(),
                'layover': True
            },
            {
                'origin': layover,
                'destination': final_dest,
                'departure': date.isoformat(),
                'note': 'You would skip this leg (hidden city)'
            }
        ]

        return FlightRoute(
            origin=origin,
            destination=layover,  # Actual destination where you get off
            departure_date=date,
            price=price,
            currency='EUR',
            legs=legs,
            route_type='hidden_city'
        )

    def _analyze_price_gaps(self, routes: List[FlightRoute], direct_price: float) -> Dict[str, Any]:
        """Analyze price gaps between different routing strategies."""
        if not routes:
            return {}

        cheapest = routes[0]
        savings = calculate_price_difference(cheapest.price, direct_price)

        # Group by route type
        route_types = {}
        for route in routes:
            if route.route_type not in route_types:
                route_types[route.route_type] = []
            route_types[route.route_type].append(route.price)

        # Calculate average price by type
        avg_by_type = {
            rtype: sum(prices) / len(prices)
            for rtype, prices in route_types.items()
        }

        return {
            'direct_price': direct_price,
            'cheapest_price': cheapest.price,
            'savings_amount': abs(savings['absolute']),
            'savings_percentage': abs(savings['percentage']),
            'cheapest_route_type': cheapest.route_type,
            'average_by_route_type': avg_by_type,
            'price_range': {
                'min': routes[0].price,
                'max': routes[-1].price
            }
        }


def rank_legal_options(routes: List[FlightRoute]) -> List[Dict[str, Any]]:
    """
    Rank options by legality and practicality.

    Hidden city tickets violate most airline ToS.
    Separate tickets have risks (missed connections, no protection).
    """
    ranked = []

    legality_scores = {
        'direct': {'score': 10, 'legal': True, 'risk': 'None'},
        'nearby_airport': {'score': 10, 'legal': True, 'risk': 'Ground transportation needed'},
        'multi_leg_split': {'score': 7, 'legal': True, 'risk': 'No connection protection'},
        'hidden_city': {'score': 3, 'legal': False, 'risk': 'Violates airline ToS, bags checked through'}
    }

    for route in routes:
        legality = legality_scores.get(route.route_type, {'score': 5, 'legal': True, 'risk': 'Unknown'})

        ranked.append({
            'route': route.to_dict(),
            'legality_score': legality['score'],
            'is_legal': legality['legal'],
            'risks': legality['risk'],
            'recommendation': _get_recommendation(route.route_type, legality)
        })

    # Sort by price but keep legality info
    ranked.sort(key=lambda x: x['route']['price'])

    return ranked


def _get_recommendation(route_type: str, legality: Dict) -> str:
    """Get recommendation text for route type."""
    recommendations = {
        'direct': 'Safest option with full airline protection.',
        'nearby_airport': 'Legal and safe. Consider ground transportation time and cost.',
        'multi_leg_split': 'Legal but risky. No protection if first flight delayed. Allow buffer time.',
        'hidden_city': 'NOT RECOMMENDED: Violates ToS, can lead to account suspension. Only check carry-on bags.'
    }
    return recommendations.get(route_type, 'Review terms carefully.')
