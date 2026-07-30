# Summary — 项目总结章节

> 根据 PPT 前三章（Introduction、Algorithms、Codes Demonstration、Results）内容编写，用于补充第 05 节 Summary 幻灯片。

---

## Summary

### Problem Recap

The Traveling Salesman Problem (TSP) asks: given a list of cities and distances between each pair, find the shortest possible route that visits every city exactly once and returns to the starting city. As the number of cities grows, the number of possible paths explodes factorially — from 12 paths for 5 cities to over 43 billion for 15 cities — making brute force enumeration impractical for all but the smallest cases.

### Algorithms Compared

We implemented and evaluated three algorithms:

| Algorithm | Type | Strategy | Guarantee |
|-----------|------|----------|-----------|
| **Brute Force** | Exact baseline | Enumerate every fixed-start permutation | Optimal, but O(n!) |
| **Branch & Bound** | Exact with pruning | DFS with lower-bound pruning | Optimal, much faster in practice |
| **Nearest Neighbor** | Greedy heuristic | Always move to the closest unvisited city | Fast O(n²), approximate only |

### Key Results

**Running Time:** Branch and Bound consistently outperforms Brute Force for n ≥ 7. At n = 9, B&B is approximately 2× faster. At n = 10, Brute Force becomes infeasible while B&B still completes in milliseconds. Nearest Neighbor runs in near-zero time regardless of problem size.

**Pruning Effectiveness:** The lower-bound pruning avoids an increasingly large fraction of the search space as n grows. At n = 10, B&B prunes over 98% of all possible branches — meaning it explores less than 2% of the full search tree while still guaranteeing the optimal answer.

**Solution Quality:** Both Brute Force and Branch & Bound achieve ratio = 1.0 (optimal) on all tested instances, confirming the correctness of our B&B implementation. Nearest Neighbor produces routes that are 2–10% longer than optimal.

### Conclusions

1. **Branch and Bound is the best choice among the three methods** when we need an exact TSP solution but also want better efficiency than simple exhaustive search.

2. **The pruning mechanism becomes more effective as problem size increases** — the lower bound is an admissible heuristic that provides increasing value for larger instances.

3. **Nearest Neighbor is the fastest** but may produce longer routes. It is suitable for applications where speed is critical and optimality can be sacrificed.

4. **Brute Force is accurate** but does not scale. Its exponential growth makes it unusable beyond 10–12 cities.

### Limitations & Future Work

- B&B remains an exponential-time algorithm; for n > 20 it becomes impractical.
- Current lower bound uses minimum outgoing edges. Tighter bounds (MST-based, Held-Karp) could further improve pruning.
- Future directions include parallel B&B, hybrid metaheuristic approaches, and testing on real-world TSP datasets (e.g., TSPLIB).
