# mlc_04 · k-means from scratch

**Task.** Write `kmeans(points, centroids, iterations=10)`.
- `points` is a list of points (lists of numbers). `centroids` is the list of starting centres, so the result is deterministic.
- Repeat `iterations` times: (1) assign each point to its nearest centroid (ties go to the lower index); (2) move each centroid to the mean of its points. A centroid with no points stays where it is.
- Stop early when no assignment changes.
- Return `(centroids, assignments)`: the final centres as lists of floats, and one cluster index per point.
- Do not change the caller's `centroids` list.

**Then, out loud.** Supervised or unsupervised? Why does the starting point matter, and how do you choose k?

**Conditions.** Blank file, plain Python (no numpy, no sklearn), no autocomplete, 20 minutes. Say the time complexity when you finish.
