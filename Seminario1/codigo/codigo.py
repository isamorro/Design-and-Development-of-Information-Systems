import oracledb
import config

# Función para conectarse a la base de datos Oracle
def conectar_bd():
    try:
        conn = oracledb.connect(user=config.username, password=config.password, host=config.dsn, port=config.port, service_name=config.service_name)
        print("Conexión exitosa a la base de datos")
        return conn
    except oracledb.DatabaseError as e:
        print("Error al conectarse a la base de datos", e)
        return None

# Función para crear tablas y predefinir datos
def crear_tablas(conn):
    try:
		
        # Crea objeto asociado con la conexión conn
        # así cursor nos permite interactuar con la BD
        cursor = conn.cursor()
        
		# Función auxiliar para eliminar tablas si existen
        def drop_table_if_exists(table_name):
            cursor.execute(f"BEGIN EXECUTE IMMEDIATE 'DROP TABLE {table_name}'; EXCEPTION WHEN OTHERS THEN NULL; END;")
        
        # Eliminar tablas si existen
        drop_table_if_exists('detalle_pedido')
        drop_table_if_exists('pedido')
        drop_table_if_exists('stock')
        
        # Se vuelven a crear las tablas
        # cursor.execute nos permite ejecutar sentencias SQL
        cursor.execute("""
        CREATE TABLE stock (
            cproducto NUMBER(4) CONSTRAINT Cproducto PRIMARY KEY,
            cantidad NUMBER(4) CONSTRAINT Cantidad NOT NULL
        )""")
        
        cursor.execute("""
        CREATE TABLE pedido (
            cpedido NUMBER(4) CONSTRAINT cpedido_clave_primaria PRIMARY KEY,
            ccliente NUMBER(4),
            fecha_pedido DATE
        )""")
        
        cursor.execute("""
        CREATE TABLE detalle_pedido (
            cpedido CONSTRAINT cpedido_clave_externa_pedido 
                REFERENCES pedido(cpedido),
            cproducto CONSTRAINT cproducto_clave_externa_producto
                REFERENCES stock(cproducto),
            cantidad NUMBER(4),
            CONSTRAINT clave_primaria PRIMARY KEY (cpedido, cproducto)
        )""")
        
        # Insertamos 10 tuplas predefinidas en la tabla Stock
        cursor.executemany("""
        INSERT INTO stock (cproducto, cantidad)
        VALUES (:1, :2)""", 
        [(1, 10), (2, 20), (3, 30), 
         (4, 40), (5, 50), (6, 60),
         (7, 70), (8, 80), (9, 90), 
         (10, 100)])
        
        # Aqui estamos diciendo que a inserción de las 10 tuplas es una sola 
        # transacción
        # Pero conceptualmente se deberían hacer las 10 operaciones de inserción
        # por separado
        # Se debe hacer cada inserción con un commit

        # conn.commit confirma los cambios realizados en la BD durante la sesión
        # si no se ejecuta, los cmabios no se reflejan en la BD
        conn.commit()
        print("\nTablas creadas y datos insertados.")

    except oracledb.DatabaseError as e:
        print("Error al crear las tablas o insertar datos:", e)
        conn.rollback()


