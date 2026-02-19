import pandas as pd

df = pd.read_csv('Practicas_2/Housing.csv')

price = list(df['price'])
bathrooms = list(df['bathrooms'])
sqft_living = list(df['sqft_living'])
sqft_lot = list(df['sqft_lot'])
floors = list(df['floors'])
sqft_above = list(df['sqft_above'])

def media(list):
    sum = 0
    for i in list:
        sum += i
    m = sum/(len(list))
    return m

def moda(list):
    moda = {}
    max = 0
    for i in list:
        valor = int(list.count(i))
        moda[i] = valor
        if moda[i] > max:
            max = moda[i]
            x = i
    return x

def varianza(list):
    sumV = 0
    for i in list:
        sumV += ((i - media(list))**2)  
    v = sumV/len(list)
    return v

def desv(list):
    d = varianza(list)
    return d**0.5

def datos_resultantes(lista):
    print (media(lista))
    print (moda(lista))
    print (varianza(lista))
    print (desv(lista),'\n')

datos_resultantes(price)
datos_resultantes(bathrooms)
datos_resultantes(sqft_living)
datos_resultantes(sqft_lot)
datos_resultantes(floors)
datos_resultantes(sqft_above)

    


    