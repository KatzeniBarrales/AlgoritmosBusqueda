"""
Laboratorio de algoritmos de búsqueda - Fundamentos de IA
Archivo 2: interfaz gráfica con Tkinter.
Ejecutar con:  python interfaz.py   (debe estar junto a algoritmos.py)
"""
import tkinter as tk
from tkinter import ttk
import algoritmos as alg

ventana = tk.Tk()
ventana.title("Laboratorio de algoritmos de búsqueda - Logística")
{}
# ---------------- Panel izquierdo: controles ----------------
panel = tk.Frame(ventana, padx=10, pady=10)
panel.grid(row=0, column=0, sticky="n")

tk.Label(panel, text="Algoritmo:").pack(anchor="w")
caja_alg = ttk.Combobox(panel, state="readonly", width=20,
                        values=["BFS", "DFS", "Greedy Best-First", "A*"])
caja_alg.current(3)
caja_alg.pack(pady=(0, 8))

tk.Label(panel, text="Nodo inicial:").pack(anchor="w")
caja_ini = ttk.Combobox(panel, state="readonly", width=20, values=sorted(alg.NODOS))
caja_ini.set(alg.INICIO)
caja_ini.pack(pady=(0, 8))

tk.Label(panel, text="Nodo destino:").pack(anchor="w")
caja_fin = ttk.Combobox(panel, state="readonly", width=20, values=sorted(alg.NODOS))
caja_fin.set(alg.DESTINO)
caja_fin.pack(pady=(0, 8))

tk.Label(panel, text="Heurística (Greedy / A*):").pack(anchor="w")
caja_h = ttk.Combobox(panel, state="readonly", width=20,
                      values=["Euclidiana", "Inflada (x3)", "Cero"])
caja_h.current(0)
caja_h.pack(pady=(0, 8))

# ---------------- Canvas: dibujo del mapa ----------------
lienzo = tk.Canvas(ventana, width=700, height=430, bg="white")
lienzo.grid(row=0, column=1, padx=5, pady=5)

# ---------------- Cuadro de resultados ----------------
texto = tk.Text(ventana, width=100, height=11, wrap="word")
texto.grid(row=1, column=0, columnspan=2, padx=5, pady=5)


def dibujar(ruta=None, explorados=None):
    """Dibuja el grafo. Ruta en verde, explorados en naranja, bloqueadas en rojo."""
    lienzo.delete("all")
    ruta = ruta or []
    explorados = explorados or []
    aristas_ruta = [(ruta[i], ruta[i + 1]) for i in range(len(ruta) - 1)]

    # conexiones normales
    for a, b, costo in alg.CONEXIONES:
        x1, y1 = alg.NODOS[a]
        x2, y2 = alg.NODOS[b]
        en_ruta = (a, b) in aristas_ruta or (b, a) in aristas_ruta
        color = "green" if en_ruta else "gray"
        grosor = 5 if en_ruta else 2
        lienzo.create_line(x1, y1, x2, y2, fill=color, width=grosor)
        lienzo.create_text((x1 + x2) / 2, (y1 + y2) / 2 - 8, text=str(costo),
                           fill="blue", font=("Arial", 10, "bold"))

    # conexiones bloqueadas
    for a, b, costo in alg.BLOQUEADAS:
        x1, y1 = alg.NODOS[a]
        x2, y2 = alg.NODOS[b]
        lienzo.create_line(x1, y1, x2, y2, fill="red", width=2, dash=(6, 4))
        lienzo.create_text((x1 + x2) / 2, (y1 + y2) / 2 - 8, text="X bloqueada",
                           fill="red", font=("Arial", 9, "bold"))

    # nodos
    for nombre, (x, y) in alg.NODOS.items():
        if nombre in ruta:
            relleno = "lightgreen"
        elif nombre in explorados:
            relleno = "orange"
        else:
            relleno = "lightblue"
        lienzo.create_oval(x - 18, y - 18, x + 18, y + 18, fill=relleno, outline="black", width=2)
        lienzo.create_text(x, y, text=nombre, font=("Arial", 12, "bold"))

    # leyenda
    lienzo.create_text(10, 415, anchor="w", font=("Arial", 9),
                       text="Verde = ruta   Naranja = explorado   Azul = no explorado   "
                            "Rojo punteado = bloqueada   Número azul = costo")


def ejecutar_busqueda():
    nombre = caja_alg.get()
    inicio = caja_ini.get()
    destino = caja_fin.get()
    tipo_h = caja_h.get()

    ruta, explorados, costo, tiempo = alg.ejecutar(nombre, inicio, destino, tipo_h)
    dibujar(ruta, explorados)

    texto.delete("1.0", tk.END)
    texto.insert(tk.END, f"Algoritmo: {nombre}")
    if nombre in ("Greedy Best-First", "A*"):
        texto.insert(tk.END, f"  (heurística: {tipo_h})")
    texto.insert(tk.END, "\n")
    if ruta:
        texto.insert(tk.END, "Ruta encontrada: " + " -> ".join(ruta) + "\n")
        texto.insert(tk.END, f"Costo total: {costo}\n")
    else:
        texto.insert(tk.END, "No existe ruta entre esos nodos.\n")
    texto.insert(tk.END, f"Nodos explorados: {len(explorados)}  ({', '.join(explorados)})\n")
    texto.insert(tk.END, f"Tiempo de ejecución: {tiempo:.4f} ms\n\n")
    texto.insert(tk.END, "Explicación: " + alg.EXPLICACIONES[nombre])


tk.Button(panel, text="Ejecutar búsqueda", command=ejecutar_busqueda,
          bg="lightgreen", width=18).pack(pady=10)

dibujar()
ventana.mainloop()
