def kmeans(points, centroids, iterations=10):
    centroids = [list(c) for c in centroids]          # copy: leave the caller's list alone
    assignments = None
    for _ in range(iterations):
        new = []
        for p in points:
            distances = [sum((a - b) ** 2 for a, b in zip(p, c)) for c in centroids]
            new.append(distances.index(min(distances)))    # index() returns the first minimum: ties go low
        if new == assignments:
            break
        assignments = new
        for k in range(len(centroids)):
            members = [p for p, a in zip(points, assignments) if a == k]
            if members:
                centroids[k] = [sum(column) / len(members) for column in zip(*members)]
    return centroids, assignments

# Unsupervised. It only finds a local optimum, so the start matters: run several random starts
# (or k-means++) and keep the lowest within-cluster distance. Choose k with the elbow or silhouette,
# and by whether the clusters mean something.
