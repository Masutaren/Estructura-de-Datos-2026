def mostrar_barras(canvas, arreglo, indices_resaltados):
    canvas.delete("all")
    ancho = canvas.winfo_width()
    alto = canvas.winfo_height()
    ancho_barra = ancho / len(arreglo)

    for i, valor in enumerate(arreglo):
        x0 = i * ancho_barra
        y0 = alto - (valor*6)
        x1 = (i + 1) * ancho_barra
        y1 = alto
        color = "red" if i in indices_resaltados else "skyblue"
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
        canvas.create_text(
            (x0 + x1) / 2, y0 - 10,
            text=str(valor),
            fill="black",
            font=("Arial", 10, "bold")
        )

