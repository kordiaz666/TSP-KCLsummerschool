# TSP Batch Benchmark

This benchmark is based on the Branch and Bound TSP solver from the Tkinter map visualizer. It separates the algorithm from the GUI so that many random test cases can be run automatically.

## What it tests

- `branch_and_bound`: exact solver with pruning.
- `brute_force`: traditional exhaustive search baseline. It is exact, but factorial-time, so it is only run for small `n`.
- `nearest_neighbor`: simple greedy baseline. It is fast, but not guaranteed to find the optimal route.

## Metrics

- `runtime_s`: wall-clock running time.
- `visited_nodes`: search nodes visited by the algorithm.
- `pruned_branches`: number of Branch and Bound branches cut by the lower bound.
- `total_possible_nodes`: number of recursive states a fixed-start DFS would visit without pruning.
- `pruning_rate`: `1 - visited_nodes / total_possible_nodes`.
- `ratio_to_optimal`: solution cost divided by the optimal cost. Lower is better; `1.0` means optimal.

## Run

From this folder:

```bash
python3 benchmark_tsp.py
```

Useful options:

```bash
python3 benchmark_tsp.py --min-cities 4 --max-cities 11 --instances 10
python3 benchmark_tsp.py --max-cities 12 --brute-max-cities 9
python3 benchmark_tsp.py --no-greedy-bound
```

Be careful with large city counts. Exact TSP grows very quickly.

## Output

The script creates a `results/` folder containing:

- `benchmark_results.csv`: one row per algorithm per test instance.
- `benchmark_summary.csv`: averaged results by city count and algorithm.
- `benchmark_summary.md`: readable Markdown summary table.
- `runtime_by_cities.png`: time comparison chart.
- `pruning_by_cities.png`: pruning and search-space chart.
- `quality_by_cities.png`: greedy/Branch and Bound quality compared with optimum.
