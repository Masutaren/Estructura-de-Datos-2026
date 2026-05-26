# Visualizador de Estructuras de Datos 2026

**Proyecto Final Integrador — Estructura de Datos · Abraham Lopez Moreno · Universidad Autonoma de Zacatecas - Ingeniería en Software · 2026**

Visualizador Interactivo en Python + Tkinter que integra los ejercicios de la materia Estructura de Datos - 2026. Cada ejercicio muestra el código fuente original junto a una visualización animada e interactiva paso a paso.

---

## Requisitos

- Python 3.10 o superior
- Las dependencias listadas en `requirements.txt`

### Instalación de dependencias

```bash
pip install -r requirements.txt
```

O individualmente:

```bash
pip install pandas pillow
```

## Ejecutar

Desde la carpeta `ProyectoFinal/`:

```bash
python main.py
```

O desde la raíz del proyecto:

```bash
python ProyectoFinal/main.py
```

---

## Estructura del proyecto

```
ProyectoFinal/
├── main.py                  # Punto de entrada
├── app.py                   # Ventana principal y navegación lateral
├── theme.py                 # Paleta de colores y constantes de fuentes
├── requirements.txt
├── adaptadores/
│   └── capture.py           # Importación dinámica con captura de stdout
└── vistas/
    ├── _layout.py           # Layout compartido y resaltado de sintaxis
    ├── home.py              # Pantalla de inicio con tarjetas de navegación
    ├── listas_view.py       # Practicas_1  — 4 ejercicios
    ├── matrices_view.py     # Practicas_2  — 4 ejercicios
    ├── lineales_view.py     # Practicas 3, 4 y 5 — 9 ejercicios
    ├── arboles_view.py      # Carpeta Arboles — 3 ejercicios
    └── grafos_view.py       # Carpeta Grafos  — 4 ejercicios
```

---

## Ejercicios integrados — 24 total

| # | Categoría | Ejercicio | Descripción |
|---|-----------|-----------|-------------|
| 1 | Listas y Cadenas | listas01 | Tabla de producción mensual con comparación por colores |
| 2 | Listas y Cadenas | listas02 | Tabla de calificaciones con indicador aprobado / reprobado |
| 3 | Listas y Cadenas | cadenas01 | Frecuencia de letras con barra visual |
| 4 | Listas y Cadenas | numEnteros01 | Eliminación de duplicados antes/después |
| 5 | Matrices y Datos | Matrices01 | Multiplicación de matrices A × B = C animada |
| 6 | Matrices y Datos | coordenadasMatriz | Búsqueda de valor en matriz 6×6 con coordenadas |
| 7 | Matrices y Datos | asientos | Sistema de reserva de asientos 6×6 |
| 8 | Matrices y Datos | DataFrame | Estadísticas sobre Housing.csv (media, moda, varianza, desv. estándar) |
| 9 | Estructuras Lineales | colas | Cola FIFO — enqueue/dequeue animado |
| 10 | Estructuras Lineales | bicolas | Bicola — inserciones y extracciones por ambos extremos |
| 11 | Estructuras Lineales | deque | Deque (Practicas_3) — operaciones combinadas |
| 12 | Estructuras Lineales | colaCircular | Cola circular — visualización en rueda |
| 13 | Estructuras Lineales | ejercicioCircular | Cola circular con operaciones mixtas |
| 14 | Estructuras Lineales | Tareas | Gestión de tareas con cola animada |
| 15 | Estructuras Lineales | pila | Pila LIFO — push/pop animado |
| 16 | Estructuras Lineales | cola | Cola (Practicas_5) — operaciones estándar |
| 17 | Estructuras Lineales | dulces | Pipeline Cola → Pila → Lista (Resultado) |
| 18 | Árboles | ArbolBinario | BST con recorridos Preorden / Inorden / Postorden animados |
| 19 | Árboles | nodoArbol | Árbol con NodoArbol, inserción y recorrido |
| 20 | Árboles | BFS | Recorrido BFS con cola de nivel animada |
| 21 | Grafos y Recursión | Dijkstra | Camino mínimo — nodos visitados animados paso a paso |
| 22 | Grafos y Recursión | Prim | Árbol de expansión mínima — aristas MST animadas |
| 23 | Grafos y Recursión | Kruskal | MST por ordenamiento de aristas con Union-Find |
| 24 | Grafos y Recursión | Hanoi | Torres de Hanói — 5 discos, animación completa (31 movimientos) |

---

## Notas técnicas

- La integración usa `importlib.util.spec_from_file_location` con captura de `sys.stdout` para ejecutar cada módulo sin efectos secundarios en la UI.
- Velocidad de animación fija: 700 ms por paso.
