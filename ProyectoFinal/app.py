import tkinter as tk
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import theme as th


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Estructura de Datos 2026 - Proyecto Final")
        self.geometry("1340x820")
        self.configure(bg=th.BG)
        self.minsize(1100, 700)

        self._frames = {}
        self._active_btn = None

        self._build_ui()
        self.show_view("home")

    # ── Layout ──────────────────────────────────────────────────────────────

    def _build_ui(self):
        # Header
        hdr = tk.Frame(self, bg=th.SIDEBAR_BG, height=th.HEADER_HEIGHT)
        hdr.pack(fill=tk.X, side=tk.TOP)
        hdr.pack_propagate(False)
        tk.Label(
            hdr,
            text="  ◆  Visualizador de Estructuras de Datos  |  Bram 2026",
            font=("Segoe UI", 12, "bold"),
            bg=th.SIDEBAR_BG,
            fg=th.TEXT_BRIGHT,
        ).pack(side=tk.LEFT, padx=15, pady=10)

        # Body
        body = tk.Frame(self, bg=th.BG)
        body.pack(fill=tk.BOTH, expand=True)

        # Sidebar
        sidebar = tk.Frame(body, bg=th.SIDEBAR_BG, width=th.SIDEBAR_WIDTH)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        self._build_nav(sidebar)

        # Divider
        tk.Frame(body, bg=th.BORDER, width=1).pack(side=tk.LEFT, fill=tk.Y)

        # Content area
        self.content = tk.Frame(body, bg=th.BG)
        self.content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _build_nav(self, sidebar):
        self._nav_buttons = {}

        categories = [
            ("🏠", "Inicio",                "home"),
            ("📋", "Listas y Cadenas",      "listas"),
            ("🔢", "Matrices y Datos",      "matrices"),
            ("📦", "Estructuras Lineales",  "lineales"),
            ("🌳", "Árboles",              "arboles"),
            ("🔗", "Grafos y Recursión",    "grafos"),
        ]

        tk.Frame(sidebar, bg=th.SIDEBAR_BG, height=12).pack(fill=tk.X)
        tk.Label(
            sidebar,
            text="  CATEGORÍAS",
            font=("Segoe UI", 8, "bold"),
            bg=th.SIDEBAR_BG,
            fg=th.TEXT_DIM,
        ).pack(anchor=tk.W, padx=5, pady=(5, 10))

        for icon, label, key in categories:
            btn = tk.Button(
                sidebar,
                text=f"  {icon}  {label}",
                font=th.FONT_NAV,
                bg=th.SIDEBAR_BG,
                fg=th.TEXT,
                bd=0,
                relief=tk.FLAT,
                activebackground=th.PANEL_BG,
                activeforeground=th.TEXT_BRIGHT,
                cursor="hand2",
                anchor=tk.W,
                padx=10,
                pady=9,
                command=lambda k=key: self.show_view(k),
            )
            btn.pack(fill=tk.X)
            self._nav_buttons[key] = btn

        # Footer
        tk.Frame(sidebar, bg=th.SIDEBAR_BG).pack(fill=tk.BOTH, expand=True)
        tk.Label(
            sidebar,
            text="Abraham Lopez Moreno · UAZ · 2026",
            font=th.FONT_SMALL,
            bg=th.SIDEBAR_BG,
            fg=th.TEXT_DIM,
        ).pack(side=tk.BOTTOM, pady=12)

    # ── Navigation ──────────────────────────────────────────────────────────

    def show_view(self, name):
        if name not in self._frames:
            self._frames[name] = self._create_view(name)

        for f in self._frames.values():
            f.pack_forget()

        self._frames[name].pack(fill=tk.BOTH, expand=True)

        if self._active_btn:
            self._active_btn.configure(bg=th.SIDEBAR_BG, fg=th.TEXT)
        if name in self._nav_buttons:
            self._nav_buttons[name].configure(bg=th.PANEL_BG, fg=th.ACCENT)
            self._active_btn = self._nav_buttons[name]

    def _create_view(self, name):
        if name == "home":
            from vistas.home import HomeView
            return HomeView(self.content, navigate=self.show_view)
        if name == "listas":
            from vistas.listas_view import ListasView
            return ListasView(self.content)
        if name == "matrices":
            from vistas.matrices_view import MatricesView
            return MatricesView(self.content)
        if name == "lineales":
            from vistas.lineales_view import LinealesView
            return LinealesView(self.content)
        if name == "arboles":
            from vistas.arboles_view import ArbolesView
            return ArbolesView(self.content)
        if name == "grafos":
            from vistas.grafos_view import GrafosView
            return GrafosView(self.content)
        return tk.Frame(self.content, bg=th.BG)
