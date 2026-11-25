def find_subgrid(matrix, target, height, width):
    """Brute force: O(rows * cols * height * width)."""
    rows, cols = len(matrix), len(matrix[0])
    for r in range(rows - height + 1):
        for c in range(cols - width + 1):
            total = sum(sum(row[c:c + width]) for row in matrix[r:r + height])
            if total == target:
                return (r, c)
    return None


def find_subgrid_prefix(matrix, target, height, width):
    """2D prefix sums: O(rows * cols). prefix[r][c] = sum of matrix[:r][:c]."""
    rows, cols = len(matrix), len(matrix[0])
    prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
    for r in range(rows):
        for c in range(cols):
            prefix[r + 1][c + 1] = matrix[r][c] + prefix[r][c + 1] + prefix[r + 1][c] - prefix[r][c]
    for r in range(rows - height + 1):
        for c in range(cols - width + 1):
            total = (prefix[r + height][c + width] - prefix[r][c + width]
                     - prefix[r + height][c] + prefix[r][c])
            if total == target:
                return (r, c)
    return None
