def es_primo(numero):
    if numero <= 1:
        return False
    for i in range(2, int(numero**0.5) + 1):
        if numero % i == 0:
            return False
    return True

def imprimir_primos(n):
    contador = 0
    numero = 2
    while contador < n:
        if es_primo(numero):
            print(numero, end=" ")
            contador += 1
        numero += 1

def main():

    n = int(input("Introduce la cantidad de números primos que deseas imprimir: "))

    if n <= 0:
        print("Por favor, introduce un número entero positivo.")
        return
    
    print(f"\nLos primeros {n} números primos son:")
    imprimir_primos(n)
    print()

main()