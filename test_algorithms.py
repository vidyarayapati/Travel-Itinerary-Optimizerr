"""
Unit Tests — Travel Itinerary Optimizer
Tests correctness of Greedy TSP, DP Knapsack, and Dijkstra.

Run: python -m pytest tests/ -v
  or: python tests/test_algorithms.py
"""

import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from algorithms.greedy_tsp import greedy_tsp, haversine
from algorithms.dp_knapsack import knapsack_dp
from algorithms.dijkstra import dijkstra


# ── Fixtures ─────────────────────────────────────────────────────────────────
SMALL_CITIES = [
    {"name": "A", "lat": 0.0,  "lng": 0.0,  "cost": 5000, "days": 2},
    {"name": "B", "lat": 0.0,  "lng": 1.0,  "cost": 3000, "days": 1},
    {"name": "C", "lat": 1.0,  "lng": 0.0,  "cost": 4000, "days": 2},
    {"name": "D", "lat": 10.0, "lng": 10.0, "cost": 8000, "days": 3},
]


# ── Haversine tests ───────────────────────────────────────────────────────────
def test_haversine_zero_distance():
    city = {"lat": 19.0, "lng": 72.0}
    assert haversine(city, city) == 0.0

def test_haversine_symmetry():
    a = {"lat": 19.07, "lng": 72.87}
    b = {"lat": 28.67, "lng": 77.20}
    assert abs(haversine(a, b) - haversine(b, a)) < 0.001

def test_haversine_known_distance():
    # Mumbai to Delhi is approximately 1148 km
    mumbai  = {"lat": 19.07, "lng": 72.87}
    delhi   = {"lat": 28.67, "lng": 77.20}
    d = haversine(mumbai, delhi)
    assert 1100 < d < 1200, f"Expected ~1148 km, got {d:.0f} km"


# ── Greedy TSP tests ──────────────────────────────────────────────────────────
def test_greedy_tsp_visits_all_cities():
    route, _ = greedy_tsp(SMALL_CITIES)
    assert len(route) == len(SMALL_CITIES)
    assert sorted(route) == list(range(len(SMALL_CITIES)))

def test_greedy_tsp_starts_at_zero_by_default():
    route, _ = greedy_tsp(SMALL_CITIES)
    assert route[0] == 0

def test_greedy_tsp_custom_start():
    route, _ = greedy_tsp(SMALL_CITIES, start=2)
    assert route[0] == 2

def test_greedy_tsp_positive_distance():
    _, dist = greedy_tsp(SMALL_CITIES)
    assert dist > 0

def test_greedy_tsp_single_city():
    route, dist = greedy_tsp([SMALL_CITIES[0]])
    assert route == [0]
    assert dist == 0.0

def test_greedy_tsp_empty():
    route, dist = greedy_tsp([])
    assert route == []
    assert dist == 0.0

def test_greedy_tsp_nearby_city_picked_first():
    # B (lng=1) and C (lat=1) are both close to A (0,0).
    # D (10,10) is far — it must be visited last.
    route, _ = greedy_tsp(SMALL_CITIES, start=0)
    assert route[-1] == 3, "Farthest city D should be visited last"


# ── DP Knapsack tests ─────────────────────────────────────────────────────────
def test_knapsack_empty_budget():
    selected, days = knapsack_dp(SMALL_CITIES, 0)
    assert selected == []
    assert days == 0

def test_knapsack_unlimited_budget():
    total_cost = sum(c["cost"] for c in SMALL_CITIES)
    selected, days = knapsack_dp(SMALL_CITIES, total_cost + 10_000)
    assert len(selected) == len(SMALL_CITIES)

def test_knapsack_respects_budget():
    budget = 8_000
    selected, _ = knapsack_dp(SMALL_CITIES, budget)
    total_spent = sum(SMALL_CITIES[i]["cost"] for i in selected)
    assert total_spent <= budget

def test_knapsack_maximises_days():
    # Budget = 8000: can take A(5000,2d) or B+C(3000+4000=7000,3d)
    # Optimal: B+C = 3 days
    budget = 8_000
    selected, days = knapsack_dp(SMALL_CITIES, budget)
    assert days == 3

def test_knapsack_no_duplicate_cities():
    selected, _ = knapsack_dp(SMALL_CITIES, 20_000)
    assert len(selected) == len(set(selected))

def test_knapsack_indices_valid():
    selected, _ = knapsack_dp(SMALL_CITIES, 20_000)
    for i in selected:
        assert 0 <= i < len(SMALL_CITIES)


# ── Dijkstra tests ────────────────────────────────────────────────────────────
def test_dijkstra_source_to_self():
    dist, path = dijkstra(SMALL_CITIES, 0, 0)
    assert dist == 0.0
    assert path == [0]

def test_dijkstra_path_contains_source_and_target():
    dist, path = dijkstra(SMALL_CITIES, 0, 3)
    assert path[0] == 0
    assert path[-1] == 3

def test_dijkstra_positive_distance():
    dist, _ = dijkstra(SMALL_CITIES, 0, 3)
    assert dist > 0

def test_dijkstra_direct_is_shortest_on_complete_graph():
    # In a complete graph the direct edge A→B should be ≤ any detour
    direct = haversine(SMALL_CITIES[0], SMALL_CITIES[1])
    dist, _ = dijkstra(SMALL_CITIES, 0, 1)
    assert abs(dist - direct) < 0.01


# ── Runner ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = failed = 0
    for test in tests:
        try:
            test()
            print(f"  PASS  {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL  {test.__name__}  —  {e}")
            failed += 1
        except Exception as e:
            print(f"  ERROR {test.__name__}  —  {e}")
            failed += 1
    print(f"\n{passed + failed} tests · {passed} passed · {failed} failed")
