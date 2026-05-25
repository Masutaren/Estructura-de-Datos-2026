from colaCircular import ColaCircular

cola=ColaCircular(5)

turnos = ["A01", "A02", "A03", "A04", "A05", "A06"]

for turno in turnos[:5]:
    cola.encolar(turno)
print("Inicio:")
cola.mostrar()
print("Turno atendido:", cola.desencolar())
print("Frente actual:", cola.ver_frente())
cola.mostrar()
cola.encolar(turnos[5])
print("Encolar A06:")
cola.mostrar()