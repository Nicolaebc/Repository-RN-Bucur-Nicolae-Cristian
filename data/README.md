### Descrierea Setului de Date

## Sursa datelor

* **Origine:** Se simuleaza pe baza unei intersectii reale o macheta virtuala in Python simplificata la nivel de baza.
* **Modul de achiziție:** Generare programatica.
* **Condițiile colectării:** Se colecteaza datele pe baza a scenarii specifice si a fluiditatii traficului.

## Caracteristicile dataset-ului

* **Număr total de observații:** Dupa 100-1000 de observatii programul poate deja sa inceapa sa isi realizeze rolul.
* **Număr de caracteristici (features):** 6.
* **Tipuri de date:** Numerice/Categoriale.
* **Format fișiere:** CSV.

## Descrierea fiecărei caracteristici

| **Caracteristică** | **Tip** | **Unitate**   | **Descriere**             | **Domeniu valori** |
|--------------------|---------|---------------|---------------------------|--------------------|
| numar_vehicule  | numeric | count | Număr vehicule detectate | 0–50|
| tip_vehicul | categorial | -          | Tip vehicul          | {autoturism, autobuz, bicicletă, ambulanță, poliție, pompieri}              |
| numar_pietoni  | numeric | count         | Număr pietoni detectați     | 0–30              |
| tip_pieton  | categorial | -         | Tip pieton     | {adult, copil, grup}       |
| vehicul_urgenta  | boolean | -         | Dacă există vehicul de urgență     | {True, False}             |
| semafor_output  | categorial | -         | Culoare semafor     | {roșu, galben, verde}              |
