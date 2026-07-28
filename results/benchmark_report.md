# TSP Batch Benchmark Report

## What this experiment does

For each city count `n`, the program generates several random TSP instances. Each instance is solved with Branch and Bound, Nearest Neighbor, and, for small `n`, Brute Force. The report compares running time, search effort, pruning, and route quality.

## Algorithms

- `branch_and_bound`: exact method. It searches possible routes but cuts branches when the lower bound is already worse than the best known route.
- `brute_force`: exact baseline. It tries every possible route, so it becomes very slow as `n` grows.
- `nearest_neighbor`: greedy baseline. It always goes to the nearest unvisited city. It is fast but not always optimal.

## Chart guide

- `runtime_by_cities.png`: compares average runtime as the number of cities increases. The y-axis uses a log scale because exact TSP grows very quickly.
- `pruning_by_cities.png`: shows how much search Branch and Bound avoids. The left plot is pruning rate; the right plot compares no-pruning search states with actually visited Branch and Bound states.
- `quality_by_cities.png`: compares route quality. A value of `1.0` means optimal. Values above `1.0` mean the route is longer than the optimal route.

## Summary table

| Cities | Algorithm | Runs | Mean runtime (s) | Mean cost | Ratio to optimal | Visited nodes | Pruned branches | Pruning rate |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 4 | branch_and_bound | 5 | 0.000021 | 1534.55 | 1.0000 | 15 | 1 | 0.0375 |
| 4 | brute_force | 5 | 0.000006 | 1534.55 | 1.0000 | 6 | - | 0.0000 |
| 4 | nearest_neighbor | 5 | 0.000003 | 1582.67 | 1.0216 | 4 | - | - |
| 5 | branch_and_bound | 5 | 0.000053 | 2044.34 | 1.0000 | 53 | 12 | 0.1846 |
| 5 | brute_force | 5 | 0.000010 | 2044.34 | 1.0000 | 24 | - | 0.0000 |
| 5 | nearest_neighbor | 5 | 0.000003 | 2133.60 | 1.0392 | 5 | - | - |
| 6 | branch_and_bound | 5 | 0.000192 | 2008.69 | 1.0000 | 194 | 65 | 0.4049 |
| 6 | brute_force | 5 | 0.000039 | 2008.69 | 1.0000 | 120 | - | 0.0000 |
| 6 | nearest_neighbor | 5 | 0.000004 | 2181.03 | 1.0821 | 6 | - | - |
| 7 | branch_and_bound | 5 | 0.000662 | 1940.91 | 1.0000 | 428 | 237 | 0.7813 |
| 7 | brute_force | 5 | 0.000278 | 1940.91 | 1.0000 | 720 | - | 0.0000 |
| 7 | nearest_neighbor | 5 | 0.000008 | 2082.86 | 1.0734 | 7 | - | - |
| 8 | branch_and_bound | 5 | 0.003049 | 2435.84 | 1.0000 | 2186 | 1242 | 0.8404 |
| 8 | brute_force | 5 | 0.001939 | 2435.84 | 1.0000 | 5040 | - | 0.0000 |
| 8 | nearest_neighbor | 5 | 0.000011 | 2720.07 | 1.1177 | 8 | - | - |
| 9 | branch_and_bound | 5 | 0.006481 | 2431.03 | 1.0000 | 4107 | 2771 | 0.9625 |
| 9 | brute_force | 5 | 0.014312 | 2431.03 | 1.0000 | 40320 | - | 0.0000 |
| 9 | nearest_neighbor | 5 | 0.000011 | 2639.14 | 1.1021 | 9 | - | - |
| 10 | branch_and_bound | 5 | 0.023178 | 2248.53 | 1.0000 | 12472 | 9031 | 0.9874 |
| 10 | nearest_neighbor | 5 | 0.000015 | 2471.28 | 1.0933 | 10 | - | - |

## Full per-test table

