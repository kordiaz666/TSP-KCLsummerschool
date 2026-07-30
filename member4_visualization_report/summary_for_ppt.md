# Summary — PPT 可直接复制内容

---

## Slide: Summary — Three Algorithms Compared

**Brute Force**
- Exact baseline
- Enumerates all (n−1)!/2 permutations
- Guarantees optimality — O(n!) — impractical beyond n=10

**Branch & Bound**
- Exact with pruning
- DFS + lower bound: if LB ≥ best_cost, prune
- Optimal — far more efficient than brute force

**Nearest Neighbor**
- Greedy heuristic
- Always picks closest unvisited city
- O(n²) speed — but 2–10% above optimal

→ B&B strikes the best balance between correctness and efficiency for exact TSP solving at small to medium scale.

---

## Slide: Summary — Key Results

| N | B&B Runtime | BF Runtime | B&B Nodes | BF Nodes | Pruning Rate |
|---|------------|-----------|-----------|---------|-------------|
| 4 | 0.02 ms | 0.006 ms | 15 | 6 | 3.8% |
| 7 | 0.66 ms | 0.28 ms | 428 | 720 | 78.1% |
| 9 | 6.5 ms | 14.3 ms | 4,107 | 40,320 | 96.3% |
| 10 | 23 ms | N/A | 12,472 | 1,814,400 | 98.7% |

- B&B prunes 98.7% of search space at n=10 — explores only 1.3% of all possible nodes
- B&B becomes faster than BF from n=7 onward
- At n=10, BF is infeasible (1.8M paths) while B&B completes in 23ms

---

## Slide: Summary — Conclusions

1. **Branch and Bound is the best choice** among these three methods when we need an exact TSP solution but also want better efficiency than simple exhaustive search.

2. **Pruning becomes more effective as problem size increases** — pruning rate grows from 3.8% at n=4 to 98.7% at n=10.

3. **Nearest Neighbor is the fastest** but may produce longer routes (2–10% above optimal). Suitable when speed is critical and optimality can be sacrificed.

4. **Brute Force is accurate but does not scale** — its O(n!) growth makes it unusable beyond 10–12 cities.

5. **Limitation:** B&B remains exponential; for n > 20 it becomes impractical. Tighter bounds (MST, Held-Karp) could improve pruning.
