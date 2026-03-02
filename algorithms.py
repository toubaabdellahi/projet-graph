from __future__ import annotations
import heapq
from typing import Dict, List, Tuple, Optional, Set
from graph import Graph, Edge


# =========================
# BFS / DFS
# =========================
def bfs_order(g: Graph, start: str) -> List[str]:
    """
    Parcours en largeur (BFS) depuis un sommet de départ.

    Args:
        g: Le graphe à parcourir.
        start: Sommet de départ.

    Returns:
        Liste des sommets visités dans l'ordre BFS.
    """
    if start not in g.adj:
        return []
    visited: Set[str] = {start}
    queue: List[str] = [start]
    order: List[str] = []

    while queue:
        u = queue.pop(0)
        order.append(u)
        for v, _ in g.neighbors(u):
            if v not in visited:
                visited.add(v)
                queue.append(v)
    return order


def dfs_order(g: Graph, start: str) -> List[str]:
    """
    Parcours en profondeur (DFS) depuis un sommet de départ.

    Args:
        g: Le graphe à parcourir.
        start: Sommet de départ.

    Returns:
        Liste des sommets visités dans l'ordre DFS.
    """
    if start not in g.adj:
        return []
    visited: Set[str] = set()
    order: List[str] = []

    def dfs(u: str):
        visited.add(u)
        order.append(u)
        for v, _ in g.neighbors(u):
            if v not in visited:
                dfs(v)

    dfs(start)
    return order


def is_connected(g: Graph) -> bool:
    """
    Vérifie si le graphe est connexe (tous les sommets sont atteignables).

    Returns:
        True si le graphe est connexe, False sinon.
    """
    nodes = g.nodes()
    if not nodes:
        return True
    return len(bfs_order(g, nodes[0])) == len(nodes)


def reachable_from(g: Graph, start: str) -> Set[str]:
    """
    Retourne l'ensemble des sommets atteignables depuis un sommet donné.

    Args:
        g: Le graphe.
        start: Sommet de départ.

    Returns:
        Ensemble des sommets accessibles depuis start.
    """
    return set(bfs_order(g, start))


# =========================
# DIJKSTRA
# =========================
def dijkstra(g: Graph, source: str) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
    """
    Algorithme de Dijkstra : calcule les distances minimales depuis une source.

    Fonctionne sur des graphes à poids positifs.
    Utilise une file de priorité (tas min) pour une complexité O((V + E) log V).

    Args:
        g: Le graphe pondéré.
        source: Sommet de départ.

    Returns:
        dist: Dictionnaire {sommet: distance minimale depuis source}.
        prev: Dictionnaire {sommet: prédécesseur sur le chemin optimal}.
    """
    dist: Dict[str, float] = {v: float("inf") for v in g.nodes()}
    prev: Dict[str, Optional[str]] = {v: None for v in g.nodes()}

    if source not in g.adj:
        return dist, prev

    dist[source] = 0.0
    pq = [(0.0, source)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in g.neighbors(u):
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))

    return dist, prev


def reconstruct_path(prev: Dict[str, Optional[str]], start: str, end: str) -> List[str]:
    """
    Reconstruit le chemin optimal à partir du dictionnaire des prédécesseurs.

    Args:
        prev: Dictionnaire des prédécesseurs (produit par dijkstra).
        start: Sommet de départ.
        end: Sommet d'arrivée.

    Returns:
        Liste des sommets formant le chemin de start à end. Liste vide si aucun chemin.
    """
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        if cur == start:
            break
        cur = prev[cur]
    path.reverse()
    return path if path and path[0] == start else []


def shortest_path(g: Graph, start: str, end: str) -> Tuple[List[str], float]:
    """
    Calcule le chemin le plus court entre deux sommets via Dijkstra.

    Args:
        g: Le graphe pondéré.
        start: Sommet de départ.
        end: Sommet d'arrivée.

    Returns:
        Tuple (chemin, coût). Le chemin est une liste de sommets.
        Retourne ([], inf) si aucun chemin n'existe.
    """
    dist, prev = dijkstra(g, start)
    # FIX: utiliser .get() pour éviter un KeyError si end n'est pas dans dist
    cost = dist.get(end, float("inf"))
    path = reconstruct_path(prev, start, end)
    return path, cost


# =========================
# MST - PRIM
# =========================
def mst_prim(g: Graph, start: Optional[str] = None) -> Tuple[List[Edge], float]:
    """
    Algorithme de Prim : construit un arbre couvrant minimal (MST).

    Principe : part d'un sommet et étend l'arbre en ajoutant à chaque étape
    l'arête de poids minimal reliant un sommet visité à un sommet non visité.
    Complexité : O(E log V) avec un tas min.

    Args:
        g: Le graphe non orienté pondéré.
        start: Sommet de départ (optionnel, premier sommet par défaut).

    Returns:
        Tuple (liste des arêtes du MST, coût total).

    Raises:
        ValueError: Si le graphe est orienté.
    """
    if g.directed:
        raise ValueError("Prim nécessite un graphe non orienté")

    nodes = g.nodes()
    if not nodes:
        return [], 0.0

    if start is None:
        start = nodes[0]

    visited = {start}
    edges = []
    total = 0.0
    pq = []

    for v, w in g.neighbors(start):
        heapq.heappush(pq, (w, start, v))

    while pq and len(visited) < len(nodes):
        w, u, v = heapq.heappop(pq)
        if v in visited:
            continue
        visited.add(v)
        edges.append(Edge(u, v, w))
        total += w
        for x, wx in g.neighbors(v):
            if x not in visited:
                heapq.heappush(pq, (wx, v, x))

    return edges, total


# =========================
# MST - KRUSKAL
# =========================
class DSU:
    """
    Structure Union-Find (Disjoint Set Union) avec compression de chemin et union par rang.

    Utilisée par Kruskal pour détecter les cycles efficacement.
    Complexité quasi-linéaire grâce aux deux optimisations.
    """

    def __init__(self, nodes: List[str]):
        """
        Args:
            nodes: Liste de tous les sommets du graphe.
        """
        self.parent = {n: n for n in nodes}
        self.rank = {n: 0 for n in nodes}  # union par rang pour équilibrer l'arbre

    def find(self, x: str) -> str:
        """Trouve la racine de x avec compression de chemin."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # compression de chemin
        return self.parent[x]

    def union(self, a: str, b: str) -> bool:
        """
        Fusionne les ensembles de a et b. Utilise l'union par rang.

        Returns:
            True si a et b étaient dans des ensembles différents (arête utile),
            False s'ils étaient déjà connectés (formerait un cycle).
        """
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        # Union par rang : on attache l'arbre de rang inférieur sous celui de rang supérieur
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


def mst_kruskal(g: Graph) -> Tuple[List[Edge], float]:
    """
    Algorithme de Kruskal : construit un arbre couvrant minimal (MST).

    Principe : trie toutes les arêtes par poids croissant et ajoute chaque arête
    si elle ne crée pas de cycle (vérifié via DSU).
    Complexité : O(E log E) dominée par le tri.

    Args:
        g: Le graphe non orienté pondéré.

    Returns:
        Tuple (liste des arêtes du MST, coût total).

    Raises:
        ValueError: Si le graphe est orienté.
    """
    if g.directed:
        raise ValueError("Kruskal nécessite un graphe non orienté")

    edges = sorted(g.edges(), key=lambda e: e.w)
    dsu = DSU(g.nodes())
    mst = []
    total = 0.0

    for e in edges:
        if dsu.union(e.u, e.v):
            mst.append(e)
            total += e.w

    return mst, total
