def enque_tail(lista, elemento):
    lista.append(elemento)
def enque_head(lista, elemento):
    lista.insert(0, elemento)
def deque_head(lista):
    lista.pop(0)
def deque_tail(lista):
    lista.pop(-1)
def head(lista):
    return (lista[0])
def tail(lista):
    return (lista[-1])
def is_empty(lista):
    if lista == []:
        return True
    else:
        return False
def size(lista):
    return len(lista)

def retiro(lista,monto):
    global retiros
    enque_head(retiros, (lista[0] - monto))
    print('Operacion:',head(lista),'-',monto,'=',head(retiros))
    deque_head(lista)
    enque_tail(lista,(retiros[0]))

def deposito(lista,monto):
    global depositos
    enque_tail(depositos, (lista[-1] + monto))
    print('Operacion:',tail(lista),'+',monto,'=',tail(depositos))
    deque_tail(lista)
    enque_head(lista,(depositos[-1]))

saldos = [1000,1000,1000,1000,1000]
retiros = []
depositos = []

retiro(saldos,500)
retiro(saldos,400)
retiro(saldos,300)
retiro(saldos,200)
retiro(saldos,100)
print(saldos)
deposito(saldos,400)
deposito(saldos,300)
deposito(saldos,300)
deposito(saldos,300)
deposito(saldos,400)
print(saldos)

