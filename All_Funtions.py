# Numeros aleatoreos positivos del 1 al 20.000
import random

def NumberRandom(CantNumber):
    numeros_aleatorios = []
    for _ in range(CantNumber):
        numeros_aleatorios.append(random.randint(1, 20000))
    return numeros_aleatorios

CantNumber = int(input('Ingrese la cantidad de numeros que desea ver: '))
numeros_aleatorios = NumberRandom(CantNumber)
print(numeros_aleatorios)
