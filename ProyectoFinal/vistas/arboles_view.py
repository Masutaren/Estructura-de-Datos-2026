"""
Árboles
Exercises: ArbolBinario (BST + recorridos), nodoArbol (BST con NodoArbol), BFS
"""
import tkinter as tk
import os

import theme as th
from vistas._layout import make_exercise_view, make_nav_btn, make_ctrl_btn, load_code
from adaptadores.capture import path_for

ARB = path_for("Arboles")

EXERCISES = [
    ("Árbol Binario — Recorridos",  "ArbolBinario"),
    ("Nodo Árbol — BST Complejo",   "nodoArbol"),
    ("BFS — Búsqueda en Amplitud",  "BFS"),
]

NODE_R    = 22   # node circle radius
LEVEL_GAP = 72   # vertical gap between levels
EDGE_CLR  = "#404060"


# ─── Tree layout ─────────────────────────────────────────────────────────────

def _bst_positions(node, x, y, h_offset, attr_iz="izquierdo", attr_der="derecho",
                   attr_val="dato", positions=None):
    if positions is None:
        positions = {}
    if node is None:
        return positions
    positions[id(node)] = (x, y, getattr(node, attr_val))
    left  = getattr(node, attr_iz, None)
    right = getattr(node, attr_der, None)
    if left:
        _bst_positions(left,  x - h_offset, y + LEVEL_GAP, max(h_offset//2, 30),
                       attr_iz, attr_der, attr_val, positions)
    if right:
        _bst_positions(right, x + h_offset, y + LEVEL_GAP, max(h_offset//2, 30),
                       attr_iz, attr_der, attr_val, positions)
    return positions


def _bst_nodo_positions(node, x, y, h_offset, positions=None):
    """For NodoArbol class (different attribute names)."""
    if positions is None:
        positions = {}
    if node is None:
        return positions
    positions[id(node)] = (x, y, node.clave)
    if node.hijoIzquierdo:
        _bst_nodo_positions(node.hijoIzquierdo, x - h_offset, y + LEVEL_GAP,
                            max(h_offset//2, 28), positions)
    if node.hijoDerecho:
        _bst_nodo_positions(node.hijoDerecho,   x + h_offset, y + LEVEL_GAP,
                            max(h_offset//2, 28), positions)
    return positions


def _collect_edges(node, positions, attr_iz="izquierdo", attr_der="derecho"):
    """Return list of (parent_id, child_id) pairs."""
    if node is None:
        return []
    edges = []
    left  = getattr(node, attr_iz, None)
    right = getattr(node, attr_der, None)
    if left:
        edges.append((id(node), id(left)))
        edges.extend(_collect_edges(left, positions, attr_iz, attr_der))
    if right:
        edges.append((id(node), id(right)))
        edges.extend(_collect_edges(right, positions, attr_iz, attr_der))
    return edges


def _collect_edges_nodo(node):
    if node is None:
        return []
    edges = []
    if node.hijoIzquierdo:
        edges.append((id(node), id(node.hijoIzquierdo)))
        edges.extend(_collect_edges_nodo(node.hijoIzquierdo))
    if node.hijoDerecho:
        edges.append((id(node), id(node.hijoDerecho)))
        edges.extend(_collect_edges_nodo(node.hijoDerecho))
    return edges


def draw_tree(canvas, root, positions, edges, node_colors=None, ox=0, oy=0):
    """Draw the tree on canvas."""
    canvas.delete("all")
    node_colors = node_colors or {}

    # Edges
    for pid, cid in edges:
        if pid in positions and cid in positions:
            px, py, _ = positions[pid]
            cx, cy, _ = positions[cid]
            canvas.create_line(px+ox, py+oy, cx+ox, cy+oy,
                               fill=EDGE_CLR, width=2)

    # Nodes
    for nid, (x, y, val) in positions.items():
        fill = node_colors.get(nid, th.ACCENT)
        nx, ny = x + ox, y + oy
        canvas.create_oval(nx-NODE_R, ny-NODE_R, nx+NODE_R, ny+NODE_R,
                           fill=fill, outline=th.BG, width=2)
        canvas.create_text(nx, ny, text=str(val),
                           font=("Segoe UI", 10, "bold"), fill="white")


# ─── Traversal step generators ───────────────────────────────────────────────

def preorden_steps(node, attr_iz="izquierdo", attr_der="derecho"):
    steps = []
    def _pre(n):
        if n is None: return
        steps.append(id(n))
        _pre(getattr(n, attr_iz, None))
        _pre(getattr(n, attr_der, None))
    _pre(node)
    return steps


def inorden_steps(node, attr_iz="izquierdo", attr_der="derecho"):
    steps = []
    def _in(n):
        if n is None: return
        _in(getattr(n, attr_iz, None))
        steps.append(id(n))
        _in(getattr(n, attr_der, None))
    _in(node)
    return steps


def postorden_steps(node, attr_iz="izquierdo", attr_der="derecho"):
    steps = []
    def _post(n):
        if n is None: return
        _post(getattr(n, attr_iz, None))
        _post(getattr(n, attr_der, None))
        steps.append(id(n))
    _post(node)
    return steps


def preorden_nodo(node):
    steps = []
    def _pre(n):
        if n is None: return
        steps.append(id(n))
        _pre(n.hijoIzquierdo)
        _pre(n.hijoDerecho)
    _pre(node)
    return steps


def inorden_nodo(node):
    steps = []
    def _in(n):
        if n is None: return
        _in(n.hijoIzquierdo)
        steps.append(id(n))
        _in(n.hijoDerecho)
    _in(node)
    return steps


# ─── Main view ───────────────────────────────────────────────────────────────

class ArbolesView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=th.BG)
        self._ui = make_exercise_view(self)
        self._ui["root"].pack(fill=tk.BOTH, expand=True)

        self._nav_btns = []
        self._steps    = []
        self._step_idx = 0
        self._after_id = None
        self._canvas   = None

        self._root_node = None   # current tree root
        self._positions = {}     # {node_id: (x, y, val)}
        self._edges     = []     # [(parent_id, child_id)]
        self._visited   = set()  # visited node ids

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
        load_code(self._ui["code_text"], os.path.join(ARB, key + ".py"))
        self._clear_viz()
        getattr(self, f"_setup_{key}")()

    def _clear_viz(self):
        for w in self._ui["viz_frame"].winfo_children():
            w.destroy()
        for w in self._ui["ctrl_frame"].winfo_children():
            w.destroy()
        self._canvas = None
        self._steps = []
        self._step_idx = 0
        self._visited = set()

    def _make_canvas(self):
        c = tk.Canvas(self._ui["viz_frame"], bg=th.BG, highlightthickness=0)
        c.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self._canvas = c
        return c

    def _make_controls(self, traversals=None):
        ctrl = self._ui["ctrl_frame"]
        make_ctrl_btn(ctrl, "▶  Iniciar",   self._play,  th.GREEN)
        make_ctrl_btn(ctrl, "⏭  Paso",      self._step,  th.ACCENT)
        make_ctrl_btn(ctrl, "↺  Reiniciar", self._reset, th.YELLOW)

        if traversals:
            tk.Label(ctrl, text=" | Recorrido:", font=th.FONT_SMALL,
                     bg=th.SIDEBAR_BG, fg=th.TEXT_DIM).pack(side=tk.LEFT, padx=(15, 4))
            for name, fn in traversals:
                make_ctrl_btn(ctrl, name, fn, th.ORANGE)

        self._step_lbl = tk.Label(ctrl, text="Paso 0 / 0",
            font=th.FONT_SMALL, bg=th.SIDEBAR_BG, fg=th.TEXT_DIM)
        self._step_lbl.pack(side=tk.RIGHT, padx=12)

    def _cancel_anim(self):
        if self._after_id:
            self.after_cancel(self._after_id)
            self._after_id = None

    def _play(self):
        if self._step_idx >= len(self._steps):
            self._step_idx = 0
            self._visited = set()
        self._animate()

    def _animate(self):
        if self._step_idx < len(self._steps):
            self._draw_step_tree()
            self._step_idx += 1
            self._after_id = self.after(th.ANIM_SPEED, self._animate)

    def _step(self):
        self._cancel_anim()
        if self._step_idx < len(self._steps):
            self._draw_step_tree()
            self._step_idx += 1

    def _reset(self):
        self._cancel_anim()
        self._step_idx = 0
        self._visited  = set()
        self._refresh_tree()

    def _draw_step_tree(self):
        if not self._steps:
            return
        nid = self._steps[self._step_idx] if self._step_idx < len(self._steps) else None
        if nid:
            self._visited.add(nid)
        self._refresh_tree(current=nid)
        total = len(self._steps)
        disp  = min(self._step_idx + 1, total)
        if hasattr(self, "_step_lbl"):
            self._step_lbl.configure(text=f"Paso {disp} / {total}")

    def _refresh_tree(self, current=None):
        if not self._canvas or not self._positions:
            return
        self._canvas.update_idletasks()
        cw = self._canvas.winfo_width()  or 600
        ch = self._canvas.winfo_height() or 400
        # Center offset
        xs = [x for x, y, v in self._positions.values()]
        ys = [y for x, y, v in self._positions.values()]
        if not xs:
            return
        mid_x = (max(xs) + min(xs)) / 2
        mid_y = (max(ys) + min(ys)) / 2
        ox = cw//2 - int(mid_x)
        oy = 50     - int(min(ys))

        colors = {}
        for nid in self._positions:
            if nid == current:
                colors[nid] = th.YELLOW
            elif nid in self._visited:
                colors[nid] = th.GREEN
            else:
                colors[nid] = th.ACCENT

        draw_tree(self._canvas, None, self._positions, self._edges, colors, ox, oy)

        # Legend
        if self._visited or current:
            self._canvas.create_text(10, 12, anchor=tk.W,
                text="🟡 Actual  🟢 Visitado  🔵 Pendiente",
                font=th.FONT_SMALL, fill=th.TEXT_DIM)

    # ── ArbolBinario ────────────────────────────────────────────────────────

    def _setup_ArbolBinario(self):
        self._ui["desc_lbl"].configure(text="Arboles / ArbolBinario.py")

        # Recreate tree from original data
        class Nodo:
            def __init__(self, dato):
                self.dato, self.izquierdo, self.derecho = dato, None, None
            def agregar(self, dato):
                if dato < self.dato:
                    if self.izquierdo is None: self.izquierdo = Nodo(dato)
                    else: self.izquierdo.agregar(dato)
                else:
                    if self.derecho is None: self.derecho = Nodo(dato)
                    else: self.derecho.agregar(dato)

        datos = [3, 1, 2, 4, 5]
        raiz  = Nodo(datos[0])
        for d in datos[1:]:
            raiz.agregar(d)

        self._root_node = raiz
        self._positions = _bst_positions(raiz, 0, 0, 120)
        self._edges     = _collect_edges(raiz, self._positions)

        tk.Label(self._ui["viz_frame"],
            text=f"BST  —  datos: {datos}",
            font=th.FONT_SUBTITLE, bg=th.BG, fg=th.TEXT_BRIGHT,
        ).pack(pady=(12, 0))

        info = tk.Label(self._ui["viz_frame"], text="",
                        font=th.FONT_BODY, bg=th.BG, fg=th.YELLOW)
        info.pack()
        self._info_lbl = info

        self._make_canvas()
        self._make_controls(traversals=[
            ("Preorden",  lambda: self._set_traversal("pre",  raiz)),
            ("Inorden",   lambda: self._set_traversal("in",   raiz)),
            ("Postorden", lambda: self._set_traversal("post", raiz)),
        ])
        self._set_traversal("pre", raiz)

    def _set_traversal(self, mode, raiz):
        self._cancel_anim()
        self._visited  = set()
        self._step_idx = 0
        if mode == "pre":
            self._steps = preorden_steps(raiz)
            self._info_lbl.configure(text="Preorden: Raíz → Izq → Der")
        elif mode == "in":
            self._steps = inorden_steps(raiz)
            self._info_lbl.configure(text="Inorden: Izq → Raíz → Der  (ordenado)")
        else:
            self._steps = postorden_steps(raiz)
            self._info_lbl.configure(text="Postorden: Izq → Der → Raíz")
        self._refresh_tree()

    # ── nodoArbol ────────────────────────────────────────────────────────────

    def _setup_nodoArbol(self):
        self._ui["desc_lbl"].configure(text="Arboles / nodoArbol.py")

        class NodoArbol:
            def __init__(self, clave, valor, padre=None):
                self.clave = clave; self.cargaUtil = valor
                self.hijoIzquierdo = None; self.hijoDerecho = None
                self.padre = padre

        def insertar(raiz, clave, valor=None):
            if raiz is None:
                return NodoArbol(clave, valor)
            actual = raiz
            while True:
                if clave < actual.clave:
                    if actual.hijoIzquierdo is None:
                        actual.hijoIzquierdo = NodoArbol(clave, valor, padre=actual); break
                    else: actual = actual.hijoIzquierdo
                elif clave > actual.clave:
                    if actual.hijoDerecho is None:
                        actual.hijoDerecho = NodoArbol(clave, valor, padre=actual); break
                    else: actual = actual.hijoDerecho
                else:
                    actual.cargaUtil = valor; break
            return raiz

        lista = [1, 13, 11, 5, 9, 10, 1, 12, 3, 6]
        raiz  = None
        for n in lista:
            raiz = insertar(raiz, n, n)

        self._root_node = raiz
        self._positions = _bst_nodo_positions(raiz, 0, 0, 160)
        self._edges     = _collect_edges_nodo(raiz)

        tk.Label(self._ui["viz_frame"],
            text=f"BST con NodoArbol  —  insertar: {lista}",
            font=th.FONT_SUBTITLE, bg=th.BG, fg=th.TEXT_BRIGHT,
        ).pack(pady=(12, 0))

        info = tk.Label(self._ui["viz_frame"],
                        text="Preorden: Raíz → Izq → Der",
                        font=th.FONT_BODY, bg=th.BG, fg=th.YELLOW)
        info.pack()
        self._info_lbl = info

        self._make_canvas()

        def pre():
            self._cancel_anim(); self._visited = set(); self._step_idx = 0
            self._steps = preorden_nodo(raiz)
            self._info_lbl.configure(text="Preorden")
            self._refresh_tree()

        def ino():
            self._cancel_anim(); self._visited = set(); self._step_idx = 0
            self._steps = inorden_nodo(raiz)
            self._info_lbl.configure(text="Inorden (ordenado)")
            self._refresh_tree()

        self._make_controls(traversals=[("Preorden", pre), ("Inorden", ino)])
        self._steps = preorden_nodo(raiz)
        self._refresh_tree()

    # ── BFS ──────────────────────────────────────────────────────────────────

    def _setup_BFS(self):
        self._ui["desc_lbl"].configure(text="Arboles / BFS.py")

        grafo = {
            'A': ['B', 'C'],
            'B': ['D', 'E'],
            'C': ['F', 'G'],
            'D': [], 'E': [], 'F': [], 'G': [],
        }

        # Fixed positions for this tree-shaped graph
        manual_pos = {
            'A': (0,   0),
            'B': (-180, 70),  'C': (180, 70),
            'D': (-270, 150), 'E': (-90, 150),
            'F': (90, 150),   'G': (270, 150),
        }
        self._positions = {n: (x, y, n) for n, (x, y) in manual_pos.items()}
        self._edges     = [(n, nb) for n, nbs in grafo.items() for nb in nbs]

        tk.Label(self._ui["viz_frame"],
            text="BFS — Breadth-First Search desde nodo A",
            font=th.FONT_SUBTITLE, bg=th.BG, fg=th.TEXT_BRIGHT,
        ).pack(pady=(12, 0))

        queue_lbl = tk.Label(self._ui["viz_frame"], text="Cola BFS: []",
                             font=th.FONT_BODY, bg=th.BG, fg=th.YELLOW)
        queue_lbl.pack()

        self._make_canvas()

        # Compute BFS order
        visited_order = []
        queue_states  = []
        visited_set   = set()
        bfs_queue     = ['A']
        queue_states.append(list(bfs_queue))
        while bfs_queue:
            node = bfs_queue.pop(0)
            if node not in visited_set:
                visited_set.add(node)
                visited_order.append(node)
                for nb in grafo[node]:
                    if nb not in visited_set:
                        bfs_queue.append(nb)
                queue_states.append(list(bfs_queue))

        # Steps: each step is the next node to highlight
        bfs_steps = []
        visited   = set()
        bfs_q     = ['A']
        for node in visited_order:
            bfs_q2 = [x for x in bfs_q if x != node]
            for nb in grafo[node]:
                if nb not in visited and nb not in bfs_q2:
                    bfs_q2.extend([nb])
            bfs_steps.append({"current": node, "visited": set(visited),
                               "bfs_q": list(bfs_q2)})
            visited.add(node)
            bfs_q = bfs_q2

        self._bfs_steps    = bfs_steps
        self._bfs_visited  = set()
        self._bfs_current  = None
        self._queue_lbl    = queue_lbl

        def draw_bfs_step():
            if self._step_idx >= len(bfs_steps): return
            s = bfs_steps[self._step_idx]
            self._bfs_current = s["current"]
            self._bfs_visited = set(s["visited"])
            colors = {}
            for nid, (x, y, n) in self._positions.items():
                if n == self._bfs_current:
                    colors[nid] = th.YELLOW
                elif n in self._bfs_visited:
                    colors[nid] = th.GREEN
                else:
                    colors[nid] = th.ACCENT

            self._canvas.update_idletasks()
            cw = self._canvas.winfo_width() or 600
            ch = self._canvas.winfo_height() or 400
            ox = cw//2; oy = 50

            self._canvas.delete("all")
            # Draw edges
            for u, v in self._edges:
                ux, uy, _ = self._positions[u]
                vx, vy, _ = self._positions[v]
                active = (u in self._bfs_visited or u == self._bfs_current)
                clr = th.ACCENT if active else EDGE_CLR
                self._canvas.create_line(ux+ox, uy+oy, vx+ox, vy+oy,
                                         fill=clr, width=2)
            # Draw nodes
            for nid, (x, y, n) in self._positions.items():
                fill = colors[nid]
                self._canvas.create_oval(x+ox-NODE_R, y+oy-NODE_R,
                                         x+ox+NODE_R, y+oy+NODE_R,
                                         fill=fill, outline=th.BG, width=2)
                self._canvas.create_text(x+ox, y+oy, text=n,
                                         font=("Segoe UI", 11, "bold"), fill="white")

            queue_lbl.configure(
                text=f"Visitando: {s['current']}   |   Cola BFS: {s['bfs_q']}"
            )

        self._steps   = bfs_steps
        self._draw_fn = lambda s: draw_bfs_step()

        def play():
            if self._step_idx >= len(self._steps): self._step_idx = 0
            self._bfs_visited = set()
            self._do_anim()

        def do_step():
            self._cancel_anim()
            if self._step_idx < len(self._steps):
                draw_bfs_step()
                self._step_idx += 1

        def reset():
            self._cancel_anim()
            self._step_idx = 0
            self._bfs_visited = set()
            self._bfs_current = None
            self._refresh_bfs_tree()

        self._do_anim = lambda: self._bfs_animate(draw_bfs_step)

        ctrl = self._ui["ctrl_frame"]
        make_ctrl_btn(ctrl, "▶  Iniciar",   play,     th.GREEN)
        make_ctrl_btn(ctrl, "⏭  Paso",      do_step,  th.ACCENT)
        make_ctrl_btn(ctrl, "↺  Reiniciar", reset,    th.YELLOW)
        self._step_lbl_bfs = tk.Label(ctrl, text=f"Orden: {visited_order}",
            font=th.FONT_SMALL, bg=th.SIDEBAR_BG, fg=th.TEXT_DIM)
        self._step_lbl_bfs.pack(side=tk.RIGHT, padx=12)

        reset()

    def _bfs_animate(self, draw_fn):
        if self._step_idx < len(self._steps):
            draw_fn()
            self._step_idx += 1
            self._after_id = self.after(th.ANIM_SPEED, lambda: self._bfs_animate(draw_fn))

    def _refresh_bfs_tree(self):
        if not self._canvas:
            return
        self._canvas.update_idletasks()
        cw = self._canvas.winfo_width() or 600
        ch = self._canvas.winfo_height() or 400
        ox, oy = cw//2, 50
        self._canvas.delete("all")
        for u, v in self._edges:
            ux, uy, _ = self._positions[u]
            vx, vy, _ = self._positions[v]
            self._canvas.create_line(ux+ox, uy+oy, vx+ox, vy+oy,
                                     fill=EDGE_CLR, width=2)
        for nid, (x, y, n) in self._positions.items():
            self._canvas.create_oval(x+ox-NODE_R, y+oy-NODE_R,
                                     x+ox+NODE_R, y+oy+NODE_R,
                                     fill=th.ACCENT, outline=th.BG, width=2)
            self._canvas.create_text(x+ox, y+oy, text=n,
                                     font=("Segoe UI", 11, "bold"), fill="white")
