import tkinter as tk
import theme as th


class HomeView(tk.Frame):
    def __init__(self, parent, navigate):
        super().__init__(parent, bg=th.BG)
        self._navigate = navigate
        self._build()

    def _build(self):
        tk.Frame(self, bg=th.BG, height=55).pack()

        tk.Label(
            self,
            text="Estructura de Datos - Proyecto Final Integrador",
            font=("Segoe UI", 30, "bold"),
            bg=th.BG,
            fg=th.TEXT_BRIGHT,
        ).pack()

        tk.Label(
            self,
            text="Visualizador Interactivo de Algoritmos y Estructuras de Datos de la Materia ED2026",
            font=("Segoe UI", 12),
            bg=th.BG,
            fg=th.TEXT_DIM,
        ).pack(pady=(8, 50))

        grid = tk.Frame(self, bg=th.BG)
        grid.pack()

        cards = [
            ("📋", "Listas y Cadenas",
             "4 ejercicios  —  Practicas_1\nArreglos, cadenas, estadísticas básicas",
             "listas"),
            ("🔢", "Matrices y Datos",
             "4 ejercicios  —  Practicas_2\nMultiplicación, coordenadas, asientos, DataFrame",
             "matrices"),
            ("📦", "Estructuras Lineales",
             "9 ejercicios  —  Practicas 3, 4 y 5\nPilas, colas, bicolas, colas circulares",
             "lineales"),
            ("🌳", "Árboles",
             "3 ejercicios  —  Carpeta Arboles\nBST, recorridos DFS animados, BFS animado",
             "arboles"),
            ("🔗", "Grafos y Recursión",
             "4 ejercicios  —  Carpeta Grafos\nDijkstra, Prim, Kruskal, Torres de Hanoi",
             "grafos"),
        ]

        for idx, (icon, title, desc, key) in enumerate(cards):
            row, col = divmod(idx, 3)
            self._make_card(grid, icon, title, desc, key, row, col)

    def _make_card(self, parent, icon, title, desc, key, row, col):
        card = tk.Frame(parent, bg=th.PANEL_BG, padx=22, pady=18, cursor="hand2")
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        tk.Label(card, text=icon, font=("Segoe UI", 28),
                 bg=th.PANEL_BG, fg=th.ACCENT).pack(anchor=tk.W)
        tk.Label(card, text=title, font=("Segoe UI", 13, "bold"),
                 bg=th.PANEL_BG, fg=th.TEXT_BRIGHT).pack(anchor=tk.W, pady=(6, 3))
        tk.Label(card, text=desc, font=th.FONT_SMALL,
                 bg=th.PANEL_BG, fg=th.TEXT_DIM, justify=tk.LEFT).pack(anchor=tk.W)
        tk.Label(card, text="→ Abrir", font=("Segoe UI", 9),
                 bg=th.PANEL_BG, fg=th.ACCENT).pack(anchor=tk.E, pady=(12, 0))

        def on_click(e, k=key):
            self._navigate(k)

        def on_enter(e, c=card):
            c.configure(bg=th.SURFACE_BG)
            for w in c.winfo_children():
                w.configure(bg=th.SURFACE_BG)

        def on_leave(e, c=card):
            c.configure(bg=th.PANEL_BG)
            for w in c.winfo_children():
                w.configure(bg=th.PANEL_BG)

        card.bind("<Button-1>", on_click)
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        for child in card.winfo_children():
            child.bind("<Button-1>", on_click)
            child.bind("<Enter>", on_enter)
            child.bind("<Leave>", on_leave)
