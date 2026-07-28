from __future__ import annotations

import itertools
import math
import time
from dataclasses import dataclass
from typing import Sequence

Point = tuple[float, float]


@dataclass(frozen=True)
class SolverResult:
    algorithm: str
    path: list[int]
    cost: float
    runtime_s: float
    visited_nodes: int | None = None
    pruned_branches: int | None = None
    total_possible_nodes: int | None = None
    pruning_rate: float | None = None
    is_optimal: bool = False


def distance_matrix(points: Sequence[Point]) -> list[list[float]]:
    return [
        [
            math.hypot(points[i][0] - points[j][0], points[i][1] - points[j][1])
            for j in range(len(points))
        ]
        for i in range(len(points))
    ]


def closed_route_cost(path: Sequence[int], dist: Sequence[Sequence[float]]) -> float:
    if len(path) < 2:
        return 0.0

    cost = 0.0
    for i in range(len(path) - 1):
        cost += dist[path[i]][path[i + 1]]

    if path[0] != path[-1]:
        cost += dist[path[-1]][path[0]]

    return cost


def total_fixed_start_partial_nodes(n: int) -> int:
    """Number of recursive partial paths a no-pruning DFS visits with city 0 fixed."""
    if n <= 1:
        return 1
    return sum(math.perm(n - 1, depth) for depth in range(n))


def total_fixed_start_tours(n: int) -> int:
    if n <= 1:
        return 1
    return math.factorial(n - 1)


def nearest_neighbor(points: Sequence[Point]) -> SolverResult:
    start_time = time.perf_counter()
    n = len(points)
    dist = distance_matrix(points)

    if n == 0:
        return SolverResult("nearest_neighbor", [], 0.0, time.perf_counter() - start_time)

    path = [0]
    unvisited = set(range(1, n))
    while unvisited:
        last = path[-1]
        nxt = min(unvisited, key=lambda city: dist[last][city])
        path.append(nxt)
        unvisited.remove(nxt)

    path.append(0)
    runtime_s = time.perf_counter() - start_time
    return SolverResult(
        algorithm="nearest_neighbor",
        path=path,
        cost=closed_route_cost(path, dist),
        runtime_s=runtime_s,
        visited_nodes=n,
        is_optimal=False,
    )


def brute_force(points: Sequence[Point]) -> SolverResult:
    start_time = time.perf_counter()
    n = len(points)
    dist = distance_matrix(points)

    if n == 0:
        return SolverResult("brute_force", [], 0.0, time.perf_counter() - start_time)

    best_path: list[int] | None = None
    best_cost = float("inf")
    visited_tours = 0

    # Fix city 0 as the start to remove rotational duplicates.
    for perm in itertools.permutations(range(1, n)):
        path = [0, *perm, 0]
        cost = closed_route_cost(path, dist)
        visited_tours += 1
        if cost < best_cost:
            best_cost = cost
            best_path = path

    runtime_s = time.perf_counter() - start_time
    return SolverResult(
        algorithm="brute_force",
        path=best_path or [0],
        cost=best_cost,
        runtime_s=runtime_s,
        visited_nodes=visited_tours,
        total_possible_nodes=total_fixed_start_tours(n),
        pruning_rate=0.0,
        is_optimal=True,
    )


def branch_and_bound(points: Sequence[Point], use_greedy_initial_bound: bool = True) -> SolverResult:
    start_time = time.perf_counter()
    n = len(points)
    dist = distance_matrix(points)

    if n == 0:
        return SolverResult("branch_and_bound", [], 0.0, time.perf_counter() - start_time)

    best_path: list[int] | None = None
    best_cost = float("inf")

    # A quick greedy tour gives Branch and Bound an early upper bound, so more
    # branches can be cut before reaching full tours.
    if use_greedy_initial_bound and n >= 2:
        greedy = nearest_neighbor(points)
        best_path = greedy.path
        best_cost = greedy.cost

    visited_nodes = 0
    pruned_branches = 0

    def lower_bound(curr_path: list[int], current_cost: float, visited: list[bool]) -> float:
        bound = current_cost
        start = curr_path[0]

        for city in range(n):
            if visited[city]:
                continue

            min_edge = float("inf")
            for other in range(n):
                if city == other:
                    continue
                if not visited[other] or other == start:
                    min_edge = min(min_edge, dist[city][other])

            if min_edge != float("inf"):
                bound += min_edge

        return bound

    def search(curr_path: list[int], current_cost: float, visited: list[bool]) -> None:
        nonlocal best_path, best_cost, visited_nodes, pruned_branches
        visited_nodes += 1

        if lower_bound(curr_path, current_cost, visited) >= best_cost:
            pruned_branches += 1
            return

        if len(curr_path) == n:
            final_cost = current_cost + dist[curr_path[-1]][curr_path[0]]
            if final_cost < best_cost:
                best_cost = final_cost
                best_path = [*curr_path, curr_path[0]]
            return

        last = curr_path[-1]
        candidates = sorted(
            ((dist[last][city], city) for city in range(n) if not visited[city]),
            key=lambda item: item[0],
        )

        for edge_cost, city in candidates:
            visited[city] = True
            curr_path.append(city)
            search(curr_path, current_cost + edge_cost, visited)
            curr_path.pop()
            visited[city] = False

    visited = [False] * n
    visited[0] = True
    search([0], 0.0, visited)

    runtime_s = time.perf_counter() - start_time
    total_nodes = total_fixed_start_partial_nodes(n)
    pruning_rate = 1.0 - (visited_nodes / total_nodes) if total_nodes else None

    return SolverResult(
        algorithm="branch_and_bound",
        path=best_path or [],
        cost=best_cost,
        runtime_s=runtime_s,
        visited_nodes=visited_nodes,
        pruned_branches=pruned_branches,
        total_possible_nodes=total_nodes,
        pruning_rate=pruning_rate,
        is_optimal=True,
    )
