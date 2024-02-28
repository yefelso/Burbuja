def burbuja(arr):
    n = len(arr)

    for i in range(n):
        # Últimos i elementos ya están ordenados, no es necesario compararlos
        for j in range(0, n - i - 1):
            # Si el elemento actual es mayor que el siguiente, intercambiarlos
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

# Ejemplo de uso
arreglo = [64, 34, 25, 12, 22, 11, 90]

print("Arreglo original:", arreglo)
burbuja(arreglo)
print("Arreglo ordenado:", arreglo)
