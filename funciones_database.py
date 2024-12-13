import sqlite3


# Var/Const
DB_NAME = "./inventario.db"

# FUNCIONES DATABASE

# Crear tabla_productos()
"""
    Utilizamos los datos sqlite3 para crear/conectarse a la base "Inventario.db" y crea la tabla productos          
"""
def db_crear_tabla_productos():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS productos (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nombre TEXT NOT NULL,
                   descripcion TEXT,
                   categoria TEXT NOT NULL,
                   precio REAL NOT NULL,
                   cantidad INTEGER NOT NULL
                   )
                   """ )
    conexion.commit()
    conexion.close()


# db_insertar_producto(productos)
"""
 1. recibe como argumento un diccionario con las claves/valor de cada campo de la tabla
 2. Inserta los datos en la tabla productos
 3. Cierra la conexión
"""
def db_insertar_producto(producto) :
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    query = 'INSERT INTO productos (nombre, descripcion, categoria, precio, cantidad) VALUES (?,?,?,?,?)'
    placeholder = ( producto['nombre'], producto['descripcion'], producto['categoria'], producto['precio'], producto['cantidad'])
    cursor.execute( query , placeholder  )
    
    conexion.commit()
    conexion.close()

"""
db_get_productos()

1. lee todos los datos de la tabla productos
2. retorna una lista de tuplas con los datos de la tabla

"""
def db_get_productos():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    query = "SELECT * FROM productos"
    cursor.execute(query)
    productos = cursor.fetchall()
    conexion.close()
    return productos


"""
db_get_producto_by_id(id)

1. busco y retorno el registro según el id
2. retorno una tupla con el resultado
"""

def db_get_producto_by_id(id):
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        query = "SELECT * FROM productos WHERE id = ?"
        placeholders = (id,)
        cursor.execute(query, placeholders)
        producto = cursor.fetchone()
        conexion.close()
        return producto
    except sqlite3.Error as e:
        print(f"Error al obtener el producto: {e}")

"""
db_get_producto_by_condicion(condicion_busqueda)

1. busco y retorno los registros según la condición de búsqueda
2. retorno una lista de tuplas con los resultados
"""

def db_buscar_productos_by_condicion(condicion_busqueda):
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        query = """SELECT * FROM productos 
                  WHERE nombre LIKE ? OR categoria LIKE ?"""
        termino = f"%{condicion_busqueda}%"  # Los % Como comodines para lograr una búsqueda mas flexible
        placeholders = (termino, termino)
        cursor.execute(query, placeholders)
        productos = cursor.fetchall()
        conexion.close()
        return productos
    except sqlite3.Error as e:
        print(f"Error en la búsqueda: {e}")
        return False


"""
db_actualizar_producto(id, nueva_cantidad)

1. actualiza la cantidad y precio del producto según el id
"""

def db_actualizar_producto(id, nueva_cantidad, nuevo_precio): 
    try:
        conexion = sqlite3.connect( DB_NAME )
        cursor = conexion.cursor()
        query = "UPDATE productos SET cantidad = ?, precio = ? WHERE id = ?"
        placeholders = (nueva_cantidad, nuevo_precio, id)
        cursor.execute(query, placeholders)
        conexion.commit()
        conexion.close()

        return True  # Retorna True si todo salió bien       
    except sqlite3.Error as e: # esto es para capturar errores
         print(f"Error al actualizar: {e}")
         # Retorna False si hubo algún error
         return False

"""
db_eliminar_producto(id)

1. eliminar de la tabla el producto con el id que recibo como argumento
"""
def db_eliminar_producto(id):
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        query = "DELETE FROM productos WHERE id = ?"
        placeholders = (id,)
        cursor.execute(query, placeholders)
        conexion.commit()
        conexion.close()

        return True  # Retorna True si todo salió bien
    except sqlite3.Error as e: # esto es para capturar errores
         print(f"Error al actualizar: {e}")
         # Retorna False si hubo algún error
         return False


"""
db_get_productos_by_condicion(minimo_stock)

1. retornar una lista_producto con aquellos registros cuya cantidad < minimo_stock
"""


def db_get_productos_by_condicion(minimo_stock):
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        query = "SELECT * FROM productos WHERE cantidad < ?"
        placeholders = (minimo_stock,)
        cursor.execute(query, placeholders)
        lista_productos = cursor.fetchall()
        conexion.close()
        return lista_productos # Retorna la lista de productos
    except sqlite3.Error as e: # esto es para capturar errores
        print(f"Error al obtener productos: {e}")
        # Retorna False si hubo algún error
        return False
    