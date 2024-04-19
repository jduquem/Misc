import random

# Numeros aleatoreos positivos del 1 al 20.000
def random_number(number_count):
    numeros_aleatorios = []
    for _ in range(number_count):
        numeros_aleatorios.append(random.randint(1, 20000))
    return numeros_aleatorios


def number_is_par(number):
    if number %2 == 0:
        result = True
    elif number != 0:
        result = False
    return result


def __init__():
    number_count = int(input('Ingrese la cantidad de numeros que desea ver: '))
    random_numbers = random_number(number_count)
    print(random_numbers)

    num = int(input('Ingrese el numero: '))
    print(number_is_par(num))
