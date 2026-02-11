import tensorflow as tf
import pandas as pd
import os
from sklearn.model_selection import train_test_split

layers = tf.keras.layers
models = tf.keras.models

def antreneaza_modelul():
    # Verificam intai daca avem datele brute
    fisier_date = 'data/raw/trafic_complex_final.csv'
    if not os.path.exists(fisier_date):
        print(f"Nu exista fisierul CSV, ruleaza intai generator.py!")
        return
    #Pregatim datele
    df = pd.read_csv(fisier_date)
    
    # Definim Intrarile (X): Totul in afara de Timestamp (nu ne ajuta) si Faza_decisa (asta vrem sa prezicem)
    X = df.drop(['timestamp', 'faza_decisa'], axis=1)
    
    # Definim Tinta (y): Doar coloana cu decizia corecta (0, 1 sau 2)
    y = df['faza_decisa']
    
    # Impartim datele
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    
    #Incarcam structura goala a modelului pe care am facut-o in pasul anterior
    try:
        model = tf.keras.models.load_model('models/untrained_model.h5', compile=False)
    except:
        print("Nu exista modelul gol, ruleaza intai model.py")
        return
    
    # Compilam modelul cu optimizatorul adam
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Procesul de invatare 
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=20,
        batch_size=32,
        verbose=1 
    )
    # Salvam modelul "absolvent"
    model.save('models/trained_model.h5')
    print("Modelul a fost antrenat si salvat in models/trained_model.h5")
    loss, acc = model.evaluate(X_val, y_val, verbose=0)
    print(f"Acuratete finala pe date noi: {acc*100:.2f}%")

if __name__ == "__main__":
    antreneaza_modelul()