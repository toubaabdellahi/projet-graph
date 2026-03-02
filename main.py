from __future__ import annotations
import argparse
from graph import Graph
from datasets import sample_transport_graph, random_transport_graph
from algorithms import (
    bfs_order, dfs_order, is_connected, reachable_from,
    shortest_path, mst_prim, mst_kruskal
)


def print_graph(g: Graph) -> None:
    print(g)
    for u in sorted(g.nodes()):
        neigh = ", ".join([f"{v}({w:g})" for v, w in g.neighbors(u)])
        print(f"  {u}: {neigh}")


def run_demo(g: Graph, start: str, target: str) -> None:
    print("\n====================")
    print("1) Graphe")
    print("====================")
    print_graph(g)

    print("\n====================")
    print("2) Connexité / Accessibilité")
    print("====================")
    print("Connexe ?", is_connected(g))
    print("BFS ordre visite :", bfs_order(g, start))
    print("DFS ordre visite :", dfs_order(g, start))
    print(f"Atteignables depuis {start} :", sorted(reachable_from(g, start)))

    print("\n====================")
    print("3) Plus court chemin (Dijkstra)")
    print("====================")
    path, cost = shortest_path(g, start, target)
    if path and cost != float("inf"):
        print(f"Chemin optimal {start} -> {target} :", " -> ".join(path))
        print("Coût total :", cost)
    elif not is_connected(g):
        print(f"⚠️ Aucun chemin trouvé : le graphe n'est pas connexe.")
        print(f"   '{target}' n'est pas accessible depuis '{start}'.")
    else:
        print(f"Aucun chemin trouvé entre {start} et {target}.")

    print("\n====================")
    print("4) Arbre couvrant minimal (MST)")
    print("====================")
    mst1, total1 = mst_prim(g, start=start)
    print("Prim - coût total :", total1)
    for e in mst1:
        print(f"  {e.u} -- {e.v}  (w={e.w:g})")

    mst2, total2 = mst_kruskal(g)
    print("\nKruskal - coût total :", total2)
    for e in mst2:
        print(f"  {e.u} -- {e.v}  (w={e.w:g})")

    if not is_connected(g):
        print("\n⚠️ Note: le graphe n'est pas connexe, donc MST ne couvre pas tout le graphe.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Sujet 1 - Réseau de transport (graphes)")
    parser.add_argument("--mode", choices=["sample", "random"], default="sample")
    parser.add_argument("--start", default="Nouakchott")
    parser.add_argument("--target", default="Nema")
    parser.add_argument("--n", type=int, default=10)
    parser.add_argument("--density", type=float, default=0.25)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if args.mode == "sample":
        g = sample_transport_graph()
    else:
        g = random_transport_graph(n=args.n, density=args.density, seed=args.seed)
        # Pour random, start/target doivent exister : V0..V(n-1)
        if args.start not in g.adj:
            args.start = "V0"
        if args.target not in g.adj:
            args.target = f"V{min(args.n - 1, 1)}"

    run_demo(g, args.start, args.target)


if __name__ == "__main__":
    main()