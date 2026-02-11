# Proiect Retele Neuronale: Sistem Inteligent de Semaforizare Adaptiva

**Disciplina:** Retele Neuronale  
**Institutie:** POLITEHNICA Bucuresti – FIIR  
**Student:** BUCUR Nicolae-Cristian
**Grupa:** 633AB  
**Link Repository GitHub:** https://github.com/Nicolaebc/Repository-RN-Bucur-Nicolae-Cristian
**Stack Tehnologic:** Python
**Domeniul Industrial de Interes (DII):** Automatizare

---

### 5. Tabelul Nevoie Reala

| **Nevoie reala concreta** | **Cum o rezolva SIA-ul vostru** | **Modul software responsabil** |
|---------------------------|--------------------------------|--------------------------------|
| Congestie in intersectii cauzata de timpi ficsi la semafor | Predictia fazei optime (Verde N-S sau E-V) bazata pe volumul real de trafic | Neural Network (`src/neural_network`) + UI |
| Prioritizarea vehiculelor de interventie (Ambulanta/Politie) | Detectarea semnalului acustic (sirena) si comutarea instanta pe rosu general | Preprocessing + Rule-based Logic in `src/app` |
| Monitorizarea fluxului de trafic pentru statistici urbane | Logarea datelor generate si a deciziilor luate in baza de date SQLite | Data Acquisition (`src/data_acquisition`) |

---

### 6. Contributia Originala la Setul de Date

**Total observatii finale:** 10.000 (100%)
**Observatii originale:** 10.000 (100%)

**Tipul contributiei:**
[X] Date generate prin simulare fizica
[ ] Date achizitionate cu senzori proprii
[ ] Etichetare/adnotare manuala
[ ] Date sintetice prin metode avansate

**Descriere detaliata:**
Am dezvoltat un simulator de trafic in Python (`src/data_acquisition/generator.py`) care modeleaza o intersectie cu 4 directii auto si 4 treceri de pietoni. Simulatorul nu genereaza doar numere aleatorii, ci foloseste o logica de tip "Expert System" pentru a eticheta corect datele (Target: faza_decisa).
Scenariile simulate includ: trafic normal, ore de varf (aglomeratie pe o singura axa) si situatii de urgenta (sirena activa).

**Locatia codului:** `src/data_acquisition/generator.py`
**Locatia datelor:** `data/raw/trafic_complex_final.csv`

---

### 7. Diagrama State Machine a Intregului Sistem

**Legenda State Machine:**

Am ales o arhitectura de tip **Monitorizare si Control in Timp Real** pentru ca intersectia necesita decizii rapide bazate pe starea curenta.

Starile principale sunt:
1.  **IDLE:** Starea de asteptare, sistemul verifica daca simularea este pornita.
2.  **GENERATE_TRAFFIC:** Simulatorul creeaza un nou scenariu (numar masini N-S/E-V, pietoni, sirena).
3.  **PREPROCESS:** Datele brute sunt standardizate folosind Scaler-ul antrenat (aducerea valorilor la intervale comparabile).
4.  **INFERENCE (RN):** Reteaua neuronala primeste vectorul de input (9 features) si prezice faza optima.
5.  **DECISION_LOGIC:** Se compara outputul RN cu regulile de siguranta (ex: daca sirena e activa, override la predictie).
6.  **UPDATE_UI:** Afisarea culorilor semaforului in interfata grafica.

Starea de **ERROR/FAILSAFE** este esentiala: in cazul in care datele de intrare sunt corupte sau modelul are o incertitudine mare, semaforul intra in modul intermitent galben pentru siguranta.

*(Nota: Diagrama vizuala state_machine.png se regaseste in folderul docs/)*

---

### 8. Scheletul Complet al celor 3 Module

| **Modul** | **Implementare** | **Stare Functionala** |
|-----------|------------------|-----------------------|
| **1. Data Acquisition** | `src/data_acquisition/generator.py` | **Functional:** Genereaza CSV cu 10.000 intrari si baza de date SQLite. |
| **2. Neural Network** | `src/neural_network/model.py` | **Definit:** Arhitectura Dense (3 straturi), input shape (9,), output (3, softmax). |
| **3. Web Service / UI** | `src/app/main.py` | **Functional:** Interfata Streamlit/Terminal care simuleaza traficul si afiseaza decizia. |

---