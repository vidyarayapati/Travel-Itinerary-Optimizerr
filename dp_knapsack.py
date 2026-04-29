"""
Dynamic Programming — 0/1 Knapsack Budget Allocator
=====================================================
Given a list of cities (each with a visit cost and a 'days' value),
find the subset of cities that maximises total days within a budget.

This is the classic 0/1 Knapsack problem:
  - Each city is either included fully or excluded (no partial trips).
  - We build a DP table bottom-up to find the optimal allocation.

Time Complexity : O(n × B)   where B = budget // 1000 (scaled)
Space Complexity: O(n × B)
  — can be reduced to O(B) with a 1D rolling array, but 2D is shown
    here for clarity so you can trace the table during demos.

Why DP and not Greedy?
  A greedy approach (sort by value/cost ratio) works perfectly for the
  FRACTIONAL knapsack, but fails for 0/1 knapsack because you cannot
  take partial cities. DP handles this by explicitly considering every
  (item, capacity) sub-problem exactly once — giving the true optimum.
"""


def knapsack_dp(cities: list[dict], budget: int) -> tuple[list[int], int]:
    """
    0/1 Knapsack DP for travel budget allocation.

    Args:
        cities : list of dicts with 'name', 'cost' (₹), 'days' (value)
        budget : total available budget in ₹

    Returns:
        selected  : list of indices of chosen cities
        max_days  : maximum achievable stay days within budget
    """
    n = len(cities)
    B = budget // 1000          # scale so costs become small integers
    # costs & values scaled the same way
    costs = [c["cost"] // 1000 for c in cities]
    values = [c["days"] for c in cities]

    # dp[i][w] = best total days using first i cities with capacity w
    dp = [[0] * (B + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        c = costs[i - 1]
        v = values[i - 1]
        for w in range(B + 1):
            # Option 1: skip city i
            skip = dp[i - 1][w]
            # Option 2: include city i (only if it fits)
            take = dp[i - 1][w - c] + v if c <= w else 0
            dp[i][w] = max(skip, take)

    # ── Backtrack to recover which cities were selected ──────────────
    selected = []
    w = B
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:   # city i was included
            selected.append(i - 1)
            w -= costs[i - 1]

    selected.reverse()
    return selected, dp[n][B]


def print_dp_result(cities: list[dict], selected: list[int], max_days: int, budget: int) -> None:
    """Pretty-print the DP allocation result."""
    total_cost = sum(cities[i]["cost"] for i in selected)
    chosen_names = [cities[i]["name"] for i in selected]
    skipped_names = [c["name"] for i, c in enumerate(cities) if i not in selected]

    print("\n=== DP Budget Allocation (0/1 Knapsack) ===")
    print(f"\nBudget  : ₹{budget:,}")
    print(f"Spent   : ₹{total_cost:,}  ({total_cost/budget*100:.0f}% of budget)")
    print(f"Savings : ₹{budget-total_cost:,}")
    print(f"\nOptimal stay: {max_days} days")
    print(f"\nIncluded cities ({len(selected)}):")
    for name in chosen_names:
        city = next(c for c in cities if c["name"] == name)
        print(f"  ✓  {name:<15} ₹{city['cost']:>7,}  {city['days']} day(s)")
    if skipped_names:
        print(f"\nSkipped cities ({len(skipped_names)}):")
        for name in skipped_names:
            city = next(c for c in cities if c["name"] == name)
            print(f"  ✗  {name:<15} ₹{city['cost']:>7,}  {city['days']} day(s)")


# ── Demo ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    from data.cities import CITIES

    BUDGET = 40_000
    selected, max_days = knapsack_dp(CITIES, BUDGET)
    print_dp_result(CITIES, selected, max_days, BUDGET)
