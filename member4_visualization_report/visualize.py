import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['figure.figsize'] = (10, 6)

summary = pd.read_csv(r'D:\0work\www\成员3\results\benchmark_summary.csv')
raw = pd.read_csv(r'D:\0work\www\成员3\results\benchmark_results.csv')

# ============================================================
# Chart 1: N vs Average Runtime (log scale, B&B vs Brute Force)
# ============================================================
fig, ax = plt.subplots()
bb = summary[summary['algorithm'] == 'branch_and_bound']
bf = summary[summary['algorithm'] == 'brute_force']
nn = summary[summary['algorithm'] == 'nearest_neighbor']

ax.plot(bb['cities'], bb['mean_runtime_s'], 'o-', color='#E74C3C', linewidth=2, markersize=8, label='Branch & Bound')
ax.plot(bf['cities'], bf['mean_runtime_s'], 's--', color='#3498DB', linewidth=2, markersize=8, label='Brute Force (DFS)')
ax.plot(nn['cities'], nn['mean_runtime_s'], '^-.', color='#2ECC71', linewidth=2, markersize=8, label='Nearest Neighbor')

ax.set_xlabel('Number of Cities (N)', fontsize=13)
ax.set_ylabel('Average Runtime (seconds)', fontsize=13)
ax.set_title('TSP Algorithm Performance: Runtime vs Problem Size', fontsize=14, fontweight='bold')
ax.set_yscale('log')
ax.set_xticks(range(4, 11))
ax.grid(True, which='both', linestyle='--', alpha=0.6)
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig(r'D:\0work\www\成员4\runtime_by_cities.png')
plt.close()

# ============================================================
# Chart 2: N vs Average Searched Branches (Visited Nodes)
# ============================================================
fig, ax = plt.subplots()
ax.plot(bb['cities'], bb['mean_visited_nodes'], 'o-', color='#E74C3C', linewidth=2, markersize=8, label='Branch & Bound (visited nodes)')
ax.plot(bf['cities'], bf['mean_visited_nodes'], 's--', color='#3498DB', linewidth=2, markersize=8, label='Brute Force (all nodes)')

ax.set_xlabel('Number of Cities (N)', fontsize=13)
ax.set_ylabel('Average Number of Nodes Searched', fontsize=13)
ax.set_title('Search Space Comparison: B&B vs Brute Force', fontsize=14, fontweight='bold')
ax.set_yscale('log')
ax.set_xticks(range(4, 10))
ax.grid(True, which='both', linestyle='--', alpha=0.6)
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig(r'D:\0work\www\成员4\nodes_by_cities.png')
plt.close()

# ============================================================
# Chart 3: N vs Pruning Rate
# ============================================================
fig, ax = plt.subplots()
ax.plot(bb['cities'], bb['mean_pruning_rate'], 'o-', color='#9B59B6', linewidth=2, markersize=8)
ax.set_xlabel('Number of Cities (N)', fontsize=13)
ax.set_ylabel('Average Pruning Rate', fontsize=13)
ax.set_title('Branch & Bound Pruning Efficiency vs Problem Size', fontsize=14, fontweight='bold')
ax.set_xticks(range(4, 11))
ax.set_ylim(0, 1.05)
ax.grid(True, linestyle='--', alpha=0.6)
for i, row in bb.iterrows():
    ax.annotate(f'{row["mean_pruning_rate"]:.1%}',
                (row['cities'], row['mean_pruning_rate']),
                textcoords="offset points", xytext=(0, 12),
                ha='center', fontsize=9, color='#9B59B6')
plt.tight_layout()
plt.savefig(r'D:\0work\www\成员4\pruning_rate_by_cities.png')
plt.close()

# ============================================================
# Chart 4: Nodes visited comparison bar chart for N=4..9
# ============================================================
fig, ax = plt.subplots()
cities_bfbf = bf[bf['cities'] <= 9]
cities_bb = bb[bb['cities'] <= 9]
x = np.arange(len(cities_bfbf))
width = 0.35
ax.bar(x - width/2, cities_bfbf['mean_visited_nodes'], width, label='Brute Force (total nodes)', color='#3498DB', alpha=0.8)
ax.bar(x + width/2, cities_bb['mean_visited_nodes'], width, label='B&B (visited nodes)', color='#E74C3C', alpha=0.8)
ax.set_xticks(x)
ax.set_xticklabels(cities_bfbf['cities'])
ax.set_xlabel('Number of Cities (N)', fontsize=13)
ax.set_ylabel('Mean Nodes Searched', fontsize=13)
ax.set_title('Nodes Searched: Brute Force vs Branch & Bound', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(True, axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig(r'D:\0work\www\成员4\nodes_bar_comparison.png')
plt.close()

# ============================================================
# Chart 5: Cost quality comparison (ratio to optimal)
# ============================================================
fig, ax = plt.subplots()
nn_qual = nn[nn['mean_ratio_to_optimal'].notna()]
ax.bar(nn_qual['cities'], nn_qual['mean_ratio_to_optimal'], color='#F39C12', alpha=0.8, label='Nearest Neighbor')
ax.axhline(y=1.0, color='#E74C3C', linestyle='--', linewidth=1.5, label='Optimal (ratio=1.0)')
ax.set_xlabel('Number of Cities (N)', fontsize=13)
ax.set_ylabel('Mean Ratio to Optimal Cost', fontsize=13)
ax.set_title('Route Quality: Nearest Neighbor vs Optimal', fontsize=14, fontweight='bold')
ax.set_xticks(nn_qual['cities'])
ax.grid(True, axis='y', linestyle='--', alpha=0.6)
ax.legend(fontsize=11)
for i, row in nn_qual.iterrows():
    ax.annotate(f'{row["mean_ratio_to_optimal"]:.3f}',
                (row['cities'], row['mean_ratio_to_optimal']),
                textcoords="offset points", xytext=(0, 8),
                ha='center', fontsize=9)
plt.tight_layout()
plt.savefig(r'D:\0work\www\成员4\quality_comparison.png')
plt.close()

# ============================================================
# Chart 6: Average pruned branches vs N
# ============================================================
fig, ax = plt.subplots()
ax.plot(bb['cities'], bb['mean_pruned_branches'], 'o-', color='#1ABC9C', linewidth=2, markersize=8)
ax.set_xlabel('Number of Cities (N)', fontsize=13)
ax.set_ylabel('Average Pruned Branches', fontsize=13)
ax.set_title('B&B Pruned Branches vs Problem Size', fontsize=14, fontweight='bold')
ax.set_xticks(range(4, 11))
ax.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig(r'D:\0work\www\成员4\pruned_branches_by_cities.png')
plt.close()

print("All 6 charts generated successfully.")
