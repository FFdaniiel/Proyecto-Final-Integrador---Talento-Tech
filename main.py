from funciones_menu import *
from funciones_database import db_crear_tabla_productos


# Pre - Entrega de Proyecto

# Menu
def main() :
# inicializamos la tabla producto 
    db_crear_tabla_productos()
#----- Menu -----
    while True :
        opcion = menu_mostrar_opciones()

        match opcion:
            case "1" | "añadir producto":
                menu_registrar_producto()
            case "2" | "mostrar el inventario":
                menu_mostrar_productos()
            case "3" | "buscar producto por ID":
                menu_buscar_producto_by_id()
            case "4" | "buscar por nombre/categoría":
                menu_buscar_productos_by_condicion()
            case "5" | "actualizar producto":
                menu_actualizar_producto()
            case "6" | "eliminar producto":
                menu_eliminar_producto()
            case "7" | "reporte bajo stock":
                menu_reporte_bajo_stock()
            case "8" | "salir":
                print("Gracias por usar nuestro servicio de control de stock 🥰")
                break
            case _:
                print("Opción no válida 🫠")

main()