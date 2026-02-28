# from __future__ import annotations
# from dataclasses import dataclass
# from typing import Dict, List, Tuple, Iterable, Any


# @dataclass(frozen=True)
# class Edge:
#     u: str
#     v: str
#     w: float


# class Graph:
#     """
#     Graphe de transport: sommets = villes/stations, arêtes = routes/lignes
#     Représentation: liste d'adjacence
#     Non orienté par défaut (route dans les deux sens)
#     Pondéré (poids = distance/temps/coût)
#     """
#     def __init__(self, directed: bool = False):
#         self.directed = directed
#         self.adj: Dict[str, List[Tuple[str, float]]] = {}

#     def add_node(self, node: str) -> None:
#         if node not in self.adj:
#             self.adj[node] = []

#     def add_edge(self, u: str, v: str, w: float = 1.0) -> None:
#         self.add_node(u)
#         self.add_node(v)
#         self.adj[u].append((v, float(w)))
#         if not self.directed:
#             self.adj[v].append((u, float(w)))

#     def nodes(self) -> List[str]:
#         return list(self.adj.keys())

#     def neighbors(self, u: str) -> List[Tuple[str, float]]:
#         return self.adj.get(u, [])

#     def edges(self) -> List[Edge]:
#         # Pour éviter les doublons en non orienté
#         seen = set()
#         res: List[Edge] = []
#         for u in self.adj:
#             for v, w in self.adj[u]:
#                 if self.directed:
#                     res.append(Edge(u, v, w))
#                 else:
#                     key = tuple(sorted([u, v]))
#                     if key not in seen:
#                         seen.add(key)
#                         res.append(Edge(u, v, w))
#         return res

#     def __len__(self) -> int:
#         return len(self.adj)

#     def __repr__(self) -> str:
#         kind = "directed" if self.directed else "undirected"
#         return f"Graph({kind}, |V|={len(self.adj)}, |E|={len(self.edges())})"
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class Edge:
    u: str
    v: str
    w: float


class Graph:
    """
    Graphe de transport (non orienté, pondéré)
    Représentation par liste d'adjacence
    """

    def __init__(self, directed: bool = False):
        self.directed = directed
        self.adj: Dict[str, List[Tuple[str, float]]] = {}

    def add_node(self, node: str) -> None:
        if node not in self.adj:
            self.adj[node] = []

    def add_edge(self, u: str, v: str, w: float = 1.0) -> None:
        self.add_node(u)
        self.add_node(v)
        self.adj[u].append((v, float(w)))
        if not self.directed:
            self.adj[v].append((u, float(w)))

    def nodes(self) -> List[str]:
        return list(self.adj.keys())

    def neighbors(self, u: str) -> List[Tuple[str, float]]:
        return self.adj.get(u, [])

    def edges(self) -> List[Edge]:
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