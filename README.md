# 📘 Manual: Interfaces Gráficas con Tkinter

Este repositorio contiene un manual para aprender a desarrollar aplicaciones de escritorio utilizando **Python** en **Tkinter** y persistencia de datos con **SQLite3**.

---

## 📅 Fundamentos y la Ventana Raíz
Toda aplicación en Tkinter tiene tres pasos obligatorios para cobrar vida.

### 1.1 La Anatomía de una App
1. **Importar** la librería.
2. **Crear** la ventana principal (la raíz).
3. **Ejecutar** el bucle de eventos (`mainloop`).

```python
import tkinter as tk

# Crear la base de nuestra app
app = tk.Tk()
app.title("Mi Manual de Tkinter")
app.geometry("400x200") # Ancho x Alto

# Mantiene la ventana abierta y "escuchando" al usuario
app.mainloop()

```

## 📅 Los Ladrillos (Widgets Básicos)
Los **widgets** son los componentes individuales de la interfaz. Para que una app sea funcional, necesitamos mostrar información y recibir datos.

### 2.1 Los Tres Pilares
* **Label (Etiqueta):** Espacios de texto no editable para dar instrucciones.
* **Entry (Entrada):** Campos donde el usuario puede escribir información.
* **Button (Botón):** El ejecutor. Su función principal se activa con el parámetro `command`.

```python
import tkinter as tk

def saludar():
    nombre = caja_texto.get()
    etiqueta_msg.config(text=f"¡Bienvenido, {nombre}!")

app = tk.Tk()
app.title("Widgets")

# 1. Etiqueta de instrucción
tk.Label(app, text="Escribe tu nombre:").pack(pady=5)

# 2. Caja de entrada de datos
caja_texto = tk.Entry(app)
caja_texto.pack(pady=5)

# 3. Botón de acción
tk.Button(app, text="Saludar", command=saludar).pack(pady=10)

# Etiqueta de respuesta (vacía al inicio)
etiqueta_msg = tk.Label(app, text="")
etiqueta_msg.pack()

app.mainloop()

```

## 📅 El Arte del Orden (Sistema Grid)
En el desarrollo profesional, rara vez usamos `.pack()`. En su lugar, utilizamos el gestor de geometría **Grid**. 

### 1 El Concepto de Rejilla
Imagina que la ventana de tu aplicación es una tabla de Excel o una cuadrícula invisible. Cada elemento se coloca indicando su posición exacta.

* **Row (Fila):** La posición vertical (0 es la de arriba).
* **Column (Columna):** La posición horizontal (0 es la de la izquierda).
* **Sticky:** Define hacia qué lado se "pega" el widget (N, S, E, W).
* **Padding (padx/pady):** Añade "aire" o margen alrededor del widget para que no esté pegado a los bordes.



### 2 Ejemplo: Formulario de Login Ordenado
```python
import tkinter as tk

app = tk.Tk()
app.title("Dominando el Grid")
app.geometry("300x150")

# Fila 0: Usuario
tk.Label(app, text="Usuario:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
tk.Entry(app).grid(row=0, column=1, padx=10)

# Fila 1: Contraseña
tk.Label(app, text="Contraseña:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
tk.Entry(app, show="*").grid(row=1, column=1, padx=10)

# Fila 2: Botón Iniciar
# Columnspan=2 hace que el botón ocupe el ancho de las dos columnas
tk.Button(app, text="Entrar", width=10).grid(row=2, column=0, columnspan=2, pady=15)

app.mainloop()

```

## 📅 Widgets Modernos (ttk) y Alertas
Para que nuestras aplicaciones no parezcan antiguas, utilizamos el módulo **ttk** (Themed Tkinter). Además, aprenderemos a comunicarnos con el usuario mediante ventanas emergentes.

### 1 El módulo ttk
`ttk` nos da acceso a widgets mejorados como el **Combobox** (listas desplegables). La sintaxis es casi igual, pero el acabado visual es muy superior.

### 2 Messagebox (Alertas)
Es vital dar feedback al usuario. Si algo sale bien o mal, usamos `messagebox`:
* `showinfo`: Para éxitos o información general.
* `showwarning`: Para avisos importantes.
* `showerror`: Para errores críticos.