| Cities | Test | Algorithm | Runtime (s) | Cost | Ratio to optimal | Visited nodes | Pruned branches | Pruning rate |
|---:|---:|---|---:|---:|---:|---:|---:|---:|
| 4 | 1 | branch_and_bound | 0.000033 | 1225.01 | 1.0000 | 14 | 2 | 0.1250 |
| 4 | 1 | brute_force | 0.000011 | 1225.01 | 1.0000 | 6 | - | 0.0000 |
| 4 | 1 | nearest_neighbor | 0.000004 | 1225.01 | 1.0000 | 4 | - | - |
| 4 | 2 | branch_and_bound | 0.000020 | 1313.16 | 1.0000 | 16 | 2 | 0.0000 |
| 4 | 2 | brute_force | 0.000005 | 1313.16 | 1.0000 | 6 | - | 0.0000 |
| 4 | 2 | nearest_neighbor | 0.000002 | 1313.16 | 1.0000 | 4 | - | - |
| 4 | 3 | branch_and_bound | 0.000018 | 1505.39 | 1.0000 | 16 | 1 | 0.0000 |
| 4 | 3 | brute_force | 0.000004 | 1505.39 | 1.0000 | 6 | - | 0.0000 |
| 4 | 3 | nearest_neighbor | 0.000002 | 1535.90 | 1.0203 | 4 | - | - |
| 4 | 4 | branch_and_bound | 0.000018 | 2398.44 | 1.0000 | 16 | 0 | 0.0000 |
| 4 | 4 | brute_force | 0.000004 | 2398.44 | 1.0000 | 6 | - | 0.0000 |
| 4 | 4 | nearest_neighbor | 0.000002 | 2608.54 | 1.0876 | 4 | - | - |
| 4 | 5 | branch_and_bound | 0.000016 | 1230.75 | 1.0000 | 15 | 1 | 0.0625 |
| 4 | 5 | brute_force | 0.000004 | 1230.75 | 1.0000 | 6 | - | 0.0000 |
| 4 | 5 | nearest_neighbor | 0.000002 | 1230.75 | 1.0000 | 4 | - | - |
| 5 | 1 | branch_and_bound | 0.000056 | 2391.15 | 1.0000 | 51 | 11 | 0.2154 |
| 5 | 1 | brute_force | 0.000011 | 2391.15 | 1.0000 | 24 | - | 0.0000 |
| 5 | 1 | nearest_neighbor | 0.000003 | 2554.29 | 1.0682 | 5 | - | - |
| 5 | 2 | branch_and_bound | 0.000058 | 2059.81 | 1.0000 | 61 | 8 | 0.0615 |
| 5 | 2 | brute_force | 0.000010 | 2059.81 | 1.0000 | 24 | - | 0.0000 |
| 5 | 2 | nearest_neighbor | 0.000003 | 2059.81 | 1.0000 | 5 | - | - |
| 5 | 3 | branch_and_bound | 0.000053 | 2242.07 | 1.0000 | 53 | 11 | 0.1846 |
| 5 | 3 | brute_force | 0.000009 | 2242.07 | 1.0000 | 24 | - | 0.0000 |
| 5 | 3 | nearest_neighbor | 0.000003 | 2488.79 | 1.1100 | 5 | - | - |
| 5 | 4 | branch_and_bound | 0.000053 | 1494.73 | 1.0000 | 52 | 13 | 0.2000 |
| 5 | 4 | brute_force | 0.000010 | 1494.73 | 1.0000 | 24 | - | 0.0000 |
| 5 | 4 | nearest_neighbor | 0.000003 | 1494.73 | 1.0000 | 5 | - | - |
| 5 | 5 | branch_and_bound | 0.000047 | 2033.94 | 1.0000 | 48 | 15 | 0.2615 |
| 5 | 5 | brute_force | 0.000010 | 2033.94 | 1.0000 | 24 | - | 0.0000 |
| 5 | 5 | nearest_neighbor | 0.000003 | 2070.39 | 1.0179 | 5 | - | - |
| 6 | 1 | branch_and_bound | 0.000202 | 1625.82 | 1.0000 | 197 | 63 | 0.3957 |
| 6 | 1 | brute_force | 0.000040 | 1625.82 | 1.0000 | 120 | - | 0.0000 |
| 6 | 1 | nearest_neighbor | 0.000005 | 1717.17 | 1.0562 | 6 | - | - |
| 6 | 2 | branch_and_bound | 0.000233 | 1887.14 | 1.0000 | 251 | 67 | 0.2301 |
| 6 | 2 | brute_force | 0.000038 | 1887.14 | 1.0000 | 120 | - | 0.0000 |
| 6 | 2 | nearest_neighbor | 0.000004 | 1887.14 | 1.0000 | 6 | - | - |
| 6 | 3 | branch_and_bound | 0.000145 | 2394.59 | 1.0000 | 136 | 57 | 0.5828 |
| 6 | 3 | brute_force | 0.000039 | 2394.59 | 1.0000 | 120 | - | 0.0000 |
| 6 | 3 | nearest_neighbor | 0.000004 | 2564.84 | 1.0711 | 6 | - | - |
| 6 | 4 | branch_and_bound | 0.000195 | 2288.78 | 1.0000 | 201 | 69 | 0.3834 |
| 6 | 4 | brute_force | 0.000039 | 2288.78 | 1.0000 | 120 | - | 0.0000 |
| 6 | 4 | nearest_neighbor | 0.000004 | 2688.91 | 1.1748 | 6 | - | - |
| 6 | 5 | branch_and_bound | 0.000183 | 1847.14 | 1.0000 | 185 | 71 | 0.4325 |
| 6 | 5 | brute_force | 0.000038 | 1847.14 | 1.0000 | 120 | - | 0.0000 |
| 6 | 5 | nearest_neighbor | 0.000004 | 2047.11 | 1.1083 | 6 | - | - |
| 7 | 1 | branch_and_bound | 0.000562 | 2348.92 | 1.0000 | 459 | 251 | 0.7655 |
| 7 | 1 | brute_force | 0.000241 | 2348.92 | 1.0000 | 720 | - | 0.0000 |
| 7 | 1 | nearest_neighbor | 0.000006 | 2668.92 | 1.1362 | 7 | - | - |
| 7 | 2 | branch_and_bound | 0.000408 | 1656.36 | 1.0000 | 320 | 187 | 0.8365 |
| 7 | 2 | brute_force | 0.000237 | 1656.36 | 1.0000 | 720 | - | 0.0000 |
| 7 | 2 | nearest_neighbor | 0.000006 | 1941.04 | 1.1719 | 7 | - | - |
| 7 | 3 | branch_and_bound | 0.000462 | 1758.43 | 1.0000 | 355 | 200 | 0.8186 |
| 7 | 3 | brute_force | 0.000353 | 1758.43 | 1.0000 | 720 | - | 0.0000 |
| 7 | 3 | nearest_neighbor | 0.000007 | 1797.29 | 1.0221 | 7 | - | - |
| 7 | 4 | branch_and_bound | 0.000669 | 2138.15 | 1.0000 | 571 | 303 | 0.7082 |
| 7 | 4 | brute_force | 0.000257 | 2138.15 | 1.0000 | 720 | - | 0.0000 |
| 7 | 4 | nearest_neighbor | 0.000006 | 2138.15 | 1.0000 | 7 | - | - |
| 7 | 5 | branch_and_bound | 0.001208 | 1802.69 | 1.0000 | 435 | 245 | 0.7777 |
| 7 | 5 | brute_force | 0.000302 | 1802.69 | 1.0000 | 720 | - | 0.0000 |
| 7 | 5 | nearest_neighbor | 0.000013 | 1868.90 | 1.0367 | 7 | - | - |
| 8 | 1 | branch_and_bound | 0.002907 | 2540.16 | 1.0000 | 1578 | 1012 | 0.8848 |
| 8 | 1 | brute_force | 0.002534 | 2540.16 | 1.0000 | 5040 | - | 0.0000 |
| 8 | 1 | nearest_neighbor | 0.000014 | 2691.21 | 1.0595 | 8 | - | - |
| 8 | 2 | branch_and_bound | 0.001931 | 2474.36 | 1.0000 | 1174 | 733 | 0.9143 |
| 8 | 2 | brute_force | 0.001754 | 2474.36 | 1.0000 | 5040 | - | 0.0000 |
| 8 | 2 | nearest_neighbor | 0.000009 | 3121.33 | 1.2615 | 8 | - | - |
| 8 | 3 | branch_and_bound | 0.005322 | 2236.72 | 1.0000 | 4179 | 2177 | 0.6950 |
| 8 | 3 | brute_force | 0.002022 | 2236.72 | 1.0000 | 5040 | - | 0.0000 |
| 8 | 3 | nearest_neighbor | 0.000010 | 2328.36 | 1.0410 | 8 | - | - |
| 8 | 4 | branch_and_bound | 0.001829 | 2592.99 | 1.0000 | 1321 | 844 | 0.9036 |
| 8 | 4 | brute_force | 0.001689 | 2592.99 | 1.0000 | 5040 | - | 0.0000 |
| 8 | 4 | nearest_neighbor | 0.000010 | 2617.83 | 1.0096 | 8 | - | - |
| 8 | 5 | branch_and_bound | 0.003256 | 2334.97 | 1.0000 | 2679 | 1444 | 0.8045 |
| 8 | 5 | brute_force | 0.001695 | 2334.97 | 1.0000 | 5040 | - | 0.0000 |
| 8 | 5 | nearest_neighbor | 0.000009 | 2841.61 | 1.2170 | 8 | - | - |
| 9 | 1 | branch_and_bound | 0.011557 | 2700.99 | 1.0000 | 7448 | 4892 | 0.9320 |
| 9 | 1 | brute_force | 0.014290 | 2700.99 | 1.0000 | 40320 | - | 0.0000 |
| 9 | 1 | nearest_neighbor | 0.000013 | 2700.99 | 1.0000 | 9 | - | - |
| 9 | 2 | branch_and_bound | 0.006309 | 2367.95 | 1.0000 | 4294 | 2839 | 0.9608 |
| 9 | 2 | brute_force | 0.014450 | 2367.95 | 1.0000 | 40320 | - | 0.0000 |
| 9 | 2 | nearest_neighbor | 0.000011 | 2738.09 | 1.1563 | 9 | - | - |
| 9 | 3 | branch_and_bound | 0.006075 | 2644.34 | 1.0000 | 3768 | 2617 | 0.9656 |
| 9 | 3 | brute_force | 0.013927 | 2644.34 | 1.0000 | 40320 | - | 0.0000 |
| 9 | 3 | nearest_neighbor | 0.000011 | 2883.73 | 1.0905 | 9 | - | - |
| 9 | 4 | branch_and_bound | 0.003885 | 1516.03 | 1.0000 | 2211 | 1529 | 0.9798 |
| 9 | 4 | brute_force | 0.014541 | 1516.03 | 1.0000 | 40320 | - | 0.0000 |
| 9 | 4 | nearest_neighbor | 0.000011 | 1882.00 | 1.2414 | 9 | - | - |
| 9 | 5 | branch_and_bound | 0.004580 | 2925.82 | 1.0000 | 2815 | 1977 | 0.9743 |
| 9 | 5 | brute_force | 0.014351 | 2925.82 | 1.0000 | 40320 | - | 0.0000 |
| 9 | 5 | nearest_neighbor | 0.000009 | 2990.89 | 1.0222 | 9 | - | - |
| 10 | 1 | branch_and_bound | 0.021772 | 2388.15 | 1.0000 | 11187 | 8245 | 0.9887 |
| 10 | 1 | nearest_neighbor | 0.000014 | 2396.56 | 1.0035 | 10 | - | - |
| 10 | 2 | branch_and_bound | 0.036109 | 2511.62 | 1.0000 | 20258 | 14368 | 0.9795 |
| 10 | 2 | nearest_neighbor | 0.000013 | 2653.73 | 1.0566 | 10 | - | - |
| 10 | 3 | branch_and_bound | 0.017878 | 2639.92 | 1.0000 | 9409 | 6915 | 0.9905 |
| 10 | 3 | nearest_neighbor | 0.000017 | 3205.32 | 1.2142 | 10 | - | - |
| 10 | 4 | branch_and_bound | 0.012098 | 1464.04 | 1.0000 | 5884 | 4399 | 0.9940 |
| 10 | 4 | nearest_neighbor | 0.000015 | 1525.10 | 1.0417 | 10 | - | - |
| 10 | 5 | branch_and_bound | 0.028034 | 2238.92 | 1.0000 | 15623 | 11229 | 0.9842 |
| 10 | 5 | nearest_neighbor | 0.000017 | 2575.71 | 1.1504 | 10 | - | - |
