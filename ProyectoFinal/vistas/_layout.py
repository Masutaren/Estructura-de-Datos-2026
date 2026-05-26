"""Shared layout helpers used by all exercise views."""
import tkinter as tk
from tkinter import ttk
import keyword
import theme as th


def make_exercise_view(parent):
    """Create the standard two-panel exercise layout.

    Returns a dict with keys:
        root        — outer Frame (fill BOTH, expand True)
        left        — left sidebar Frame for exercise buttons
        right       — right content Frame
        title_lbl   — Label for exercise title
        desc_lbl    — Label for exercise description
        viz_frame   — Frame for the visualization canvas / widget
        code_text   — Text widget showing original source code
        ctrl_frame  — Frame for control buttons
    """
    root = tk.Frame(parent, bg=th.BG)

    # ── Left panel (exercise list) ───────────────────────────────────────────
    left = tk.Frame(root, bg=th.SIDEBAR_BG, width=200)
    left.pack(side=tk.LEFT, fill=tk.Y)
    left.pack_propagate(False)

    tk.Label(
        left,
        text="  EJERCICIOS",
        font=("Segoe UI", 8, "bold"),
        bg=th.SIDEBAR_BG,
        fg=th.TEXT_DIM,
    ).pack(anchor=tk.W, padx=5, pady=(12, 6))

    tk.Frame(left, bg=th.BORDER, height=1).pack(fill=tk.X, padx=10)

    # ── Right panel ──────────────────────────────────────────────────────────
    right = tk.Frame(root, bg=th.BG)
    right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Title bar
    title_bar = tk.Frame(right, bg=th.PANEL_BG, padx=16, pady=10)
    title_bar.pack(fill=tk.X)

    title_lbl = tk.Label(
        title_bar,
        text="Selecciona un ejercicio",
        font=th.FONT_SUBTITLE,
        bg=th.PANEL_BG,
        fg=th.ACCENT,
        anchor=tk.W,
    )
    title_lbl.pack(side=tk.LEFT)

    desc_lbl = tk.Label(
        title_bar,
        text="",
        font=th.FONT_SMALL,
        bg=th.PANEL_BG,
        fg=th.TEXT_DIM,
        anchor=tk.E,
    )
    desc_lbl.pack(side=tk.RIGHT)

    tk.Frame(right, bg=th.BORDER, height=1).pack(fill=tk.X)

    # Paned window: visualization (left 60%) + code (right 40%)
    paned = tk.PanedWindow(
        right,
        orient=tk.HORIZONTAL,
        bg=th.SURFACE_BG,
        sashwidth=5,
        sashrelief=tk.FLAT,
        handlesize=0,
    )
    paned.pack(fill=tk.BOTH, expand=True)

    viz_frame = tk.Frame(paned, bg=th.BG)
    paned.add(viz_frame, minsize=380, stretch="always")

    # Code panel
    code_outer = tk.Frame(paned, bg=th.PANEL_BG)
    paned.add(code_outer, minsize=260, stretch="never")

    code_header = tk.Frame(code_outer, bg=th.SURFACE_BG, padx=10, pady=5)
    code_header.pack(fill=tk.X)
    tk.Label(
        code_header,
        text="◈ Código Original",
        font=("Segoe UI", 9, "bold"),
        bg=th.SURFACE_BG,
        fg=th.TEXT_DIM,
    ).pack(side=tk.LEFT)

    code_scroll_y = tk.Scrollbar(code_outer, orient=tk.VERTICAL)
    code_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    code_scroll_x = tk.Scrollbar(code_outer, orient=tk.HORIZONTAL)
    code_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

    code_text = tk.Text(
        code_outer,
        font=th.FONT_CODE,
        bg="#0d1117",
        fg="#c9d1d9",
        insertbackground=th.TEXT,
        yscrollcommand=code_scroll_y.set,
        xscrollcommand=code_scroll_x.set,
        state=tk.DISABLED,
        wrap=tk.NONE,
        selectbackground=th.SURFACE_BG,
        relief=tk.FLAT,
        padx=10,
        pady=8,
    )
    code_text.pack(fill=tk.BOTH, expand=True)
    code_scroll_y.config(command=code_text.yview)
    code_scroll_x.config(command=code_text.xview)

    # Configure syntax highlight tags
    _configure_code_tags(code_text)

    # Control bar
    ctrl_frame = tk.Frame(right, bg=th.SIDEBAR_BG, padx=12, pady=7)
    ctrl_frame.pack(fill=tk.X, side=tk.BOTTOM)

    return {
        "root": root,
        "left": left,
        "right": right,
        "title_lbl": title_lbl,
        "desc_lbl": desc_lbl,
        "viz_frame": viz_frame,
        "code_text": code_text,
        "ctrl_frame": ctrl_frame,
    }


