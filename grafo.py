import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from collections import deque
import random
import math

# Clase que representa el grafo de usuarios
class Graph:
    def __init__(self):
        self.adjacency = {}  # Diccionario de listas de adyacencia

    def add_user(self, user):
        if user not in self.adjacency:
            self.adjacency[user] = []  # Agrega un nuevo nodo

    def add_friendship(self, user1, user2):
        # Crea una conexión bidireccional entre dos usuarios
        if user1 in self.adjacency and user2 in self.adjacency:
            if user2 not in self.adjacency[user1]:
                self.adjacency[user1].append(user2)
            if user1 not in self.adjacency[user2]:
                self.adjacency[user2].append(user1)

    def get_friends(self, user):
        return self.adjacency.get(user, [])

    def suggest_friends(self, user):
        # Usa BFS para encontrar usuarios a 2 niveles de distancia
        visited = set()
        queue = deque([(user, 0)])
        suggestions = set()

        while queue:
            current, level = queue.popleft()
            if level > 2:
                break
            for neighbor in self.adjacency.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    if level == 1 and neighbor != user and neighbor not in self.adjacency[user]:
                        suggestions.add(neighbor)
                    queue.append((neighbor, level + 1))

        return suggestions - set(self.get_friends(user)) - {user}

# Clase principal de la aplicación gráfica
class SocialNetworkApp:
    def __init__(self, root):
        self.graph = Graph()
        self.root = root
        self.root.title("Red Social - Grafo")
        self.style = tb.Style("cosmo")  # Tema visual de ttkbootstrap

        self.setup_ui()
        self.user_positions = {}  # Diccionario para guardar posiciones de nodos

    def setup_ui(self):
        # Configura los elementos de la interfaz gráfica
        frame = ttk.Frame(self.root)
        frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        ttk.Label(frame, text="Usuario:").pack(pady=5)
        self.user_entry = ttk.Entry(frame)
        self.user_entry.pack(pady=5)

        ttk.Button(frame, text="Agregar Usuario", command=self.add_user).pack(pady=5)
        ttk.Button(frame, text="Hacer Amigos", command=self.add_friendship).pack(pady=5)

        ttk.Label(frame, text="Seleccionar Usuario:").pack(pady=5)
        self.select_user = ttk.Combobox(frame, state="readonly")
        self.select_user.pack(pady=5)
        self.select_user.bind("<<ComboboxSelected>>", self.update_info_panel)

        self.results = tk.Text(frame, height=15, width=30)
        self.results.pack(pady=5)

        self.canvas = tk.Canvas(self.root, bg="white", width=600, height=600)
        self.canvas.pack(side=tk.RIGHT, padx=10, pady=10)

    def add_user(self):
        # Agrega un nuevo usuario y lo posiciona aleatoriamente en el canvas
        user = self.user_entry.get().strip()
        if user and user not in self.graph.adjacency:
            self.graph.add_user(user)
            self.select_user["values"] = list(self.graph.adjacency.keys())
            self.user_positions[user] = (random.randint(50, 550), random.randint(50, 550))
            self.draw_graph()
            self.user_entry.delete(0, tk.END)

    def add_friendship(self):
        # Ventana emergente para seleccionar dos usuarios a conectar
        users = self.select_user["values"]
        if len(users) >= 2:
            win = tk.Toplevel(self.root)
            win.title("Seleccionar Amigos")
            cb1 = ttk.Combobox(win, values=users, state="readonly")
            cb2 = ttk.Combobox(win, values=users, state="readonly")
            cb1.pack(pady=5)
            cb2.pack(pady=5)
            ttk.Button(win, text="Conectar", command=lambda: self.confirm_friendship(cb1.get(), cb2.get(), win)).pack(pady=5)

    def confirm_friendship(self, u1, u2, window):
        # Conecta dos usuarios si son distintos
        if u1 != u2:
            self.graph.add_friendship(u1, u2)
            self.draw_graph()
        window.destroy()

    def draw_graph(self):
        # Dibuja los nodos y aristas en el canvas
        self.canvas.delete("all")
        for user, pos in self.user_positions.items():
            for friend in self.graph.get_friends(user):
                if friend in self.user_positions:
                    x1, y1 = pos
                    x2, y2 = self.user_positions[friend]
                    self.canvas.create_line(x1, y1, x2, y2, fill="gray")

        for user, (x, y) in self.user_positions.items():
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="lightblue")
            self.canvas.create_text(x, y, text=user)

    def update_info_panel(self, event):
        # Muestra amigos y sugerencias de amistad del usuario seleccionado
        user = self.select_user.get()
        if user:
            friends = self.graph.get_friends(user)
            suggestions = self.graph.suggest_friends(user)
            self.results.delete("1.0", tk.END)
            self.results.insert(tk.END, f"Amigos de {user}:\n")
            self.results.insert(tk.END, ", ".join(friends) + "\n\n")
            self.results.insert(tk.END, f"Sugerencias de amistad para {user}:\n")
            self.results.insert(tk.END, ", ".join(suggestions))

# Punto de entrada del programa
if __name__ == "__main__":
    root = tb.Window(themename="cosmo")
    app = SocialNetworkApp(root)
    root.mainloop()
