"""
Estructuras Lineales — Practicas 3, 4 y 5
Exercises: colas, bicolas, deque, colaCircular, ejercicioCircular,
           Tareas, pila, cola, dulces
"""
import tkinter as tk
import math
import os

import theme as th
from vistas._layout import make_exercise_view, make_nav_btn, make_ctrl_btn, load_code
from adaptadores.capture import path_for

P3 = path_for("Practicas_3")
P4 = path_for("Practica_4")
P5 = path_for("Practica_5")

EXERCISES = [
    ("Colas — Cola Bancaria",         "colas",           P3),
    ("Bicolas — Doble Extremo",       "bicolas",         P3),
    ("Deque — Cola con Historial",    "deque_p3",        P3),
    ("Cola Circular — Clase",         "colaCircular",    P4),
    ("Ej. Circular — Turnos",         "ejercicioCirc",   P4),
    ("Tareas — Cola con Reintentos",  "Tareas",          P4),
    ("Pila — LIFO",                   "pila",            P5),
    ("Cola — FIFO",                   "cola_p5",         P5),
    ("Dulces — Pipeline Cola→Pila",   "dulces",          P5),
]

BLOCK_W, BLOCK_H = 82, 46
GAP = 6


# ─── Drawing helpers ─────────────────────────────────────────────────────────