def make_nav_btn(parent, text, command, selected=False):
    """Exercise selection button for the left panel."""
    btn = tk.Button(
        parent,
        text=text,
        font=("Segoe UI", 9),
        bg=th.PANEL_BG if selected else th.SIDEBAR_BG,
        fg=th.ACCENT if selected else th.TEXT,
        bd=0,
        relief=tk.FLAT,
        activebackground=th.PANEL_BG,
        activeforeground=th.TEXT_BRIGHT,
        cursor="hand2",
        anchor=tk.W,
        padx=14,
        pady=7,
        wraplength=175,
        justify=tk.LEFT,
        command=command,
    )
    btn.pack(fill=tk.X)
    return btn


def make_ctrl_btn(parent, text, command, color=th.ACCENT):
    """Control button (Play / Step / Reset)."""
    btn = tk.Button(
        parent,
        text=text,
        font=th.FONT_BTN,
        bg=th.SURFACE_BG,
        fg=color,
        activebackground=th.PANEL_BG,
        activeforeground=color,
        bd=0,
        relief=tk.FLAT,
        cursor="hand2",
        padx=14,
        pady=5,
        command=command,
    )
    btn.pack(side=tk.LEFT, padx=4)
    return btn


def load_code(code_text, filepath):
    """Read source file and display with basic syntax highlighting."""
    import os
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
    except Exception as e:
        source = f"# No se pudo leer el archivo:\n# {e}"

    code_text.config(state=tk.NORMAL)
    code_text.delete("1.0", tk.END)
    code_text.insert("1.0", source)

    _apply_highlight(code_text)
    code_text.config(state=tk.DISABLED)
    code_text.yview_moveto(0)


def _configure_code_tags(text_widget):
    text_widget.tag_configure("kw",      foreground="#ff7b72")
    text_widget.tag_configure("builtin", foreground="#ffa657")
    text_widget.tag_configure("string",  foreground="#a5d6ff")
    text_widget.tag_configure("comment", foreground="#6e7681", font=("Consolas", 10, "italic"))
    text_widget.tag_configure("number",  foreground="#79c0ff")
    text_widget.tag_configure("defname", foreground="#d2a8ff")


def _apply_highlight(text_widget):
    """Basic Python syntax highlighting on a Text widget."""
    # Comments
    idx = "1.0"
    while True:
        idx = text_widget.search("#", idx, tk.END)
        if not idx:
            break
        line_end = text_widget.index(f"{idx} lineend")
        text_widget.tag_add("comment", idx, line_end)
        idx = line_end

    # Keywords
    for kw in keyword.kwlist:
        idx = "1.0"
        while True:
            idx = text_widget.search(r"\b" + kw + r"\b", idx, tk.END, regexp=True)
            if not idx:
                break
            end = f"{idx}+{len(kw)}c"
            text_widget.tag_add("kw", idx, end)
            idx = end

    # Built-in functions
    builtins = ["print", "len", "range", "list", "dict", "set", "int",
                "float", "str", "bool", "append", "pop", "sort", "sorted",
                "sum", "min", "max", "enumerate", "zip", "type"]
    for name in builtins:
        idx = "1.0"
        while True:
            idx = text_widget.search(r"\b" + name + r"\b", idx, tk.END, regexp=True)
            if not idx:
                break
            end = f"{idx}+{len(name)}c"
            text_widget.tag_add("builtin", idx, end)
            idx = end

    # Numbers
    idx = "1.0"
    while True:
        idx = text_widget.search(r"\b\d+(?:\.\d+)?\b", idx, tk.END, regexp=True)
        if not idx:
            break
        end_idx = text_widget.search(r"\D", idx, tk.END, regexp=True)
        if not end_idx:
            end_idx = tk.END
        text_widget.tag_add("number", idx, end_idx)
        idx = end_idx if end_idx != tk.END else tk.END
        if idx == tk.END:
            break
