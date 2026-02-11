'''
En un arreglo unidimensional se almacenan las calificaciones finales de N alumnos de un
curso universitario. Escriba un programa que calcule e imprima:
a) El promedio general del grupo.
b) Número de alumnos aprobados y reprobados.
c)Porcentaje de alumnos reprobados y reprobados.
d) Número de alumnos cuya calificacion fue mayor o igual a 8. '''

def sumlist(lista):
    if len(lista) == 1:
        return lista[0]
    else:
        return lista[0] + sumlist(lista[1:])
def calif(lista):
    lista.sort()
    for i in range(len(lista)):
        if lista[i] >= 7:
            return print(f'aprobados = {len(lista[i:])} \nreprobados = {len(lista[:i])}'), print(f'% aprobados = {(len(lista[i:])*100)/len(lista)} \n% reprobados = {(len(lista[:i])*100)/len(lista)}') 
def mayor8(lista):
    lista.sort()    
    for i in range(len(lista)):
        if lista[i] >= 8:
            return print(f'alumnos mauyor a 8 = {len(lista[i:])}')
        
calificaciones=[8,8,7,5,10,9,9,5,6,10]

promedio = sumlist(calificaciones)/len(calificaciones)
print (f'promedio = {promedio}')

calif(calificaciones)
mayor8(calificaciones)