# Función para dar de alta un nuevo pedido
def nuevo_pedido(conn):
    try:
        cursor = conn.cursor()

        # Elimina el pedido y todos sus detalles
        # Este safepoint en realidad no debería estar es innecesario, no es un punto intermedio
        # Se bería hacer un rollback a secas
        cursor.execute("SAVEPOINT savepoint1")

        print("\nInserta los datos del pedido: ")

        # Se pide la inserción del cod de l pedido hasta q sea numérico 
        cod = input("Código del pedido (numérico): ")
        while (not cod.isnumeric()):
            print("\n Por favor, introduzca un número menor que 10000: ")
            cod = input("Código del pedido: ")

        # Se pide cod del cliente hasta que sea numérico
        cli = input("Código del cliente (numérico): ")
        while (not cli.isnumeric()):
            print("\n Por favor, introduzca un número menor que 10000: ")
            cli = input("Código del cliente: ")

        cursor.execute("INSERT INTO pedido (cpedido, ccliente, fecha_pedido) VALUES (:1, :2, SYSDATE)", (cod, cli))
        
        # Savepoint para guardar el pedido pero borrar los detalles-pedido
        cursor.execute("SAVEPOINT savepoint2")
        
        while True:

            print("\n1. Añadir detalle de producto")
            print("2. Eliminar todos los detalles de producto")
            print("3. Cancelar pedido")
            print("4. Finalizar pedido")
            opcion = input("Seleccione una opción: ")

            # Añadir detalle de producto
            if opcion == '1':
                cproducto = input("Código del producto (numérico): ")
                while (not cproducto.isnumeric()):
                    print("\n Por favor, introduzca un número menor que 10000: ")
                    cproducto = input("Código del producto (numérico): ")

                cantidad = input("Cantidad (numérico): ")

                while (not cantidad.isnumeric()):
                    print("\n Por favor, introduzca un número menor que 10000: ")
                    cantidad = input("Código del producto (numérico): ")
                
                cantidad = int(cantidad)
                cursor.execute("SELECT cantidad FROM stock WHERE cproducto = :1", [cproducto])
                # cortafuegos guarda los resultados del SELECT
                cortafuegos = cursor.fetchone()

                # Verifica si hay datos en el resultado
                if cortafuegos is not None:
                    # Guarda la cantidad del SELECT en stock disponible
                    stock_disponible = cortafuegos[0] 
                else:
                    print("No se encontraron registros.")
                    stock_disponible=0
                
                # Eliminamos la cantidad del stock si hay suficiente
                if cantidad <= stock_disponible:
                    cursor.execute("""
                    INSERT INTO detalle_pedido (cpedido, cproducto, cantidad) 
                    VALUES (:1, :2, :3)
                    """, (cod, cproducto, cantidad))
                    cursor.execute("UPDATE stock SET cantidad = cantidad - :1 WHERE cproducto = :2", (cantidad, cproducto))
                    print("Producto añadido al pedido.")
                else:
                    print("Stock insuficiente.")

            # Elimina detalles del pedido (pero el pedido no) 
            elif opcion == '2':
                print("Detalles del pedido eliminados.")
                cursor.execute("ROLLBACK TO savepoint2")

            # Eliminar pedido por completo
            elif opcion == '3':
                print("Pedido cancelado.")
                # Se debe usar un ROLLBACK a secas 
                # Un savepoint debe estar intermedio
                cursor.execute("ROLLBACK TO savepoint1")
                return
            
            # Se finaliza el pedido, se guarda
            elif opcion == '4':
                print("Pedido finalizado con éxito.")
                # Se hacen permanentes los cambios
                conn.commit()
                return
            else:
                print("Opción no válida.")

    except oracledb.DatabaseError as e:
        print("Error al procesar el pedido:", e)
        cursor.execute("ROLLBACK TO savepoint1")

# Mostrar el contenido de las tablas
def mostrar_tablas(conn):
    try:
        cursor = conn.cursor()
        print("\nTabla Stock:")
        cursor.execute("SELECT * FROM Stock")
        for row in cursor:
            print(row)
        
        print("\nTabla Pedido:")
        cursor.execute("SELECT cpedido, ccliente, to_char(fecha_pedido, 'DD/MON/YYYY HH24:MI:SS') FROM Pedido")
        for row in cursor:
            print(row)

        print("\nTabla detalle_pedido:")
        cursor.execute("SELECT * FROM detalle_pedido")
        for row in cursor:
            print(row)

    except oracledb.DatabaseError as e:
        print("Error al mostrar el contenido de las tablas:", e)

# Menú principal
def menu_principal(conn):
    
    while True:
        print("\n--- Menú Principal ---")
        print("1. Borrar y crear tablas")
        print("2. Dar de alta nuevo pedido")
        print("3. Mostrar contenido de las tablas")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            crear_tablas(conn)
            mostrar_tablas(conn)
        elif opcion == '2':
            nuevo_pedido(conn)
            mostrar_tablas(conn)
        elif opcion == '3':
            mostrar_tablas(conn)
        elif opcion == '4':
            conn.close()
            print("Conexión cerrada. Salir del programa.")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    conn = conectar_bd()
    if conn:
        menu_principal(conn)

