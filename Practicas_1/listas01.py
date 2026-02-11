'''
En un arreglo unidimensional se ha almacenado el numero total de toneladas de cereales
cosechadas durante cada mes del año anterior. Escriba un programa que obtenga e imprima la
siguiente informacion:
a) El promedio anual de toneladas cosechadas
b) ¿Cuantos meses tuvieron una cosecha superior al promedio anual?
c) ¿Cuantos meses tuvieron una cosecha inferior al promedio anual? '''

def sumlist(lista):
    if len(lista) == 1:
        return lista[0]
    else:
        return lista[0] + sumlist(lista[1:])
def compare_list(lista, prom):
    lista.sort()
    a = int(len(lista)/2)
    if prom >= a:
       return print(lista[a:]), print(lista[:a])
    else:
        return print(lista[:a]), print(lista[a:])
        
toneladas=[12,24,16,15,20,18,6,10,12,11,15,12]

promedio = sumlist(toneladas)/len(toneladas)
print (promedio)

compare_list(toneladas, promedio)









