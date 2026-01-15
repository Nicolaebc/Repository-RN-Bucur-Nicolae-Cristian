import tensorflow as tf
import os

layers = tf.keras.layers
models = tf.keras.models

def build_traffic_model(input_shape=(9,)):
    """
    Construim 'creierul' retelei.
    Avem nevoie de 9 intrari: 4 pentru masini, 4 pentru pietoni si 1 pentru sirena.
    """
    model = models.Sequential([
        # Primul strat: primeste datele brute si incepe sa caute tipare simple
        layers.Dense(32, activation='relu', input_shape=input_shape),
        
        # Al doilea strat: rafinam informatia, ajuta la decizii mai nuantate
        layers.Dense(16, activation='relu'),
        
        # Ultimul strat (Decizia): Avem 3 variante posibile
        # 0 = Urgenta, 1 = Verde N-S, 2 = Verde E-V
        # Softmax ne da probabilitatea pentru fiecare (ex: 80% sa fie verde N-S)
        layers.Dense(3, activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

if __name__ == "__main__":
    # Cream modelul gol
    model_sia = build_traffic_model()
    
    # Vedem in consola cum arata structura (cate straturi, cati parametri)
    model_sia.summary()
    
    # Facem folderul daca nu exista si salvam arhitectura
    # E important sa il salvam acum ca sa fim siguri ca structura e buna
    if not os.path.exists('models'):
        os.makedirs('models')
        
    model_sia.save('models/untrained_model.h5')
    print("\n Gata! Am definit arhitectura si am salvat modelul gol in 'models/untrained_model.h5'")