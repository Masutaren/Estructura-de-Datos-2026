"""
Grafos y Recursión — Carpeta Grafos
Exercises: Dijkstra, Prim, Kruskal, Torres de Hanoi
Draws graphs on tkinter Canvas (no external graph library needed).
"""
import tkinter as tk
import math
import os

import theme as th
from vistas._layout import make_exercise_view, make_nav_btn, make_ctrl_btn, load_code
from adaptadores.capture import path_for

GRF = path_for("Grafos")

EXERCISES = [
    ("Dijkstra — Camino Más Corto",    "Dijkstra"),
    ("Prim — Árbol Expansión Mínima",  "Prim"),
    ("Kruskal — Árbol Exp. Mínima",    "Kruskal"),
    ("Torres de Hanoi — Recursión",    "Hanoi"),
]

NODE_R = 24   # circle radius

# ─── Canvas graph drawing ─────────────────────────────────────────────────────

def scale_positions(pos_norm, cw, ch, margin=60):
    """Convert normalized [0,1] positions to canvas pixel positions."""
    result = {}
    for node, (nx, ny) in pos_norm.items():
        result[node] = (
            int(margin + nx * (cw - 2*margin)),
            int(margin + ny * (ch - 2*margin)),
        )
    return result


def draw_graph_canvas(canvas, nodes, edges, pos, node_colors, edge_colors,
                      edge_labels=None, info=""):
    """Draw a weighted graph on a tkinter Canvas."""
    canvas.delete("all")
    cw = canvas.winfo_width()  or 620
    ch = canvas.winfo_height() or 400
    px = scale_positions(pos, cw, ch)

    # Draw edges
    for (u, v), data in edges.items():
        weight = data.get("w", "")
        ux, uy = px[u]
        vx, vy = px[v]
        ec = edge_colors.get((u, v), edge_colors.get((v, u), th.BORDER))
        ew = 3 if ec in (th.ORANGE, th.PURPLE) else 1
        canvas.create_line(ux, uy, vx, vy, fill=ec, width=ew)

        # Weight label at midpoint
        mx = (ux + vx) // 2
        my = (uy + vy) // 2
        if weight != "":
            canvas.create_oval(mx-11, my-9, mx+11, my+9,
                               fill=th.SURFACE_BG, outline="")
            canvas.create_text(mx, my, text=str(weight),
                               font=("Segoe UI", 8), fill=th.YELLOW)

    # Draw nodes
    for node in nodes:
        x, y = px[node]
        fill = node_colors.get(node, th.ACCENT)
        canvas.create_oval(x-NODE_R, y-NODE_R, x+NODE_R, y+NODE_R,
                           fill=fill, outline=th.BG, width=2)
        canvas.create_text(x, y, text=str(node),
                           font=("Segoe UI", 10, "bold"), fill="white")

    # Info text
    if info:
        canvas.create_text(cw//2, ch-16, text=info,
                           font=th.FONT_BODY, fill=th.YELLOW)


# ─── Main view ────────────────────────────────────────────────────────────────

