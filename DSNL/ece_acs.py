import os
import matplotlib.pyplot as plt
import numpy as np

# Expected Calibration Error (ECE)
def compute_ece(true_labels, pred_labels, confidences, num_bins):
    """
    Arguments:
        true_labels: the true labels for the test examples
        pred_labels: the predicted labels for the test examples
        confidences: the predicted confidences for the test examples
        num_bins: number of bins
    The true_labels, pred_labels, confidences arguments must be NumPy arrays;
    pred_labels and true_labels may contain numeric or string labels.
    For a multi-class model, the predicted label and confidence should be those
    of the highest scoring class.
    Returns a dictionary containing the following NumPy arrays:
        accuracies: the average accuracy for each bin
        confidences: the average confidence for each bin
        counts: the number of examples in each bin
        bins: the confidence thresholds for each bin
        avg_accuracy: the accuracy over the entire test set
        avg_confidence: the average confidence over the entire test set
        expected_calibration_error: a weighted average of all calibration gaps
        max_calibration_error: the largest calibration gap across all bins
    """
    assert (len(confidences) == len(pred_labels))
    assert (len(confidences) == len(true_labels))
    assert (num_bins > 0)

    bin_size = 1.0 / num_bins
    bins = np.linspace(0.0, 1.0, num_bins + 1)
    indices = np.digitize(confidences, bins, right=True)

    bin_accuracies = np.zeros(num_bins, dtype=np.float)
    bin_confidences = np.zeros(num_bins, dtype=np.float)
    bin_counts = np.zeros(num_bins, dtype=np.int)

    for b in range(num_bins):
        selected = np.where(indices == b + 1)[0]
        if len(selected) > 0:
            bin_accuracies[b] = np.mean(true_labels[selected] == pred_labels[selected])
            bin_confidences[b] = np.mean(confidences[selected])
            bin_counts[b] = len(selected)

    avg_acc = np.sum(bin_accuracies * bin_counts) / np.sum(bin_counts)
    avg_conf = np.sum(bin_confidences * bin_counts) / np.sum(bin_counts)

    gaps = np.abs(bin_accuracies - bin_confidences)
    ece  = abs(avg_acc-avg_conf)
    #ece = np.sum(gaps * bin_counts) / np.sum(bin_counts)
    mce = np.max(gaps)
  
    return {"accuracies": bin_accuracies,
            "confidences": bin_confidences,
            "counts": bin_counts,
            "bins": bins,
            "avg_accuracy": avg_acc,
            "avg_confidence": avg_conf,
            "expected_calibration_error": ece,
            "max_calibration_error": mce}



def cos_sim(p,q):
    return np.dot(p,q)/(np.linalg.norm(p)*np.linalg.norm(q))
    
# Averaged Cosine Similarity (ACS)
def compute_acs(hypno_true, hypno_pred):
    cos_ = []
    for i in range(len(hypno_true)):
      cos_.append(cos_sim(hypno_true[i], hypno_pred[i]))
    return np.mean(cos_)
