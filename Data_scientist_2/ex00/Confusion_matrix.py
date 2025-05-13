#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Computes the confusion matrix and metrics for a classification task.
Usage:
    python Confusion_matrix.py predictions.txt truth.txt [--save-png output.png]
"""

import sys
import argparse
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import matplotlib.pyplot as plt

def parse_args():
    parser = argparse.ArgumentParser(
        description="Exercise ex00: compute confusion matrix and classification metrics"
    )
    parser.add_argument("predictions", help="File with predicted labels, one label per line")
    parser.add_argument("truth", help="File with ground truth labels, one label per line")
    parser.add_argument("--save-png", dest="pngpath",
                        help="If provided, save the heatmap to the given path")
    return parser.parse_args()

def load_labels(path):
    with open(path, encoding='utf-8') as f:
        labels = [line.strip() for line in f if line.strip()]
    return labels

def main():
    args = parse_args()
    preds = load_labels(args.predictions)
    truths = load_labels(args.truth)

    if len(preds) != len(truths):
        sys.exit(f"Error: {args.predictions} and {args.truth} have different numbers of lines "
                 f"({len(preds)} vs {len(truths)})")

    # Determine unique labels
    labels = sorted(set(truths + preds))

    # Compute confusion matrix and metrics
    cm = confusion_matrix(truths, preds, labels=labels)
    report = classification_report(truths, preds, labels=labels)
    acc = accuracy_score(truths, preds)

    # Print results
    print("=== Classification Report ===")
    print(report)
    print(f"Overall accuracy: {acc:.2f} ({len(truths)} samples)\n")

    # Plot heatmap
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.colorbar(im, ax=ax)
    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_yticklabels(labels)
    ax.set_xlabel('Predicted label')
    ax.set_ylabel('True label')
    ax.set_title('Confusion Matrix Heatmap')

    # Annotate cells with counts
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, f"{cm[i, j]:d}",
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()

    # Save or show the plot
    if args.pngpath:
        plt.savefig(args.pngpath, dpi=150)
        print(f"Heatmap saved to: {args.pngpath}")
    else:
        plt.show()

if __name__ == "__main__":
    main()
