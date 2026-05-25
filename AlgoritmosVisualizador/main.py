import tkinter as tk
import time

from algoritmos import merge_sort, insertion_sort, bubble_sort, selection_sort, quick_sort, random_quick_sort, counting_sort
from visualizer import mostrar_barras

class Ordenamiento:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Algoritmos de Ordenamiento")
        self.tiempo_inicio = 0
        self.pasos_ejecutados = 0

        # Dibujar las barras
        self.canvas = tk.Canvas(self.ventana, width=800, height=400, bg='white')
        self.canvas.pack(pady=20)

        # Botones y menú de selección
        self.menu = tk.Frame(self.ventana)
        self.menu.pack()

        self.algoritmo_seleccionado = tk.StringVar()
        self.algoritmo_seleccionado.set("Bubble Sort")

        self.lista_algoritmos = tk.OptionMenu(self.menu, self.algoritmo_seleccionado,
                                              "Bubble Sort", "Insertion Sort", "Merge Sort", "Selection Sort", "Quick Sort", "Random Quick Sort", "Counting Sort")
        self.lista_algoritmos.pack(side="left", padx=10)

        self.boton_generar = tk.Button(self.menu, text="Insertar arreglo", command=self.generar_datos)
        self.boton_generar.pack(side="left", padx=10)

        self.boton_ordenar = tk.Button(self.menu, text="Iniciar ordenamiento", command=self.iniciar_ordenamiento)
        self.boton_ordenar.pack(side="left", padx=10)

        self.boton_detener = tk.Button(self.menu, text="Detener", command=self.detener_ordenamiento)
        self.boton_detener.pack(side="left", padx=10)

        # Estado y estadisticas
        self.etiqueta_estado = tk.Label(self.ventana, text="Listo.")
        self.etiqueta_estado.pack()
        self.etiqueta_estadisticas = tk.Label(self.ventana, text="Tiempo: 0.00s | Pasos: 0")
        self.etiqueta_estadisticas.pack()

        # Datos a ordenar
        self.datos = []
        self.generar_datos()

    def detener_ordenamiento(self):
        self.detener = True

    def generar_datos(self):
        self.datos = [10,50,23,3,43,23,29,49,12,40]
        mostrar_barras(self.canvas, self.datos, [])

    def iniciar_ordenamiento(self):
        algoritmo = self.algoritmo_seleccionado.get()
        self.etiqueta_estado.config(text=f"Ejecutando: {algoritmo}")
        self.ventana.update_idletasks()
        self.pasos_ejecutados = 0
        self.tiempo_inicio = time.perf_counter()
        self.detener = False  # Reinicia estado del botón detener

        if algoritmo == "Bubble Sort":
            self.generador = bubble_sort(self.datos, self.canvas)
        elif algoritmo == "Insertion Sort":
            self.generador = insertion_sort(self.datos, self.canvas)
        elif algoritmo == "Merge Sort":
            self.generador = merge_sort(self.datos, self.canvas)
        elif algoritmo == "Selection Sort":
            self.generador = selection_sort(self.datos, self.canvas)
        elif algoritmo == "Quick Sort":
            self.generador = quick_sort(self.datos, self.canvas)
        elif algoritmo == "Random Quick Sort":
            self.generador = random_quick_sort(self.datos, self.canvas)
        elif algoritmo == "Counting Sort":
            self.generador = counting_sort(self.datos, self.canvas)
        else:
            return

        self.animar()

    def animar(self):
        if self.detener:
            self.etiqueta_estado.config(text="Ordenamiento detenido.")
            return
        try:
            next(self.generador)
            self.pasos_ejecutados +=1

            tiempo_actual = time.perf_counter() - self.tiempo_inicio
            self.etiqueta_estadisticas.config(
                text=f"Tiempo: {tiempo_actual:.02f}s | Pasos: {self.pasos_ejecutados}"
            )
            
            self.ventana.after(50, self.animar)
        except StopIteration:
            self.etiqueta_estado.config(
                text=f"Ordenamiento finalizado."
            )

# Ejecutar aplicación
if __name__ == "__main__":
    ventana = tk.Tk()
    app = Ordenamiento(ventana)
    ventana.mainloop()
