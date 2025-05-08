#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tree.py: Train a Random Forest Classifier (with hyperparameter tuning) on the hard-coded
Train_knight.csv and Validation_knight.csv, then predict and evaluate.

Usage:
    python3 Tree.py
(no arguments needed — paths are all hard-coded)

Outputs:
  - Tree.txt: one prediction per line (“Jedi” or “Sith”)
  - tree.png: graphical representation of one tree from the forest
  - Prints F1-score (binary, pos_label='Jedi'), must be ≥ 0.90
"""
import os
import sys
import pandas as pd

# Use non-interactive backend so the script never blocks on plt.show()
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import f1_score, make_scorer
from sklearn.tree import plot_tree

def main():
    # script_dir = .../Data_scientist_2/ex04
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # hard-coded paths (relative to script location)
    train_path = os.path.abspath(os.path.join(
        script_dir, '..', '..',
        'Data_scientist_1', 'ex05', 'Training_knight.csv'
    ))
    test_path = os.path.abspath(os.path.join(
        script_dir, '..', '..',
        'Data_scientist_1', 'ex05', 'Validation_knight.csv'
    ))
    truth_path = os.path.abspath(os.path.join(
        script_dir, '..', 'ex00', 'truth.txt'
    ))

    # verify files exist
    for p in (train_path, test_path, truth_path):
        if not os.path.isfile(p):
            print(f"Error: no se encontró el archivo: {p}")
            sys.exit(1)

    # load data
    train_df = pd.read_csv(train_path)
    test_df  = pd.read_csv(test_path)

    # prepare features / labels
    X_train = train_df.drop(columns=['knight'])
    y_train = train_df['knight']
    X_test = test_df.drop(columns=['knight'], errors='ignore')
    X_test = X_test.loc[:, X_train.columns]  # same column order

    # hyperparameter grid
    param_grid = {
        'n_estimators':    [100, 200],
        'max_depth':       [None, 5, 10],
        'min_samples_split':[2, 5],
        'min_samples_leaf': [1, 2],
        'class_weight':    [None, 'balanced']
    }
    # use f1_score with pos_label='Jedi'
    jedi_scorer = make_scorer(f1_score, pos_label='Jedi', average='binary')

    # grid search WITHOUT parallel workers to avoid child‐process errors
    grid = GridSearchCV(
        RandomForestClassifier(random_state=42),
        param_grid,
        scoring=jedi_scorer,
        cv=5,
        n_jobs=1,      # <- force single‐process execution
        verbose=1
    )
    grid.fit(X_train, y_train)
    clf = grid.best_estimator_
    print("Mejores parámetros:", grid.best_params_)

    # predict and write Tree.txt
    y_pred = clf.predict(X_test)
    with open('Tree.txt', 'w') as f:
        for lbl in y_pred:
            f.write(f"{lbl}\n")
    print("Predictions saved to Tree.txt")

    # plot one tree
    tree = clf.estimators_[0]
    plt.figure(figsize=(15, 10))
    plot_tree(
        tree,
        feature_names=X_train.columns,
        class_names=clf.classes_,
        filled=True,
        rounded=True,
        fontsize=8
    )
    plt.title("Decision tree trained in all Knight features")
    plt.tight_layout()
    plt.savefig('tree.png', bbox_inches='tight', pad_inches=0, dpi=500)
    plt.close()   # <- no plt.show(), script continues immediately
    print("Decision tree graph saved to tree.png")

    # evaluate F1
    with open(truth_path, 'r') as f:
        y_true = [line.strip() for line in f]
    y_true = y_true[:len(y_pred)]
    f1 = f1_score(y_true, y_pred, average='binary', pos_label='Jedi')
    print(f"F1-score (binary, pos_label='Jedi'): {f1:.4f}")
    if f1 < 0.90:
        print("Warning: F1-score is below 90% requirement.")
        sys.exit(1)

if __name__ == '__main__':
    main()










