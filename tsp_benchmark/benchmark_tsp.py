from __future__ import annotations

import argparse
import csv
import os
import random
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any

from tsp_algorithms import (
    Point,
    branch_and_bound,
    brute_force,
    nearest_neighbor,
)


def generate_points(n: int, seed: int, width: int = 1000, height: int = 700) -> list[Point]:
    rng = random.Random(seed)
    return [(rng.uniform(0, width), rng.uniform(0, height)) for _ in range(n)]


def mean_or_none(values: list[float | int | None]) -> float | None:
    clean = [float(value) for value in values if value is not None]
    if not clean:
        return None
    return statistics.mean(clean)


def fmt(value: float | int | None, digits: int = 4) -> str:
    if value is None:
        return "-"
    if isinstance(value, int):
        return str(value)
    return f"{value:.{digits}f}"


def result_to_row(
    n: int,
    instance: int,
    seed: int,
    result: Any,
    optimal_cost: float | None,
) -> dict[str, str | int | float | None]:
    ratio_to_optimal = None
    if optimal_cost and optimal_cost > 0:
        ratio_to_optimal = result.cost / optimal_cost

    return {
        "cities": n,
        "instance": instance,
        "seed": seed,
        "algorithm": result.algorithm,
        "cost": result.cost,
        "runtime_s": result.runtime_s,
        "visited_nodes": result.visited_nodes,
        "pruned_branches": result.pruned_branches,
        "total_possible_nodes": result.total_possible_nodes,
        "pruning_rate": result.pruning_rate,
        "ratio_to_optimal": ratio_to_optimal,
        "path": "->".join(str(city) for city in result.path),
    }


