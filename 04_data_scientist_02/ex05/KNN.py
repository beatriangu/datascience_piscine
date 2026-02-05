#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KNN.py: Finds the optimal k by measuring precision on a validation split,
plots Precision vs k to precision_vs_k.png, trains on full set, predicts on Test_knight.csv,
and writes KNN.txt.

Usage:
    python3 KNN.py <Train_knight.csv> <Test_knight.csv>

Arguments:
  1) Train_knight.csv   CSV with features + 'knight' label (Jedi/Sith)
  2) Test_knight.csv    CSV with features only

Outputs:
  - KNN.txt            Predictions (one per line: "Jedi" or "Sith")
  - precision_vs_k.png  Plot of Precision (%) vs k
  - Console: precision and F1 for each k, best k, and final confirmation
"""
import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, f1_score


def main():
    # 1) Validate args
    if len(sys.argv) != 3:
        print("Usage: python3 KNN.py <Train_knight.csv> <Test_knight.csv>")
        sys.exit(1)
    train_csv, test_csv = sys.argv[1], sys.argv[2]

    # 2) Check files
    for path in (train_csv, test_csv):
        if not os.path.isfile(path):
            print(f"Error: file not found: {path}")
            sys.exit(1)

    # 3) Load data
    df_train = pd.read_csv(train_csv)
    df_test  = pd.read_csv(test_csv)
    X = df_train.drop(columns=['knight'])
    y = df_train['knight']
    X_test = df_test[X.columns]

    # 4) Split train/validation (stratified)
    X_tr, X_val, y_tr, y_val = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    # 5) Evaluate odd k’s from 1 to 29
    ks = list(range(1, 30, 2))
    precisions, f1s = [], []
    print("Evaluating on validation set:")
    for k in ks:
        pipe = Pipeline([
            ('scaler', MinMaxScaler()),
            ('knn', KNeighborsClassifier(n_neighbors=k, weights='distance'))
        ])
        pipe.fit(X_tr, y_tr)
        y_val_pred = pipe.predict(X_val)
        p = precision_score(y_val, y_val_pred, pos_label='Jedi')
        f = f1_score(y_val, y_val_pred, pos_label='Jedi')
        precisions.append(p)
        f1s.append(f)
        print(f" k={k:2d} -> Precision={p*100:.2f}%, F1={f*100:.2f}%")

    # 6) Plot Precision vs k and save
    plt.figure(figsize=(8, 5))
    plt.plot(ks, np.array(precisions) * 100, marker='o')
    plt.title('Precision (%) vs k', fontweight='bold')
    plt.xlabel('k (number of neighbors)')
    plt.ylabel('Precision (%)')
    plt.grid(True)
    plt.savefig('precision_vs_k.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Plot saved as precision_vs_k.png")

    # 7) Choose best k by max F1
    best_idx = int(np.argmax(f1s))
    best_k = ks[best_idx]
    best_p = precisions[best_idx]
    best_f = f1s[best_idx]
    print(f"\nBest k={best_k} -> Precision={best_p*100:.2f}%, F1={best_f*100:.2f}%")

    # 8) Require minimum F1
    if best_f < 0.92:
        print("Error: validation F1 < 92%. Please adjust k or features.")
        sys.exit(1)

    # 9) Train final model on full train set and predict test
    final_pipe = Pipeline([
        ('scaler', MinMaxScaler()),
        ('knn', KNeighborsClassifier(n_neighbors=best_k, weights='distance'))
    ])
    final_pipe.fit(X, y)
    y_test_pred = final_pipe.predict(X_test)

    # 10) Save predictions
    with open('KNN.txt', 'w') as f:
        for label in y_test_pred:
            f.write(f"{label}\n")
    print("Predictions saved to KNN.txt")
    print(f"Done! Your KNN predictions with k={best_k} are in KNN.txt.")


if __name__ == '__main__':
    main()




