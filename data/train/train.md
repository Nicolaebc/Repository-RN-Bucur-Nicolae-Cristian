
import random
import pandas as pd

# Definim intrările sistemului
vehicule = ["autoturism", "autobuz", "bicicletă", "ambulanță", "poliție", "pompieri"]
pietoni = ["adult", "copil", "grup"]
semafoare = ["roșu", "galben", "verde"]

def genereaza_date_random(n=100):
    """
    Generează un set de date random pentru simularea traficului.
    n = numărul de observații (rânduri).
    """
    data = []
    for i in range(n):
        rand = {
            "numar_vehicule": random.randint(0, 50),
            "tip_vehicul": random.choice(vehicule),
            "numar_pietoni": random.randint(0, 30),
            "tip_pieton": random.choice(pietoni),
            "vehicul_urgenta": random.choice([True, False]),
            "semafor_output": random.choice(semafoare)
        }
        data.append(rand)
    return pd.DataFrame(data)

# Exemplu de rulare
if __name__ == "__main__":
    df = genereaza_date_random(20)  # generează 20 de rânduri
    print(df.head())                # afișează primele 5 rânduri
    # Salvează în CSV pentru etapa de preprocesare
    df.to_csv("data/raw/traffic.csv", index=False)