### 3 Ejemplo: Selector de Perfil con Alerta
```python
import tkinter as tk
from tkinter import ttk, messagebox # Importamos los módulos específicos

def confirmar_seleccion():
    opcion = combo.get()
    if opcion:
        messagebox.showinfo("Éxito", f"Perfil '{opcion}' configurado correctamente.")
    else:
        messagebox.showwarning("Atención", "Por favor, selecciona un perfil antes de continuar.")

app = tk.Tk()
app.title("ttk y Mensajes")
app.geometry("350x200")

tk.Label(app, text="Selecciona tu perfil de usuario:", font=("Arial", 10)).pack(pady=10)

# El Combobox es de ttk
combo = ttk.Combobox(app, values=["Administrador", "Editor", "Invitado"], state="readonly")
combo.pack(pady=5)

# Botón moderno de ttk
boton = ttk.Button(app, text="Guardar Configuración", command=confirmar_seleccion)
boton.pack(pady=20)

app.mainloop()

```

## 📅 Persistencia con SQLite3 (La Memoria de la App)
Una interfaz sin base de datos es como un formulario que se borra solo. Para solucionar esto, integramos **SQLite3**, un sistema de base de datos ligero que guarda la información en un archivo local.

### 1 El Ciclo de Vida de los Datos
Para trabajar con bases de datos en Python, seguimos siempre estos 4 pasos:
1. **Conectar:** Abrimos el archivo de la base de datos.
2. **Cursor:** Creamos un "mensajero" (cursor) para ejecutar las órdenes SQL.
3. **Ejecutar (Execute):** Enviamos la orden (Crear tabla, Insertar, Borrar).
4. **Confirmar (Commit) y Cerrar:** Guardamos los cambios y liberamos el archivo.



### 2 Ejemplo: Crear una Base de Datos y Guardar Información
```python
import sqlite3

def registrar_alumno(nombre_alumno):
    # 1. Conectamos (si el archivo no existe, se crea solo)
    conexion = sqlite3.connect("academia.db")
    cursor = conexion.cursor()

    # 2. Creamos la tabla (solo si no existe)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alumnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        )
    """)

    # 3. Insertamos el dato (usamos ? para evitar ataques de inyección SQL)
    cursor.execute("INSERT INTO alumnos (nombre) VALUES (?)", (nombre_alumno,))

    # 4. Guardamos y cerramos
    conexion.commit()
    conexion.close()
    print(f"Alumno '{nombre_alumno}' guardado en la base de datos.")

# Prueba de la función
registrar_alumno("Ignacio")

```

## 📅 Sistema CRUD Completo
El objetivo es integrar la interfaz gráfica (Tkinter), la estética moderna (ttk) y la persistencia de datos (SQLite3) en una sola aplicación funcional.

### 1 El Widget Treeview:
Para mostrar los datos de la base de datos de forma profesional, utilizamos el widget `Treeview`. Es una tabla avanzada que permite ver columnas y filas de datos de manera organizada.

### 2 Estructura del Sistema:
Un CRUD bien construido se divide en:
1. **Interfaz (Vista):** Formulario con `Grid` para introducir datos.
2. **Base de Datos (Modelo):** Funciones SQL para insertar y consultar.
3. **Lógica (Controlador):** Funciones que conectan los botones con la base de datos y refrescan la tabla.

### 3 Ejemplo de Estructura Completa (Mini CRUD)
```python
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# --- FUNCIONES DE BASE DE DATOS ---
def conectar_bd():
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS productos (id INTEGER PRIMARY KEY, nombre TEXT, precio REAL)")
    conn.commit()
    return conn

def guardar_producto():
    nombre = entry_nombre.get()
    precio = entry_precio.get()
    
    if nombre and precio:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos (nombre, precio) VALUES (?, ?)", (nombre, precio))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Producto guardado")
        limpiar_campos()
    else:
        messagebox.showerror("Error", "Todos los campos son obligatorios")

def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_precio.delete(0, tk.END)

# --- INTERFAZ GRÁFICA ---
app = tk.Tk()
app.title("CRUD Inventario")

# Formulario
tk.Label(app, text="Nombre Producto:").grid(row=0, column=0, padx=10, pady=10)
entry_nombre = tk.Entry(app)
entry_nombre.grid(row=0, column=1)

tk.Label(app, text="Precio:").grid(row=1, column=0, padx=10, pady=10)
entry_precio = tk.Entry(app)
entry_precio.grid(row=1, column=1)

# Botones
tk.Button(app, text="Guardar Registro", command=guardar_producto, bg="#2ecc71", fg="white").grid(row=2, column=0, columnspan=2, pady=10, sticky="nsew")

app.mainloop()
```
