"""
Laboratorio de algoritmos de búsqueda - Fundamentos de IA
Archivo 1: el mapa (grafo) y los algoritmos BFS, DFS, Greedy y A*.
"""
import time
import heapq
from collections import deque

# ---------------------------------------------------------------
# 1. EL MAPA (GRAFO)
# ---------------------------------------------------------------
# Posición (x, y) de cada ciudad. Sirve para dibujar y para la heurística.
NODOS = {
    "A": (60, 80),   "B": (200, 50),  "C": (350, 70),  "D": (500, 50),
    "E": (640, 90),  "F": (120, 220), "G": (270, 200), "H": (420, 210),
    "I": (570, 230), "J": (80, 370),  "K": (260, 360), "L": (600, 370),
}

# Conexiones: (ciudad1, ciudad2, costo)
CONEXIONES = [
    ("A", "B", 4), ("A", "F", 5), ("B", "C", 5), ("B", "G", 6),
    ("C", "D", 4), ("C", "H", 6), ("D", "E", 3), ("D", "H", 7),
    ("E", "I", 4), ("F", "G", 4), ("F", "J", 5), ("G", "H", 4),
    ("G", "K", 5), ("H", "I", 5), ("H", "L", 8), ("I", "L", 4),
    ("J", "K", 4), ("K", "L", 9),
]

# Conexión bloqueada (no se puede usar)
BLOQUEADAS = [("H", "K", 5)]

INICIO = "A"
DESTINO = "L"


def construir_vecinos():
    """Diccionario: ciudad -> lista de (vecino, costo). No incluye bloqueadas."""
    vecinos = {n: [] for n in NODOS}
    for a, b, costo in CONEXIONES:
        vecinos[a].append((b, costo))
        vecinos[b].append((a, costo))
    for n in vecinos:
        vecinos[n].sort()  # orden alfabético para que siempre sea igual
    return vecinos


VECINOS = construir_vecinos()


# ---------------------------------------------------------------
# 2. HEURÍSTICAS
# ---------------------------------------------------------------
def heuristica(nodo, destino, tipo="Euclidiana"):
    """Estimación del costo que falta para llegar al destino."""
    x1, y1 = NODOS[nodo]
    x2, y2 = NODOS[destino]
    distancia = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5 / 50  # 50 px = 1 unidad
    if tipo == "Euclidiana":
        return distancia
    if tipo == "Inflada (x3)":
        return distancia * 3
    return 0  # "Cero": no sabe nada


def costo_de_ruta(ruta):
    """Suma el costo de todas las conexiones de una ruta."""
    total = 0
    for i in range(len(ruta) - 1):
        for vecino, costo in VECINOS[ruta[i]]:
            if vecino == ruta[i + 1]:
                total += costo
    return total


def reconstruir(padres, destino):
    """Arma la ruta yendo hacia atrás con el diccionario de padres."""
    ruta = []
    nodo = destino
    while nodo is not None:
        ruta.append(nodo)
        nodo = padres[nodo]
    return ruta[::-1]


# ---------------------------------------------------------------
# 3. ALGORITMOS
# Todos regresan: (ruta, nodos_explorados(lista), costo, tiempo_ms)
# ---------------------------------------------------------------
def bfs(inicio, destino):
    t0 = time.perf_counter()
    cola = deque([inicio])               # cola FIFO
    padres = {inicio: None}
    explorados = []
    while cola:
        actual = cola.popleft()
        explorados.append(actual)
        if actual == destino:
            ruta = reconstruir(padres, destino)
            return ruta, explorados, costo_de_ruta(ruta), (time.perf_counter() - t0) * 1000
        for vecino, _ in VECINOS[actual]:
            if vecino not in padres:
                padres[vecino] = actual
                cola.append(vecino)
    return None, explorados, 0, (time.perf_counter() - t0) * 1000


