def confusion(y_true, y_pred):
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length")
    tp = fp = fn = tn = 0
    for actual, predicted in zip(y_true, y_pred):
        if predicted == 1 and actual == 1:
            tp += 1
        elif predicted == 1:
            fp += 1
        elif actual == 1:
            fn += 1
        else:
            tn += 1
    return tp, fp, fn, tn


def precision_recall(y_true, y_pred):
    tp, fp, fn, _ = confusion(y_true, y_pred)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return precision, recall


def f1(y_true, y_pred):
    precision, recall = precision_recall(y_true, y_pred)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)
