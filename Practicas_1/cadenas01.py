'''
Dada una cadena de caracteres como dato, se desea saber el número de veces que aparecen
las letras 'a', 'b',...,'z' y 'A', 'B',...,'Z' en dicha cadena. Escriba un programa que
resuelva el problema.

a) Si usó arreglos, ¿cuantos necesitó? ¿Por qué?
b) ¿Existe otra forma de resolverlo? '''

def compare_string(string,min,may):
    for x,y in zip(min,may):
        if x in string:
            print (f'{x} =',string.count(x))
        elif y in string:
            print(f'{y} =',string.count(y))
def without(string,min,may):
    print(min)
    for x in min:
        if x in string:
            print (f'{x} =',string.count(x))
        elif x.upper() in string:
            print (f'{x.upper()} =',string.count(x.upper()))
    '''for x in may:
        if x in string:
            print (f'{x} =',string.count(x))'''
    
    



cadena = "Parangaricutirimicuaro"
minw= "abcdefghijklmnopqrstuvwyz"
mayw= minw.upper()

min = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","y","z"]
may = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","Y","Z"]

compare_string(cadena,min,may)
without(cadena, minw, mayw)





        