def dfs(inicio, destino):
    t0 = time.perf_counter()
    explorados = []

    def visitar(nodo, camino):
        explorados.append(nodo)
        if nodo == destino:
            return camino
        for vecino, _ in VECINOS[nodo]:
            if vecino not in explorados:
                resultado = visitar(vecino, camino + [vecino])  # profundidad
                if resultado:
                    return resultado
        return None  # callejón sin salida: retroceso

    ruta = visitar(inicio, [inicio])
    costo = costo_de_ruta(ruta) if ruta else 0
    return ruta, explorados, costo, (time.perf_counter() - t0) * 1000


def greedy(inicio, destino, tipo_h="Euclidiana"):
    t0 = time.perf_counter()
    # Se ordena SOLO por la heurística h(n)
    frontera = [(heuristica(inicio, destino, tipo_h), inicio)]
    padres = {inicio: None}
    explorados = []
    while frontera:
        _, actual = heapq.heappop(frontera)
        if actual in explorados:
            continue
        explorados.append(actual)
        if actual == destino:
            ruta = reconstruir(padres, destino)
            return ruta, explorados, costo_de_ruta(ruta), (time.perf_counter() - t0) * 1000
        for vecino, _ in VECINOS[actual]:
            if vecino not in padres:
                padres[vecino] = actual
                heapq.heappush(frontera, (heuristica(vecino, destino, tipo_h), vecino))
    return None, explorados, 0, (time.perf_counter() - t0) * 1000


def a_estrella(inicio, destino, tipo_h="Euclidiana"):
    t0 = time.perf_counter()
    # Se ordena por f(n) = g(n) + h(n)
    frontera = [(heuristica(inicio, destino, tipo_h), 0, inicio)]
    padres = {inicio: None}
    mejor_g = {inicio: 0}
    explorados = []
    while frontera:
        _, g, actual = heapq.heappop(frontera)
        if actual in explorados:
            continue
        explorados.append(actual)
        if actual == destino:
            ruta = reconstruir(padres, destino)
            return ruta, explorados, g, (time.perf_counter() - t0) * 1000
        for vecino, costo in VECINOS[actual]:
            nuevo_g = g + costo
            if vecino not in mejor_g or nuevo_g < mejor_g[vecino]:
                mejor_g[vecino] = nuevo_g
                padres[vecino] = actual
                f = nuevo_g + heuristica(vecino, destino, tipo_h)
                heapq.heappush(frontera, (f, nuevo_g, vecino))
    return None, explorados, 0, (time.perf_counter() - t0) * 1000


def ejecutar(nombre, inicio, destino, tipo_h="Euclidiana"):
    """Ejecuta el algoritmo por nombre."""
    if nombre == "BFS":
        return bfs(inicio, destino)
    if nombre == "DFS":
        return dfs(inicio, destino)
    if nombre == "Greedy Best-First":
        return greedy(inicio, destino, tipo_h)
    return a_estrella(inicio, destino, tipo_h)


EXPLICACIONES = {
    "BFS": "Explora por niveles usando una cola: primero todos los vecinos del inicio, "
           "luego los vecinos de esos, etc. Garantiza la ruta con MENOS conexiones, "
           "pero no mira los costos.",
    "DFS": "Se va por un camino hasta el fondo usando una pila (recursión) y, si llega a un "
           "callejón sin salida, retrocede. Encuentra una ruta, pero no necesariamente "
           "corta ni barata.",
    "Greedy Best-First": "Siempre expande el nodo que parece más cercano al destino (solo usa "
           "h(n)). Es rápido, pero ignora lo que ya costó llegar, por eso puede no dar la "
           "ruta más barata.",
    "A*": "Expande el nodo con menor f(n) = g(n) + h(n): costo ya recorrido + estimación "
          "restante. Con una heurística que nunca sobreestima, garantiza la ruta de menor costo.",
}


if __name__ == "__main__":
    # Prueba rápida en consola
    for nombre in ["BFS", "DFS", "Greedy Best-First", "A*"]:
        ruta, exp, costo, t = ejecutar(nombre, INICIO, DESTINO)
        print(f"{nombre}: {' -> '.join(ruta)} | costo={costo} | explorados={len(exp)} | {t:.4f} ms")
