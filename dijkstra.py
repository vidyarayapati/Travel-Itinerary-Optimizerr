"""
Dijkstra's Shortest Path Algorithm
====================================
Finds the shortest path between any two cities in the network,
treating haversine distances as edge weights.

This is a BONUS algorithm included to demonstrate:
  - Graph representation (adjacency list with weights)
  - Priority queue (min-heap) for efficient next-node selection
  - Relaxation: updating shortest known distance when a better path is found

Time Complexity : O((V + E) log V) with a binary heap
Space Complexity: O(V + E)
"""

import heapq
import math


def haversine(a: dict, b: dict) -> float:
    R = 6371
    lat1, lng1 = math.radians(a["lat"]), math.radians(a["lng"])
    lat2, lng2 = math.radians(b["lat"]), math.radians(b["lng"])
    dlat, dlng = lat2 - lat1, lng2 - lng1
    x = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(x), math.sqrt(1 - x))


def build_graph(cities: list[dict]) -> dict[int, list[tuple[int, float]]]:
    """
    Build a complete weighted graph: every city is connected to every other.
    Edge weight = haversine distance in km.
    """
    n = len(cities)
    graph = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(n):
            if i != j:
                graph[i].append((j, haversine(cities[i], cities[j])))
    return graph


def dijkstra(cities: list[dict], source: int, target: int) -> tuple[float, list[int]]:
    """
    Dijkstra's algorithm from source to target city index.

    Returns:
        shortest_dist : distance in km
        path          : list of city indices from source to target
    """
    n = len(cities)
    graph = build_graph(cities)

    dist = [float("inf")] * n
    prev = [-1] * n
    dist[source] = 0.0

    # Min-heap: (distance, node_index)
    heap = [(0.0, source)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:         # stale entry — skip
            continue
        if u == target:
            break               # found shortest path to target

        for v, w in graph[u]:
            relaxed = dist[u] + w
            if relaxed < dist[v]:
                dist[v] = relaxed
                prev[v] = u
                heapq.heappush(heap, (relaxed, v))

    # Reconstruct path by backtracking through prev[]
    path = []
    node = target
    while node != -1:
        path.append(node)
        node = prev[node]
    path.reverse()

    return round(dist[target], 2), path


def print_shortest_path(cities, source, target, distance, path):
    print(f"\n=== Dijkstra Shortest Path ===")
    print(f"From : {cities[source]['name']}")
    print(f"To   : {cities[target]['name']}")
    print(f"Path : {' → '.join(cities[i]['name'] for i in path)}")
    print(f"Dist : {distance:.0f} km")


# ── Demo ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    from data.cities import CITIES

    SRC, TGT = 0, 5     # Mumbai → Kolkata
    dist, path = dijkstra(CITIES, SRC, TGT)
    print_shortest_path(CITIES, SRC, TGT, dist, path)
