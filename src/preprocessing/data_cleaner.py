import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os

def preprocess_and_split():
    # Verificam intai daca avem fisierul cu date brute
    input_file = 'data/raw/trafic_complex_final.csv'
    if not os.path.exists(input_file):
        print("Eroare: Nu gasesc fisierul CSV! Ruleaza intai generator.py")
        return

    # 1. Incarcam datele
    print("Incarc datele si incep procesarea...")
    df = pd.read_csv(input_file)
    
    # Separam intrarile (X) de rezultatul dorit (y)
    # Scoatem 'timestamp' pentru ca ora exacta nu ajuta reteaua sa decida semaforul
    X = df.drop(['faza_decisa', 'timestamp'], axis=1)
    y = df['faza_decisa']

    # 2. Normalizare (Standardizare)
    # Asta e un pas critic pentru AI. Modelul invata greu daca unele numere sunt mici (0-1) si altele mari (50-100).
    # Le aducem pe toate la o scara comuna.
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Salvam "rigla" de masurare (scaler-ul) intr-un fisier
    # O sa avem nevoie de ea in aplicatia finala cand vin date reale, sa le transformam la fel.
    if not os.path.exists('config'):
        os.makedirs('config')
    joblib.dump(scaler, 'config/preprocessing_params.pkl')

    # 3. Impartirea datelor (Split) - Strategia 70% / 15% / 15%
    
    # Pasul A: Luam 70% pentru Antrenament (Materia de invatat)
    # Folosim stratify=y ca sa fim siguri ca pastram proportiile de urgente/trafic normal
    X_train, X_temp, y_train, y_temp = train_test_split(
        X_scaled, y, train_size=0.7, stratify=y, random_state=42
    )
    
    # Pasul B: Restul de 30% il impartim egal in doua
    # 15% Validare (Teste pe parcurs) si 15% Test (Examenul final)
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42
    )

    # 4. Salvarea fisierelor
    # Ne asiguram ca folderele exista
    for folder in ['data/train', 'data/validation', 'data/test']:
        if not os.path.exists(folder):
            os.makedirs(folder)

    # Scriem fisierele CSV curate
    pd.DataFrame(X_train).to_csv('data/train/X_train.csv', index=False)
    pd.DataFrame(y_train).to_csv('data/train/y_train.csv', index=False)
    
    pd.DataFrame(X_val).to_csv('data/validation/X_val.csv', index=False)
    pd.DataFrame(y_val).to_csv('data/validation/y_val.csv', index=False)
    
    pd.DataFrame(X_test).to_csv('data/test/X_test.csv', index=False)
    pd.DataFrame(y_test).to_csv('data/test/y_test.csv', index=False)

    print(" Succes! Datele au fost normalizate si impartite.")
    print(f" - Pentru antrenament: {len(X_train)} exemple")
    print(f" - Pentru validare:    {len(X_val)} exemple")
    print(f" - Pentru test final:  {len(X_test)} exemple")

if __name__ == "__main__":
    preprocess_and_split()