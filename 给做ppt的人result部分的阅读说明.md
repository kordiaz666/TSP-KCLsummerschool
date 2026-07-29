# 给做ppt的人result部分的阅读说明

仅需阅读提炼以下文件。注意：`result pre.md`、`benchmark_summary.md` 和三张结果图必须使用同一套数据。

- `results/benchmark_summary.md`: readable Markdown summary table. 易于阅读的 Markdown 格式汇总表格。
- `results/runtime_by_cities.png`: time comparison chart. 运行时间对比图表。
- `results/pruning_by_cities.png`: pruning and search-space chart. 剪枝与搜索空间图表。
- `results/quality_by_cities.png`: greedy/Branch and Bound quality compared with optimum. 贪心算法与分枝限界算法相对于最优解的解质量对比图表。
- `result pre.md`: 演讲稿参考。

数据核对状态：已确认 `result pre.md` 中引用的关键数据与 `results/benchmark_summary.md`、`results/runtime_by_cities.png`、`results/pruning_by_cities.png`、`results/quality_by_cities.png` 当前结果一致。
