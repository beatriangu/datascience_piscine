#!/usr/bin/env python3
import sys
import os
import pandas as pd
from sklearn.model_selection import train_test_split

# ─── Constants ─────────────────────────────────────────────────────────────────
TRAIN_OUT = "Train_knight.csv"
TEST_OUT = "Test_knight.csv"
TRUTH_OUT = "truth.txt"
SPLIT_RATIO = 0.2  # 20% para test/validation

# ─── Main ──────────────────────────────────────────────────────────────────────
def main():
    # 1. Cargar datos originales
    input_arg = sys.argv[1] if len(sys.argv) > 1 else None
    df = pd.read_csv(input_arg) if input_arg else pd.read_csv("../ex00/Train_knight.csv")
    
    # 2. Split estratificado (mantiene proporción Jedi/Sith)
    train, test = train_test_split(
        df,
        test_size=SPLIT_RATIO,
        stratify=df['knight'],  # <- Clave para balance de clases
        random_state=42
    )
    
    # 3. Guardar archivos con nombres consistentes
    train.to_csv(TRAIN_OUT, index=False)
    test.to_csv(TEST_OUT, index=False)
    
    # 4. Generar truth.txt desde el test set
    test['knight'].to_csv(TRUTH_OUT, index=False, header=False)
    
    # 5. Verificación final
    print(f"✅ {TRAIN_OUT}: {len(train)} muestras")
    print(f"✅ {TEST_OUT}: {len(test)} muestras")
    print(f"✅ {TRUTH_OUT}: {len(test)} etiquetas")

if __name__ == "__main__":
    main()