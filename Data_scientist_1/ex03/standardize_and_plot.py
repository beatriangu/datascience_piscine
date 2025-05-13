#!/usr/bin/env python3

import os
import pandas as pd
import matplotlib.pyplot as plt

# Paths
BASE = os.path.dirname(__file__)
EX00 = os.path.normpath(os.path.join(BASE, '..', 'ex00'))
TRAIN_CSV = os.path.join(EX00, 'Train_knight.csv')
TEST_CSV  = os.path.join(EX00, 'Test_knight.csv')

# 1) Load data
df_train = pd.read_csv(TRAIN_CSV)
df_test  = pd.read_csv(TEST_CSV)

# 2) Map knight to numeric (only present in train)
df_train['knight'] = df_train['knight'].map({'Jedi':1,'Sith':0})
# If test had a knight column, drop it:
if 'knight' in df_test.columns:
    df_test = df_test.drop(columns='knight')

# 3) Identify feature columns
FEATURES = [c for c in df_train.columns if c != 'knight']

# 4) Compute means/stds on train
means = df_train[FEATURES].mean()
stds  = df_train[FEATURES].std(ddof=0)

# 5) Standardize
train_std = (df_train[FEATURES] - means) / stds
train_std['knight'] = df_train['knight']

test_std  = (df_test[FEATURES] - means) / stds
# No knight in test; if you want to plot both classes on test, skip color

# 6) Print standardized tables
print("=== TRAIN (standardized) ===")
print(train_std.head().round(2))
print("\n=== TEST (standardized) ===")
print(test_std.head().round(2))

# 7) Plot Empowered vs. Stims for Train
plt.figure()
for cls, col in [('Jedi','blue'), ('Sith','red')]:
    sub = train_std[train_std['knight'] == (1 if cls=='Jedi' else 0)]
    plt.scatter(sub['Empowered'], sub['Stims'], c=col, label=cls, alpha=0.6)
plt.xlabel('Empowered (std)')
plt.ylabel('Stims (std)')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(BASE, 'train_empowered_stims.png'))
plt.close()

# 8) Plot Empowered vs. Stims for Test (single color)
plt.figure()
plt.scatter(test_std['Empowered'], test_std['Stims'], c='green', alpha=0.6)
plt.xlabel('Empowered (std)')
plt.ylabel('Stims (std)')
plt.tight_layout()
plt.savefig(os.path.join(BASE, 'test_empowered_stims.png'))
plt.close()

print("\nPlots saved as train_empowered_stims.png and test_empowered_stims.png")






