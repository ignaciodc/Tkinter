import tkinter as tk
from tkinter import messagebox, ttk
from VentanaBase import VentanaBase

# Clase: VentanaLibros - Ventana para gestionar los libros comprados

class VentanaLibros(VentanaBase):
    def __init__(self, master, db_manager):
        super().__init__(master, "Mis Libros Comprados", ("ID", "Título", "Autor", "Páginas", "Género", "¿Leído?", "Reseña"), db_manager)
        self.configurar_tabla()
        
        self.tree.bind("<Double-1>", self.validar_y_editar)        
        
        btn_frame = tk.Frame(self.window); btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="+ Añadir Nuevo", command=self.crear_nuevo, bg="#4CAF50", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Eliminar", command=self.eliminar, bg="#f44336", fg="white").pack(side="left", padx=5)
        self.refrescar()

    def refrescar(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for r in self.db.ejecutar("SELECT * FROM libros"):
            self.tree.insert("", "end", values=(r[0], r[1], r[2], r[3], r[4], "Sí" if r[5] else "No", r[6]))

    def crear_nuevo(self): 
        self.abrir_formulario() # Sin datos = Crear

    def validar_y_editar(self, event):
        """Solo permite editar si el doble clic cae sobre una fila real"""
        item_id = self.tree.identify_row(event.y) # Identifica la fila bajo el cursor
        
        if item_id:
            # Si hay una fila, la seleccionamos visualmente y abrimos formulario
            self.tree.selection_set(item_id)
            valores = self.tree.item(item_id)['values']
            self.abrir_formulario(valores)
        # Si item_id es "", no ocurre nada (el doble clic en vacío se ignora)

    def abrir_formulario(self, datos=None):
        f = tk.Toplevel(self.window)
        f.title("Editar Libro" if datos else "Nuevo Libro")
        f.geometry("350x500")
        f.grab_set() # Bloquea la tabla mientras se edita

        tk.Label(f, text="Título").pack(); e_t = tk.Entry(f); e_t.pack()
        tk.Label(f, text="Autor").pack(); e_a = tk.Entry(f); e_a.pack()
        tk.Label(f, text="Páginas").pack(); e_p = tk.Spinbox(f, from_=0, to=9999); e_p.pack()
        v_l = tk.IntVar()
        tk.Checkbutton(f, text="¿Leído?", variable=v_l).pack()

        if datos:
            e_t.insert(0, datos[1]); e_a.insert(0, datos[2])
            e_p.delete(0, "end"); e_p.insert(0, datos[3]); v_l.set(1 if datos[5] == "Sí" else 0)

        def guardar():
            if not e_t.get().strip(): return messagebox.showwarning("Aviso", "Título requerido")
            vals = (e_t.get(), e_a.get(), e_p.get(), "General", v_l.get(), "")
            if datos:
                self.db.ejecutar("UPDATE libros SET titulo=?, autor=?, paginas=?, genero=?, leido=?, resena=? WHERE id=?", vals + (datos[0],))
            else:
                self.db.ejecutar("INSERT INTO libros (titulo, autor, paginas, genero, leido, resena) VALUES (?,?,?,?,?,?)", vals)
            f.destroy(); self.refrescar()

        tk.Button(f, text="Guardar", command=guardar, bg="blue", fg="white").pack(pady=20)

    def eliminar(self):
        sel = self.tree.selection()
        if sel and messagebox.askyesno("Confirmar", "¿Eliminar registro?"):
            self.db.ejecutar("DELETE FROM libros WHERE id=?", (self.tree.item(sel)['values'][0],))
            self.refrescar()