import pandas as pd
import numpy as np
import sqlite3
import os
from datetime import datetime

def initializare_db():
    # Ne conectam la baza de date locala.
    conn = sqlite3.connect('data/trafic_istoric.db')
    cursor = conn.cursor()
    
    # Facem tabelul daca nu exista. Aici tinem minte tot: masini, pietoni si ce a decis semaforul
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS istoric_intersectie (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            auto_N_S INTEGER, auto_S_N INTEGER,
            auto_E_V INTEGER, auto_V_E INTEGER,
            pietoni_N INTEGER, pietoni_S INTEGER,
            pietoni_E INTEGER, pietoni_V INTEGER,
            sirena_activa INTEGER,
            faza_decisa INTEGER
        )
    ''')
    conn.commit()
    return conn
def genereaza_si_salveaza(n=10000):
    # Verificam daca avem folderul pentru date, daca nu, il facem noi
    if not os.path.exists('data/raw'):
        os.makedirs('data/raw')
    conn = initializare_db()
    
    np.random.seed(42)
    
    # Generam datele random pentru simulare (scenarii posibile)
    data = {
        'timestamp': [datetime.now().isoformat() for _ in range(n)],
        'auto_N_S': np.random.randint(0, 50, n),
        'auto_S_N': np.random.randint(0, 50, n),
        'auto_E_V': np.random.randint(0, 50, n),
        'auto_V_E': np.random.randint(0, 50, n),
        'pietoni_N': np.random.randint(0, 20, n),
        'pietoni_S': np.random.randint(0, 20, n),
        'pietoni_E': np.random.randint(0, 20, n),
        'pietoni_V': np.random.randint(0, 20, n),
        'sirena_activa': np.random.choice([0, 1], n, p=[0.93, 0.07])
    }
    
    df = pd.DataFrame(data)
    
    # Aici e "creierul": stabilim regulile dupa care s-a mers pana acum
    def decide_faza(row):
        # Daca se aude sirena, oprim tot (Faza 0 - Urgenta)
        if row['sirena_activa'] == 1: return 0
        
        # Calculam aglomeratia. Pietonii conteaza putin mai mult (x1.5) la decizie
        presiune_NS = row['auto_N_S'] + row['auto_S_N'] + (row['pietoni_N'] + row['pietoni_S']) * 1.5
        presiune_EV = row['auto_E_V'] + row['auto_V_E'] + (row['pietoni_E'] + row['pietoni_V']) * 1.5
        PRAG_CRITIC = 40
        
        # Daca e coada prea mare pe E-V, le dam verde fortat
        if row['auto_E_V'] > PRAG_CRITIC or row['auto_V_E'] > PRAG_CRITIC: return 2
        # Altfel, dam verde partii mai aglomerate
        return 1 if presiune_NS >= presiune_EV else 2

    df['faza_decisa'] = df.apply(decide_faza, axis=1)
    # Salvam in baza de date SQLite
    df.to_sql('istoric_intersectie', conn, if_exists='replace', index=False)
    # Exportam si in CSV (ca sa avem datele pregatite pentru AI mai tarziu)
    df.to_csv('data/raw/trafic_complex_final.csv', index=False)
    conn.close()
    print(f"Am generat {n} inregistrari in baza de date")

if __name__ == "__main__":
    genereaza_si_salveaza()