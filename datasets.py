from __future__ import annotations
import random
from graph import Graph


def sample_transport_graph() -> Graph:
    """
    Graphe simple (fait à la main) pour tester.
    Poids = distance (km) par exemple.
    """
    g = Graph(directed=False)
    g.add_edge("Nouakchott", "Rosso", 200)
    g.add_edge("Nouakchott", "Atar", 450)
    g.add_edge("Nouakchott", "Akjoujt", 250)
    g.add_edge("Akjoujt", "Atar", 220)
    g.add_edge("Rosso", "Kaedi", 150)
    g.add_edge("Kaedi", "Kiffa", 330)
    g.add_edge("Atar", "Chinguetti", 90)
    g.add_edge("Kiffa", "Nema", 380)
    g.add_edge("Kaedi", "Aleg", 220)
    g.add_edge("Aleg", "Nouakchott", 250)
    return g


def random_transport_graph(
    n: int = 10,
    density: float = 0.25,
    wmin: int = 5,
    wmax: int = 100,
    seed: int = 42,
) -> Graph:
    """
    Génère un graphe aléatoire non orienté pondéré.
    density ~ probabilité d'avoir une arête entre 2 sommets.
    """
    random.seed(seed)
    g = Graph(directed=False)
    nodes = [f"V{i}" for i in range(n)]
    for v in nodes:
        g.add_node(v)

    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < density:
                w = random.randint(wmin, wmax)
                g.add_edge(nodes[i], nodes[j], w)

    return g