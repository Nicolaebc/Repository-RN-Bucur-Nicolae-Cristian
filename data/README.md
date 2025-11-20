### Descrierea Setului de Date

## Sursa datelor

* **Origine:** Se simuleaza pe baza unei intersectii reale o macheta virtuala in LabView simplificata la nivel de baza.
* **Modul de achiziție:** Simulare in LabView.
* **Condițiile colectării:** Se colecteaza datele pe baza a scenarii specifice si a fluiditatii traficului.

## Caracteristicile dataset-ului

* **Număr total de observații:** Dupa 1000 de observatii programul poate deja sa inceapa sa isi realizeze rolul.
* **Număr de caracteristici (features):** 3.
* **Tipuri de date:** Numerice/Temporale
* **Format fișiere:** VI/TXT.

## Descrierea fiecărei caracteristici

| **Caracteristică** | **Tip** | **Unitate**   | **Descriere**             | **Domeniu valori** |
|--------------------|---------|---------------|---------------------------|--------------------|
| feature_1/pietoni  | numeric | densitate/m^2 | numarul de pietoni pe m^2 | 0–150              |
| feature_2/vehicule | numeric | km/h          | viteza soferilor          | 0-75               |
| feature_3/veh_urg  | numeric | km/h          | viteza veh de urgenta     | 0–10               |
