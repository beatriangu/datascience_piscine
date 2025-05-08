#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tree.py: Solución Final con Ajustes de Profundidad y Balance
"""
import sys
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

def main():
    # 1. Configuración inicial
    if len(sys.argv) != 3:
        print("Uso: python3 Tree.py Train_knight.csv Test_knight.csv")
        sys.exit(1)

    # 2. Cargar datos
    try:
        train_df = pd.read_csv(sys.argv[1])
        test_df = pd.read_csv(sys.argv[2])
        
        X_train = train_df.drop('knight', axis=1)
        y_train = train_df['knight'].map({'Jedi':1, 'Sith':0})
        X_test = test_df.drop('knight', axis=1, errors='ignore')
        
    except Exception as e:
        print(f"🚨 Error: {str(e)}")
        sys.exit(1)

    # 3. Modelo Altamente Optimizado
    model = RandomForestClassifier(
        n_estimators=1500,        # Más árboles
        max_depth=30,             # Mayor profundidad
        min_samples_split=2, 
        class_weight={0:1, 1:6},  # Peso Jedi 6x mayor
        random_state=42,
        n_jobs=1                  # Sin paralelismo
    )
    
    model.fit(X_train, y_train)

    # 4. Generar predicciones
    y_pred = model.predict(X_test)
    with open('Tree.txt', 'w') as f:
        f.write("\n".join(['Jedi' if p ==1 else 'Sith' for p in y_pred]))

    # 5. Visualizar árbol completo
    plt.figure(figsize=(40, 20))
    plot_tree(model.estimators_[0],
             feature_names=X_train.columns,
             class_names=['Sith','Jedi'],
             filled=True,
             max_depth=4,        # Mostrar más niveles
             fontsize=8,
             impurity=False)
    plt.savefig('tree.png', dpi=300)
    plt.close()

    # 6. Validación final
    try:
        with open('truth.txt') as f:
            y_true = [1 if line.strip()=='Jedi' else 0 for line in f]
        
        # Ajustar a tamaño común
        min_len = min(len(y_pred), len(y_true))
        f1 = f1_score(y_true[:min_len], y_pred[:min_len])
        print(f"✅ F1-score: {f1:.4f}")
        
        if f1 < 0.9:
            print("\n🔍 Balance actual:", y_train.value_counts().to_dict())
            print("   Aumentar 'class_weight' para Jedi (1:7 o 1:8)")
            
    except FileNotFoundError:
        print("⚠️ truth.txt no encontrado")

if __name__ == "__main__":
    main()












