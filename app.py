from __future__ import annotations

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

from datasets import sample_transport_graph, random_transport_graph
from algorithms import bfs_order, dfs_order, shortest_path, mst_prim, mst_kruskal
from graph import Graph, Edge


# ----------------------------
# Helpers
# ----------------------------
def to_networkx(g: Graph) -> nx.Graph:
    G = nx.Graph() if not g.directed else nx.DiGraph()
    for u in g.nodes():
        G.add_node(u)
    for e in g.edges():
        G.add_edge(e.u, e.v, weight=e.w)
    return G


def edges_from_path(path: list[str]) -> set[tuple[str, str]]:
    s = set()
    for i in range(len(path) - 1):
        a, b = path[i], path[i + 1]
        s.add(tuple(sorted((a, b))))
    return s


def edges_from_edge_list(edge_list: list[Edge]) -> set[tuple[str, str]]:
    return {tuple(sorted((e.u, e.v))) for e in edge_list}


def draw_graph(G: nx.Graph, highlight_edges: set[tuple[str, str]] | None = None, title: str = ""):
    highlight_edges = highlight_edges or set()

    pos = nx.spring_layout(G, seed=7)  # layout stable
    fig = plt.figure(figsize=(9, 6))
    ax = plt.gca()
    ax.set_title(title)

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=900, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=9, ax=ax)

    # edges normal vs highlighted
    normal = []
    high = []
    for (u, v) in G.edges():
        key = tuple(sorted((u, v)))
        if key in highlight_edges:
            high.append((u, v))
        else:
            normal.append((u, v))

    nx.draw_networkx_edges(G, pos, edgelist=normal, width=1.5, ax=ax)
    if high:
        nx.draw_networkx_edges(G, pos, edgelist=high, width=4.0, ax=ax)

    # edge labels (weights)
    labels = {(u, v): f"{G[u][v].get('weight', '')}" for (u, v) in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8, ax=ax)

    ax.axis("off")
    st.pyplot(fig)
    plt.close(fig)


# ----------------------------
# UI
# ----------------------------
st.set_page_config(page_title="Transport Graph Visual Tester", layout="wide")
st.title("🚍 Sujet 1 — Réseau de transport (Visual Tester)")

with st.sidebar:
    st.header("Graphe")
    mode = st.selectbox("Choisir un graphe", ["Exemple (villes)", "Aléatoire"])

    if mode == "Aléatoire":
        n = st.slider("Nombre de sommets (n)", 5, 30, 12)
        density = st.slider("Densité (probabilité d'arête)", 0.05, 0.8, 0.2)
        seed = st.number_input("Seed", value=7, step=1)
        g = random_transport_graph(n=int(n), density=float(density), seed=int(seed))
    else:
        g = sample_transport_graph()

    st.divider()
    st.header("Opérations")
    op = st.radio(
        "Choisir une opération",
        ["Vue normale", "BFS / DFS", "Dijkstra (plus court chemin)", "MST (Prim)", "MST (Kruskal)"],
    )

Gnx = to_networkx(g)
nodes = sorted(g.nodes())

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("🔎 Paramètres")
    if nodes:
        start = st.selectbox("Sommet de départ", nodes, index=0)
        target = st.selectbox("Sommet d'arrivée (Dijkstra)", nodes, index=min(1, len(nodes) - 1))
    else:
        start, target = "", ""

    st.subheader("📊 Résultats")
    if op == "BFS / DFS":
        bfs = bfs_order(g, start)
        dfs = dfs_order(g, start)
        st.write("**Connexe ?**", len(set(bfs)) == len(nodes))
        st.write("**BFS ordre visite :**", bfs)
        st.write("**DFS ordre visite :**", dfs)

    elif op == "Dijkstra (plus court chemin)":
        path, cost = shortest_path(g, start, target)
        if path:
            st.success(f"Chemin optimal: {' -> '.join(path)}")
            st.write("**Coût total :**", cost)
        else:
            st.error("Aucun chemin trouvé entre ces deux sommets.")

    elif op == "MST (Prim)":
        mst_edges, total = mst_prim(g, start=start)
        st.write("**Coût total MST (Prim) :**", total)
        st.write("**Arêtes :**")
        for e in mst_edges:
            st.write(f"- {e.u} — {e.v} (w={e.w})")

    elif op == "MST (Kruskal)":
        mst_edges, total = mst_kruskal(g)
        st.write("**Coût total MST (Kruskal) :**", total)
        st.write("**Arêtes :**")
        for e in mst_edges:
            st.write(f"- {e.u} — {e.v} (w={e.w})")
    else:
        st.write("Choisis une opération à gauche pour voir les résultats.")

with col2:
    st.subheader("🗺️ Visualisation du graphe")

    highlight = set()
    title = "Graphe (vue normale)"

    if op == "Dijkstra (plus court chemin)":
        path, cost = shortest_path(g, start, target)
        highlight = edges_from_path(path)
        title = f"Dijkstra — chemin optimal ({start} → {target})"

    elif op == "MST (Prim)":
        mst_edges, total = mst_prim(g, start=start)
        highlight = edges_from_edge_list(mst_edges)
        title = "MST (Prim) — arêtes surlignées"

    elif op == "MST (Kruskal)":
        mst_edges, total = mst_kruskal(g)
        highlight = edges_from_edge_list(mst_edges)
        title = "MST (Kruskal) — arêtes surlignées"

    elif op == "BFS / DFS":
        title = "BFS / DFS — vue du graphe (ordre affiché à gauche)"

    draw_graph(Gnx, highlight_edges=highlight, title=title)

st.caption("Astuce: si la disposition change trop, relance avec le même seed (layout stable).")