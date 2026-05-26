import pandas as pd

df = pd.read_csv('Practicas_2/Housing.csv')

price = list(df['price'])
bathrooms = list(df['bathrooms'])
sqft_living = list(df['sqft_living'])
sqft_lot = list(df['sqft_lot'])
floors = list(df['floors'])
sqft_above = list(df['sqft_above'])

def media(lista):
    suma = 0
    for i in lista:
        suma += i
    return suma / len(lista)

def moda(lista):
    frecuencias = {}
    max_frec = 0
    moda_valor = None
    for i in lista:
        frecuencias[i] = frecuencias.get(i, 0) + 1
        if frecuencias[i] > max_frec:
            max_frec = frecuencias[i]
            moda_valor = i
    return moda_valor

def varianza(lista):
    m = media(lista)   # calcular una sola vez ya que el anterior me tardaba mucho
    suma = 0
    for i in lista:
        suma += (i - m) ** 2
    return suma / len(lista)

def desv(lista):
    return varianza(lista) ** 0.5

def datos_resultantes(lista):
    print("Media:", media(lista))
    print("Moda:", moda(lista))
    print("Varianza:", varianza(lista))
    print("Desviación estándar:", desv(lista), '\n')

datos_resultantes(price)
datos_resultantes(bathrooms)
datos_resultantes(sqft_living)
datos_resultantes(sqft_lot)
datos_resultantes(floors)
datos_resultantes(sqft_above)