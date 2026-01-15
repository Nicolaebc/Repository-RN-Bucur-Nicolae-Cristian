import os
import sys
import time
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# Configurare Cai
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
data_path = os.path.join(project_root, 'data')
models_path = os.path.join(project_root, 'models')
docs_path = os.path.join(project_root, 'docs')

# Creare foldere daca nu exista
os.makedirs(models_path, exist_ok=True)
os.makedirs(docs_path, exist_ok=True)

# Incarcare Date
def load_data():
    print("⏳ Incarcare date...")
    try:
        X_train = pd.read_csv(os.path.join(data_path, 'train', 'X_train.csv'))
        y_train = pd.read_csv(os.path.join(data_path, 'train', 'y_train.csv'))
        X_test = pd.read_csv(os.path.join(data_path, 'test', 'X_test.csv'))
        y_test = pd.read_csv(os.path.join(data_path, 'test', 'y_test.csv'))
        return X_train, y_train, X_test, y_test
    except FileNotFoundError:
        print("❌ Eroare: Nu am găsit fișierele CSV! Asigură-te că ai rulat generatorul și cleaner-ul.")
        sys.exit(1)

# Functie creare model flexibil
def build_model(input_shape, hidden_layers=[32, 16], learning_rate=0.001, dropout=0.0):
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.InputLayer(input_shape=(input_shape,)))
    
    for neurons in hidden_layers:
        model.add(tf.keras.layers.Dense(neurons, activation='relu'))
        if dropout > 0:
            model.add(tf.keras.layers.Dropout(dropout))
            
    model.add(tf.keras.layers.Dense(3, activation='softmax')) 
    
    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer,
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

#Definire Experimente (Cele 4 cerute)
experiments = [
    {
        "name": "Baseline (Etapa 5)",
        "layers": [32, 16],
        "lr": 0.001,
        "dropout": 0.0,
        "batch_size": 32
    },
    {
        "name": "Exp 1: Learning Rate Mic",
        "layers": [32, 16],
        "lr": 0.0001,
        "dropout": 0.0,
        "batch_size": 32
    },
    {
        "name": "Exp 2: Arhitectura Complexa",
        "layers": [64, 32, 16],
        "lr": 0.001,
        "dropout": 0.0,
        "batch_size": 32
    },
    {
        "name": "Exp 3: Regularizare & Batch",
        "layers": [64, 32],
        "lr": 0.001,
        "dropout": 0.2, # Dropout pentru a preveni overfitting
        "batch_size": 64
    }
]

# Rulare Experimente
X_train, y_train, X_test, y_test = load_data()
results = []
best_f1 = 0
best_model = None
best_exp_name = ""

print(f"\n🚀 Pornire 4 Experimente de Optimizare...\n")

for exp in experiments:
    print(f"--- Rulare: {exp['name']} ---")
    start_time = time.time()
    
    model = build_model(X_train.shape[1], exp['layers'], exp['lr'], exp['dropout'])
    
    # Callback pentru oprire rapida
    early_stop = tf.keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True)
    
    history = model.fit(
        X_train, y_train,
        epochs=30, # Maxim 30 epoci
        batch_size=exp['batch_size'],
        validation_split=0.15,
        callbacks=[early_stop],
        verbose=0 # Nu afisam toate liniile ca sa fie curat
    )
    
    # Evaluare
    y_pred_probs = model.predict(X_test, verbose=0)
    y_pred = np.argmax(y_pred_probs, axis=1)
    
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='macro')
    duration = time.time() - start_time
    
    results.append({
        "Exp#": exp['name'],
        "Accuracy": f"{acc:.4f}",
        "F1-score": f"{f1:.4f}",
        "Timp": f"{duration:.1f}s",
        "Observatii": f"Loss final: {history.history['loss'][-1]:.4f}"
    })
    
    print(f"   -> Rezultat: Acc={acc:.4f}, F1={f1:.4f}, Timp={duration:.1f}s")
    
    # Salvare cel mai bun model
    if f1 >= best_f1: 
        best_f1 = f1
        best_model = model
        best_exp_name = exp['name']

# Salvare Model Optimizat
if best_model is None:
    print("❌ Eroare: Nu s-a antrenat niciun model corect.")
    sys.exit(1)

print(f"\n Cel mai bun experiment: {best_exp_name}")
save_path = os.path.join(models_path, 'optimized_model.h5')
best_model.save(save_path)
print(f" Model optimizat salvat in: {save_path}")

# Generare Confusion Matrix
y_pred_best = np.argmax(best_model.predict(X_test, verbose=0), axis=1)
cm = confusion_matrix(y_test, y_pred_best)

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Urgenta', 'Verde N-S', 'Verde E-V'],
            yticklabels=['Urgenta', 'Verde N-S', 'Verde E-V'])
plt.xlabel('Predictie')
plt.ylabel('Adevarat')
plt.title(f'Confusion Matrix - {best_exp_name}')
cm_path = os.path.join(docs_path, 'confusion_matrix_optimized.png')
plt.savefig(cm_path)
print(f"✅ Confusion Matrix salvata in: {cm_path}")

# README
df_res = pd.DataFrame(results)
print(df_res.to_markdown(index=False))

# Analiza Erori (Top 5)
print("\n Analiza Erori (Exemple pentru README):")
errors = np.where(y_test.values.flatten() != y_pred_best)[0]
if len(errors) > 0:
    for i in errors[:5]: # Luam primele 5 erori
        true_lbl = y_test.values.flatten()[i]
        pred_lbl = y_pred_best[i]
        probs = best_model.predict(X_test.iloc[[i]], verbose=0)[0]
        confidence = np.max(probs)
        print(f"   - Index {i}: Adevarat={true_lbl}, Prez= {pred_lbl}, Conf={confidence:.2f}")
else:
    print("Modelul nu are erori pe setul de test.")