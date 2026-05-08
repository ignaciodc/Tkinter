import tkinter as tk
from tkinter import messagebox, ttk
from VentanaBase import VentanaBase

# Clase: VentanaPrestados - Ventana para gestionar los libros prestados

class VentanaPrestados(VentanaBase):
    def __init__(self, master, db_manager):
        super().__init__(master, "Libros Prestados", ("ID", "Título", "Autor", "Dueño", "Género", "¿Devuelto?"), db_manager)
        self.configurar_tabla()
        self.tree.bind("<Double-1>", lambda e: self.abrir_formulario(self.tree.item(self.tree.selection())['values']))
        
        btn_frame = tk.Frame(self.window); btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="+ Nuevo Préstamo", command=self.abrir_formulario, bg="#FF9800", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Eliminar", command=self.eliminar, bg="#f44336", fg="white").pack(side="left", padx=5)
        self.refrescar()

    def refrescar(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for r in self.db.ejecutar("SELECT * FROM prestados"):
            self.tree.insert("", "end", values=(r[0], r[1], r[2], r[3], r[4], "Sí" if r[5] else "No"))

    def abrir_formulario(self, datos=None):
        f = tk.Toplevel(self.window); f.title("Detalle Préstamo"); f.geometry("300x400"); f.grab_set()
        tk.Label(f, text="Título del libro *").pack()
        e_t = tk.Entry(f); e_t.pack()
        tk.Label(f, text="Persona / Dueño *").pack()
        e_d = tk.Entry(f); e_d.pack()
        v_d = tk.IntVar()
        tk.Checkbutton(f, text="¿Ya se ha devuelto?", variable=v_d).pack()

        if datos:
            e_t.insert(0, datos[1]); e_d.insert(0, datos[3]); v_d.set(1 if datos[5] == "Sí" else 0)

        def guardar():
            if not e_t.get().strip() or not e_d.get().strip():
                messagebox.showwarning("Faltan datos", "El título y el dueño son necesarios.")
                return
            vals = (e_t.get(), "N/A", e_d.get(), "Préstamo", v_d.get())
            if datos:
                self.db.ejecutar("UPDATE prestados SET titulo=?, autor=?, dueno=?, genero=?, devuelto=? WHERE id=?", vals + (datos[0],))
            else:
                self.db.ejecutar("INSERT INTO prestados (titulo, autor, dueno, genero, devuelto) VALUES (?,?,?,?,?)", vals)
            f.destroy(); self.refrescar()
        
        tk.Button(f, text="Guardar", command=guardar, bg="#FF9800", fg="white").pack(pady=10)

    def eliminar(self):
        sel = self.tree.selection()
        if sel:
            self.db.ejecutar("DELETE FROM prestados WHERE id=?", (self.tree.item(sel)['values'][0],))
            self.refrescar()