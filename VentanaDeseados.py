import tkinter as tk
from tkinter import messagebox, ttk
from VentanaBase import VentanaBase

# Clase: VentanaDeseados - Ventana para gestionar la lista de libros deseados

class VentanaDeseados(VentanaBase):
    def __init__(self, master, db_manager):
        super().__init__(master, "Lista de Deseados", ("ID", "Título", "Autor", "Género", "Precio", "Idioma"), db_manager)
        self.configurar_tabla()
        self.tree.bind("<Double-1>", lambda e: self.abrir_formulario(self.tree.item(self.tree.selection())['values']))
        
        btn_frame = tk.Frame(self.window); btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="+ Añadir", command=self.abrir_formulario, bg="#9C27B0", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Eliminar", command=self.eliminar, bg="#f44336", fg="white").pack(side="left", padx=5)
        self.refrescar()

    def refrescar(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for r in self.db.ejecutar("SELECT id, titulo, autor, genero, precio, idioma FROM deseados"):
            self.tree.insert("", "end", values=(r[0], r[1], r[2], r[3], f"{r[4]:.2f}€", r[5]))

    def abrir_formulario(self, datos=None):
        f = tk.Toplevel(self.window); f.title("Detalle Deseo"); f.geometry("300x450"); f.grab_set()
        
        tk.Label(f, text="Título *").pack()
        e_t = tk.Entry(f); e_t.pack()
        tk.Label(f, text="Autor *").pack()
        e_a = tk.Entry(f); e_a.pack()
        tk.Label(f, text="Precio (€) *").pack()
        e_pr = tk.Entry(f); e_pr.pack()
        tk.Label(f, text="Idioma").pack()
        e_i = tk.Entry(f); e_i.pack()

        if datos:
            e_t.insert(0, datos[1]); e_a.insert(0, datos[2])
            e_pr.insert(0, str(datos[4]).replace('€',''))
            e_i.insert(0, datos[5])

        def guardar():
            if not e_t.get().strip() or not e_pr.get().strip():
                messagebox.showwarning("Faltan datos", "Título y Precio son obligatorios.")
                return
            try:
                precio = float(e_pr.get().replace(',', '.'))
                vals = (e_t.get(), e_a.get(), 0, "Varios", precio, e_i.get())
                if datos:
                    self.db.ejecutar("UPDATE deseados SET titulo=?, autor=?, paginas=?, genero=?, precio=?, idioma=? WHERE id=?", vals + (datos[0],))
                else:
                    self.db.ejecutar("INSERT INTO deseados (titulo, autor, paginas, genero, precio, idioma) VALUES (?,?,?,?,?,?)", vals)
                f.destroy(); self.refrescar()
            except ValueError:
                messagebox.showerror("Error", "Precio debe ser un número (ej: 19.99).")

        tk.Button(f, text="Guardar", command=guardar, bg="#9C27B0", fg="white").pack(pady=10)

    def eliminar(self):
        sel = self.tree.selection()
        if sel:
            self.db.ejecutar("DELETE FROM deseados WHERE id=?", (self.tree.item(sel)['values'][0],))
            self.refrescar()