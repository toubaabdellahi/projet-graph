from __future__ import annotations

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import rcParams

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

    rcParams['font.family'] = 'sans-serif'

    pos = nx.spring_layout(G, seed=7)
    fig, ax = plt.subplots(figsize=(9, 6))
    fig.patch.set_facecolor('#f8fafc')
    ax.set_facecolor('#f8fafc')
    ax.set_title(title, color='#1e293b', fontsize=13, fontweight='600', pad=14)

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=950, node_color='#2563eb', alpha=0.90, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=9, font_color='white', font_weight='bold', ax=ax)

    # edges normal vs highlighted
    normal = []
    high = []
    for (u, v) in G.edges():
        key = tuple(sorted((u, v)))
        if key in highlight_edges:
            high.append((u, v))
        else:
            normal.append((u, v))

    nx.draw_networkx_edges(G, pos, edgelist=normal, width=1.5, edge_color='#94a3b8', ax=ax)
    if high:
        nx.draw_networkx_edges(G, pos, edgelist=high, width=4.0, edge_color='#f97316', ax=ax, style='solid')

    # edge labels (weights)
    labels = {(u, v): f"{G[u][v].get('weight', '')}" for (u, v) in G.edges()}
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=labels, font_size=8,
        font_color='#475569',
        bbox=dict(boxstyle='round,pad=0.25', fc='#ffffff', ec='#e2e8f0', alpha=0.85),
        ax=ax
    )

    ax.axis("off")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# ----------------------------
# Page config & global CSS
# ----------------------------
st.set_page_config(page_title="Transport Graph Visual Tester", layout="wide", page_icon="🚍")

st.markdown("""
<style>
/* ---------- Google Font ---------- */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ---------- Global ---------- */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* ---------- App background ---------- */
.stApp {
    background: #f1f5f9;
    color: #1e293b;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e2e8f0;
    box-shadow: 2px 0 12px rgba(0,0,0,0.04);
}
section[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p {
    color: #334155 !important;
}
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.13em !important;
    text-transform: uppercase !important;
    color: #94a3b8 !important;
    margin-bottom: 0.5rem !important;
}

/* ---------- Selectbox / number input ---------- */
.stSelectbox > div > div,
.stNumberInput > div > div > input {
    background: #f8fafc !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
    color: #1e293b !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.stSelectbox > div > div:focus-within,
.stNumberInput > div > div > input:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
}

/* ---------- Slider ---------- */
.stSlider > div > div > div > div {
    background: #2563eb !important;
}

/* ---------- Radio buttons ---------- */
.stRadio label {
    color: #64748b !important;
    font-size: 0.9rem !important;
    padding: 6px 10px;
    border-radius: 6px;
    transition: color .2s, background .2s;
}
.stRadio label:hover {
    color: #1e293b !important;
    background: #f1f5f9;
}

/* ---------- Main title ---------- */
h1 {
    font-size: 1.9rem !important;
    font-weight: 700 !important;
    background: linear-gradient(120deg, #2563eb, #7c3aed);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem !important;
}

/* ---------- Section subheaders ---------- */
h2 {
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.13em !important;
    text-transform: uppercase !important;
    color: #94a3b8 !important;
    margin-bottom: 0.8rem !important;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 6px;
}

h3 {
    font-size: 1rem !important;
    font-weight: 600 !important;
    color: #1e293b !important;
}

/* ---------- Cards ---------- */
.result-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.75rem;
    transition: border-color .2s, box-shadow .2s;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.result-card:hover {
    border-color: #93c5fd;
    box-shadow: 0 4px 14px rgba(37,99,235,0.08);
}
.result-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.11em;
    text-transform: uppercase;
    color: #94a3b8;
    margin-bottom: 6px;
}
.result-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.88rem;
    color: #1e293b;
    word-break: break-all;
}

/* ---------- Badges ---------- */
.badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
}
.badge-green { background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; }
.badge-red   { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; }
.badge-blue  { background: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; }

/* ---------- Edge list ---------- */
.edge-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 6px 0;
    border-bottom: 1px solid #f1f5f9;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.83rem;
    color: #475569;
}
.edge-item:last-child { border-bottom: none; }
.edge-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #f97316;
    flex-shrink: 0;
}
.edge-weight {
    margin-left: auto;
    color: #2563eb;
    font-weight: 600;
}

/* ---------- Graph panel ---------- */
.graph-panel {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 1.2rem;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* ---------- Alerts ---------- */
.stAlert {
    border-radius: 10px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* ---------- Caption ---------- */
.stCaption {
    color: #94a3b8 !important;
    font-size: 0.75rem !important;
}

/* ---------- Divider ---------- */
hr {
    border-color: #e2e8f0 !important;
    margin: 1rem 0 !important;
}

/* ---------- Scrollbar ---------- */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #f1f5f9; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>
""", unsafe_allow_html=True)


