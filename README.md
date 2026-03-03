# 🚍 Réseau de Transport — Analyse de Graphes

---

## 🌐 Demo en ligne

👉 **[Ouvrir l'application Streamlit](https://transport-graph.streamlit.app/)**

---

## 📌 Description

Ce projet modélise un **réseau de transport mauritanien** sous forme de graphe pondéré non orienté et applique les algorithmes fondamentaux vus en cours d'analyse de graphes :

- Parcours **BFS** et **DFS** avec analyse de connexité
- Plus court chemin via **Dijkstra**
- Arbre couvrant minimal via **Prim** et **Kruskal**

---

## 🗂️ Structure du projet

```
transport_project/
│
├── graph.py          # Structures de données (classe Graph, classe Edge)
├── algorithms.py     # BFS, DFS, Dijkstra, Prim, Kruskal, DSU
├── datasets.py       # Graphe mauritanien + générateur aléatoire
├── main.py           # Interface ligne de commande (CLI)
└── app.py            # Interface web interactive (Streamlit)
```

---

## ⚙️ Installation

# Installer les dépendances
pip install rich streamlit networkx matplotlib
```
---

## 🚀 Utilisation

### Interface Web (Streamlit)

```bash
streamlit run app.py
```

### Interface CLI

```bash
# Graphe exemple (villes mauritaniennes)
python main.py --mode sample --start Nouakchott --target Nema

# Graphe aléatoire
python main.py --mode random --n 15 --density 0.3 --seed 42
```

---

## 🔬 Algorithmes implémentés

| Algorithme | Fichier | Complexité |
|---|---|---|
| BFS | `algorithms.py` | O(V + E) |
| DFS | `algorithms.py` | O(V + E) |
| Dijkstra | `algorithms.py` | O((V+E) log V) |
| Prim (MST) | `algorithms.py` | O(E log V) |
| Kruskal (MST) | `algorithms.py` | O(E log E) |

---

## 🗺️ Graphe exemple — Villes mauritaniennes

| Ville A | Ville B | Distance (km) |
|---|---|---|
| Nouakchott | Rosso | 200 |
| Nouakchott | Atar | 450 |
| Nouakchott | Akjoujt | 250 |
| Akjoujt | Atar | 220 |
| Rosso | Kaedi | 150 |
| Kaedi | Kiffa | 330 |
| Kaedi | Aleg | 220 |
| Atar | Chinguetti | 90 |
| Kiffa | Nema | 380 |
| Aleg | Nouakchott | 250 |

**Résultat Dijkstra** — Chemin optimal Nouakchott → Nema :
```
Nouakchott → Rosso → Kaedi → Kiffa → Nema  (1060 km)
```

**Résultat MST** — Coût total du réseau minimal :
```
Prim   : 1840 km
Kruskal: 1840 km  ✓
```

---

