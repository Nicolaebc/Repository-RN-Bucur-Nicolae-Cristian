# Proiect Retele Neuronale: Sistem Inteligent de Semaforizare Adaptiva

**Disciplina:** Retele Neuronale  
**Institutie:** POLITEHNICA Bucuresti – FIIR  
**Student:** BUCUR Nicolae-Cristian
**Grupa:** 633AB  
**Link Repository GitHub:** https://github.com/Nicolaebc/Repository-RN-Bucur-Nicolae-Cristian
**Stack Tehnologic:** Python
**Domeniul Industrial de Interes (DII):** Automatizare

---

### 9. Pregatire Date si Cerinte Nivel 1

**Set date:** 10.000 inregistrari generate integral (100% originale).
**Split:** 70% Train, 15% Validation, 15% Test.
**Metrici Test:**
- **Acuratete:** > 95% (Datorita naturii deterministe a simulatorului)
- **F1-score:** > 0.90

### Tabel Hiperparametri si Justificari

| **Hiperparametru** | **Valoare Aleasa** | **Justificare** |
|--------------------|-------------------|-----------------|
| **Learning rate** | 0.001 | Valoare standard pentru optimizerul Adam, asigura o convergenta rapida fara oscilatii majore. |
| **Batch size** | 32 | Compromis optim intre viteza de antrenare si stabilitatea gradientului pentru un dataset de 10.000 randuri. |
| **Number of epochs** | 20 | Suficient pentru ca loss-ul sa se stabilizeze (convergenta atinsa rapid pe date sintetice). |
| **Optimizer** | Adam | Cel mai versatil optimizer pentru date tabulare, gestioneaza automat rata de invatare. |
| **Loss function** | Sparse Categorical Crossentropy | Avem o problema de clasificare multi-clasa (3 clase: Urgenta, N-S, E-V) cu etichete intregi. |
| **Activation Hidden** | ReLU | Previne problema "vanishing gradient" si introduce non-linearitate eficienta. |
| **Activation Output** | Softmax | Obligatoriu pentru stratul final de clasificare, ne ofera probabilitatile pentru fiecare faza. |

---

### 10. Analiza Erori in Context Industrial (Nivel 2)

### Pe ce clase greseste cel mai mult modelul?
Modelul poate avea dificultati minore la granita dintre cele doua faze de verde (Clasa 1 vs Clasa 2) atunci cand traficul este aproape egal pe ambele axe (ex: 20 masini N-S vs 21 masini E-V).

### Ce caracteristici ale datelor cauzeaza erori?
Zgomotul in date (simulat prin variatii aleatoare) sau situatiile de "egalitate perfecta" unde decizia umana ar fi arbitrara. De asemenea, cazurile rare cu pietoni multi dar masini putine pot induce confuzie daca modelul a invatat sa prioritizeze doar masinile.

### Ce implicatii are pentru aplicatia industriala?
- **False Negative pe Urgenta (Clasa 0):** CRITIC. Daca modelul nu vede ambulanta, poate cauza accidente.
- **Confuzie N-S vs E-V:** ACCEPTABIL. Cel mult creste timpul de asteptare cu cateva secunde, dar nu pune vieti in pericol.

### Masuri corective propuse:
1.  **Class Weights:** Cresterea ponderii pentru Clasa 0 (Urgenta) in functia de Loss pentru a penaliza drastic orice eroare aici.
2.  **Augmentare:** Generarea mai multor scenarii de "trafic egal" pentru a invata modelul sa ia decizii mai ferme.
3.  **Failsafe Rule:** Implementarea unei reguli hard-coded: Daca probabilitatea predictiei e sub 60%, se pastreaza faza curenta sau se trece pe galben intermitent.

---

### 11. Verificare Consistenta cu State Machine

Antrenarea respecta fluxul definit in Etapa 4:

| **Stare din Etapa 4** | **Implementare in Etapa 5** |
|-----------------------|-----------------------------|
| `ACQUIRE_DATA` | Generatorul creeaza vectorul `[auto_NS, ..., sirena]` |
| `PREPROCESS` | Aplicare `StandardScaler` salvat in `config/preprocessing_params.pkl` |
| `RN_INFERENCE` | `model.predict()` folosind `trained_model.h5` |
| `DECISION` | Alegerea indexului cu probabilitatea maxima (argmax) |
| `DISPLAY` | Afisarea fazei in consola/UI |

---