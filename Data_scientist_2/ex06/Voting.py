#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Voting.py: Trains a VotingClassifier combining three models (Logistic Regression,
KNeighborsClassifier, RandomForestClassifier) on Train_knight.csv, evaluates
F1 on a validation split, predicts on Test_knight.csv, and writes Voting.txt.

Usage:
    python3 Voting.py <Train_knight.csv> <Test_knight.csv>

Arguments:
  1) Train_knight.csv   CSV with features + 'knight' label (Jedi/Sith)
  2) Test_knight.csv    CSV with features only

Outputs:
  - Voting.txt           Predictions (one per line: "Jedi" or "Sith")
  - Console: F1-score on validation and final confirmation

Requirements:
  - Validation F1 ≥ 0.94, otherwise abort
"""
import sys
import os
import numpy as np
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score


def main():
    # 1) Validate command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python3 Voting.py <Train_knight.csv> <Test_knight.csv>")
        sys.exit(1)
    train_csv, test_csv = sys.argv[1], sys.argv[2]

    # 2) Check that input files exist
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

    # 5) Define base estimators
    estimators = [
        ('lr', LogisticRegression(random_state=42, max_iter=1000)),
        ('knn', KNeighborsClassifier(n_neighbors=5, weights='distance')),
        ('rf', RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=1))
    ]
    # 6) Create VotingClassifier
    voting = VotingClassifier(
        estimators=estimators,
        voting='soft',
        n_jobs=1
    )

    # 7) Build pipeline with scaler + voting
    pipe = Pipeline([
        ('scaler', MinMaxScaler()),
        ('voting', voting)
    ])

    # 8) Train on training split and evaluate on validation
    pipe.fit(X_tr, y_tr)
    y_val_pred = pipe.predict(X_val)
    f1 = f1_score(y_val, y_val_pred, pos_label='Jedi')
    print(f"Validation F1-score: {f1*100:.2f}%")

    # 9) Check threshold
    if f1 < 0.94:
        print("Error: Validation F1 below 94% requirement.")
        sys.exit(1)

    # 10) Train on full training data and predict test
    pipe.fit(X, y)
    y_test_pred = pipe.predict(X_test)

    # 11) Save predictions
    with open('Voting.txt', 'w') as f:
        for lbl in y_test_pred:
            f.write(f"{lbl}\n")
    print("Predictions saved to Voting.txt")
    print("Done! Voting classifier predictions are in Voting.txt.")

if __name__ == '__main__':
    main()