class GrafosView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=th.BG)
        self._ui = make_exercise_view(self)
        self._ui["root"].pack(fill=tk.BOTH, expand=True)

        self._nav_btns = []
        self._steps    = []
        self._step_idx = 0
        self._after_id = None
        self._draw_fn  = None

        self._build_nav()
        self._select(0)

    def _build_nav(self):
        for i, (label, _) in enumerate(EXERCISES):
            btn = make_nav_btn(self._ui["left"], label, lambda i=i: self._select(i))
            self._nav_btns.append(btn)

    def _select(self, idx):
        self._cancel_anim()
        for i, btn in enumerate(self._nav_btns):
            btn.configure(
                bg=th.PANEL_BG if i == idx else th.SIDEBAR_BG,
                fg=th.ACCENT  if i == idx else th.TEXT,
            )
        label, key = EXERCISES[idx]
        self._ui["title_lbl"].configure(text=label)
        load_code(self._ui["code_text"], os.path.join(GRF, key + ".py"))
        self._clear_viz()
        getattr(self, f"_setup_{key}")()

    def _clear_viz(self):
        for w in self._ui["viz_frame"].winfo_children():
            w.destroy()
        for w in self._ui["ctrl_frame"].winfo_children():
            w.destroy()
        self._steps = []; self._step_idx = 0

    def _cancel_anim(self):
        if self._after_id:
            self.after_cancel(self._after_id)
            self._after_id = None

    def _play(self):
        if self._step_idx >= len(self._steps):
            self._step_idx = 0
        self._animate()

    def _animate(self):
        if self._step_idx < len(self._steps):
            if self._draw_fn:
                self._draw_fn(self._steps[self._step_idx])
            self._step_idx += 1
            self._after_id = self.after(th.ANIM_SPEED, self._animate)

    def _do_step(self):
        self._cancel_anim()
        if self._step_idx < len(self._steps):
            if self._draw_fn:
                self._draw_fn(self._steps[self._step_idx])
            self._step_idx += 1

    def _reset_anim(self):
        self._cancel_anim()
        self._step_idx = 0
        if self._steps and self._draw_fn:
            self._draw_fn(self._steps[0])

    def _make_canvas(self):
        c = tk.Canvas(self._ui["viz_frame"], bg=th.BG, highlightthickness=0)
        c.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)
        return c

    def _make_controls(self):
        ctrl = self._ui["ctrl_frame"]
        make_ctrl_btn(ctrl, "▶  Iniciar",   self._play,       th.GREEN)
        make_ctrl_btn(ctrl, "⏭  Paso",      self._do_step,    th.ACCENT)
        make_ctrl_btn(ctrl, "↺  Reiniciar", self._reset_anim, th.YELLOW)
        self._step_lbl = tk.Label(ctrl, text="",
            font=th.FONT_SMALL, bg=th.SIDEBAR_BG, fg=th.TEXT_DIM)
        self._step_lbl.pack(side=tk.RIGHT, padx=12)

    # ── Shared graph data ─────────────────────────────────────────────────────

    def _dijkstra_kruskal_graph(self):
        graph = {
            "0": {"1": 9, "4": 6},
            "1": {"0": 9, "3": 8},
            "2": {"4": 5, "5": 6},
            "3": {"1": 8, "5": 1, "7": 7},
            "4": {"0": 6, "2": 5, "6": 3},
            "5": {"2": 6, "3": 1},
            "6": {"4": 3, "7": 2},
            "7": {"3": 7, "6": 2},
        }
        nodes = list(graph.keys())
        # Build unique undirected edges
        seen = set()
        edges = {}
        for u, nbrs in graph.items():
            for v, w in nbrs.items():
                key = tuple(sorted([u, v]))
                if key not in seen:
                    edges[(u, v)] = {"w": w}
                    seen.add(key)

        pos = {
            "0": (0.15, 0.15), "1": (0.45, 0.10), "3": (0.80, 0.15),
            "4": (0.15, 0.50), "2": (0.55, 0.55), "5": (0.80, 0.50),
            "6": (0.10, 0.85), "7": (0.70, 0.85),
        }
        return graph, nodes, edges, pos

    def _prim_graph(self):
        graph = {
            "0": {"1": 10, "2": 20},
            "1": {"0": 10, "3": 50, "4": 10},
            "2": {"0": 20, "3": 20, "4": 20},
            "3": {"1": 50, "2": 20, "4": 20},
            "4": {"1": 10, "2": 33, "3": 20, "5": 1},
            "5": {"3": 2, "4": 1},
        }
        nodes = list(graph.keys())
        seen  = set()
        edges = {}
        for u, nbrs in graph.items():
            for v, w in nbrs.items():
                key = tuple(sorted([u, v]))
                if key not in seen:
                    edges[(u, v)] = {"w": w}
                    seen.add(key)
        pos = {
            "0": (0.15, 0.35), "1": (0.45, 0.15), "2": (0.15, 0.72),
            "3": (0.75, 0.72), "4": (0.72, 0.35), "5": (0.90, 0.15),
        }
        return graph, nodes, edges, pos

    # ── Dijkstra ──────────────────────────────────────────────────────────────

    def _setup_Dijkstra(self):
        self._ui["desc_lbl"].configure(text="Grafos / Dijkstra.py")
        graph, nodes, edges, pos = self._dijkstra_kruskal_graph()
        start, end = "0", "7"

        tk.Label(self._ui["viz_frame"],
            text=f"Dijkstra — Camino más corto de {start} a {end}",
            font=th.FONT_SUBTITLE, bg=th.BG, fg=th.TEXT_BRIGHT,
        ).pack(pady=(10, 0))

        info_lbl = tk.Label(self._ui["viz_frame"], text="",
                            font=th.FONT_BODY, bg=th.BG, fg=th.YELLOW)
        info_lbl.pack()

        c = self._make_canvas()
        self._make_controls()

        # Run Dijkstra
        dist  = {n: float("inf") for n in nodes}
        prev  = {n: None for n in nodes}
        dist[start] = 0
        unvisited   = set(nodes)
        steps       = []

        def get_adj(u):
            """Neighbors from graph dict."""
            return graph[u].items()

        def snap(current, msg):
            visited = set(nodes) - unvisited
            path_nodes = set()
            node = end
            while prev.get(node):
                path_nodes.add(node)
                path_nodes.add(prev[node])
                node = prev[node]
            steps.append({"visited": set(visited), "current": current,
                          "path_nodes": path_nodes, "dist": dict(dist), "info": msg})

        snap(None, f"Inicio — dist[{start}]=0, todos los demás=∞")

        while unvisited:
            u = min(unvisited, key=lambda n: dist[n])
            if dist[u] == float("inf"): break
            unvisited.remove(u)
            for v, w in get_adj(u):
                nd = dist[u] + w
                if nd < dist[v]:
                    dist[v] = nd; prev[v] = u
            d_end = dist[end] if dist[end] < float("inf") else "∞"
            snap(u, f"Visitado: {u}  |  dist[{end}] = {d_end}")

        final_path = []
        n = end
        while n:
            final_path.insert(0, n)
            n = prev.get(n)

        steps.append({"visited": set(nodes), "current": None,
                      "path_nodes": set(final_path),
                      "dist": dist,
                      "info": f"Ruta: {' → '.join(final_path)}   Distancia: {dist[end]}"})

        def draw(step):
            nc = {}
            for node in nodes:
                if node == step["current"]:        nc[node] = th.YELLOW
                elif node in step.get("path_nodes", set()): nc[node] = th.PURPLE
                elif node in step["visited"]:      nc[node] = th.GREEN
                else:                              nc[node] = th.ACCENT
            ec = {}
            for (u, v) in edges:
                pn = step.get("path_nodes", set())
                if u in pn and v in pn:            ec[(u, v)] = th.PURPLE
                elif u in step["visited"] and v in step["visited"]:
                                                   ec[(u, v)] = th.GREEN
                else:                              ec[(u, v)] = th.BORDER
            c.update_idletasks()
            draw_graph_canvas(c, nodes, edges, pos, nc, ec, info=step["info"])
            info_lbl.configure(text=step["info"])
            if hasattr(self, "_step_lbl"):
                self._step_lbl.configure(
                    text=f"Paso {min(self._step_idx+1, len(steps))} / {len(steps)}")

        self._steps = steps; self._draw_fn = draw
        draw(steps[0])

    # ── Prim ──────────────────────────────────────────────────────────────────

    def _setup_Prim(self):
        self._ui["desc_lbl"].configure(text="Grafos / Prim.py")
        graph, nodes, edges, pos = self._prim_graph()
        root = "2"

        tk.Label(self._ui["viz_frame"],
            text=f"Prim — Árbol de Expansión Mínima desde nodo {root}",
            font=th.FONT_SUBTITLE, bg=th.BG, fg=th.TEXT_BRIGHT,
        ).pack(pady=(10, 0))

        info_lbl = tk.Label(self._ui["viz_frame"], text="",
                            font=th.FONT_BODY, bg=th.BG, fg=th.YELLOW)
        info_lbl.pack()

        c = self._make_canvas()
        self._make_controls()

        visitados  = {root}
        mst_edges  = set()
        total      = 0
        steps      = [{"visitados": {root}, "mst_edges": set(),
                       "total": 0, "info": f"Inicio desde nodo {root}"}]

        while len(visitados) < len(graph):
            mejor = None; menor_w = float("inf")
            for u in visitados:
                for v, w in graph[u].items():
                    if v not in visitados and w < menor_w:
                        menor_w = w; mejor = (u, v)
            if not mejor: break
            u, v = mejor
            mst_edges.add((u, v)); visitados.add(v)
            total += menor_w
            steps.append({"visitados": set(visitados), "mst_edges": set(mst_edges),
                          "total": total,
                          "info": f"Añadir ({u}—{v}, w={menor_w})  |  Peso MST total: {total}"})

        steps.append({**steps[-1], "info": f"MST completo  |  Peso total: {total}"})

        def draw(step):
            nc = {n: (th.GREEN if n in step["visitados"] else th.ACCENT) for n in nodes}
            ec = {}
            for (u, v) in edges:
                if (u, v) in step["mst_edges"] or (v, u) in step["mst_edges"]:
                    ec[(u, v)] = th.ORANGE
                else:
                    ec[(u, v)] = th.BORDER
            c.update_idletasks()
            draw_graph_canvas(c, nodes, edges, pos, nc, ec, info=step["info"])
            info_lbl.configure(text=step["info"])
            if hasattr(self, "_step_lbl"):
                self._step_lbl.configure(
                    text=f"Paso {min(self._step_idx+1, len(steps))} / {len(steps)}")

        self._steps = steps; self._draw_fn = draw
        draw(steps[0])

    # ── Kruskal ───────────────────────────────────────────────────────────────

    def _setup_Kruskal(self):
        self._ui["desc_lbl"].configure(text="Grafos / Kruskal.py")
        graph, nodes, edges, pos = self._dijkstra_kruskal_graph()

        tk.Label(self._ui["viz_frame"],
            text="Kruskal — MST por aristas ordenadas (Union-Find)",
            font=th.FONT_SUBTITLE, bg=th.BG, fg=th.TEXT_BRIGHT,
        ).pack(pady=(10, 0))

        info_lbl = tk.Label(self._ui["viz_frame"], text="",
                            font=th.FONT_BODY, bg=th.BG, fg=th.YELLOW)
        info_lbl.pack()

        c = self._make_canvas()
        self._make_controls()

        # Union-Find
        parent = {n: n for n in nodes}
        rank   = {n: 0  for n in nodes}

        def find(x):
            if parent[x] != x: parent[x] = find(parent[x])
            return parent[x]

        def union(x, y):
            rx, ry = find(x), find(y)
            if rank[rx] < rank[ry]: parent[rx] = ry
            elif rank[rx] > rank[ry]: parent[ry] = rx
            else: parent[ry] = rx; rank[rx] += 1

        sorted_edges = sorted(edges.items(), key=lambda x: x[1]["w"])

        mst_edges  = set()
        rej_edges  = set()
        total      = 0
        steps      = [{"mst": set(), "rej": set(), "total": 0,
                       "info": "Kruskal: aristas ordenadas por peso"}]

        for (u, v), data in sorted_edges:
            w = data["w"]
            if find(u) != find(v):
                union(u, v); mst_edges.add((u, v)); total += w
                steps.append({"mst": set(mst_edges), "rej": set(rej_edges), "total": total,
                              "info": f"✓ Añadir ({u}—{v}, w={w}) — sin ciclo  |  Peso: {total}"})
            else:
                rej_edges.add((u, v))
                steps.append({"mst": set(mst_edges), "rej": set(rej_edges), "total": total,
                              "info": f"✗ Rechazar ({u}—{v}, w={w}) — formaría ciclo"})

        steps.append({**steps[-1], "info": f"MST completo  |  Peso total: {total}"})

        def draw(step):
            nc = {}
            for n in nodes:
                if any(n in e for e in step["mst"]): nc[n] = th.GREEN
                else: nc[n] = th.ACCENT
            ec = {}
            for (u, v) in edges:
                if (u, v) in step["mst"] or (v, u) in step["mst"]: ec[(u, v)] = th.ORANGE
                elif (u, v) in step["rej"] or (v, u) in step["rej"]: ec[(u, v)] = th.RED
                else: ec[(u, v)] = th.BORDER
            c.update_idletasks()
            draw_graph_canvas(c, nodes, edges, pos, nc, ec, info=step["info"])
            info_lbl.configure(text=step["info"])
            if hasattr(self, "_step_lbl"):
                self._step_lbl.configure(
                    text=f"Paso {min(self._step_idx+1, len(steps))} / {len(steps)}")

        self._steps = steps; self._draw_fn = draw
        draw(steps[0])

    # ── Torres de Hanoi ───────────────────────────────────────────────────────

    def _setup_Hanoi(self):
        self._ui["desc_lbl"].configure(text="Grafos / Hanoi.py")

        N = 5
        tk.Label(self._ui["viz_frame"],
            text=f"Torres de Hanoi — {N} discos (A → C usando B)",
            font=th.FONT_SUBTITLE, bg=th.BG, fg=th.TEXT_BRIGHT,
        ).pack(pady=(10, 0))

        move_lbl = tk.Label(self._ui["viz_frame"],
            text="Presiona ▶ Iniciar o ⏭ Paso para animar los movimientos",
            font=th.FONT_BODY, bg=th.BG, fg=th.YELLOW)
        move_lbl.pack()

        canvas = tk.Canvas(self._ui["viz_frame"], bg=th.BG, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self._make_controls()

        # Compute all moves
        moves = []
        def hanoi(n, src, dst, aux):
            if n >= 1:
                hanoi(n-1, src, aux, dst)
                moves.append((src, dst))
                hanoi(n-1, aux, dst, src)
        hanoi(N, "A", "C", "B")

        # Build states
        pegs = {"A": list(range(N, 0, -1)), "B": [], "C": []}
        states = [{"pegs": {k: list(v) for k, v in pegs.items()},
                   "move": None, "step_num": 0, "total": len(moves)}]
        for i, (src, dst) in enumerate(moves):
            disk = pegs[src].pop(); pegs[dst].append(disk)
            states.append({"pegs": {k: list(v) for k, v in pegs.items()},
                           "move": (src, dst, disk),
                           "step_num": i+1, "total": len(moves)})

        DISK_H = 22
        PEG_H  = N * (DISK_H + 4) + 40
        MAX_W  = 160
        COLORS = ["#e74c3c","#e67e22","#f1c40f","#2ecc71","#3498db",
                  "#9b59b6","#1abc9c","#e91e63"]

        def draw_state(state):
            canvas.delete("all")
            canvas.update_idletasks()
            cw = canvas.winfo_width() or 620
            ch = canvas.winfo_height() or 320

            base_y = ch - 50
            peg_xs = {"A": cw//4, "B": cw//2, "C": 3*cw//4}
            labels  = {"A": "A  (Origen)", "B": "B  (Auxiliar)", "C": "C  (Destino)"}

            # Base
            canvas.create_line(30, base_y+5, cw-30, base_y+5,
                               fill=th.SURFACE_BG, width=4)

            for peg, px in peg_xs.items():
                # Post
                canvas.create_rectangle(px-5, base_y-PEG_H, px+5, base_y,
                                        fill=th.SURFACE_BG, outline="")
                # Label
                canvas.create_text(px, base_y+24, text=labels[peg],
                                   font=("Segoe UI", 9, "bold"), fill=th.TEXT_DIM)

                # Disks (bottom=index 0)
                for level, disk in enumerate(state["pegs"][peg]):
                    dw   = int(MAX_W * disk / N)
                    dy   = base_y - (level+1)*(DISK_H+4)
                    clr  = COLORS[(disk-1) % len(COLORS)]
                    canvas.create_rectangle(px-dw//2, dy, px+dw//2, dy+DISK_H,
                                            fill=clr, outline=th.BG, width=2)
                    canvas.create_text(px, dy+DISK_H//2, text=str(disk),
                                       font=("Segoe UI", 9, "bold"), fill="white")

            m = state["move"]
            if m:
                src, dst, disk = m
                msg = (f"Mover disco {disk}:  {src}  →  {dst}   "
                       f"(movimiento {state['step_num']} / {state['total']})")
            else:
                msg = f"Estado inicial — {N} discos en torre A"
            move_lbl.configure(text=msg)

            if hasattr(self, "_step_lbl"):
                self._step_lbl.configure(
                    text=f"Paso {state['step_num']} / {state['total']}")

        self._steps   = states
        self._draw_fn = draw_state
        draw_state(states[0])
