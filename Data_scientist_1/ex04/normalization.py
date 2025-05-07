#!/usr/bin/env python3
import sys
import csv
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# ─── Feature list ───────────────────────────────────────────────────────────────
FEATURES = [
    "Sensitivity","Hability","Strength","Power","Agility","Dexterity",
    "Awareness","Prescience","Reactivity","Midi-chlorien","Slash","Push",
    "Pull","Lightsaber","Survival","Repulse","Friendship","Blocking",
    "Deflection","Mass","Recovery","Evade","Stims","Sprint","Combo",
    "Delay","Attunement","Empowered","Burst","Grasping"
]

# ─── Locate ex00 ─────────────────────────────────────────────────────────────────
def find_ex00():
    base = Path(__file__).resolve().parent
    for cand in (base/"ex00", base.parent/"ex00"):
        if (cand/"Train_knight.csv").exists() and (cand/"Test_knight.csv").exists():
            return cand
    sys.exit("ERROR: ex00/ not found")

# ─── Load & clean ────────────────────────────────────────────────────────────────
def load_and_clean(path, has_knight):
    txt = path.open("r", encoding="utf-8").read(2048)
    try:
        sep = csv.Sniffer().sniff(txt, delimiters=[",",";"]).delimiter
    except csv.Error:
        sep = ","
    df = pd.read_csv(path, sep=sep)
    if has_knight:
        if "knight" not in df.columns:
            df = pd.read_csv(path, sep=sep, header=None,
                             names=FEATURES+["knight"], skiprows=1)
        df["knight"] = df["knight"].str.strip().map({"Jedi":1,"Sith":0})
    # ensure numeric + fill NaN with mean
    df[FEATURES] = df[FEATURES].apply(pd.to_numeric, errors="coerce")
    df[FEATURES] = df[FEATURES].fillna(df[FEATURES].mean())
    return df

# ─── Min–Max normalize using TRAIN only ─────────────────────────────────────────
def minmax(train, df):
    mins = train[FEATURES].min()
    maxs = train[FEATURES].max()
    norm = (df[FEATURES] - mins) / (maxs - mins)
    out = norm.copy()
    if "knight" in df:
        out["knight"] = df["knight"].astype(int)
    return out

# ─── Scatter & save ─────────────────────────────────────────────────────────────
def scatter_save(df, x, y, out_path, by_class):
    plt.figure(figsize=(6,4))
    if by_class:
        for cls,color in ((1,"blue"),(0,"red")):
            sub = df[df["knight"]==cls]
            plt.scatter(sub[x], sub[y], c=color, alpha=0.6,
                        label="Jedi" if cls==1 else "Sith")
        plt.legend(title="Class")
    else:
        plt.scatter(df[x], df[y], c="green", alpha=0.6, label="All")
        plt.legend()
    plt.xlabel(f"{x} (normalized)")
    plt.ylabel(f"{y} (normalized)")
    plt.title(f"{'Train' if by_class else 'Test'}: {x} vs {y}")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()

# ─── Main ──────────────────────────────────────────────────────────────────────
def main():
    ex00 = find_ex00()
    train = load_and_clean(ex00/"Train_knight.csv", has_knight=True)
    test  = load_and_clean(ex00/"Test_knight.csv",  has_knight=False)

# … [keep everything up to after normalization]
    train_norm = minmax(train, train)
    test_norm  = minmax(train, test)

    # ---- Print exactly first 3 rows in the requested truncated format ----
    first3 = FEATURES[:3]
    last3  = FEATURES[-3:]
    header_train = first3 + ["…"] + last3 + ["knight"]
    print("TRAIN (normalized) — first 3 rows:")
    print(" " + "  ".join(header_train))
    for _, row in train_norm.head(3).iterrows():
        vals = [f"{row[f]:>6.2f}" for f in first3] \
             + ["   …"] \
             + [f"{row[f]:>6.2f}" for f in last3] \
             + [f"{int(row['knight']):>6d}"]
        print(" " + "  ".join(vals))

    header_test = first3 + ["…"] + last3
    print("\nTEST (normalized) — first 3 rows:")
    print(" " + "  ".join(header_test))
    for _, row in test_norm.head(3).iterrows():
        vals = [f"{row[f]:>6.2f}" for f in first3] \
             + ["   …"] \
             + [f"{row[f]:>6.2f}" for f in last3]
        print(" " + "  ".join(vals))

    # … [rest of your plotting code unchanged]


    # ---- Save the four normalized scatter plots ----
    out = Path(__file__).parent
    scatter_save(train_norm, "Empowered", "Stims",
                 out/"normalized_train_stims_empowered.png", by_class=True)
    scatter_save(test_norm,  "Empowered", "Stims",
                 out/"normalized_test_stims_empowered.png", by_class=False)
    scatter_save(train_norm, "Push", "Deflection",
                 out/"normalized_train_deflection_push.png", by_class=True)
    scatter_save(test_norm,  "Push", "Deflection",
                 out/"normalized_test_deflection_push.png", by_class=False)

    print("\nSaved 4 normalized scatter plots in ex04/")

if __name__ == "__main__":
    main()




