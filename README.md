# 📊 Projet : Simulation de Chute Libre & Modèle Épidémiologique SIR

Ce dépôt contient **deux mini-projets de simulation scientifique** regroupés dans le même rapport :

- 🪂 **Chute libre** : étude du mouvement d’un corps soumis à la gravité (avec ou sans frottements).
- 🦠 **Modèle SIR** : simulation de la propagation d’une épidémie à l’aide du modèle compartimental **SIR (Susceptible – Infectious – Recovered)**.

---

# 📁 1. Structure du dépôt

```
projet-simulation/
│
├── chute-libre/
│   ├── main_chute_libre.py
│   └── README.md
│
├── sir-model/
│   ├── main_sir.py
│   └── README.md
│
├── rapport/
│   └── rapport_simulation.pdf
│
└── README.md
```

*(Adapte les noms si ta structure est différente.)*

---

# 🎯 2. Objectifs pédagogiques

## 🪂 Simulation de chute libre

Objectifs :

- Rappeler les **lois du mouvement de Newton**
- Simuler le mouvement d’un objet sous l’effet de la **gravité**
- Implémenter une **simulation numérique**
- Visualiser l’évolution de :
  - la **position**
  - la **vitesse**
  
en fonction du temps.

---

## 🦠 Simulation du modèle SIR

Objectifs :

- Comprendre les **modèles compartimentaux en épidémiologie**
- Résoudre un **système d’équations différentielles**
- Étudier l’impact des paramètres :

| Paramètre | Description |
|-----------|-------------|
| β | taux de transmission |
| γ | taux de guérison |
| N | population totale |

---

# 🛠 3. Technologies utilisées

### Langage

- **Python**

### Bibliothèques principales

- `numpy`
- `matplotlib`
- `scipy` *(optionnel)*

### Outils

- VS Code / Cursor
- Git & GitHub

---

# ⚙️ 4. Installation

### 1️⃣ Cloner le dépôt

```bash
git clone https://github.com/<TON-UTILISATEUR>/<NOM-DU-REPO>.git
cd <NOM-DU-REPO>
```

### 2️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

---

# ▶️ 5. Utilisation

## 🪂 5.1 Simulation de chute libre

Depuis le dossier `chute-libre` :

```bash
python main_chute_libre.py
```

### Paramètres configurables

- Hauteur initiale `h0`
- Vitesse initiale `v0`
- Gravité `g`
- Coefficient de frottement (optionnel)

### Sorties

- Courbe **position vs temps**
- Courbe **vitesse vs temps**
- Temps total de chute
- Graphiques de simulation

---

## 🦠 5.2 Simulation du modèle SIR

Depuis le dossier `sir-model` :

```bash
python main_sir.py
```

### Paramètres configurables

| Paramètre | Description |
|-----------|-------------|
| N | Population totale |
| I₀ | Infectés initiaux |
| R₀ | Guéris initiaux |
| β | Taux de transmission |
| γ | Taux de guérison |
| t | Durée de simulation |

### Sorties

- Courbes :
```
S(t) : Susceptibles
I(t) : Infectés
R(t) : Guéris
```

- Pic épidémique
- Durée de l’épidémie
- Analyse des scénarios

---

# 📄 6. Rapport

Le rapport présent dans le dossier `rapport/` contient :

### Chute libre

- équations physiques
- hypothèses
- méthode numérique
- graphiques et interprétation

### Modèle SIR

- système d’équations différentielles
- explication des paramètres
- résultats et simulation
- limites du modèle

---

# 👨‍💻 7. Auteur

**Abdelouahab Kribaa**

- Licence d’Excellence : Mathématiques Appliquées & Intelligence Artificielle  
- Université Polydisciplinaire de Nador  
- Génie Informatique – EST Oujda  

---

# 📜 8. Licence

Licence **MIT**

Voir le fichier `LICENSE` pour plus d’informations.

---

⭐ Si ce projet vous aide, n'hésitez pas à **mettre une étoile sur le dépôt GitHub** !
