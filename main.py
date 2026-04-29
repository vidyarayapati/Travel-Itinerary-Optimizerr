"""
Travel Itinerary Optimizer — Main Runner
=========================================
Demonstrates three algorithms on Indian city travel data:

  1. Greedy TSP     — Nearest-neighbor route planning
  2. DP Knapsack    — Optimal budget allocation
  3. Dijkstra       — Shortest path between two cities

Run: python main.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from data.cities import CITIES
from algorithms.greedy_tsp import greedy_tsp, print_route
from algorithms.dp_knapsack import knapsack_dp, print_dp_result
from algorithms.dijkstra import dijkstra, print_shortest_path


def separator(title: str) -> None:
    print("\n" + "=" * 55)
    print(f"  {title}")
    print("=" * 55)


def main():
    print("\n╔══════════════════════════════════════════════════════╗")
    print("║          TRAVEL ITINERARY OPTIMIZER                  ║")
    print("║   Greedy  ·  Dynamic Programming  ·  Dijkstra        ║")
    print("╚══════════════════════════════════════════════════════╝")
    print(f"\nDataset: {len(CITIES)} Indian cities loaded.")

    # ── 1. Greedy TSP ─────────────────────────────────────────────
    separator("1. GREEDY TSP — Nearest Neighbor Route")
    route, total_dist = greedy_tsp(CITIES)
    print_route(CITIES, route, total_dist)

    # ── 2. DP Knapsack ────────────────────────────────────────────
    separator("2. DP KNAPSACK — Budget Allocation")
    BUDGET = 40_000
    selected, max_days = knapsack_dp(CITIES, BUDGET)
    print_dp_result(CITIES, selected, max_days, BUDGET)

    # ── 3. Dijkstra ───────────────────────────────────────────────
    separator("3. DIJKSTRA — Shortest Path")
    src, tgt = 0, 5    # Mumbai → Kolkata
    dist, path = dijkstra(CITIES, src, tgt)
    print_shortest_path(CITIES, src, tgt, dist, path)

    # ── Summary ───────────────────────────────────────────────────
    separator("SUMMARY")
    print(f"  Route length  (Greedy TSP)   : {total_dist:.0f} km")
    print(f"  Optimal days  (DP Knapsack)  : {max_days} days / ₹{BUDGET:,} budget")
    chosen_cost = sum(CITIES[i]["cost"] for i in selected)
    print(f"  Spend         (DP Knapsack)  : ₹{chosen_cost:,}")
    print(f"  Shortest path (Dijkstra)     : {dist:.0f} km")
    print()


if __name__ == "__main__":
    main()
