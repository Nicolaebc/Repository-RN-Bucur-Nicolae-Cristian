import tensorflow as tf
import pandas as pd
import os
from sklearn.model_selection import train_test_split

# Acces direct la module
layers = tf.keras.layers
models = tf.keras.models

def antreneaza_modelul():
    # Verificam intai daca avem datele brute
    fisier_date = 'data/raw/trafic_complex_final.csv'
    if not os.path.exists(fisier_date):
        print(f"Nu am gasit fisierul {fisier_date}. Ruleaza intai generator.py!")
        return

    # 1. Pregatim datele (Data Preprocessing)
    print("Incarc datele si le pregatesc...")
    df = pd.read_csv(fisier_date)
    
    # Definim Intrarile (X): Totul in afara de Timestamp (nu ne ajuta) si Faza_decisa (asta vrem sa prezicem)
    X = df.drop(['timestamp', 'faza_decisa'], axis=1)
    
    # Definim Tinta (y): Doar coloana cu decizia corecta (0, 1 sau 2)
    y = df['faza_decisa']

    # Impartim datele: 80% pentru antrenare (invatat), 20% pentru validare (testat la final)
    # E ca la scoala: manualul e pentru invatat, culegerea e pentru examen.
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # 2. Incarcam structura goala a modelului pe care am facut-o in pasul anterior
    print("Incarc arhitectura modelului...")
    try:
        model = tf.keras.models.load_model('models/untrained_model.h5', compile=False)
    except:
        print("Nu gasesc modelul gol. Ruleaza intai model_definition.py!")
        return

    # 3. Compilam modelul
    # Ii spunem cum sa invete (optimizer 'adam' e standardul de aur acum)
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    print("--- Incepem Antrenarea (Poate dura cateva secunde) ---")
    
    # 4. Procesul de invatare (Fitting)
    # epochs=20 inseamna ca trece prin toata materia de 20 de ori
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=20,
        batch_size=32,
        verbose=1 
    )

    # 5. Salvam modelul "absolvent"
    model.save('models/trained_model.h5')
    print("\n Gata! Modelul a invatat si a fost salvat ca 'models/trained_model.h5'")
    
    # Afisam cat de bine se descurca (acuratetea finala pe datele de test)
    loss, acc = model.evaluate(X_val, y_val, verbose=0)
    print(f"Acuratete finala pe date noi: {acc*100:.2f}%")

if __name__ == "__main__":
    antreneaza_modelul()