# ----------------------------
# UI
# ----------------------------
st.markdown("""
<div style="display:flex; align-items:center; gap:12px; margin-bottom:4px;">
  <span style="font-size:2rem;">🚍</span>
  <div>
    <h1 style="margin:0;">Réseau de Transport</h1>
    <p style="color:#94a3b8; font-size:0.85rem; margin:0;">Visual Tester — Sujet 1</p>
  </div>
</div>
<hr style="margin-bottom:1.5rem;">
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## Graphe")
    mode = st.selectbox("Source", ["Exemple (villes)", "Aléatoire"])

    if mode == "Aléatoire":
        n = st.slider("Sommets (n)", 5, 30, 12)
        density = st.slider("Densité", 0.05, 0.8, 0.2)
        seed = st.number_input("Seed", value=7, step=1)
        g = random_transport_graph(n=int(n), density=float(density), seed=int(seed))
    else:
        g = sample_transport_graph()

    st.divider()
    st.markdown("## Opérations")
    op = st.radio(
        "",
        ["Vue normale", "BFS / DFS", "Dijkstra (plus court chemin)", "MST (Prim)", "MST (Kruskal)"],
        label_visibility="collapsed"
    )

Gnx = to_networkx(g)
nodes = sorted(g.nodes())

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### ⚙️ Paramètres")
    if nodes:
        start = st.selectbox("Sommet de départ", nodes, index=0)
        target = st.selectbox("Sommet d'arrivée (Dijkstra)", nodes, index=min(1, len(nodes) - 1))
    else:
        start, target = "", ""

    st.markdown("### 📊 Résultats")

    if op == "BFS / DFS":
        bfs = bfs_order(g, start)
        dfs = dfs_order(g, start)
        is_connected = len(set(bfs)) == len(nodes)
        badge_cls = "badge-green" if is_connected else "badge-red"
        badge_txt = "Connexe" if is_connected else "Non connexe"

        st.markdown(f"""
        <div class="result-card">
          <div class="result-label">Connectivité</div>
          <span class="badge {badge_cls}">{badge_txt}</span>
        </div>
        <div class="result-card">
          <div class="result-label">BFS — ordre de visite</div>
          <div class="result-value">{' → '.join(bfs)}</div>
        </div>
        <div class="result-card">
          <div class="result-label">DFS — ordre de visite</div>
          <div class="result-value">{' → '.join(dfs)}</div>
        </div>
        """, unsafe_allow_html=True)

    elif op == "Dijkstra (plus court chemin)":
        path, cost = shortest_path(g, start, target)
        if path:
            st.markdown(f"""
            <div class="result-card">
              <div class="result-label">Chemin optimal</div>
              <div class="result-value">{' → '.join(path)}</div>
            </div>
            <div class="result-card">
              <div class="result-label">Coût total</div>
              <div class="result-value" style="color:#f97316; font-size:1.4rem; font-weight:700;">{cost}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-card" style="border-color:#fecaca;">
              <div class="result-label" style="color:#dc2626;">Erreur</div>
              <div class="result-value" style="color:#ef4444;">Aucun chemin trouvé entre <b>{start}</b> et <b>{target}</b>.</div>
            </div>
            """, unsafe_allow_html=True)

    elif op in ["MST (Prim)", "MST (Kruskal)"]:
        if op == "MST (Prim)":
            mst_edges, total = mst_prim(g, start=start)
        else:
            mst_edges, total = mst_kruskal(g)

        edges_html = "".join(
            f'<div class="edge-item"><span class="edge-dot"></span>'
            f'<span>{e.u} — {e.v}</span>'
            f'<span class="edge-weight">w = {e.w}</span></div>'
            for e in mst_edges
        )
        st.markdown(f"""
        <div class="result-card">
          <div class="result-label">Coût total MST</div>
          <div class="result-value" style="color:#f97316; font-size:1.4rem; font-weight:700;">{total}</div>
        </div>
        <div class="result-card">
          <div class="result-label">Arêtes de l'arbre couvrant</div>
          <div style="margin-top:6px;">{edges_html}</div>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="result-card" style="border-color:#bfdbfe; text-align:center; padding:2rem; background:#eff6ff;">
          <div style="font-size:2rem; margin-bottom:8px;">👈</div>
          <div style="color:#64748b; font-size:0.88rem;">Sélectionne une opération dans la barre latérale pour voir les résultats.</div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("### 🗺️ Visualisation")

    highlight = set()
    title = "Graphe — vue normale"

    if op == "Dijkstra (plus court chemin)":
        path, cost = shortest_path(g, start, target)
        highlight = edges_from_path(path)
        title = f"Dijkstra — {start} → {target}"

    elif op == "MST (Prim)":
        mst_edges, total = mst_prim(g, start=start)
        highlight = edges_from_edge_list(mst_edges)
        title = "MST — Prim"

    elif op == "MST (Kruskal)":
        mst_edges, total = mst_kruskal(g)
        highlight = edges_from_edge_list(mst_edges)
        title = "MST — Kruskal"

    elif op == "BFS / DFS":
        title = "BFS / DFS — graphe"

    st.markdown('<div class="graph-panel">', unsafe_allow_html=True)
    draw_graph(Gnx, highlight_edges=highlight, title=title)
    st.markdown('</div>', unsafe_allow_html=True)

    if highlight:
        st.markdown("""
        <div style="display:flex; align-items:center; gap:8px; margin-top:10px; color:#94a3b8; font-size:0.78rem;">
          <span style="display:inline-block;width:24px;height:3px;background:#f97316;border-radius:2px;"></span>
          Arêtes surlignées = chemin / arbre sélectionné
        </div>
        """, unsafe_allow_html=True)
