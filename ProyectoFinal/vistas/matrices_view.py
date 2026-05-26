"""
Matrices y Datos — Practicas_2
Exercises: Matrices01, coordenadasMatriz, asientos, DataFrame
"""
import tkinter as tk
from tkinter import ttk
import os

import theme as th
from vistas._layout import make_exercise_view, make_nav_btn, make_ctrl_btn, load_code
from adaptadores.capture import path_for, import_module_captured

P2 = path_for("Practicas_2")

EXERCISES = [
    ("Matrices 01 — Multiplicación",    "Matrices01"),
    ("Coordenadas — Búsqueda en Matriz","coordenadasMatriz"),
    ("Asientos — Reserva 6×6",          "asientos"),
    ("DataFrame — Estadísticas",        "DataFrame"),
]

# ─── Shared grid drawing ─────────────────────────────────────────────────────

CELL_SIZE = 52


def draw_matrix(canvas, matrix, ox, oy, highlights=None, highlight_color=None):
    """Draw a 2D matrix on a canvas starting at (ox, oy)."""
    highlights = highlights or set()
    for r, row in enumerate(matrix):
        for c, val in enumerate(row):
            x0 = ox + c * CELL_SIZE
            y0 = oy + r * CELL_SIZE
            x1, y1 = x0 + CELL_SIZE, y0 + CELL_SIZE
            fill = (highlight_color or th.ORANGE) if (r, c) in highlights else th.PANEL_BG
            canvas.create_rectangle(x0, y0, x1, y1,
                                    fill=fill, outline=th.SURFACE_BG, width=2)
            canvas.create_text((x0+x1)//2, (y0+y1)//2,
                               text=str(val), fill=th.TEXT_BRIGHT, font=th.FONT_MONO)


