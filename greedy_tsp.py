"""
Greedy TSP — Nearest Neighbor Heuristic
========================================
Given a list of cities with (lat, lng) coordinates, finds a short
Hamiltonian path using the greedy nearest-neighbor strategy.

Time Complexity : O(n²)
Space Complexity: O(n)

Why Greedy here?
  TSP is NP-Hard — the exact solution requires checking n! routes.
  The nearest-neighbor heuristic trades optimality for speed:
  at each step, we greedily pick the closest unvisited city.
  This gives a tour typically within 20-25% of the true optimum.
"""

import math


def haversine(city_a: dict, city_b: dict) -> float:
    """
    Compute the great-circle distance between two cities in km.
    Uses the Haversine formula for spherical Earth approximation.
    """
    R = 6371  # Earth's radius in km
    lat1, lng1 = math.radians(city_a["lat"]), math.radians(city_a["lng"])
    lat2, lng2 = math.radians(city_b["lat"]), math.radians(city_b["lng"])
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def greedy_tsp(cities: list[dict], start: int = 0) -> tuple[list[int], float]:
    """
    Nearest-neighbor greedy TSP heuristic.

    Args:
        cities : list of dicts, each with 'name', 'lat', 'lng'
        start  : index of the starting city (default 0)

    Returns:
        route      : ordered list of city indices
        total_dist : total distance of the route in km
    """
    n = len(cities)
    if n == 0:
        return [], 0.0
    if n == 1:
        return [0], 0.0

    visited = [False] * n
    route = [start]
    visited[start] = True
    total_dist = 0.0

    for _ in range(n - 1):
        current = route[-1]
        nearest_city, min_distance = -1, float("inf")

        # Greedy step: scan all unvisited cities, pick the closest
        for j in range(n):
            if not visited[j]:
                d = haversine(cities[current], cities[j])
                if d < min_distance:
                    nearest_city, min_distance = j, d

        route.append(nearest_city)
        visited[nearest_city] = True
        total_dist += min_distance

    return route, round(total_dist, 2)


def print_route(cities: list[dict], route: list[int], total_dist: float) -> None:
    """Pretty-print the greedy route."""
    print("\n=== Greedy TSP Route (Nearest Neighbor) ===")
    for i, idx in enumerate(route):
        arrow = " → " if i < len(route) - 1 else ""
        print(f"  {i+1}. {cities[idx]['name']}{arrow}", end="")
    print(f"\n\nTotal distance: {total_dist:.0f} km")
    print(f"Cities visited: {len(route)}")


# ── Demo ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    from data.cities import CITIES

    route, total = greedy_tsp(CITIES)
    print_route(CITIES, route, total)