def draw_queue_h(canvas, items, label="", highlights=None, colors=None):
    """Draw horizontal queue. highlights: set of indices with special color."""
    canvas.delete("all")
    if not canvas.winfo_width(): canvas.update_idletasks()
    cw = canvas.winfo_width() or 640
    ch = canvas.winfo_height() or 200

    n = len(items)
    bw = min(BLOCK_W, max(50, (cw - 60) // max(n, 1) - GAP))
    total_w = n * bw + (n-1) * GAP
    sx = max(10, (cw - total_w) // 2)
    sy = ch // 2 - BLOCK_H // 2

    highlights = highlights or set()
    colors = colors or {}

    for i, val in enumerate(items):
        x0 = sx + i * (bw + GAP)
        y0 = sy
        fill = colors.get(i, (th.GREEN if i in highlights else th.ACCENT))
        canvas.create_rectangle(x0, y0, x0+bw, y0+BLOCK_H,
                                fill=fill, outline=th.SURFACE_BG, width=2)
        canvas.create_text(x0+bw//2, y0+BLOCK_H//2, text=str(val),
                           font=th.FONT_MONO, fill="white")

    if n > 0:
        canvas.create_text(sx + bw//2, sy - 18,
                           text="FRENTE", font=th.FONT_SMALL, fill=th.YELLOW)
        canvas.create_text(sx + (n-1)*(bw+GAP) + bw//2, sy - 18,
                           text="FINAL", font=th.FONT_SMALL, fill=th.ORANGE)

    if label:
        canvas.create_text(cw//2, ch - 18, text=label,
                           font=th.FONT_BODY, fill=th.TEXT)


def draw_stack_v(canvas, items, op_label=""):
    """Draw vertical stack (LIFO)."""
    canvas.delete("all")
    if not canvas.winfo_width(): canvas.update_idletasks()
    cw = canvas.winfo_width() or 400
    ch = canvas.winfo_height() or 380

    bw, bh = 160, 44
    n = len(items)
    total_h = n * bh + (n-1) * GAP
    sx = (cw - bw) // 2
    base_y = ch // 2 + total_h // 2

    # Base line
    canvas.create_line(sx - 10, base_y + 4, sx + bw + 10, base_y + 4,
                       fill=th.BORDER, width=3)

    for i, val in enumerate(items):
        # Items[0] = bottom, items[-1] = top visually
        y0 = base_y - (i+1) * bh - i * GAP
        fill = th.GREEN if i == n-1 else th.ACCENT
        canvas.create_rectangle(sx, y0, sx+bw, y0+bh,
                                fill=fill, outline=th.SURFACE_BG, width=2)
        canvas.create_text(sx+bw//2, y0+bh//2, text=str(val),
                           font=th.FONT_MONO, fill="white")
        if i == n-1:
            canvas.create_text(sx+bw+20, y0+bh//2,
                               text="← TOP", font=th.FONT_SMALL, fill=th.GREEN)

    if not items:
        canvas.create_text(cw//2, ch//2,
                           text="[Pila vacía]", font=th.FONT_BODY, fill=th.TEXT_DIM)

    if op_label:
        canvas.create_text(cw//2, 20, text=op_label,
                           font=th.FONT_BODY, fill=th.YELLOW)


def draw_circular_queue(canvas, slots, frente, final, cap):
    """Draw circular queue as a circle of slots."""
    canvas.delete("all")
    if not canvas.winfo_width(): canvas.update_idletasks()
    cw = canvas.winfo_width() or 420
    ch = canvas.winfo_height() or 340

    cx, cy = cw // 2, ch // 2
    radius = min(cw, ch) // 2 - 60
    slot_w, slot_h = 60, 36

    for i in range(cap):
        angle = math.radians(-90 + i * (360 / cap))
        sx = cx + int(radius * math.cos(angle))
        sy = cy + int(radius * math.sin(angle))

        val = slots[i]
        if val is None:
            fill = th.SURFACE_BG
            text = "—"
            txt_color = th.TEXT_DIM
        else:
            fill = th.ACCENT
            text = str(val)
            txt_color = "white"

        if i == frente and frente != -1:
            fill = th.GREEN
        if i == final and final != -1 and i != frente:
            fill = th.ORANGE

        canvas.create_rectangle(sx - slot_w//2, sy - slot_h//2,
                                sx + slot_w//2, sy + slot_h//2,
                                fill=fill, outline=th.BORDER, width=2)
        canvas.create_text(sx, sy, text=text, font=th.FONT_MONO, fill=txt_color)
        canvas.create_text(sx, sy - slot_h//2 - 12, text=str(i),
                           font=th.FONT_SMALL, fill=th.TEXT_DIM)

    # Legend
    canvas.create_text(cx, cy - 14, text="FRENTE ●",
                       font=th.FONT_SMALL, fill=th.GREEN)
    canvas.create_text(cx, cy + 14, text="FINAL ●",
                       font=th.FONT_SMALL, fill=th.ORANGE)


# ─── Main view ───────────────────────────────────────────────────────────────

class LinealesView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=th.BG)
        self._ui = make_exercise_view(self)
        self._ui["root"].pack(fill=tk.BOTH, expand=True)

        self._nav_btns = []
        self._steps    = []
        self._step_idx = 0
        self._after_id = None
        self._canvas   = None

        self._build_nav()
        self._select(0)

    def _build_nav(self):
        for i, (label, _, _) in enumerate(EXERCISES):
            btn = make_nav_btn(self._ui["left"], label, lambda i=i: self._select(i))
            self._nav_btns.append(btn)

    def _select(self, idx):
        self._cancel_anim()
        for i, btn in enumerate(self._nav_btns):
            btn.configure(
                bg=th.PANEL_BG if i == idx else th.SIDEBAR_BG,
                fg=th.ACCENT  if i == idx else th.TEXT,
            )
        label, key, folder = EXERCISES[idx]
        self._ui["title_lbl"].configure(text=label)

        # Map key to actual filename
        fname_map = {
            "deque_p3":     "deque",
            "ejercicioCirc":"ejercicioCircular",
            "cola_p5":      "cola",
        }
        fname = fname_map.get(key, key)
        load_code(self._ui["code_text"], os.path.join(folder, fname + ".py"))

        self._clear_viz()
        getattr(self, f"_setup_{key}")()

    # ── Anim helpers ────────────────────────────────────────────────────────

    def _clear_viz(self):
        for w in self._ui["viz_frame"].winfo_children():
            w.destroy()
        for w in self._ui["ctrl_frame"].winfo_children():
            w.destroy()
        self._canvas = None
        self._steps = []
        self._step_idx = 0

    def _make_canvas(self, bg=th.BG, height=260):
        lbl_frame = tk.Frame(self._ui["viz_frame"], bg=th.BG)
        lbl_frame.pack(fill=tk.BOTH, expand=True)
        c = tk.Canvas(lbl_frame, bg=bg, highlightthickness=0)
        c.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self._canvas = c
        return c

    def _make_controls(self):
        ctrl = self._ui["ctrl_frame"]
        make_ctrl_btn(ctrl, "▶  Iniciar",    self._play,  th.GREEN)
        make_ctrl_btn(ctrl, "⏭  Paso",       self._step,  th.ACCENT)
        make_ctrl_btn(ctrl, "↺  Reiniciar",  self._reset, th.YELLOW)
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
        self._animate()

    def _animate(self):
        if self._step_idx < len(self._steps):
            self._draw_current()
            self._step_idx += 1
            self._after_id = self.after(th.ANIM_SPEED, self._animate)

    def _step(self):
        self._cancel_anim()
        if self._step_idx < len(self._steps):
            self._draw_current()
            self._step_idx += 1

    def _reset(self):
        self._cancel_anim()
        self._step_idx = 0
        if self._steps:
            self._draw_current()

    def _draw_current(self):
        if not self._steps:
            return
        step = self._steps[self._step_idx] if self._step_idx < len(self._steps) else self._steps[-1]
        self._draw_fn(step)
        total = len(self._steps)
        disp  = min(self._step_idx + 1, total)
        if hasattr(self, "_step_lbl"):
            self._step_lbl.configure(text=f"Paso {disp} / {total}")

    # ── colas (Practicas_3) ─────────────────────────────────────────────────

    def _setup_colas(self):
        tk.Label(self._ui["viz_frame"],
            text="Cola Bancaria FIFO — Retiros y Depósitos",
            font=th.FONT_SUBTITLE, bg=th.BG, fg=th.TEXT_BRIGHT,
        ).pack(pady=(12, 0))

        c = self._make_canvas()
        self._make_controls()

        saldos = [1000, 1000, 1000, 1000, 1000]
        steps  = [{"q": list(saldos), "label": "Estado inicial — 5 cuentas con $1000"}]

        q = list(saldos)
        for _ in range(5):
            nuevo = q[0] - 500
            q.pop(0); q.append(nuevo)
            steps.append({"q": list(q), "label": f"retiro(500) → saldo actualizado: ${nuevo}", "hl": len(q)-1})

        for _ in range(5):
            nuevo = q[0] + 300
            q.pop(0); q.append(nuevo)
            steps.append({"q": list(q), "label": f"deposito(300) → saldo actualizado: ${nuevo}", "hl": len(q)-1})

        self._steps = steps
        self._draw_fn = lambda s: draw_queue_h(
            c, s["q"], label=s["label"],
            highlights={s["hl"]} if "hl" in s else set()
        )
        self._draw_current()

    # ── bicolas (Practicas_3) ────────────────────────────────────────────────

    def _setup_bicolas(self):
        tk.Label(self._ui["viz_frame"],
            text="Bicola — Operaciones por Cabeza y Cola",
            font=th.FONT_SUBTITLE, bg=th.BG, fg=th.TEXT_BRIGHT,
        ).pack(pady=(12, 0))

        c = self._make_canvas()
        self._make_controls()

        saldos  = [1000, 1000, 1000, 1000, 1000]
        retiros_montos = [500, 400, 300, 200, 100]
        dep_montos     = [400, 300, 300, 300, 400]

        steps = [{"q": list(saldos), "label": "Estado inicial", "hl": -1}]
        q = list(saldos)

        for m in retiros_montos:
            nuevo = q[0] - m
            q.pop(0); q.insert(0, nuevo)
            steps.append({"q": list(q), "label": f"retiro_cabeza({m}) → ${nuevo}", "hl": 0,
                          "colors": {0: th.GREEN}})

        for m in dep_montos:
            nuevo = q[-1] + m
            q.pop(); q.append(nuevo)
            steps.append({"q": list(q), "label": f"deposito_cola({m}) → ${nuevo}", "hl": len(q)-1,
                          "colors": {len(q)-1: th.ORANGE}})

        self._steps = steps
        self._draw_fn = lambda s: draw_queue_h(
            c, s["q"], label=s["label"],
            highlights={s.get("hl", -1)} if s.get("hl", -1) >= 0 else set(),
            colors=s.get("colors", {})
        )
        self._draw_current()

    # ── deque (Practicas_3) ──────────────────────────────────────────────────

    def _setup_deque_p3(self):
        tk.Label(self._ui["viz_frame"],
            text="Deque — Cola con Historial (maxlen=5)",
            font=th.FONT_SUBTITLE, bg=th.BG, fg=th.TEXT_BRIGHT,
        ).pack(pady=(12, 0))

        c = self._make_canvas(height=320)
        hist_lbl = tk.Label(self._ui["viz_frame"], text="Historial: []",
                            font=th.FONT_BODY, bg=th.BG, fg=th.TEXT_DIM)
        hist_lbl.pack()
        self._make_controls()

        from collections import deque as Deque
        saldos   = Deque()
        historial = Deque(maxlen=5)
        for _ in range(5):
            saldos.append(1000)

        steps = []

        def snap(label, hl=-1):
            steps.append({
                "q": list(saldos), "hist": list(historial),
                "label": label, "hl": hl
            })

        snap("Estado inicial — 5 cuentas con $1000")

        for _ in range(5):
            orig = saldos.popleft()
            historial.append(orig)
            saldos.append(orig - 500)
            snap(f"retiro(500): ${orig} → ${orig-500}", len(saldos)-1)

        for _ in range(5):
            orig = saldos.popleft()
            historial.append(orig)
            saldos.append(orig + 300)
            snap(f"deposito(300): ${orig} → ${orig+300}", len(saldos)-1)

        self._steps = steps

        def render(s):
            draw_queue_h(c, s["q"], label=s["label"],
                         highlights={s["hl"]} if s["hl"] >= 0 else set())
            hist_lbl.configure(text=f"Historial (últimos 5 originales): {s['hist']}")

        self._draw_fn = render
        self._draw_current()

    # ── colaCircular ────────────────────────────────────────────────────────

    def _setup_colaCircular(self):
        tk.Label(self._ui["viz_frame"],
            text="Cola Circular — Aritmética Modular",
            font=th.FONT_SUBTITLE, bg=th.BG, fg=th.TEXT_BRIGHT,
        ).pack(pady=(12, 0))

        c = self._make_canvas(height=360)
        self._make_controls()

        cap = 5
        slots = [None] * cap
        frente, final = -1, -1

        steps = [{"slots": list(slots), "f": frente, "fin": final,
                  "label": "Cola circular vacía (cap=5)"}]

        # Simulate encolar 5 items
        data = [10, 20, 30, 40, 50]
        for d in data:
            if frente == -1:
                frente = final = 0
            else:
                final = (final + 1) % cap
            slots[final] = d
            steps.append({"slots": list(slots), "f": frente, "fin": final,
                          "label": f"encolar({d})"})

        # Simulate desencolar 2
        for _ in range(2):
            val = slots[frente]
            if frente == final:
                slots[frente] = None; frente = final = -1
            else:
                slots[frente] = None
                frente = (frente + 1) % cap
            steps.append({"slots": list(slots), "f": frente, "fin": final,
                          "label": f"desencolar() → {val}"})

        # Encolar one more
        if frente == -1:
            frente = final = 0
        else:
            final = (final + 1) % cap
        slots[final] = 99
        steps.append({"slots": list(slots), "f": frente, "fin": final,
                      "label": "encolar(99) — reutiliza espacio liberado"})

        self._steps = steps
        self._draw_fn = lambda s: (
            draw_circular_queue(c, s["slots"], s["f"], s["fin"], cap),
            c.create_text(c.winfo_width()//2, c.winfo_height()-22,
                          text=s["label"], font=th.FONT_BODY, fill=th.YELLOW)
        )
        self._draw_current()

    # ── ejercicioCircular ────────────────────────────────────────────────────

    def _setup_ejercicioCirc(self):
        tk.Label(self._ui["viz_frame"],
            text="Ejercicio Circular — Sistema de Turnos",
            font=th.FONT_SUBTITLE, bg=th.BG, fg=th.TEXT_BRIGHT,
        ).pack(pady=(12, 0))

        c = self._make_canvas(height=360)
        self._make_controls()

        cap    = 5
        turnos = ["A01", "A02", "A03", "A04", "A05", "A06"]
        slots  = [None] * cap
        frente, final = -1, -1
        steps  = [{"slots": list(slots), "f": frente, "fin": final,
                   "label": "Cola vacía — Iniciando sistema de turnos"}]

        # Encolar 5 turnos
        for t in turnos[:5]:
            if frente == -1:
                frente = final = 0
            else:
                final = (final + 1) % cap
            slots[final] = t
            steps.append({"slots": list(slots), "f": frente, "fin": final,
                          "label": f"encolar({t})"})

        # Desencolar A01
        val = slots[frente]
        if frente == final:
            slots[frente] = None; frente = final = -1
        else:
            slots[frente] = None
            frente = (frente + 1) % cap
        steps.append({"slots": list(slots), "f": frente, "fin": final,
                      "label": f"Turno atendido: {val}  |  Frente → {slots[frente]}"})

        # Encolar A06
        final = (final + 1) % cap
        slots[final] = turnos[5]
        steps.append({"slots": list(slots), "f": frente, "fin": final,
                      "label": f"encolar(A06) — espacio reutilizado"})

        self._steps = steps
        self._draw_fn = lambda s: (
            draw_circular_queue(c, s["slots"], s["f"], s["fin"], cap),
            c.create_text(c.winfo_width()//2, c.winfo_height()-22,
                          text=s["label"], font=th.FONT_BODY, fill=th.YELLOW)
        )
        self._draw_current()

    # ── Tareas ───────────────────────────────────────────────────────────────

    def _setup_Tareas(self):
        tk.Label(self._ui["viz_frame"],
            text="Gestor de Tareas — Cola con Reintentos",
            font=th.FONT_SUBTITLE, bg=th.BG, fg=th.TEXT_BRIGHT,
        ).pack(pady=(12, 0))

        c = tk.Canvas(self._ui["viz_frame"], bg=th.BG, highlightthickness=0, height=280)
        c.pack(fill=tk.X, padx=10, pady=10)
        self._canvas = c

        log_frame = tk.Frame(self._ui["viz_frame"], bg=th.PANEL_BG)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 5))
        log_text = tk.Text(log_frame, font=th.FONT_CODE, bg=th.PANEL_BG, fg=th.TEXT,
                           state=tk.DISABLED, height=5, wrap=tk.WORD, relief=tk.FLAT)
        log_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=5)

        self._make_controls()

        init_tasks = [
            {"nombre": "T1", "fallos": 1, "intentos": 0},
            {"nombre": "T2", "fallos": 0, "intentos": 0},
            {"nombre": "T3", "fallos": 2, "intentos": 0},
            {"nombre": "T4", "fallos": 1, "intentos": 0},
            {"nombre": "T5", "fallos": 2, "intentos": 2},
            {"nombre": "T6", "fallos": 2, "intentos": 1},
        ]

        import copy

        def make_step(queue, event_msg):
            return {"queue": copy.deepcopy(queue), "msg": event_msg}

        def fallo(queue):
            if not queue: return ""
            t = queue[0]
            t["fallos"] -= 1; t["intentos"] += 1
            msg = f"FALLO: {t['nombre']} (fallos={t['fallos']}, intentos={t['intentos']})"
            queue.append(queue.pop(0))
            return msg

        def exito(queue):
            if not queue: return ""
            t = queue[0]
            msg = f"ÉXITO: {t['nombre']} completada ✓"
            queue.pop(0)
            return msg

        q = copy.deepcopy(init_tasks)
        steps = [make_step(q, "Estado inicial — 6 tareas en cola")]
        for fn, name in [(fallo,"fallo"),(exito,"exito"),(fallo,"fallo"),
                          (fallo,"fallo"),(fallo,"fallo"),(fallo,"fallo")]:
            msg = fn(q)
            steps.append(make_step(q, msg))

        self._steps = steps

        def draw_tasks(step):
            c.delete("all")
            cw = c.winfo_width() or 640
            tasks = step["queue"]
            n = len(tasks)
            if n == 0:
                c.create_text(cw//2, 140, text="Cola vacía",
                              font=th.FONT_SUBTITLE, fill=th.TEXT_DIM)
                return
            bw = min(90, (cw - 40) // max(n, 1) - 8)
            sx = (cw - (n * (bw+8))) // 2
            for i, t in enumerate(tasks):
                x0 = sx + i * (bw + 8)
                fill = th.GREEN if i == 0 else (th.SURFACE_BG if t["fallos"] == 0 else th.ACCENT)
                c.create_rectangle(x0, 60, x0+bw, 60+90,
                                   fill=fill, outline=th.BORDER, width=2)
                c.create_text(x0+bw//2, 60+22, text=t["nombre"],
                              font=("Segoe UI", 11, "bold"), fill="white")
                c.create_text(x0+bw//2, 60+48, text=f"F:{t['fallos']}",
                              font=th.FONT_SMALL, fill=th.RED)
                c.create_text(x0+bw//2, 60+68, text=f"I:{t['intentos']}",
                              font=th.FONT_SMALL, fill=th.YELLOW)

            c.create_text(sx+bw//2, 40, text="HEAD", font=th.FONT_SMALL, fill=th.YELLOW)

            # Log
            log_text.configure(state=tk.NORMAL)
            log_text.delete("1.0", tk.END)
            log_text.insert(tk.END, "▶ " + step["msg"])
            log_text.configure(state=tk.DISABLED)

        self._draw_fn = draw_tasks
        self._draw_current()

    # ── pila ─────────────────────────────────────────────────────────────────

    def _setup_pila(self):
        tk.Label(self._ui["viz_frame"],
            text="Pila — Estructura LIFO",
            font=th.FONT_SUBTITLE, bg=th.BG, fg=th.TEXT_BRIGHT,
        ).pack(pady=(12, 0))

        c = self._make_canvas(height=340)
        self._make_controls()

        ops = [
            ("push", 15), ("push", 7), ("push", 23), ("push", 4),
            ("peek", None), ("pop", None), ("push", 11),
            ("pop", None), ("pop", None),
        ]

        pila = []
        steps = [{"stack": [], "label": "Pila vacía"}]
        for op, val in ops:
            if op == "push":
                pila.append(val)
                steps.append({"stack": list(pila), "label": f"push({val})"})
            elif op == "pop":
                v = pila.pop() if pila else None
                steps.append({"stack": list(pila), "label": f"pop() → {v}"})
            elif op == "peek":
                v = pila[-1] if pila else None
                steps.append({"stack": list(pila), "label": f"peek() → {v}"})

        self._steps = steps
        self._draw_fn = lambda s: draw_stack_v(c, s["stack"], s["label"])
        self._draw_current()

    # ── cola (Practica_5) ────────────────────────────────────────────────────

    def _setup_cola_p5(self):
        tk.Label(self._ui["viz_frame"],
            text="Cola — Estructura FIFO",
            font=th.FONT_SUBTITLE, bg=th.BG, fg=th.TEXT_BRIGHT,
        ).pack(pady=(12, 0))

        c = self._make_canvas()
        self._make_controls()

        ops = [
            ("enque", "Alfa"), ("enque", "Beta"), ("enque", "Gamma"),
            ("deque", None), ("enque", "Delta"), ("deque", None),
            ("enque", "Épsilon"), ("deque", None),
        ]

        cola  = []
        steps = [{"q": [], "label": "Cola vacía"}]
        for op, val in ops:
            if op == "enque":
                cola.append(val)
                steps.append({"q": list(cola), "label": f"enque('{val}')", "hl": len(cola)-1})
            elif op == "deque":
                v = cola.pop(0) if cola else None
                steps.append({"q": list(cola), "label": f"deque() → '{v}'"})

        self._steps = steps
        self._draw_fn = lambda s: draw_queue_h(
            c, s["q"], label=s["label"],
            highlights={s["hl"]} if "hl" in s else set()
        )
        self._draw_current()

    # ── dulces ───────────────────────────────────────────────────────────────

    def _setup_dulces(self):
        tk.Label(self._ui["viz_frame"],
            text="Dulces — Pipeline: Cola → Pila → Lista",
            font=th.FONT_SUBTITLE, bg=th.BG, fg=th.TEXT_BRIGHT,
        ).pack(pady=(12, 0))

        body = tk.Frame(self._ui["viz_frame"], bg=th.BG)
        body.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Three sub-canvases side by side — use grid for guaranteed equal width
        for i in range(3):
            body.columnconfigure(i, weight=1, minsize=120)
        body.rowconfigure(0, weight=0)
        body.rowconfigure(1, weight=1)

        for i, (title, attr) in enumerate([("Cola (FIFO)", "_c_cola"),
                                            ("Pila (LIFO)", "_c_pila"),
                                            ("Lista (Resultado)", "_c_lista")]):
            tk.Label(body, text=title, font=("Segoe UI", 9, "bold"),
                     bg=th.BG, fg=th.TEXT_DIM).grid(row=0, column=i, pady=(0, 2))
            canvas = tk.Canvas(body, bg=th.PANEL_BG, highlightthickness=0)
            canvas.grid(row=1, column=i, sticky="nsew", padx=3, pady=3)
            setattr(self, attr, canvas)

        stats_lbl = tk.Label(self._ui["viz_frame"], text="",
                             font=th.FONT_BODY, bg=th.BG, fg=th.YELLOW)
        stats_lbl.pack(pady=3)

        self._make_controls()

        datos = [1200.5, 11890.0, 13010.35, 14100.0, 13650.8,
                 14999.99, 15800.0, 16250.25, 15120.0, 14780.4,
                 13999.0, 15550.75]

        # Compute phases
        cola_state = list(datos)
        pila_state = []
        lista_state = []

        steps = [{"cola": list(cola_state), "pila": [], "lista": [],
                  "stats": "", "phase": "Cola inicial con datos"}]

        # pasar_a_pila
        for d in cola_state:
            pila_state.insert(0, d)
        cola_state = []
        steps.append({"cola": [], "pila": list(pila_state), "lista": [],
                      "stats": "", "phase": "pasar_a_pila() — Cola → Pila (invertida)"})

        # pasar_a_lista
        for _ in range(len(pila_state)):
            lista_state.append(pila_state.pop(0))
        steps.append({"cola": [], "pila": [], "lista": list(lista_state),
                      "stats": "", "phase": "pasar_a_lista() — Pila → Lista"})

        media    = sum(lista_state) / len(lista_state)
        varianza = sum((x - media)**2 for x in lista_state) / len(lista_state)
        steps.append({"cola": [], "pila": [], "lista": list(lista_state),
                      "stats": f"Media: {media:,.2f}   |   Varianza: {varianza:,.2f}",
                      "phase": "Estadísticas calculadas"})

        self._steps = steps

        def mini_draw(canvas, items, vertical=False):
            canvas.delete("all")
            canvas.update_idletasks()
            cw = canvas.winfo_width() or 160
            ch = canvas.winfo_height() or 240
            if not items:
                canvas.create_text(cw//2, ch//2, text="vacío",
                                   font=th.FONT_SMALL, fill=th.TEXT_DIM)
                return
            n   = len(items)
            bh  = min(30, (ch - 20) // max(n, 1) - 2)
            bw  = max(60, cw - 20)
            sy  = (ch - n*(bh+2)) // 2
            for i, val in enumerate(items):
                y0 = sy + i*(bh+2)
                fill = th.GREEN if i == 0 else (th.ACCENT if i % 2 == 0 else th.PANEL_BG)
                canvas.create_rectangle(10, y0, 10+bw, y0+bh,
                                        fill=fill, outline=th.BORDER, width=1)
                text = f"{val:.0f}" if isinstance(val, float) else str(val)
                canvas.create_text(10+bw//2, y0+bh//2, text=text,
                                   font=("Segoe UI", 8), fill="white")

        def render(s):
            mini_draw(self._c_cola,  s["cola"])
            mini_draw(self._c_pila,  s["pila"])
            mini_draw(self._c_lista, s["lista"])
            stats_lbl.configure(text=s["phase"] + ("   →   " + s["stats"] if s["stats"] else ""))

        self._draw_fn = render
        self._draw_current()
