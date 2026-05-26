"""
Listas y Cadenas — Practicas_1
Exercises: listas01, listas02, cadenas01, numEnteros01
"""
import tkinter as tk
from tkinter import ttk
import os
import sys

import theme as th
from vistas._layout import make_exercise_view, make_nav_btn, make_ctrl_btn, load_code
from adaptadores.capture import path_for, import_module_captured

P1 = path_for("Practicas_1")

EXERCISES = [
    ("Listas 01 — Cosechas",          "listas01"),
    ("Listas 02 — Calificaciones",    "listas02"),
    ("Cadenas 01 — Frec. de Letras",  "cadenas01"),
    ("Num Enteros 01 — Sin Repetidos","numEnteros01"),
]


class ListasView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=th.BG)
        self._ui = make_exercise_view(self)
        self._ui["root"].pack(fill=tk.BOTH, expand=True)

        self._nav_btns = []
        self._build_nav()
        self._select(0)

    # ── Navigation ──────────────────────────────────────────────────────────

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
        load_code(self._ui["code_text"], os.path.join(P1, key + ".py"))
        self._clear_viz()
        getattr(self, f"_show_{key}")()

    # ── Helpers ─────────────────────────────────────────────────────────────

    def _clear_viz(self):
        for w in self._ui["viz_frame"].winfo_children():
            w.destroy()
        for w in self._ui["ctrl_frame"].winfo_children():
            w.destroy()

    def _make_tree(self, frame, columns, rows, col_widths=None):
        """Generic dark-styled Treeview."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("D.Treeview",
            background=th.PANEL_BG, foreground=th.TEXT,
            fieldbackground=th.PANEL_BG, rowheight=28,
            font=th.FONT_BODY)
        style.configure("D.Treeview.Heading",
            background=th.SURFACE_BG, foreground=th.ACCENT,
            font=("Segoe UI", 10, "bold"))
        style.map("D.Treeview", background=[("selected", th.ACCENT)])

        container = tk.Frame(frame, bg=th.BG)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        scrollbar = tk.Scrollbar(container, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        tree = ttk.Treeview(
            container, columns=columns, show="headings",
            style="D.Treeview", yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=tree.yview)

        for i, col in enumerate(columns):
            w = col_widths[i] if col_widths else 120
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor=tk.CENTER)

        tree.tag_configure("alt",    background=th.SURFACE_BG)
        tree.tag_configure("green",  background="#1a3a1f", foreground=th.GREEN)
        tree.tag_configure("red",    background="#3a1a1a", foreground=th.RED)
        tree.tag_configure("yellow", background="#3a3010", foreground=th.YELLOW)

        for i, row in enumerate(rows):
            tag = row[-1] if isinstance(row[-1], str) and row[-1] in ("alt", "green", "red", "yellow") else ("alt" if i % 2 else "")
            values = row[:-1] if tag in ("alt", "green", "red", "yellow") else row
            tree.insert("", tk.END, values=values, tags=(tag,))

        tree.pack(fill=tk.BOTH, expand=True)
        return tree

    def _stat_box(self, frame, stats):
        """Show a stats row at the bottom."""
        bar = tk.Frame(frame, bg=th.SIDEBAR_BG, padx=15, pady=10)
        bar.pack(fill=tk.X, side=tk.BOTTOM)
        for label, value in stats:
            f = tk.Frame(bar, bg=th.SIDEBAR_BG)
            f.pack(side=tk.LEFT, padx=15)
            tk.Label(f, text=label, font=th.FONT_SMALL,
                     bg=th.SIDEBAR_BG, fg=th.TEXT_DIM).pack()
            tk.Label(f, text=str(value), font=("Segoe UI", 13, "bold"),
                     bg=th.SIDEBAR_BG, fg=th.ACCENT).pack()

    # ── Exercise: listas01 ──────────────────────────────────────────────────

    def _show_listas01(self):
        self._ui["desc_lbl"].configure(text="Practicas_1 / listas01.py")
        mod, _ = import_module_captured(os.path.join(P1, "listas01.py"), "listas01")
        if mod is None:
            return

        meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
                 "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
        toneladas = [12,24,16,15,20,18,6,10,12,11,15,12]
        promedio  = sum(toneladas) / len(toneladas)

        rows = []
        for i, (mes, ton) in enumerate(zip(meses, toneladas)):
            if ton >= promedio:
                rows.append((mes, ton, f"↑ Superior ({ton:.1f} ≥ {promedio:.1f})", "green"))
            else:
                rows.append((mes, ton, f"↓ Inferior ({ton:.1f} < {promedio:.1f})", "red"))

        title = tk.Label(self._ui["viz_frame"],
            text="Toneladas de Cosecha — Análisis Anual",
            font=th.FONT_SUBTITLE, bg=th.BG, fg=th.TEXT_BRIGHT)
        title.pack(pady=(18, 0))

        self._make_tree(
            self._ui["viz_frame"],
            columns=["Mes", "Toneladas", "Comparación con Promedio"],
            rows=rows,
            col_widths=[130, 100, 280],
        )
        sup = sum(1 for t in toneladas if t >= promedio)
        inf = len(toneladas) - sup
        self._stat_box(self._ui["viz_frame"], [
            ("Promedio Anual", f"{promedio:.2f} ton"),
            ("Meses Superiores", sup),
            ("Meses Inferiores", inf),
        ])

    # ── Exercise: listas02 ──────────────────────────────────────────────────

    def _show_listas02(self):
        self._ui["desc_lbl"].configure(text="Practicas_1 / listas02.py")
        calificaciones = [8,8,7,5,10,9,9,5,6,10]
        promedio = sum(calificaciones) / len(calificaciones)

        rows = []
        for i, c in enumerate(calificaciones):
            if c >= 7:
                rows.append((f"Alumno {i+1}", c, "✓ Aprobado", "green" if c >= 8 else ""))
            else:
                rows.append((f"Alumno {i+1}", c, "✗ Reprobado", "red"))

        title = tk.Label(self._ui["viz_frame"],
            text="Calificaciones del Grupo — Análisis",
            font=th.FONT_SUBTITLE, bg=th.BG, fg=th.TEXT_BRIGHT)
        title.pack(pady=(18, 0))

        self._make_tree(
            self._ui["viz_frame"],
            columns=["Alumno", "Calificación", "Resultado"],
            rows=rows,
            col_widths=[130, 130, 200],
        )
        aprobados  = sum(1 for c in calificaciones if c >= 7)
        reprobados = len(calificaciones) - aprobados
        mayor8     = sum(1 for c in calificaciones if c >= 8)
        self._stat_box(self._ui["viz_frame"], [
            ("Promedio", f"{promedio:.1f}"),
            ("Aprobados", f"{aprobados} ({aprobados*100//len(calificaciones)}%)"),
            ("Reprobados", f"{reprobados} ({reprobados*100//len(calificaciones)}%)"),
            ("≥ 8 puntos", mayor8),
        ])

    # ── Exercise: cadenas01 ─────────────────────────────────────────────────

    def _show_cadenas01(self):
        self._ui["desc_lbl"].configure(text="Practicas_1 / cadenas01.py")
        cadena = "Parangaricutirimicuaro"

        freq = {}
        for ch in cadena:
            freq[ch] = freq.get(ch, 0) + 1
        sorted_freq = sorted(freq.items(), key=lambda x: -x[1])

        title = tk.Label(self._ui["viz_frame"],
            text=f'Frecuencia de letras en: "{cadena}"',
            font=th.FONT_SUBTITLE, bg=th.BG, fg=th.TEXT_BRIGHT)
        title.pack(pady=(18, 0))

        rows = []
        for i, (ch, cnt) in enumerate(sorted_freq):
            bar = "█" * cnt
            tag = "green" if cnt >= 4 else ("yellow" if cnt >= 2 else "")
            rows.append((ch, cnt, bar, tag))

        self._make_tree(
            self._ui["viz_frame"],
            columns=["Letra", "Frecuencia", "Representación"],
            rows=rows,
            col_widths=[100, 110, 300],
        )
        self._stat_box(self._ui["viz_frame"], [
            ("Cadena", cadena),
            ("Total caracteres", len(cadena)),
            ("Letras únicas", len(freq)),
            ("Más frecuente", f'"{sorted_freq[0][0]}" ({sorted_freq[0][1]}x)'),
        ])

    # ── Exercise: numEnteros01 ──────────────────────────────────────────────

    def _show_numEnteros01(self):
        self._ui["desc_lbl"].configure(text="Practicas_1 / numEnteros01.py")
        original = [1,2,4,4,4,5,7,9,11,11,13,14,15,16,16]
        limpio   = list(dict.fromkeys(original))

        title = tk.Label(self._ui["viz_frame"],
            text="Eliminación de Números Repetidos",
            font=th.FONT_SUBTITLE, bg=th.BG, fg=th.TEXT_BRIGHT)
        title.pack(pady=(18, 4))

        # Visual comparison
        outer = tk.Frame(self._ui["viz_frame"], bg=th.BG)
        outer.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)

        self._num_panel(outer, "Arreglo Original", original, highlight_dupes=True)
        tk.Label(outer, text="→", font=("Segoe UI", 22, "bold"),
                 bg=th.BG, fg=th.ACCENT).pack(side=tk.LEFT, padx=15)
        self._num_panel(outer, "Sin Repetidos", limpio)

        self._stat_box(self._ui["viz_frame"], [
            ("Longitud original", len(original)),
            ("Longitud resultante", len(limpio)),
            ("Duplicados eliminados", len(original) - len(limpio)),
        ])

    def _num_panel(self, parent, label, nums, highlight_dupes=False):
        frame = tk.Frame(parent, bg=th.PANEL_BG, padx=15, pady=15)
        frame.pack(side=tk.LEFT, fill=tk.BOTH)

        tk.Label(frame, text=label, font=("Segoe UI", 10, "bold"),
                 bg=th.PANEL_BG, fg=th.TEXT_DIM).pack(pady=(0, 10))

        seen = set()
        for n in nums:
            is_dup = highlight_dupes and n in seen
            color = th.RED if is_dup else th.ACCENT
            cell = tk.Frame(frame, bg=color, padx=14, pady=8)
            cell.pack(fill=tk.X, pady=2)
            lbl_text = f"{n}  ✕" if is_dup else str(n)
            tk.Label(cell, text=lbl_text, font=th.FONT_MONO,
                     bg=color, fg="white").pack()
            seen.add(n)
