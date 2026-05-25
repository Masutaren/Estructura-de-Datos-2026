from visualizer import mostrar_barras
import random

# Selection Sort
def selection_sort(arr, canvas):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            mostrar_barras(canvas, arr, [min_idx, j])  # Comparación
            yield
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]  # Intercambio
        mostrar_barras(canvas, arr, [i, min_idx])
        yield

# Quick Sort
def quick_sort(arr, canvas):
    yield from quick_sort_rec(arr, 0, len(arr) - 1, canvas)

def quick_sort_rec(arr, low, high, canvas):
    if low < high:
        pi = yield from partition(arr, low, high, canvas)
        yield from quick_sort_rec(arr, low, pi - 1, canvas)
        yield from quick_sort_rec(arr, pi + 1, high, canvas)

def partition(arr, low, high, canvas):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        mostrar_barras(canvas, arr, [j, high])  # Comparación con pivote
        yield
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            mostrar_barras(canvas, arr, [i, j])
            yield
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    mostrar_barras(canvas, arr, [i + 1, high])
    yield
    return i + 1

# Random Quick Sort
def random_quick_sort(arr, canvas):
    yield from random_quick_sort_rec(arr, 0, len(arr) - 1, canvas)

def random_quick_sort_rec(arr, low, high, canvas):
    if low < high:
        pi = yield from random_partition(arr, low, high, canvas)
        yield from random_quick_sort_rec(arr, low, pi - 1, canvas)
        yield from random_quick_sort_rec(arr, pi + 1, high, canvas)

def random_partition(arr, low, high, canvas):
    rand_idx = random.randint(low, high)
    arr[high], arr[rand_idx] = arr[rand_idx], arr[high]
    mostrar_barras(canvas, arr, [high, rand_idx])  # Pivote aleatorio
    yield
    return (yield from partition(arr, low, high, canvas))

# Counting Sort
def counting_sort(arr, canvas):
    max_val = max(arr)
    min_val = min(arr)
    rango = max_val - min_val + 1
    count = [0] * rango

    # Contar ocurrencias
    for i in range(len(arr)):
        count[arr[i] - min_val] += 1
        mostrar_barras(canvas, arr, [i])
        yield

    # Reconstruir arreglo
    idx = 0
    for i in range(rango):
        while count[i] > 0:
            arr[idx] = i + min_val
            mostrar_barras(canvas, arr, [idx])
            yield
            idx += 1
            count[i] -= 1

# Bubble Sort
def bubble_sort(arr, canvas):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            mostrar_barras(canvas, arr, [j, j + 1])  # Comparación
            yield
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]  # Intercambio
                mostrar_barras(canvas, arr, [j, j + 1])
                yield

# Insertion Sort
def insertion_sort(arr, canvas):
    for i in range(1, len(arr)):
        actual = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > actual:
            arr[j + 1] = arr[j]
            mostrar_barras(canvas, arr, [j, j + 1])
            yield
            j -= 1
        arr[j + 1] = actual
        mostrar_barras(canvas, arr, [j + 1])
        yield

# Merge Sort
def merge_sort(arr, canvas):
    yield from merge_sort_rec(arr, 0, len(arr) - 1, canvas)

def merge_sort_rec(arr, inicio, fin, canvas):
    if inicio < fin:
        medio = (inicio + fin) // 2
        yield from merge_sort_rec(arr, inicio, medio, canvas)
        yield from merge_sort_rec(arr, medio + 1, fin, canvas)
        yield from merge(arr, inicio, medio, fin, canvas)

def merge(arr, inicio, medio, fin, canvas):
    izquierda = arr[inicio:medio + 1]
    derecha = arr[medio + 1:fin + 1]
    i = j = 0
    k = inicio
    while i < len(izquierda) and j < len(derecha):
        mostrar_barras(canvas, arr, [k])
        yield
        if izquierda[i] <= derecha[j]:
            arr[k] = izquierda[i]
            i += 1
        else:
            arr[k] = derecha[j]
            j += 1
        k += 1

    while i < len(izquierda):
        arr[k] = izquierda[i]
        i += 1
        k += 1
        mostrar_barras(canvas, arr, [k - 1])
        yield

    while j < len(derecha):
        arr[k] = derecha[j]
        j += 1
        k += 1
        mostrar_barras(canvas, arr, [k - 1])
        yield
