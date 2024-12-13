from funciones_database import *

#----- funciones ------


# validar las opciones numéricas de los productos para evitar errores de tipeo
def validacionNumerica(m, tipo=float):
    while True:
        try:
            return tipo(input(m))  # Intenta convertir la entrada al tipo deseado
        except ValueError: # si ocurre un error
            print(f"Por favor, ingresa un valor numérico válido para {m[-2].lower()}.") #  tomar toda la cadena menos los últimos dos caracteres

# valida texto 
def validacion_texto(mensj, campo):
    while True:
        campo = campo.capitalize()
        texto = input(mensj).strip()
        if texto:
            return texto
        else:
            print(f"{campo} no puede estar vacío.")


# FUNCIONES generales

def menu_mostrar_opciones():
    menuOpciones = [
        'Añadir producto',
        'Mostrar el inventario',
        'Buscar producto',
        'Buscar por nombre/categoría',
        'Actualizar producto',
        'Eliminar producto',
        'reporte bajo stock',
        'Salir',
    ]
    print('Ingresa la acción que quieres realizar:\n')
    for i in range(len(menuOpciones)):
        print(f'{i+1}. - {menuOpciones[i]}')
    
    opciones = input(f'- ')
    return opciones.lower()

# agrega productos a la lista de productos
def menu_registrar_producto() :
    # obtenemos los valores
    nombre = validacion_texto("Nombre del producto: ", "nombre") # validamos el texto y lo devolvemos
    descripcion = input("Descripción del producto: ") # agregar descripción | al ser opcional no necesito un validador
    categoria = validacion_texto('Categoria del producto: ', 'categoria') # agregamos categoría
    cantidad = validacionNumerica('Cantidad: ', int) # Valida y obtiene la cantidad como int
    precio = validacionNumerica('Precio unitario: ') # toma por defecto float

    # TO DO : VALIDAR ERRORES Y TIPO DE DATOS

    # Creamos un diccionario con los datos del producto
    producto = {
        "nombre": nombre,
        "descripcion": descripcion,
        "categoria": categoria,
        "cantidad": cantidad,
        "precio": precio
    }

    # LLAMAR A LA FUNCIÓN QUE INSERTA EN LA BD
    db_insertar_producto(producto)
    print("El producto fue añadido correctamente! 😉")

# Muestra la lista de productos
def menu_mostrar_productos():
    productos = db_get_productos()

    if not productos:
        print("No se encuentran productos en el inventario...")
    else:
        print("\n=================== INVENTARIO ===================\n")
        print("Bajo Stock: 🟥 | Medio Stock: 🟨 | Normal Stock: 🟩\n")
        for producto in productos:
            cantidad = producto[5]  # índice 5 corresponde a la cantidad
            estadoStock = "🟥" if cantidad <= 10 else "🟨" if cantidad <= 30 else "🟩"
            print(f"Id: {producto[0]}\nNombre: {producto[1]}\nCategoria: {producto[3]}\nDescripción: {producto[2]}\nCantidad: {producto[5]}\nPrecio: ${producto[4]:.2f}\nStock: {estadoStock}\n")
            print("-" * 48)        
        print("\n================ FIN INVENTARIO ==================")

# Actualizar producto 
def menu_actualizar_producto():
    id = int(input("\nIngrese el id del producto a actualizar: "))
    get_producto = db_get_producto_by_id(id)

    if not get_producto:
        print("Producto no encontrado. 😕")
    else:
        print("Producto encontrado. Ingresa los nuevos valores (deja en blanco para mantener el valor actual).")

        # Guardamos los valores actuales en caso de que no se modifiquen
        cantidad_actual = get_producto[5]
        precio_actual = get_producto[4]

        # Input para nuevos valores 
        nuevaCantidad = input(f"Cantidad actual: {cantidad_actual} - Nueva cantidad: ")
        nuevoPrecio = input(f"Precio actual: ${precio_actual} - Nuevo precio: ")

        # Si está vacío, mantener el valor actual
        nuevaCantidad = int(nuevaCantidad) if nuevaCantidad != "" else cantidad_actual
        nuevoPrecio = float(nuevoPrecio) if nuevoPrecio != "" else precio_actual


        if db_actualizar_producto(id, nuevaCantidad, nuevoPrecio):
            print("Producto actualizado correctamente! ✓")

# eliminar producto 
def menu_eliminar_producto():
    id = int(input("\nIngrese el id del producto a eliminar: "))
    get_producto = db_get_producto_by_id(id)

    if not get_producto:
        print('Producto no encontrado o no existe.')
    else:
        print(f'¿Desea eliminar el producto {get_producto[1]}?')
        respuesta = input('Ingresa S/N o escribe "si" o "no": ')
        if respuesta.lower() in ['s', 'si']:
            if db_eliminar_producto(id):
                print('Producto eliminado correctamente!')
            else:
                print('Error al eliminar el producto.')

"""
menu_buscar_productos_by_condicion()

1. Solicita al usuario un término de búsqueda
2. Busca coincidencias en nombre y categoría
3. Muestra los resultados encontrados con formato
4. Maneja el caso de no encontrar coincidencias
"""
def menu_buscar_producto_by_id():
        id = int(input("\nIngrese el id del producto que desea consultar: "))
        producto = db_get_producto_by_id(id)
        if not producto:
            print("Producto no encontrado.")
        else:
            print('El fue encontrado. ✓')
            print("\n=============== RESULTADOS BÚSQUEDA ===============\n")
            print(f"\nId: {producto[0]}\nNombre: {producto[1]}\nCategoria: {producto[3]}\nDescripción: {producto[2]}\nCantidad: {producto[5]}\nPrecio: ${producto[4]}\n")
            print("\n================== FIN BÚSQUEDA ==================")

# Función para buscar de manera flexible ya sea por nombre o categoría
def menu_buscar_productos_by_condicion():
    busqueda = input("\nIngrese el nombre o categoría a buscar: ").strip()
    productos = db_buscar_productos_by_condicion(busqueda)
    if busqueda:
        if productos:
            print("\n=============== RESULTADOS BÚSQUEDA ===============\n")
            for producto in productos:
                print(f"\nId: {producto[0]}\nNombre: {producto[1]}\nCategoria: {producto[3]}\nDescripción: {producto[2]}\nCantidad: {producto[5]}\nPrecio: ${producto[4]}\n")
                print("-" * 48)
            print("\n================== FIN BÚSQUEDA ==================")
        else:
            print("No se encontraron productos que coincidan con la búsqueda.")
    else:
        print("Debe ingresar un término de búsqueda.")

# Función que genera un reporte de Bajo Stock
def menu_reporte_bajo_stock():
    minimo_stock= int(input("\nIngrese el valor mínimo de stock para generar el reporte: "))
    productos = db_get_productos_by_condicion(minimo_stock)
    if not productos:
        print("No hay productos con stock bajo.")
    else:
        print("Productos con stock bajo:")
        print("\n=============== RESULTADOS REPORTE ===============\n") 
        for producto in productos:
            print(f"Id: {producto[0]}\nNombre: {producto[1]}\nCategoria: {producto[3]}\nDescripción: {producto[2]}\nCantidad: {producto[5]}\nPrecio: ${producto[4]}\n")
            print("-" * 48)
        print("\n================== FIN REPORTE ==================")
