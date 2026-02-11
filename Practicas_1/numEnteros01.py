'''
Dado un arreglo unidimensional de numeros enteros, ordenados crecientemente escribra una programa 
que elimine todos los numeros repetidos. Considere que de haber valores repetidos estos se encontrarán 
en posiciones consecutivas del arreglo. '''

x = [1,2,4,4,4,5,7,9,11,11,13,14,15,16,16]

def repetidos(list):
    y = []
    for x in list:
        if x not in y:
            y.append(x)
    return print(y)

repetidos(x)
