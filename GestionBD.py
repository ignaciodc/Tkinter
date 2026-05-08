import sqlite3

# Gestión de la Base de Datos con SQLite

class GestionBD:
    def __init__(self, db_name="biblioteca_personal.db"):
        try:
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
            self.inicializar_tablas()
        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo conectar: {e}")

    def inicializar_tablas(self):
        try:
            # Creación de la tabla "libros" para libros comprados

            self.cursor.execute("""CREATE TABLE IF NOT EXISTS libros 
                (id INTEGER PRIMARY KEY, titulo TEXT, autor TEXT, paginas INTEGER, genero TEXT, leido INTEGER, resena TEXT)""")
            # Creación de la tabla "deseados" para libros que se desean comprar

            self.cursor.execute("""CREATE TABLE IF NOT EXISTS deseados 
                (id INTEGER PRIMARY KEY, titulo TEXT, autor TEXT, paginas INTEGER, genero TEXT, precio REAL, idioma TEXT)""")
            # Creación de la tabla "prestados" para libros prestados a otros

            self.cursor.execute("""CREATE TABLE IF NOT EXISTS prestados 
                (id INTEGER PRIMARY KEY, titulo TEXT, autor TEXT, dueno TEXT, genero TEXT, devuelto INTEGER)""")
            self.conn.commit()
            
        except sqlite3.Error as e:
            print(f"Error al crear tablas: {e}")

    def ejecutar(self, query, params=()):
        """Ejecuta una consulta y gestiona errores de ejecución"""
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Error SQL", f"Error al ejecutar consulta: {e}")
            return []