class MatricesView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=th.BG)
        self._ui = make_exercise_view(self)
        self._ui["root"].pack(fill=tk.BOTH, expand=True)
        self._nav_btns = []
        self._build_nav()
        self._select(0)

    def _build_nav(self):
        for i, (label, _) in enumerate(EXERCISES):
            btn = make_nav_btn(self._ui["left"], label, lambda i=i: self._select(i))
            self._nav_btns.append(btn)

    def _select(self, idx):
        for i, btn in enumerate(self._nav_btns):
            btn.configure(
                bg=th.PANEL_BG if i == idx else th.SIDEBAR_BG,
                fg=th.ACCENT  if i == idx else th.TEXT,
            )
        label, key = EXERCISES[idx]
        self._ui["title_lbl"].configure(text=label)
        load_code(self._ui["code_text"], os.path.join(P2, key + ".py"))
        self._clear_viz()
        getattr(self, f"_show_{key}")()

    def _clear_viz(self):
        for w in self._ui["viz_frame"].winfo_children():
            w.destroy()
        for w in self._ui["ctrl_frame"].winfo_children():
            w.destroy()

    def _stat_box(self, stats):
        bar = tk.Frame(self._ui["viz_frame"], bg=th.SIDEBAR_BG, padx=15, pady=10)
        bar.pack(fill=tk.X, side=tk.BOTTOM)
        for label, value in stats:
            f = tk.Frame(bar, bg=th.SIDEBAR_BG)
            f.pack(side=tk.LEFT, padx=15)
            tk.Label(f, text=label, font=th.FONT_SMALL,
                     bg=th.SIDEBAR_BG, fg=th.TEXT_DIM).pack()
            tk.Label(f, text=str(value), font=("Segoe UI", 12, "bold"),
                     bg=th.SIDEBAR_BG, fg=th.ACCENT).pack()

    # ── Matrices01 ──────────────────────────────────────────────────────────

    def _show_Matrices01(self):
        self._ui["desc_lbl"].configure(text="Practicas_2 / Matrices01.py")

        A = [[5,6,13],[5,10,1],[2,11,3]]
        B = [[1,2,17],[6,5,15],[3,11,11]]

        # Compute C
        n = len(A)
        C = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]

        tk.Label(self._ui["viz_frame"],
            text="Multiplicación de Matrices  A × B = C",
            font=th.FONT_SUBTITLE, bg=th.BG, fg=th.TEXT_BRIGHT,
        ).pack(pady=(18, 4))

        canvas = tk.Canvas(self._ui["viz_frame"], bg=th.BG, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.update_idletasks()
        cw = canvas.winfo_width() or 680
        ch = canvas.winfo_height() or 320

        total_w = 3 * CELL_SIZE
        gap     = 60
        total   = 3 * total_w + 2 * gap + 2 * 40
        ox      = (cw - total) // 2
        oy      = (ch - 3*CELL_SIZE) // 2

        # Labels
        for label, offset in [("A", 0), ("×", total_w + 15), ("B", total_w + gap),
                               ("=", 2*total_w + gap + 15), ("C", 2*(total_w + gap))]:
            lx = ox + offset + (total_w//2 if label not in ("×","=") else 0)
            canvas.create_text(lx, oy - 22, text=label,
                               font=("Segoe UI", 14, "bold"), fill=th.ACCENT)

        draw_matrix(canvas, A, ox, oy)
        draw_matrix(canvas, B, ox + total_w + gap, oy)
        draw_matrix(canvas, C, ox + 2*(total_w + gap), oy, highlight_color=th.GREEN)

        self._stat_box([("dim(A)", f"{n}×{n}"), ("dim(B)", f"{n}×{n}"),
                        ("dim(C)", f"{n}×{n}"), ("Multiplicaciones", n**3)])

    # ── coordenadasMatriz ────────────────────────────────────────────────────

    def _show_coordenadasMatriz(self):
        self._ui["desc_lbl"].configure(text="Practicas_2 / coordenadasMatriz.py")

        A = [
            [4,7,2,9,5,7],
            [1,3,7,6,8,0],
            [9,2,5,7,4,6],
            [8,7,1,3,7,2],
            [5,0,6,4,2,9],
            [7,8,9,2,1,7],
        ]
        valor_buscado = 4
        encontrados = {(r, c) for r in range(6) for c in range(6) if A[r][c] == valor_buscado}

        tk.Label(self._ui["viz_frame"],
            text=f"Búsqueda del valor {valor_buscado} en la Matriz 6×6",
            font=th.FONT_SUBTITLE, bg=th.BG, fg=th.TEXT_BRIGHT,
        ).pack(pady=(18, 4))

        canvas = tk.Canvas(self._ui["viz_frame"], bg=th.BG, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.update_idletasks()
        cw = canvas.winfo_width() or 600
        ch = canvas.winfo_height() or 380
        ox = (cw - 6*CELL_SIZE) // 2
        oy = (ch - 6*CELL_SIZE) // 2

        draw_matrix(canvas, A, ox, oy, highlights=encontrados, highlight_color=th.YELLOW)

        # Coordinate labels
        for r, c in encontrados:
            x = ox + c*CELL_SIZE + CELL_SIZE//2
            y = oy + r*CELL_SIZE + CELL_SIZE//2
            canvas.create_text(x, y - 14, text=f"({r+1},{c+1})",
                               font=("Segoe UI", 8), fill=th.TEXT_BRIGHT)

        coords_str = ", ".join(f"({r+1},{c+1})" for r, c in sorted(encontrados))
        self._stat_box([("Valor buscado", valor_buscado),
                        ("Ocurrencias", len(encontrados)),
                        ("Coordenadas", coords_str)])

    # ── asientos ────────────────────────────────────────────────────────────

    def _show_asientos(self):
        self._ui["desc_lbl"].configure(text="Practicas_2 / asientos.py")

        asientos = [[0]*6 for _ in range(6)]
        ops = [(1,1,'R'),(1,2,'R'),(1,1,'R'),(1,1,'L'),(3,4,'R'),
               (6,6,'R'),(2,5,'R')]

        log = []
        for i, j, op in ops:
            if op == 'R':
                if asientos[i-1][j-1] == 0:
                    asientos[i-1][j-1] = 1
                    log.append(f"✓ Reservado  ({i},{j})")
                else:
                    log.append(f"✗ Ya reservado ({i},{j})")
            else:
                if asientos[i-1][j-1] == 1:
                    asientos[i-1][j-1] = 0
                    log.append(f"↩ Liberado   ({i},{j})")
                else:
                    log.append(f"– Ya libre   ({i},{j})")

        tk.Label(self._ui["viz_frame"],
            text="Sistema de Reserva de Asientos 6×6",
            font=th.FONT_SUBTITLE, bg=th.BG, fg=th.TEXT_BRIGHT,
        ).pack(pady=(18, 4))

        body = tk.Frame(self._ui["viz_frame"], bg=th.BG)
        body.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Grid canvas
        canvas = tk.Canvas(body, bg=th.BG, highlightthickness=0, width=6*CELL_SIZE + 40)
        canvas.pack(side=tk.LEFT, padx=(0, 20))

        CS = CELL_SIZE
        ox, oy = 20, 30
        # Col headers
        for c in range(6):
            canvas.create_text(ox + c*CS + CS//2, oy - 16, text=str(c+1),
                               font=th.FONT_SMALL, fill=th.TEXT_DIM)
        # Row headers + cells
        for r in range(6):
            canvas.create_text(ox - 12, oy + r*CS + CS//2, text=str(r+1),
                               font=th.FONT_SMALL, fill=th.TEXT_DIM)
            for c in range(6):
                x0, y0 = ox + c*CS, oy + r*CS
                fill = th.RED if asientos[r][c] == 1 else th.GREEN
                canvas.create_rectangle(x0, y0, x0+CS, y0+CS,
                                        fill=fill, outline=th.BG, width=3)
                txt = "●" if asientos[r][c] == 1 else "○"
                canvas.create_text(x0+CS//2, y0+CS//2, text=txt,
                                   font=("Segoe UI", 14), fill="white")

        # Legend + log
        right_panel = tk.Frame(body, bg=th.BG)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        leg = tk.Frame(right_panel, bg=th.PANEL_BG, padx=12, pady=10)
        leg.pack(fill=tk.X, pady=(0, 10))
        for color, txt in [(th.GREEN, "○  Libre"), (th.RED, "●  Reservado")]:
            r = tk.Frame(leg, bg=th.PANEL_BG)
            r.pack(anchor=tk.W, pady=2)
            tk.Frame(r, bg=color, width=18, height=18).pack(side=tk.LEFT, padx=(0,8))
            tk.Label(r, text=txt, font=th.FONT_BODY, bg=th.PANEL_BG, fg=th.TEXT).pack(side=tk.LEFT)

        tk.Label(right_panel, text="Secuencia de operaciones:",
                 font=("Segoe UI", 9, "bold"), bg=th.BG, fg=th.TEXT_DIM).pack(anchor=tk.W)
        for entry in log:
            color = th.GREEN if "✓" in entry else (th.RED if "✗" in entry else th.YELLOW)
            tk.Label(right_panel, text=entry, font=th.FONT_SMALL, bg=th.BG, fg=color,
                     anchor=tk.W).pack(fill=tk.X)

        reservados = sum(asientos[r][c] for r in range(6) for c in range(6))
        self._stat_box([("Total asientos", 36),
                        ("Reservados", reservados),
                        ("Libres", 36-reservados)])

    # ── DataFrame ───────────────────────────────────────────────────────────

    def _show_DataFrame(self):
        self._ui["desc_lbl"].configure(text="Practicas_2 / DataFrame.py")
        mod, output = import_module_captured(
            os.path.join(P2, "DataFrame.py"), "DataFrame_mod",
            extra_paths=[P2]
        )

        tk.Label(self._ui["viz_frame"],
            text="Análisis Estadístico — Housing Dataset (pandas)",
            font=th.FONT_SUBTITLE, bg=th.BG, fg=th.TEXT_BRIGHT,
        ).pack(pady=(18, 4))

        if mod is None or "[Error" in output:
            tk.Label(self._ui["viz_frame"],
                text=output or "Error al cargar pandas / Housing.csv",
                font=th.FONT_BODY, bg=th.BG, fg=th.RED,
                wraplength=500).pack(pady=30)
            return

        import pandas as pd
        csv_path = path_for("Practicas_2", "Housing.csv")
        df = pd.read_csv(csv_path)

        columns_info = [
            ("price",       "Precio ($)"),
            ("bathrooms",   "Baños"),
            ("sqft_living", "Sup. Habitable (sqft)"),
            ("sqft_lot",    "Sup. Terreno (sqft)"),
            ("floors",      "Pisos"),
            ("sqft_above",  "Sup. Superior (sqft)"),
        ]

        rows = []
        for col, label in columns_info:
            data = df[col].tolist()
            # Delegate to the module's optimised O(n) functions (user-fixed version)
            m    = mod.media(data)
            mo   = mod.moda(data)
            v    = mod.varianza(data)
            d    = mod.desv(data)
            rows.append((label, f"{m:,.2f}", str(mo), f"{v:,.2f}", f"{d:,.2f}", ""))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("D.Treeview",
            background=th.PANEL_BG, foreground=th.TEXT,
            fieldbackground=th.PANEL_BG, rowheight=30, font=th.FONT_BODY)
        style.configure("D.Treeview.Heading",
            background=th.SURFACE_BG, foreground=th.ACCENT, font=("Segoe UI", 10, "bold"))
        style.map("D.Treeview", background=[("selected", th.ACCENT)])

        container = tk.Frame(self._ui["viz_frame"], bg=th.BG)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        cols = ["Variable", "Media", "Moda", "Varianza", "Desv. Estándar"]
        tree = ttk.Treeview(container, columns=cols, show="headings", style="D.Treeview")
        for i, col in enumerate(cols):
            w = [200, 120, 120, 130, 140][i]
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor=tk.CENTER)
        tree.tag_configure("alt", background=th.SURFACE_BG)
        for i, row in enumerate(rows):
            tree.insert("", tk.END, values=row[:-1], tags=("alt" if i%2 else "",))
        tree.pack(fill=tk.BOTH, expand=True)

        self._stat_box([("Registros totales", len(df)),
                        ("Variables analizadas", len(columns_info))])
