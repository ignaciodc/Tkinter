import tkinter as tk
from tkinter import messagebox, ttk

# Clase: VentanaBase - Clase base para las ventanas de gestión de libros

class VentanaBase:
    def __init__(self, master, titulo, columnas, db_manager):
        self.window = tk.Toplevel(master)
        self.window.title(titulo)
        self.window.geometry("950x550")
        self.db = db_manager
        self.columnas = columnas
        self.orden_asc = {col: True for col in columnas}
        
        # Al cerrar, la ventana se destruye automáticamente
        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)

    def configurar_tabla(self):
        self.tree = ttk.Treeview(self.window, columns=self.columnas, show="headings")
        for col in self.columnas:
            self.tree.heading(col, text=col, command=lambda c=col: self.ordenar_columna(c))
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=15, pady=5)
        self.tree.bind("<Button-1>", self.gestionar_clic_simple)

    def gestionar_clic_simple(self, event):
        """Si se clica en el área vacía, se quita la selección"""
        item = self.tree.identify_row(event.y)
        if not item:
            # Quitamos la selección de todos los elementos seleccionados al clicar en el área vacía
            self.tree.selection_remove(self.tree.selection())

    def ordenar_columna(self, col):
        data = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
        
        def safe_float(val):
            try: return float(val.replace('€', '').replace(',', '.').strip())
            except: return 0.0

        if col in ("ID", "Páginas", "Precio"):
            data.sort(key=lambda t: safe_float(t[0]), reverse=not self.orden_asc[col])
        else:
            data.sort(key=lambda t: str(t[0]).lower(), reverse=not self.orden_asc[col])

        for index, (val, item) in enumerate(data):
            self.tree.move(item, '', index)
        self.orden_asc[col] = not self.orden_asc[col]