def aggregate_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[int, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[(int(row["cities"]), str(row["algorithm"]))].append(row)

    summary = []
    for (cities, algorithm), group_rows in sorted(groups.items()):
        summary.append(
            {
                "cities": cities,
                "algorithm": algorithm,
                "runs": len(group_rows),
                "mean_cost": mean_or_none([row["cost"] for row in group_rows]),
                "mean_runtime_s": mean_or_none([row["runtime_s"] for row in group_rows]),
                "mean_visited_nodes": mean_or_none([row["visited_nodes"] for row in group_rows]),
                "mean_pruned_branches": mean_or_none([row["pruned_branches"] for row in group_rows]),
                "mean_total_possible_nodes": mean_or_none(
                    [row["total_possible_nodes"] for row in group_rows]
                ),
                "mean_pruning_rate": mean_or_none([row["pruning_rate"] for row in group_rows]),
                "mean_ratio_to_optimal": mean_or_none([row["ratio_to_optimal"] for row in group_rows]),
            }
        )

    return summary


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_markdown_summary(path: Path, summary: list[dict[str, Any]]) -> None:
    lines = [
        "# TSP Batch Benchmark Summary",
        "",
        "| Cities | Algorithm | Runs | Mean runtime (s) | Mean cost | Ratio to optimal | Visited nodes | Pruned branches | Pruning rate |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for row in summary:
        lines.append(
            "| "
            f"{row['cities']} | "
            f"{row['algorithm']} | "
            f"{row['runs']} | "
            f"{fmt(row['mean_runtime_s'], 6)} | "
            f"{fmt(row['mean_cost'], 2)} | "
            f"{fmt(row['mean_ratio_to_optimal'], 4)} | "
            f"{fmt(row['mean_visited_nodes'], 0)} | "
            f"{fmt(row['mean_pruned_branches'], 0)} | "
            f"{fmt(row['mean_pruning_rate'], 4)} |"
        )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_markdown_report(
    path: Path,
    summary: list[dict[str, Any]],
    rows: list[dict[str, Any]],
) -> None:
    lines = [
        "# TSP Batch Benchmark Report",
        "",
        "## What this experiment does",
        "",
        "For each city count `n`, the program generates several random TSP instances. "
        "Each instance is solved with Branch and Bound, Nearest Neighbor, and, for small `n`, Brute Force. "
        "The report compares running time, search effort, pruning, and route quality.",
        "",
        "## Algorithms",
        "",
        "- `branch_and_bound`: exact method. It searches possible routes but cuts branches when the lower bound is already worse than the best known route.",
        "- `brute_force`: exact baseline. It tries every possible route, so it becomes very slow as `n` grows.",
        "- `nearest_neighbor`: greedy baseline. It always goes to the nearest unvisited city. It is fast but not always optimal.",
        "",
        "## Chart guide",
        "",
        "- `runtime_by_cities.png`: compares average runtime as the number of cities increases. The y-axis uses a log scale because exact TSP grows very quickly.",
        "- `pruning_by_cities.png`: shows how much search Branch and Bound avoids. The left plot is pruning rate; the right plot compares no-pruning search states with actually visited Branch and Bound states.",
        "- `quality_by_cities.png`: compares route quality. A value of `1.0` means optimal. Values above `1.0` mean the route is longer than the optimal route.",
        "",
        "## Summary table",
        "",
        "| Cities | Algorithm | Runs | Mean runtime (s) | Mean cost | Ratio to optimal | Visited nodes | Pruned branches | Pruning rate |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for row in summary:
        lines.append(
            "| "
            f"{row['cities']} | "
            f"{row['algorithm']} | "
            f"{row['runs']} | "
            f"{fmt(row['mean_runtime_s'], 6)} | "
            f"{fmt(row['mean_cost'], 2)} | "
            f"{fmt(row['mean_ratio_to_optimal'], 4)} | "
            f"{fmt(row['mean_visited_nodes'], 0)} | "
            f"{fmt(row['mean_pruned_branches'], 0)} | "
            f"{fmt(row['mean_pruning_rate'], 4)} |"
        )

    lines.extend(
        [
            "",
            "## Full per-test table",
            "",
            "| Cities | Test | Algorithm | Runtime (s) | Cost | Ratio to optimal | Visited nodes | Pruned branches | Pruning rate |",
            "|---:|---:|---|---:|---:|---:|---:|---:|---:|",
        ]
    )

    ordered_rows = sorted(
        rows,
        key=lambda row: (int(row["cities"]), int(row["instance"]), str(row["algorithm"])),
    )
    for row in ordered_rows:
        lines.append(
            "| "
            f"{row['cities']} | "
            f"{int(row['instance']) + 1} | "
            f"{row['algorithm']} | "
            f"{fmt(row['runtime_s'], 6)} | "
            f"{fmt(row['cost'], 2)} | "
            f"{fmt(row['ratio_to_optimal'], 4)} | "
            f"{fmt(row['visited_nodes'], 0)} | "
            f"{fmt(row['pruned_branches'], 0)} | "
            f"{fmt(row['pruning_rate'], 4)} |"
        )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def plot_results(outdir: Path, summary: list[dict[str, Any]]) -> None:
    os.environ.setdefault("MPLCONFIGDIR", str(outdir / ".matplotlib"))
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    by_algorithm: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in summary:
        by_algorithm[str(row["algorithm"])].append(row)

    plt.figure(figsize=(9, 5))
    for algorithm, rows in sorted(by_algorithm.items()):
        rows = sorted(rows, key=lambda row: row["cities"])
        xs = [row["cities"] for row in rows]
        ys = [row["mean_runtime_s"] for row in rows]
        plt.plot(xs, ys, marker="o", label=algorithm)

    plt.yscale("log")
    plt.xlabel("Number of cities")
    plt.ylabel("Mean runtime, seconds (log scale)")
    plt.title("Runtime comparison")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(outdir / "runtime_by_cities.png", dpi=180)
    plt.close()

    bnb_rows = sorted(
        [row for row in summary if row["algorithm"] == "branch_and_bound"],
        key=lambda row: row["cities"],
    )
    if bnb_rows:
        xs = [row["cities"] for row in bnb_rows]
        pruning_rates = [row["mean_pruning_rate"] for row in bnb_rows]
        visited_nodes = [row["mean_visited_nodes"] for row in bnb_rows]
        total_nodes = [row["mean_total_possible_nodes"] for row in bnb_rows]

        fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
        axes[0].plot(xs, pruning_rates, marker="o", color="#2563eb")
        axes[0].set_ylim(0, 1)
        axes[0].set_xlabel("Number of cities")
        axes[0].set_ylabel("Pruning rate")
        axes[0].set_title("Branch and Bound pruning")
        axes[0].grid(True, alpha=0.3)

        axes[1].plot(xs, total_nodes, marker="o", label="No-pruning DFS states")
        axes[1].plot(xs, visited_nodes, marker="o", label="B&B visited states")
        axes[1].set_yscale("log")
        axes[1].set_xlabel("Number of cities")
        axes[1].set_ylabel("Mean nodes (log scale)")
        axes[1].set_title("Search space reduction")
        axes[1].grid(True, which="both", alpha=0.3)
        axes[1].legend()

        fig.tight_layout()
        fig.savefig(outdir / "pruning_by_cities.png", dpi=180)
        plt.close(fig)

    quality_rows = [
        row
        for row in summary
        if row["mean_ratio_to_optimal"] is not None and row["algorithm"] != "brute_force"
    ]
    if quality_rows:
        plt.figure(figsize=(9, 5))
        for algorithm, rows in sorted(by_algorithm.items()):
            rows = [
                row
                for row in sorted(rows, key=lambda item: item["cities"])
                if row["mean_ratio_to_optimal"] is not None and algorithm != "brute_force"
            ]
            if not rows:
                continue
            plt.plot(
                [row["cities"] for row in rows],
                [row["mean_ratio_to_optimal"] for row in rows],
                marker="o",
                label=algorithm,
            )

        plt.axhline(1.0, color="black", linewidth=1, linestyle="--", label="Optimal")
        plt.xlabel("Number of cities")
        plt.ylabel("Mean cost / optimal cost")
        plt.title("Solution quality")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig(outdir / "quality_by_cities.png", dpi=180)
        plt.close()


def run_benchmark(args: argparse.Namespace) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []

    for n in range(args.min_cities, args.max_cities + 1):
        for instance in range(args.instances):
            seed = args.seed + n * 10_000 + instance
            points = generate_points(n, seed)

            brute = None
            if n <= args.brute_max_cities:
                brute = brute_force(points)
                rows.append(result_to_row(n, instance, seed, brute, brute.cost))

            bnb = branch_and_bound(points, use_greedy_initial_bound=not args.no_greedy_bound)
            optimal_cost = brute.cost if brute is not None else bnb.cost
            rows.append(result_to_row(n, instance, seed, bnb, optimal_cost))

            greedy = nearest_neighbor(points)
            rows.append(result_to_row(n, instance, seed, greedy, optimal_cost))

            if brute is not None and abs(brute.cost - bnb.cost) > 1e-6:
                raise RuntimeError(
                    f"Branch and Bound mismatch for n={n}, instance={instance}: "
                    f"bnb={bnb.cost}, brute={brute.cost}"
                )

            print(
                f"n={n:2d} instance={instance + 1:2d}/{args.instances} "
                f"bnb_time={bnb.runtime_s:.6f}s bnb_pruned={bnb.pruned_branches} "
                f"greedy_ratio={greedy.cost / optimal_cost:.3f}"
            )

    summary = aggregate_rows(rows)
    return rows, summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Batch benchmark for TSP Branch and Bound, brute force, and greedy baselines."
    )
    parser.add_argument("--min-cities", type=int, default=4)
    parser.add_argument("--max-cities", type=int, default=10)
    parser.add_argument("--instances", type=int, default=5)
    parser.add_argument("--seed", type=int, default=20260728)
    parser.add_argument("--brute-max-cities", type=int, default=9)
    parser.add_argument("--outdir", type=Path, default=Path("results"))
    parser.add_argument(
        "--no-greedy-bound",
        action="store_true",
        help="Do not initialise Branch and Bound with a nearest-neighbor upper bound.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.min_cities < 3:
        raise ValueError("Use at least 3 cities for a TSP loop.")
    if args.max_cities < args.min_cities:
        raise ValueError("--max-cities must be >= --min-cities.")

    args.outdir.mkdir(parents=True, exist_ok=True)
    rows, summary = run_benchmark(args)

    write_csv(args.outdir / "benchmark_results.csv", rows)
    write_csv(args.outdir / "benchmark_summary.csv", summary)
    write_markdown_summary(args.outdir / "benchmark_summary.md", summary)
    write_markdown_report(args.outdir / "benchmark_report.md", summary, rows)
    plot_results(args.outdir, summary)

    print()
    print(f"Saved raw results: {args.outdir / 'benchmark_results.csv'}")
    print(f"Saved summary:     {args.outdir / 'benchmark_summary.md'}")
    print(f"Saved report:      {args.outdir / 'benchmark_report.md'}")
    print(f"Saved charts:      {args.outdir / 'runtime_by_cities.png'}")
    print(f"                   {args.outdir / 'pruning_by_cities.png'}")
    print(f"                   {args.outdir / 'quality_by_cities.png'}")


if __name__ == "__main__":
    main()
