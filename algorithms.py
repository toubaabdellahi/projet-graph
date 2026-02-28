# from __future__ import annotations
# import heapq
# from typing import Dict, List, Tuple, Optional, Set
# from graph import Graph, Edge


# # -------------------------
# # Parcours BFS / DFS
# # -------------------------
# def bfs_order(g: Graph, start: str) -> List[str]:
#     if start not in g.adj:
#         return []
#     visited: Set[str] = set([start])
#     queue: List[str] = [start]
#     order: List[str] = []

#     while queue:
#         u = queue.pop(0)
#         order.append(u)
#         for v, _w in g.neighbors(u):
#             if v not in visited:
#                 visited.add(v)
#                 queue.append(v)
#     return order


# def dfs_order(g: Graph, start: str) -> List[str]:
#     if start not in g.adj:
#         return []
#     visited: Set[str] = set()
#     order: List[str] = []

#     def rec(u: str) -> None:
#         visited.add(u)
#         order.append(u)
#         for v, _w in g.neighbors(u):
#             if v not in visited:
#                 rec(v)

#     rec(start)
#     return order


# def is_connected(g: Graph) -> bool:
#     nodes = g.nodes()
#     if not nodes:
#         return True
#     # Connexité (pour non orienté). Si orienté, on peut définir autrement.
#     start = nodes[0]
#     seen = set(bfs_order(g, start))
#     return len(seen) == len(nodes)


# def reachable_from(g: Graph, start: str) -> Set[str]:
#     return set(bfs_order(g, start))


# # -------------------------
# # Dijkstra (plus court chemin)
# # -------------------------
# def dijkstra(g: Graph, source: str) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
#     dist: Dict[str, float] = {node: float("inf") for node in g.nodes()}
#     prev: Dict[str, Optional[str]] = {node: None for node in g.nodes()}

#     if source not in g.adj:
#         return dist, prev

#     dist[source] = 0.0
#     pq: List[Tuple[float, str]] = [(0.0, source)]

#     while pq:
#         d, u = heapq.heappop(pq)
#         if d != dist[u]:
#             continue  # outdated
#         for v, w in g.neighbors(u):
#             nd = d + w
#             if nd < dist[v]:
#                 dist[v] = nd
#                 prev[v] = u
#                 heapq.heappush(pq, (nd, v))

#     return dist, prev


# def reconstruct_path(prev: Dict[str, Optional[str]], source: str, target: str) -> List[str]:
#     if source == target:
#         return [source]
#     if target not in prev:
#         return []
#     path: List[str] = []
#     cur: Optional[str] = target
#     while cur is not None:
#         path.append(cur)
#         if cur == source:
#             break
#         cur = prev[cur]
#     path.reverse()
#     if not path or path[0] != source:
#         return []
#     return path


# def shortest_path(g: Graph, source: str, target: str) -> Tuple[List[str], float]:
#     dist, prev = dijkstra(g, source)
#     path = reconstruct_path(prev, source, target)
#     return path, dist.get(target, float("inf"))


# # -------------------------
# # Arbre couvrant minimal (Prim)
# # -------------------------
# def mst_prim(g: Graph, start: Optional[str] = None) -> Tuple[List[Edge], float]:
#     if g.directed:
#         raise ValueError("Prim: MST généralement défini pour graphe non orienté.")
#     nodes = g.nodes()
#     if not nodes:
#         return [], 0.0

#     if start is None:
#         start = nodes[0]
#     if start not in g.adj:
#         return [], 0.0

#     visited: Set[str] = set([start])
#     pq: List[Tuple[float, str, str]] = []  # (w, u, v)
#     for v, w in g.neighbors(start):
#         heapq.heappush(pq, (w, start, v))

#     mst: List[Edge] = []
#     total = 0.0

#     while pq and len(visited) < len(nodes):
#         w, u, v = heapq.heappop(pq)
#         if v in visited:
#             continue
#         visited.add(v)
#         mst.append(Edge(u, v, w))
#         total += w
#         for nxt, w2 in g.neighbors(v):
#             if nxt not in visited:
#                 heapq.heappush(pq, (w2, v, nxt))

#     # Si pas connexe, Prim ne couvre qu’une composante
#     return mst, total


# # -------------------------
# # Arbre couvrant minimal (Kruskal)
# # -------------------------
# class DSU:
#     def __init__(self, items: List[str]):
#         self.parent = {x: x for x in items}
#         self.rank = {x: 0 for x in items}

#     def find(self, x: str) -> str:
#         while self.parent[x] != x:
#             self.parent[x] = self.parent[self.parent[x]]
#             x = self.parent[x]
#         return x

#     def union(self, a: str, b: str) -> bool:
#         ra, rb = self.find(a), self.find(b)
#         if ra == rb:
#             return False
#         if self.rank[ra] < self.rank[rb]:
#             ra, rb = rb, ra
#         self.parent[rb] = ra
#         if self.rank[ra] == self.rank[rb]:
#             self.rank[ra] += 1
#         return True


# def mst_kruskal(g: Graph) -> Tuple[List[Edge], float]:
#     if g.directed:
#         raise ValueError("Kruskal: MST généralement défini pour graphe non orienté.")

#     edges = sorted(g.edges(), key=lambda e: e.w)
#     dsu = DSU(g.nodes())

#     mst: List[Edge] = []
#     total = 0.0
#     for e in edges:
#         if dsu.union(e.u, e.v):
#             mst.append(e)
#             total += e.w

#     return mst, total

from __future__ import annotations
import heapq
from typing import Dict, List, Tuple, Optional, Set
from graph import Graph, Edge


# =========================
# BFS / DFS
# =========================
def bfs_order(g: Graph, start: str) -> List[str]:
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
    nodes = g.nodes()
    if not nodes:
        return True
    return len(bfs_order(g, nodes[0])) == len(nodes)


def reachable_from(g: Graph, start: str) -> Set[str]:
    return set(bfs_order(g, start))


# =========================
# DIJKSTRA
# =========================
def dijkstra(g: Graph, source: str):
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


def reconstruct_path(prev, start, end):
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        if cur == start:
            break
        cur = prev[cur]
    path.reverse()
    return path if path and path[0] == start else []


def shortest_path(g: Graph, start: str, end: str):
    dist, prev = dijkstra(g, start)
    return reconstruct_path(prev, start, end), dist[end]


# =========================
# MST - PRIM
# =========================
def mst_prim(g: Graph, start: Optional[str] = None):
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
    def __init__(self, nodes):
        self.parent = {n: n for n in nodes}

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        self.parent[rb] = ra
        return True


def mst_kruskal(g: Graph):
    edges = sorted(g.edges(), key=lambda e: e.w)
    dsu = DSU(g.nodes())
    mst = []
    total = 0.0

    for e in edges:
        if dsu.union(e.u, e.v):
            mst.append(e)
            total += e.w

    return mst, total