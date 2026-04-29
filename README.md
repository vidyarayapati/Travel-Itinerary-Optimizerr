# Travel Itinerary Optimizer

A Python project that applies **Greedy**, **Dynamic Programming**, and **Dijkstra's** algorithms to solve a real-world travel planning problem: given a list of Indian cities with visit costs and stay durations, find the optimal route and budget allocation.

Built as a CCC algorithm project submission.

---

## Problem Statement

Given *n* cities, each with:
- A travel + stay **cost** (₹)
- A recommended **stay duration** (days)
- Geographic **coordinates** (lat/lng)

Answer two questions:
1. **What order should I visit them?** → Greedy TSP (Nearest Neighbor)
2. **Which cities fit my budget?** → Dynamic Programming (0/1 Knapsack)
3. **What's the shortest path between two cities?** → Dijkstra's Algorithm

---

## Algorithms

### 1. Greedy — Nearest Neighbor TSP

The Travelling Salesman Problem (TSP) is NP-Hard. We use the **nearest-neighbor greedy heuristic**: always move to the closest unvisited city.

```
Time  : O(n²)
Space : O(n)
```

**Why greedy?** At each step we make the locally optimal choice (shortest next hop). This doesn't always produce the global optimum, but it's fast and produces tours within ~20% of optimal for geographic instances.

```python
for step in range(n - 1):
    nearest = min(unvisited, key=lambda j: dist(current, j))
    visit(nearest)
```

---

### 2. Dynamic Programming — 0/1 Knapsack

Given a budget, which subset of cities maximises total stay days?

This is a classic **0/1 Knapsack** — each city is either fully included or excluded. Greedy (sort by days/cost ratio) fails here because partial trips aren't allowed.

```
Time  : O(n × B)   where B = budget ÷ 1000
Space : O(n × B)
```

**Why DP?** The problem has **optimal substructure** (the best solution to the full problem contains the best solution to sub-problems) and **overlapping sub-problems** (same (item, capacity) pairs are needed repeatedly). DP solves each sub-problem exactly once.

```python
dp[i][w] = max(dp[i-1][w],                      # skip city i
               dp[i-1][w - cost[i]] + days[i])   # include city i
```

---

### 3. Dijkstra — Shortest Path (Bonus)

Finds the shortest geographic path between any two cities using a **min-heap priority queue**.

```
Time  : O((V + E) log V)
Space : O(V + E)
```

**Key idea**: Relax edges — if we find a shorter route to a neighbour via the current node, update it and re-add to the heap.

---

## Project Structure

```
travel-optimizer/
├── main.py                     # Run all three algorithms
├── algorithms/
│   ├── greedy_tsp.py           # Nearest-neighbor TSP
│   ├── dp_knapsack.py          # 0/1 Knapsack budget allocator
│   └── dijkstra.py             # Shortest path
├── data/
│   └── cities.py               # 10 Indian city dataset
└── tests/
    └── test_algorithms.py      # 20 unit tests (all passing)
```

---

## Quick Start

```bash
# Clone the repo
git clone https://github.com/<your-username>/travel-optimizer.git
cd travel-optimizer

# No external dependencies — pure Python 3.9+
python main.py

# Run tests
python tests/test_algorithms.py
```

**Sample output:**
```
=== Greedy TSP Route (Nearest Neighbor) ===
  1. Mumbai → 2. Goa → 3. Hyderabad → 4. Chennai → ... → 10. Udaipur
  Total distance: 4744 km

=== DP Budget Allocation (0/1 Knapsack) ===
  Budget  : ₹40,000
  Optimal stay: 12 days
  ✓ Mumbai, Delhi, Jaipur, Kolkata, Hyderabad, Varanasi

=== Dijkstra Shortest Path ===
  Mumbai → Kolkata : 1655 km
```

---

## Algorithm Comparison

| Algorithm | Problem Type | Optimal? | Time Complexity |
|-----------|-------------|----------|-----------------|
| Greedy (TSP) | Route planning | No (heuristic) | O(n²) |
| DP (Knapsack) | Budget allocation | **Yes** | O(n × B) |
| Dijkstra | Shortest path | **Yes** | O((V+E) log V) |

**Key insight**: Greedy is appropriate for TSP (where optimal is intractable) but *not* for Knapsack (where DP gives the true optimum). Choosing the right algorithm for the right problem is the real lesson here.

---

## Team

| Name | Role |
|------|------|
| — | Algorithm design |
| — | Testing & validation |
| — | Documentation |

*Add your team members above before submitting.*

---

## License

MIT — free to use and extend.
