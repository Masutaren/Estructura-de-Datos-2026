Asientos = [
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0]
]

def reservar(i,j):
    global Asientos
    if Asientos[i-1][j-1] == 0:
        Asientos[i-1][j-1] = 1
        print('Asiento reservado en:',(i,j))
    else:
        print('El asiento ya ha sido reservado.')

def liberar(i,j):
    global Asientos
    if Asientos[i-1][j-1] == 1:
        Asientos[i-1][j-1] = 0
        print('Asiento liberado en:',(i,j))
    else:
        print('El asiento ya está libre.')

def consultar(i,j):
    global Asientos
    if Asientos[i-1][j-1] == 0:
        print('El asiento está libre.')
    else:
        print('El asiento ya ha sido reservado')

def totalAsientos(A):
    contador = 0
    for i in range(len(A)):
        for j in range(len(A[i])):
            if A[i][j]==1:
                contador += 1
    print('Asientos Reservados:',contador)

def masAsientos(A):
    lista=[]
    sum = 0
    for i in range(len(A)):
        sum = 0
        for j in range(len(A[i])):
            if A[i][j]==1:
                sum += A[i][j]
        lista.append(sum)
    elementomas = lista.index(max(lista))
    return print(elementomas+1)

reservar(1,1)
reservar(1,2)
reservar(1,1)
consultar(1,1)
liberar(1,1)
liberar(1,1)
reservar(3,4)
reservar(6,6)
consultar(6,6)
reservar(2,5)
totalAsientos(Asientos)
masAsientos(Asientos)
print(Asientos)