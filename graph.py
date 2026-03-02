from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class Edge:
    """Représente une arête pondérée entre deux sommets u et v."""
    u: str
    v: str
    w: float


class Graph:
    """
    Graphe de transport pondéré représenté par liste d'adjacence.

    La liste d'adjacence est choisie car elle est efficace en mémoire
    pour les graphes creux (peu d'arêtes), typiques des réseaux de transport.

    Attributs:
        directed (bool): True si le graphe est orienté, False sinon.
        adj (dict): Dictionnaire associant chaque sommet à sa liste de
                    voisins sous forme de tuples (sommet, poids).

    Exemple:
        g = Graph(directed=False)
        g.add_edge("Nouakchott", "Atar", 450)
    """

    def __init__(self, directed: bool = False):
        """
        Initialise un graphe vide.

        Args:
            directed: Si True, le graphe est orienté. Par défaut non orienté.
        """
        self.directed = directed
        self.adj: Dict[str, List[Tuple[str, float]]] = {}

    def add_node(self, node: str) -> None:
        """
        Ajoute un sommet isolé au graphe s'il n'existe pas déjà.

        Args:
            node: Identifiant du sommet (ex: nom de ville).
        """
        if node not in self.adj:
            self.adj[node] = []

    def add_edge(self, u: str, v: str, w: float = 1.0) -> None:
        """
        Ajoute une arête (u, v) de poids w. Crée les sommets si nécessaire.
        Si le graphe est non orienté, l'arête (v, u) est aussi ajoutée.

        Args:
            u: Sommet source.
            v: Sommet destination.
            w: Poids de l'arête (distance km, coût, temps...). Par défaut 1.0.
        """
        self.add_node(u)
        self.add_node(v)
        self.adj[u].append((v, float(w)))
        if not self.directed:
            self.adj[v].append((u, float(w)))

    def nodes(self) -> List[str]:
        """Retourne la liste de tous les sommets du graphe."""
        return list(self.adj.keys())

    def neighbors(self, u: str) -> List[Tuple[str, float]]:
        """
        Retourne les voisins d'un sommet avec leurs poids.

        Args:
            u: Le sommet dont on veut les voisins.

        Returns:
            Liste de tuples (voisin, poids). Liste vide si le sommet est inconnu.
        """
        return self.adj.get(u, [])

    def edges(self) -> List[Edge]:
        """
        Retourne la liste de toutes les arêtes du graphe.
        Pour un graphe non orienté, chaque arête n'apparaît qu'une seule fois.

        Returns:
            Liste d'objets Edge(u, v, w).
        """
        seen = set()
        res: List[Edge] = []
        for u in self.adj:
            for v, w in self.adj[u]:
                if self.directed:
                    res.append(Edge(u, v, w))
                else:
                    key = tuple(sorted((u, v)))
                    if key not in seen:
                        seen.add(key)
                        res.append(Edge(u, v, w))
        return res

    def __repr__(self) -> str:
        return f"Graph(directed={self.directed}, V={len(self.adj)}, E={len(self.edges())})"
