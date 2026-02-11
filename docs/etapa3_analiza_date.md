# Proiect Retele Neuronale: Sistem Inteligent de Semaforizare Adaptiva

**Disciplina:** Retele Neuronale  
**Institutie:** POLITEHNICA Bucuresti – FIIR  
**Student:** BUCUR Nicolae-Cristian
**Grupa:** 633AB  
**Link Repository GitHub:** https://github.com/Nicolaebc/Repository-RN-Bucur-Nicolae-Cristian
**Stack Tehnologic:** Python
**Domeniul Industrial de Interes (DII):** Automatizare

---

## Descriere Etapa 3: Analiza si Pregatirea Setului de Date

In aceasta etapa, am generat, analizat si preprocesat setul de date necesar pentru antrenarea retelei neuronale. Scopul este crearea unui model capabil sa decida faza semaforului (Verde N-S / Verde E-V / Urgenta) bazandu-se pe fluxul de masini, pietoni si semnale acustice.

### 1. Structura Repository-ului

Proiectul este organizat modular, separand codul sursa (`src`) de date (`data`) si configuratii.

PROIECT RETELE NEURONALE/
├── config/
│   └── preprocessing_params.pkl   # Scaler standardizat salvat
├── data/
│   ├── raw/                       # Trafic_complex_final.csv
│   ├── train/                     # Date antrenare (X, y)
│   ├── validation/                # Date validare (X, y)
│   ├── test/                      # Date testare (X, y)
│   ├── processed/                 # (Rezervat procesari intermediare)
│   ├── trafic_istoric.db          # Baza de date SQLite (backup)
│   └── README.md                  # Documentatie specifica datelor
├── docs/                          # Documentatie proiect
├── models/
│   ├── untrained_model.h5         # Arhitectura initiala
│   └── trained_model.h5           # Modelul antrenat final
├── src/                           # Cod Sursa
│   ├── app/
│   │   └── main.py                # Interfata de simulare
│   ├── data_acquisition/
│   │   └── generator.py           # Script generare date sintetice
│   ├── neural_network/
│   │   ├── model.py               # Definire arhitectura (CNN/Dense)
│   │   └── train.py               # Script antrenare model
│   └── preprocessing/
│       └── data_cleaner.py        # Curatare si impartire date
└── README.md                      # Acest fisier

### 2. Descrierea Datelor (Features)

Datele au fost generate prin scriptul `src/data_acquisition/generator.py` si contin urmatorii parametri:

| Variabila | Tip | Descriere | Rol |
| :--- | :--- | :--- | :--- |
| **auto_N_S** / **S_N** | Numeric | Nr. masini pe axa Nord-Sud | Input |
| **auto_E_V** / **V_E** | Numeric | Nr. masini pe axa Est-Vest | Input |
| **pietoni_N/S/E/V** | Numeric | Nr. pietoni la cele 4 treceri | Input |
| **sirena_activa** | Binar (0/1)| Detectie ambulanta/politie | Input (Prioritar) |
| **faza_decisa** | Categorial | 0=Urgenta, 1=Verde NS, 2=Verde EV | **Target (Output)** |

### 3. Procesul de Transformare

Datele din folderele `train`, `test` si `validation` au trecut prin scriptul `src/preprocessing/data_cleaner.py`:

1.  **Standardizare:** Valorile numerice au fost scalate (media=0, deviatia=1) folosind parametrii salvati in `config/preprocessing_params.pkl`.
2.  **Stratificare:** Impartirea s-a facut pastrand proportia de urgente (sirene) in toate cele 3 seturi, pentru a evita ca modelul sa ignore cazurile rare.
3.  **Curatare:** S-a eliminat coloana `timestamp` deoarece nu este relevanta pentru logica de semaforizare imediata.

### 4. Statistici Volum

* **Total Inregistrari:** 10.000
* **Set Antrenare:** 7.000 (70%)
* **Set Validare:** 1.500 (15%)
* **Set Testare:** 1.500 (15%)
