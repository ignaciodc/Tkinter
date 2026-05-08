import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from GestionBD import GestionBD
from VentanaBase import VentanaBase
from VentanaPrestados import VentanaPrestados
from VentanaDeseados import VentanaDeseados
from VentanaComprados import VentanaLibros


# Panel Principal de la Aplicación

class AppPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("LibroPy v3.0")
        self.root.geometry("400x400")
        self.db = GestionBD()
        
        # Diccionario para rastrear ventanas abiertas
        self.ventanas_abiertas = {
            "libros": None,
            "deseados": None,
            "prestados": None
        }

        tk.Label(root, text="GESTOR DE BIBLIOTECA", font=("Arial", 14, "bold")).pack(pady=30)
        
        self.btn(root, "Mis Libros", "libros", VentanaLibros, "#4CAF50")
        self.btn(root, "Lista Deseados", "deseados", VentanaDeseados, "#9C27B0")
        self.btn(root, "Prestados", "prestados", VentanaPrestados, "#FF9800")

    def btn(self, master, texto, clave, clase, color):
        tk.Button(master, text=texto, width=25, bg=color, fg="white", font=("Arial", 10, "bold"),
                  command=lambda: self.controlar_ventana(clave, clase)).pack(pady=10)

    def controlar_ventana(self, clave, clase_ventana):
        """Gestiona que solo haya una ventana abierta de cada tipo"""
        ventana = self.ventanas_abiertas[clave]
        
        # Si la ventana no existe o fue cerrada (winfo_exists == 0)
        if ventana is None or not ventana.window.winfo_exists():
            self.ventanas_abiertas[clave] = clase_ventana(self.root, self.db)
        else:
            # Si ya está abierta, la traemos al frente
            self.ventanas_abiertas[clave].window.lift()
            self.ventanas_abiertas[clave].window.focus_force()

if __name__ == "__main__":
    root = tk.Tk()
    app = AppPrincipal(root)
    root.mainloop()