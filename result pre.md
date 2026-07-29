# Result Presentation Script

## English

Now I will present the results of our experiment.

For the result section, our goal was to evaluate how well our Branch and Bound method performs compared with two baseline methods: Brute Force and Nearest Neighbor. We wanted to look at three main aspects: running time, pruning effectiveness, and solution quality.

In our batch testing, we tested different numbers of cities, from 4 to 10. For each number of cities, we generated 10 random test cases. This is important because a single test case may be affected by the positions of the cities. By using 10 random instances for each value of `n`, the average result becomes more reliable and gives us a better view of the general performance.

The first result is the runtime comparison. This is shown in the runtime chart. In this chart, the x-axis represents the number of cities, and the y-axis represents the average running time in seconds. We use a logarithmic scale on the y-axis because the running time grows very quickly, especially for exact methods.

From this chart, we can see that Nearest Neighbor is always the fastest method. This is expected, because it only chooses the nearest unvisited city at each step. However, speed alone does not mean it gives the best route.

Brute Force is also exact, but its running time increases much faster as the number of cities becomes larger. This is because Brute Force checks every possible route. For example, at 9 cities, Brute Force checks `40,320` possible routes and takes about `0.0145` seconds on average. This may still sound small, but the growth is factorial, so if we continue increasing the number of cities, the runtime will become much worse.

Branch and Bound also gives the optimal result, but it performs better than Brute Force for larger cases because it avoids searching unnecessary branches. At 9 cities, Branch and Bound takes about `0.0064` seconds on average, which is faster than Brute Force while still producing the optimal route.

The second result is the pruning performance of Branch and Bound. This is the most important result in our experiment. The pruning chart shows how much of the search space is avoided by the algorithm.

At small city numbers, the pruning effect is not very strong. For example, at 4 cities, the pruning rate is only around `5.6%`. This makes sense because the search space is still very small, so there are not many branches to remove.

But as the number of cities increases, the pruning effect becomes much stronger. At 6 cities, the pruning rate is about `50.8%`. At 8 cities, it increases to about `86.4%`. And at 10 cities, the pruning rate reaches about `98.8%`.

This means that for 10 cities, Branch and Bound avoids almost all of the unnecessary search space. Instead of blindly checking every route, it uses bounds to decide whether a partial route is still worth exploring. If a partial route is already worse than the best route found so far, the algorithm stops exploring that branch.

The third result is solution quality. This is shown in the quality comparison chart. In this chart, a ratio of `1.0` means the algorithm found the optimal route. A value above `1.0` means the route is longer than the optimal route.

Branch and Bound and Brute Force both have a ratio of `1.0`, which means they both find the optimal solution. This confirms that our Branch and Bound implementation is correct for the tested cases, because it matches the Brute Force result where Brute Force is available.

Nearest Neighbor is much faster, but its route is not always optimal. For example, at 8 cities, its average route cost is about `1.13` times the optimal route. At 10 cities, it is about `1.09` times the optimal route. So the greedy method sacrifices accuracy in exchange for speed.

Overall, these results show a clear trade-off between speed and accuracy. Nearest Neighbor is the fastest, but it may produce longer routes. Brute Force is accurate, but it does not scale well. Branch and Bound gives the optimal answer and becomes much more efficient as the number of cities increases, because pruning removes a large part of the search space.

Therefore, based on our results, Branch and Bound is the best choice among these three methods when we need an exact TSP solution but also want better efficiency than simple exhaustive search.

## 中文翻译

现在我来展示我们实验的结果。

在结果部分，我们的目标是评估 Branch and Bound 方法的表现，并把它和两个基准方法进行比较：Brute Force 和 Nearest Neighbor。我们主要关注三个方面：运行时间、剪枝效果，以及解的质量。

在批量测试中，我们测试了不同数量的城市，从 4 个城市到 10 个城市。对于每一个城市数量，我们都生成了 10 组随机测试样例。这样做很重要，因为单独一次测试可能会受到城市位置分布的影响。每个 `n` 使用 10 组随机测试后，平均结果会更可靠，也更能反映算法整体表现。

第一个结果是运行时间对比，也就是 runtime chart。在这张图中，横轴表示城市数量，纵轴表示平均运行时间，单位是秒。纵轴使用了对数刻度，因为运行时间增长得非常快，尤其是对于精确算法来说。

从这张图可以看到，Nearest Neighbor 始终是最快的方法。这是符合预期的，因为它每一步只选择最近的未访问城市。不过，速度快并不代表它一定能找到最好的路线。

Brute Force 也是精确算法，但随着城市数量增加，它的运行时间增长得更快。这是因为 Brute Force 会检查每一种可能的路线。比如在 9 个城市时，Brute Force 需要检查 `40,320` 条可能路线，平均耗时大约是 `0.0145` 秒。这个数字看起来可能还不大，但它的增长是阶乘级别的，所以如果继续增加城市数量，运行时间会迅速变得非常大。

Branch and Bound 同样可以得到最优结果，但在较大规模时，它比 Brute Force 表现更好，因为它可以避免搜索不必要的分支。比如在 9 个城市时，Branch and Bound 平均耗时大约是 `0.0064` 秒，比 Brute Force 更快，同时仍然能得到最优路线。

第二个结果是 Branch and Bound 的剪枝表现。这是我们实验中最重要的结果。剪枝图展示了这个算法避免了多少搜索空间。

在城市数量较小时，剪枝效果并不特别明显。比如在 4 个城市时，剪枝率只有大约 `5.6%`。这是合理的，因为搜索空间本身还很小，没有太多分支可以被剪掉。

但是随着城市数量增加，剪枝效果会明显增强。在 6 个城市时，剪枝率大约是 `50.8%`。在 8 个城市时，剪枝率上升到大约 `86.4%`。到了 10 个城市时，剪枝率达到了大约 `98.8%`。

这意味着在 10 个城市的情况下，Branch and Bound 几乎避免了所有不必要的搜索空间。它不是盲目检查所有路线，而是利用 bound 来判断一个部分路线是否还值得继续探索。如果某条部分路线已经不可能比当前找到的最好路线更短，算法就会停止继续搜索这个分支。

第三个结果是解的质量，也就是 quality comparison chart。在这张图中，ratio 等于 `1.0` 表示算法找到了最优路线。如果数值大于 `1.0`，就表示这条路线比最优路线更长。

Branch and Bound 和 Brute Force 的 ratio 都是 `1.0`，说明它们都找到了最优解。这也证明了我们的 Branch and Bound 实现在测试样例中是正确的，因为在可以使用 Brute Force 验证的情况下，它和 Brute Force 的结果一致。

Nearest Neighbor 虽然速度快很多，但它不一定能找到最优路线。比如在 8 个城市时，它的平均路线长度大约是最优路线的 `1.13` 倍。在 10 个城市时，大约是最优路线的 `1.09` 倍。所以贪心方法是用准确性换取速度。

总体来看，这些结果展示了速度和准确性之间的明显权衡。Nearest Neighbor 最快，但可能产生更长的路线。Brute Force 准确，但扩展性很差。Branch and Bound 能找到最优解，同时随着城市数量增加，由于剪枝去除了大量搜索空间，它比简单的穷举搜索更高效。

因此，根据我们的结果，当我们需要一个精确的 TSP 解，同时又希望比暴力穷举更高效时，Branch and Bound 是这三种方法中最合适的选择。
