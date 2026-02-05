#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tree.py: Clasificador de Caballeros Jedi/Sith usando Random Forest
"""
import sys
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

# ─── Parámetros de Configuración ───────────────────────────────────────────────
PARAMS_MODELO = {
    'n_estimators': 100,
    'max_depth': 30,
    'min_samples_split': 2,
    'class_weight': {0: 1, 1: 6},
    'random_state': 42,
    'n_jobs': 1
}

PARAMS_VISUALIZACION = {
    'max_depth': 6,
    'fontsize': 10,
    'impurity': True,
    'proportion': True,
    'filled': True,
    'rounded': True,
    'feature_names': None,
    'class_names': ['Sith', 'Jedi']
}

# ─── Funciones Principales ─────────────────────────────────────────────────────
def cargar_datos(train_path, test_path):
    """Carga y valida los datasets de entrenamiento y prueba"""
    try:
        train_df = pd.read_csv(train_path)
        test_df = pd.read_csv(test_path)
        return train_df, test_df
    except Exception as e:
        raise ValueError(f"Error cargando datos: {str(e)}")

def entrenar_modelo(X_train, y_train):
    """Entrena el modelo Random Forest con parámetros optimizados"""
    modelo = RandomForestClassifier(**PARAMS_MODELO)
    modelo.fit(X_train, y_train)
    return modelo

def visualizar_arbol(estimador, params_vis):
    """Genera visualización detallada del árbol de decisión"""
    plt.figure(figsize=(60, 30), dpi=300)
    plot_tree(estimador,
             **params_vis)
    plt.title("Árbol de Decisión - Random Forest\n"
             f"Profundidad: {params_vis['max_depth']} niveles | "
             f"Peso Jedi: {PARAMS_MODELO['class_weight'][1]}x",
             fontsize=18,
             pad=20)
    plt.savefig('tree.png', bbox_inches='tight')
    plt.close()

def validar_modelo(y_true, y_pred):
    """Realiza validación final del modelo"""
    min_len = min(len(y_pred), len(y_true))
    f1 = f1_score(y_true[:min_len], y_pred[:min_len])
    
    print(f"\n{'='*40}")
    print(f"✅ F1-score: {f1:.4f}")
    print(f"🔵 Muestras validadas: {min_len}")
    print(f"🔴 Requisito mínimo: 0.9000")
    print(f"{'='*40}\n")
    
    return f1 >= 0.9

# ─── Ejecución Principal ──────────────────────────────────────────────────────
def main():
    # 1. Validación de argumentos
    if len(sys.argv) != 3:
        print("Uso: python3 Tree.py <Train_knight.csv> <Test_knight.csv>")
        sys.exit(1)

    try:
        # 2. Carga de datos
        train_df, test_df = cargar_datos(sys.argv[1], sys.argv[2])
        X_train = train_df.drop('knight', axis=1)
        y_train = train_df['knight'].map({'Jedi': 1, 'Sith': 0})
        X_test = test_df.drop('knight', axis=1, errors='ignore')

        # 3. Entrenamiento del modelo
        modelo = entrenar_modelo(X_train, y_train)
        
        # 4. Generación de predicciones
        y_pred = modelo.predict(X_test)
        with open('Tree.txt', 'w') as f:
            f.write("\n".join(['Jedi' if p == 1 else 'Sith' for p in y_pred]))

        # 5. Visualización del árbol
        PARAMS_VISUALIZACION['feature_names'] = X_train.columns.tolist()
        visualizar_arbol(modelo.estimators_[0], PARAMS_VISUALIZACION)
        # 6. Validación con truth.txt
        with open('truth.txt') as f:
            y_true = [1 if line.strip() == 'Jedi' else 0 for line in f]
        
        if not validar_modelo(y_true, y_pred):
            print("🔍 Acciones recomendadas:")
            print("- Aumentar 'class_weight' para Jedi")
            print("- Incrementar 'n_estimators'")
            print("- Verificar balance de clases en training data")
            sys.exit(1)
            
    except Exception as e:
        print(f"🚨 Error crítico: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()












