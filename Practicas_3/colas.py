#
def enque(lista, elemento):
    lista.append(elemento)
def deque(lista):
    lista.pop(0)
def peek(lista):
    return (lista[0])
def is_empty(lista):
    if lista == []:
        return True
    else:
        return False
def size(lista):
    return len(lista)

def retiro(lista,monto):
    global retiros
    peek(lista)
    enque(retiros, (lista[0] - monto))
    print('Operacion:',peek(lista),'-',monto,'=',peek(retiros))
    deque(lista)
    enque(lista,(retiros[0]))

def deposito(lista,monto):
    global depositos
    enque(depositos, (lista[0] + monto))
    print('Operacion:',peek(lista),'+',monto,'=',peek(depositos))
    deque(lista)
    enque(lista,(depositos[0]))

saldos = [1000,1000,1000,1000,1000]
retiros = []
depositos = []

retiro(saldos,500)
retiro(saldos,500)
retiro(saldos,500)
retiro(saldos,500)
retiro(saldos,500)
print(saldos)
deposito(saldos,300)
deposito(saldos,300)
deposito(saldos,300)
deposito(saldos,300)
deposito(saldos,300)
print(saldos)

