import oracledb
import config
import datetime
#===================================================================================
# Función para conectarse a la base de datos Oracle
#===================================================================================
def conectar_bd():
    try:
        conn = oracledb.connect(user=config.username, password=config.password, host=config.dsn, port=config.port, service_name=config.service_name)
        print("Conexión exitosa a la base de datos")
        return conn
    except oracledb.DatabaseError as e:
        print("Error al conectarse a la base de datos", e)
        return None
#===================================================================================
# Función para crear tablas y predefinir datos
#===================================================================================
def crear_tablas(conn):
    try:
		# Crea objeto asociado con la conexión conn
        # así cursor nos permite interactuar con la BD
        cursor = conn.cursor()
        def drop_table_if_exists(table_name):
            try:
                cursor.execute(f"""
                    BEGIN
                        EXECUTE IMMEDIATE 'DROP TABLE {table_name} CASCADE CONSTRAINTS';
                    EXCEPTION
                        WHEN OTHERS THEN
                            NULL; -- Ignorar si no existe
                    END;
                """)
                #print(f"Tabla {table_name} eliminada correctamente (con restricciones).")
            except oracledb.DatabaseError as e:
                print(f"Error al eliminar la tabla {table_name}: {e}")
            
        # Eliminar tablas si existen
        drop_table_if_exists('hace')
        drop_table_if_exists('asociado')
        drop_table_if_exists('proveedor')
        drop_table_if_exists('tiene')
        
        drop_table_if_exists('pedido_proveedor')
        drop_table_if_exists('contiene')

        drop_table_if_exists('reparte')
        drop_table_if_exists('realiza')
        drop_table_if_exists('usuario')
        drop_table_if_exists('pedido')

        drop_table_if_exists('entrada_comanda')
        drop_table_if_exists('comanda')
        
        drop_table_if_exists('formado_por')

        drop_table_if_exists('asignado')
        drop_table_if_exists('reporta')
        drop_table_if_exists('encargado_de')
        drop_table_if_exists('empleado')
        drop_table_if_exists('reserva')
        drop_table_if_exists('viveres')
        drop_table_if_exists('incidencia')
        drop_table_if_exists('mesa')
        drop_table_if_exists('producto')
        

        # Se vuelven a crear las tablas
        # cursor.execute nos permite ejecutar sentencias SQL
        #print("creando tabla proveedor")
        cursor.execute("""
        CREATE TABLE proveedor (
            cif VARCHAR(9) PRIMARY KEY,
            correo VARCHAR(30),
            telefono VARCHAR(20),
            nombre VARCHAR(20)
        )""")

        #print("creando tabla pedido_proveedor")
        cursor.execute("""
        CREATE TABLE pedido_proveedor (
            id INT PRIMARY KEY,
            estado VARCHAR(50),
            fecha DATE
        )""")

        #print("creando tabla asociado")
        cursor.execute("""
        CREATE TABLE asociado (
            cif VARCHAR(9),
            id INT PRIMARY KEY,
            FOREIGN KEY (cif) REFERENCES proveedor(cif),
            FOREIGN KEY (id) REFERENCES pedido_proveedor(id)
        )""")

        #print("creando tabla usuario")
        cursor.execute("""
        CREATE TABLE usuario (
            telefono VARCHAR(20) PRIMARY KEY,
            correo VARCHAR(20),
            nombre VARCHAR(20),
            apellido VARCHAR(20)
        )""")

        #print("creando tabla pedido")
        cursor.execute("""
        CREATE TABLE pedido (
            id_pedido INT PRIMARY KEY,
            estado VARCHAR(50),
            direccion VARCHAR(50)
        )""")

        #print("creando tabla realiza")
        cursor.execute("""
        CREATE TABLE realiza (
            id_pedido INT PRIMARY KEY,
            telefono VARCHAR(20),
            FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido),
            FOREIGN KEY (telefono) REFERENCES usuario(telefono)
        )""")

        #print("creando tabla empleado")
        cursor.execute("""
        CREATE TABLE empleado (
            dni VARCHAR(9) PRIMARY KEY,
            nombre VARCHAR(20),
            apellido VARCHAR(20),
            cargo VARCHAR(20),
            telefono VARCHAR(20), 
            num_ss VARCHAR(12),
            salario INT
        )""")

        #print("creando tabla hace")
        cursor.execute("""
        CREATE TABLE hace (
            id INT PRIMARY KEY,
            dni VARCHAR(9),
            FOREIGN KEY (id) REFERENCES pedido_proveedor(id),
            FOREIGN KEY (dni) REFERENCES empleado(dni)
        )""")

        #print("creando tabla reserva")
        cursor.execute("""
        CREATE TABLE reserva(
            fecha DATE,
            telefono VARCHAR(20),
            nombre VARCHAR(20),
            apellido VARCHAR(20),
            numero_personas INT,
            lugar INT,
            PRIMARY KEY (fecha, telefono)
        )
        """)

        #print("creando tabla encargado_de")
        cursor.execute("""
        CREATE TABLE encargado_de(
            dni_empleado VARCHAR(9),
            fecha DATE,
            tlf VARCHAR(20),
            PRIMARY KEY (dni_empleado, fecha, tlf),
            FOREIGN KEY (dni_empleado) REFERENCES empleado(dni),
            FOREIGN KEY (fecha, tlf) REFERENCES reserva(fecha, telefono)
        )
        """)

        #print("creando tabla reparte")
        cursor.execute("""
        CREATE TABLE reparte(
            id_pedido INT PRIMARY KEY,
            dni VARCHAR(9),
            FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido),
            FOREIGN KEY (dni) REFERENCES empleado(dni)
        )""")

        #print("creando tabla viveres")
        cursor.execute("""
        CREATE TABLE viveres(
            codigo VARCHAR(10)PRIMARY KEY,
            nombre VARCHAR(20)
        )""")

        #print("creando tabla tiene")
        cursor.execute("""
        CREATE TABLE tiene (
            id INT,
            codigo VARCHAR(10),
            cantidad INT,
            PRIMARY KEY (id, codigo),
            FOREIGN KEY (id) REFERENCES pedido_proveedor(id),
            FOREIGN KEY (codigo) REFERENCES viveres(codigo)
        )
        """)

        #print("creando tabla incidencia")
        cursor.execute("""
        CREATE TABLE incidencia (
            id_incidencia INT PRIMARY KEY,
            fecha DATE,
            descripcion VARCHAR2(500)
        )""")

        #print("creando tabla reporta")
        cursor.execute("""
        CREATE TABLE reporta (
            dni VARCHAR(9),
            id_incidencia INT,
            PRIMARY KEY (dni , id_incidencia),
            FOREIGN KEY (dni) REFERENCES empleado(dni),
            FOREIGN KEY (id_incidencia) REFERENCES incidencia(id_incidencia)
        )""")

        #print("creando tabla producto")
        cursor.execute("""
        CREATE TABLE producto (
            id_producto INT PRIMARY KEY,
            nombre VARCHAR(20),
            precio DECIMAL(10, 2)
        )""")


        #print("creando tabla contiene")
        cursor.execute("""
        CREATE TABLE contiene(
            id_pedido INT,
            id_producto INT,
            cantidad INT,
            PRIMARY KEY (id_pedido , id_producto),
            FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido),
            FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
        )""")

        
        #print("creando tabla mesa")
        cursor.execute("""
        CREATE TABLE mesa (
            id_mesa INT PRIMARY KEY,
            estado VARCHAR(50)
        )""")
        
        #print("creando tabla asignado")
        cursor.execute("""
        CREATE TABLE asignado(
            id_mesa INT PRIMARY KEY,
            dni_empleado VARCHAR(9),
            FOREIGN KEY (id_mesa) REFERENCES mesa(id_mesa),
            FOREIGN KEY (dni_empleado) REFERENCES empleado(dni)
        )""")
    
        #print("creando tabla comanda")
        cursor.execute("""
        CREATE TABLE comanda (
            id_comanda INT,
            id_mesa INT,
            estado VARCHAR(10),
            fecha_entrada DATE,
            PRIMARY KEY (id_comanda, id_mesa),
            FOREIGN KEY (id_mesa) REFERENCES mesa(id_mesa)
        )""")

        #print("creando tabla entrada_comanda")
        cursor.execute("""
        CREATE TABLE entrada_comanda (
            id_mesa INT,           
            id_comanda INT,
            id_entrada INT,
            num_consumidores INT CHECK (num_consumidores >= 0),
            PRIMARY KEY(id_entrada, id_comanda, id_mesa),
            FOREIGN KEY (id_comanda, id_mesa) REFERENCES 
            comanda(id_comanda, id_mesa))
            
        """)
        
        #print("creando tabla formado_por")
        cursor.execute("""
        CREATE TABLE formado_por(
            id_entrada INT,
            id_comanda INT,
            id_mesa INT,
            id_producto INT,
            PRIMARY KEY(id_entrada, id_comanda, id_mesa, id_producto),
            FOREIGN KEY(id_entrada, id_comanda, id_mesa) REFERENCES entrada_comanda(id_entrada, id_comanda,id_mesa), 
            FOREIGN KEY(id_producto) REFERENCES producto(id_producto)
        )""")
        
        conn.commit()

        # Insertamos tuplas predefinidas en la tabla proveedor
        proveedor = [('cif1', 'correo1@gmail.com', '111111111','prov1'), 
            ('cif2', 'correo2@gmail.com', '222222222','prov2'), 
            ('cif3', 'correo3@gmail.com', '333333333','prov3')]
        
        #print("INSERTANDO TUPLAS DE PROVEEDOR")
        for prov in proveedor:
            cursor.execute("""
                INSERT INTO proveedor (cif, correo, telefono, nombre)
                VALUES (:1, :2, :3, :4)""", prov)
            conn.commit()
        
         # Insertamos tuplas predefinidas en la tabla pedido_proveedor
        pedido_proveedor = [(1, 'ACTIVO'),
                            (2, 'ACTIVO'),
                            (3, 'FINALIZADO')]

        
        #print("INSERTANDO TUPLAS DE PEDIDO_PROVEEDOR")
        for pedido in pedido_proveedor:
            cursor.execute("""
                INSERT INTO pedido_proveedor (id, estado, fecha)
                VALUES (:1, :2, SYSDATE)""", pedido)
            conn.commit()

        #Insertamos tuplas predefinidas en la tabla asociado
        asociado = [('cif1', 1),
            ('cif2', 2),
            ('cif3', 3)]
        
        #print("INSERTANDO TUPLAS DE ASOCIADO")
        for asoc in asociado:
            cursor.execute("""
                INSERT INTO asociado (cif, id)
                VALUES (:1, :2)""", asoc)
            conn.commit()

        #Insertamos tuplas predefinidas en la tabla usuario
        usuario = [
            ('999999999', 'usuario1@gmail.com', 'Nombre1', 'Apellido1'),
            ('888888888', 'usuario2@gmail.com', 'Nombre2', 'Apellido2'),
            ('777777777', 'usuario3@gmail.com', 'Nombre3', 'Apellido3')]

        #print("INSERTANDO TUPLAS DE USUARIO")
        for usr in usuario:
            cursor.execute("""
                INSERT INTO usuario (telefono, correo, nombre, apellido)
                VALUES (:1, :2, :3, :4)""", usr)
            conn.commit()

        #Insertamos tuplas predefinidas en la tabla pedido
        #print("INSERTANDO TUPLAS DE pedido")
        pedido = [
            (1, 'PENDIENTE', "calle Gran Via, 9, Granada"),
            (2, 'ENTREGADO', "calle Gonzalo Gallas, 4, Granada"),
            (3, 'PENDIENTE', " C. Periodista Daniel Saucedo Aranda, s/n, Granada")]

        for ped in pedido:
            cursor.execute("""
                INSERT INTO pedido (id_pedido, estado, direccion)
                VALUES (:1, :2, :3)""", ped)
            conn.commit()

        #Insertamos tuplas predefinidas en la tabla realiza
        realiza = [
            (1, '999999999'),
            (2, '888888888'),
            (3, '777777777')]

        #print("INSERTANDO TUPLAS DE REALIZA")

        for rel in realiza:
            cursor.execute("""
                INSERT INTO realiza (id_pedido, telefono)
                VALUES (:1, :2)""", rel)
            conn.commit()

        
        empleado = [ 
            ('12345678A', 'Pedro', 'García', 'JEFE', '123456789', '000111222', 1500),
            ('87654321B', 'Ana', 'López', 'REPARTIDOR', '987654321', '333444555', 1200)
        ]

        #print("INSERTANDO TUPLAS DE Empleado")

        for emp in empleado:
            cursor.execute("""
                INSERT INTO empleado (dni, nombre, apellido, cargo, telefono, num_ss, salario)
                VALUES (:1, :2, :3, :4, :5, :6, :7)""", emp)
            conn.commit()

        # Insertamos tuplas predefinidas en la tabla hace

        hace = [
            (1, '12345678A'),
            (2, '12345678A')
        ]

        for h in hace: 
            cursor.execute ("""
                INSERT INTO hace (id, dni)
                VALUES (:1, :2)""", h)
            conn.commit()

        # Insertamos tuplas predefinidas en la tabla reserva
        reserva = [
            ('999999999', 'Nombre1', 'Apellido1', 4, 0),
            ('888888888', 'Nombre2', 'Apellido2', 2, 1)]
                
        #print("INSERTANDO TUPLAS DE RESERVA")
        for res in reserva:
            cursor.execute("""
                INSERT INTO reserva (fecha, telefono, nombre, apellido, numero_personas, lugar)
                VALUES (TO_DATE('2024-12-10', 'YYYY-MM-DD'), :1, :2, :3, :4, :5)""", res)
            conn.commit()

        # Insertamos tuplas predefinidas en la tabla encargado_de
        encargado_de = [
            ('12345678A', '999999999'),
            ('87654321B', '888888888')
        ]

        #print("INSERTANDO TUPLAS DE ENCARGADO_DE")
        for enc in encargado_de:
            cursor.execute("""
                INSERT INTO encargado_de (dni_empleado, fecha, tlf)
                VALUES (:1, TO_DATE('2024-12-10', 'YYYY-MM-DD'), :3)""", enc)
            conn.commit()
        
        repartes = [
            (1, '87654321B'),
            (2, '87654321B')
        ]

        #print("INSERTANDO TUPLAS DE REPARTE")
        for rep in repartes:
            cursor.execute("""
                INSERT INTO reparte (id_pedido, dni)
                VALUES (:1,:2)""", rep)
            conn.commit()

        viveres = [
            ('V001', 'Harina'),
            ('V002', 'Leche'),
            ('V003', 'Huevos')
        ]

        #print("INSERTANDO TUPLAS DE VIVERES")
        for viv in viveres:
            cursor.execute("""
                INSERT INTO viveres (codigo, nombre)
                VALUES (:1, :2)""", viv)
            conn.commit()
        

        tiene = [
            (1, 'V001', 20),
            (2, 'V002', 50)
        ]

        #print("INSERTANDO TUPLAS DE TIENE")
        for tie in tiene:
            cursor.execute("""
                INSERT INTO tiene (id, codigo, cantidad)
                VALUES (:1, :2, :3)""", tie)
            conn.commit()

        incidencia = [
            (1, 'El cliente faltó al respeto al camarero'),
            (2, 'El cliente se fue corriendo y no pagó la cuenta')
        ]

        #print("INSERTANDO TUPLAS DE INCIDENCIA")
        for inc in incidencia:
            cursor.execute("""
                INSERT INTO incidencia (id_incidencia, fecha, descripcion)
                VALUES (:1, TO_DATE('2024-12-05', 'YYYY-MM-DD'), :2)""", inc)
            conn.commit()

        reporta = [
            ('12345678A', 1),
            ('87654321B', 2)
        ]

        #print("INSERTANDO TUPLAS DE REPORTA")
        for rep in reporta:
            cursor.execute("""
                INSERT INTO reporta (dni, id_incidencia)
                VALUES (:1, :2)""", rep)
            conn.commit()

        producto = [
            (1, 'Pizza', 8.50),
            (2, 'Pasta', 7.30),
            (3, 'Ensalada', 5.90)
        ]

        #print("INSERTANDO TUPLAS DE PRODUCTO")
        for prod in producto:
            cursor.execute("""
                INSERT INTO producto (id_producto, nombre, precio)
                VALUES (:1, :2, :3)""", prod)
            conn.commit()

        contiene = [
            (1, 1, 2),
            (2, 2, 1),
            (3, 3, 3)
        ]

        #print("INSERTANDO TUPLAS DE CONTIENE")
        for cont in contiene:
            cursor.execute("""
                INSERT INTO contiene (id_pedido, id_producto, cantidad)
                VALUES (:1, :2, :3)""", cont)
            conn.commit()

        mesa = [
            (1, 'Disponible'),
            (2, 'Ocupada'),
            (3, 'Reservada')
        ]

        #print("INSERTANDO TUPLAS DE MESA")
        for mes in mesa:
            cursor.execute("""
                INSERT INTO mesa (id_mesa, estado)
                VALUES (:1, :2)""", mes)
            conn.commit()

        asignado = [
            (1, '12345678A'),
            (2, '87654321B')
        ]

        #print("INSERTANDO TUPLAS DE ASIGNADO")
        for asi in asignado:
            cursor.execute("""
                INSERT INTO asignado (id_mesa, dni_empleado)
                VALUES (:1, :2)""", asi)
            conn.commit()

        comanda = [
            (1, 1, 'PAGADO'),
            (2, 2, 'ACTIVO')
        ]

        for com in comanda:
            cursor.execute("""
                INSERT INTO comanda (id_comanda, id_mesa, estado, fecha_entrada)
                VALUES (:1, :2, :3, SYSDATE)""", com)
            conn.commit()

        # # Insertamos tuplas predefinidas en la tabla entrada_comanda
        # entrada_comanda = [
        #     (1, 1, 1, 2),
        #     (2, 2, 2, 4)
        # ]

        # for ent in entrada_comanda:
        #     cursor.execute("""
        #         INSERT INTO entrada_comanda (id_entrada, id_comanda, id_mesa, num_consumidores)
        #         VALUES (:1, :2, :3, :4)""", ent)
        #     conn.commit()

        # # Insertamos tuplas predefinidas en la tabla formado_por
        # formado_por = [
        #     (1, 1, 1, 1),
        #     (2, 2, 2, 3)
        # ]

        # for form in formado_por:
        #     cursor.execute("""
        #         INSERT INTO formado_por (id_entrada, id_comanda, id_mesa, id_producto)
        #         VALUES (:1, :2, :3, :4)""", form)
        #     conn.commit()
        # conn.commit confirma los cambios realizados en la BD durante la sesión
        # si no se ejecuta, los cmabios no se reflejan en la BD
        print("\nTablas creadas y datos insertados.")

    except oracledb.DatabaseError as e:
        print("Error al crear las tablas o insertar datos:", e)
        conn.rollback()



#========================================================================================
#DISPARADORES
#========================================================================================
#NOTAS
"""
-) ERROR ORA-06512: Este error indica que la excepción se ha generado dentro de un bloque PL/SQL (Esperado)
   corresponde a la instrucción RAISE_APPLICATION_ERROR.

-)ERROR ORA-04088: Este es un error que indica que un error ocurrió durante la ejecución de un trigger. 
  Como el trigger lanzó un error con RAISE_APPLICATION_ERROR, Oracle lo reporta con el código ORA-04088.

-) No se termina la ejecución porque estos errores pueden ser controlados
"""
#--------------------------------------------------------------------------------------------
#DISPARADORES EMPLEADOS
#--------------------------------------------------------------------------------------------

# #disparador comprobar que un empleado no tiene mesas asociadas a la hora de borrarlo
def trigger_verificar_mesas_antes_de_eliminar(conn):
    try:
        cursor = conn.cursor()

        # Código del trigger en SQL: antes de eliminar de empleado, contar las mesas asignadas
        trigger_sql = """
        CREATE OR REPLACE TRIGGER verificar_mesas_antes_de_eliminar
        BEFORE DELETE ON empleado
        FOR EACH ROW
        DECLARE
            mesas_asignadas INT;
        BEGIN
            -- Contar las mesas asignadas al empleado
            SELECT COUNT(*)
            INTO mesas_asignadas
            FROM mesa m
            JOIN asignado a ON m.id_mesa = a.id_mesa
            WHERE a.dni_empleado = :OLD.dni
            AND (m.estado = 'Ocupada' OR m_estado = "Reservada");

            -- Si hay mesas asignadas, lanzar un error
            IF mesas_asignadas > 0 THEN
                RAISE_APPLICATION_ERROR(-20031, 'No se puede eliminar el usuario porque tiene mesas asociadas.');
            END IF;
        END;"""

        # Ejecutar el SQL para crear el trigger
        cursor.execute(trigger_sql)

    except oracledb.DatabaseError as e:
        error, = e.args

    finally:
        cursor.close()

# #--------------------------------------------------------------------------------------------

# #disparador comprobar que un empleado no tiene repartos asociadas a la hora de borrarlo
def trigger_verificar_repartos_antes_de_eliminar(conn):
    try:
        cursor = conn.cursor()

        # Código del trigger en SQL: antes de eliminar de empleado, contar los repartos asignados
        trigger_sql = """
        CREATE OR REPLACE TRIGGER verificar_repartos_antes_de_eliminar
        BEFORE DELETE ON empleado
        FOR EACH ROW
        DECLARE
            repartos_asignados INT;
        BEGIN
            -- Contar los repartos asignadas al empleado
            SELECT COUNT(*)
            INTO repartos_asignados
            FROM pedido p
            JOIN reparte r ON p.id_pedido = r.id_pedido
            WHERE r.dni = :OLD.dni
            AND p.estado = 'PENDIENTE';

            -- Si hay mesas asignadas, lanzar un error
            IF repartos_asignados > 0 THEN
                RAISE_APPLICATION_ERROR(-20031, 'No se puede eliminar el usuario porque tiene repartos asociados.');
            END IF;
        END;"""

        # Ejecutar el SQL para crear el trigger
        cursor.execute(trigger_sql)

    except oracledb.DatabaseError as e:
        error, = e.args

    finally:
        cursor.close()

# #--------------------------------------------------------------------------------------------

def trigger_verificar_salario_positivo(conn):
    try:
        cursor = conn.cursor()

        # Código del trigger en SQL: verifica que el salario es positivo antes de insertar en la tabla empleado
        trigger_sql = """
        CREATE OR REPLACE TRIGGER verificar_salario_positivo
        BEFORE INSERT OR UPDATE ON empleado
        FOR EACH ROW
        BEGIN
            IF :NEW.salario < 0 THEN
                RAISE_APPLICATION_ERROR(-20003, 'El salario no puede ser negativo.');
            END IF;
        END;
        """

        # Ejecutar el SQL para crear el trigger
        cursor.execute(trigger_sql)

    except oracledb.DatabaseError as e:
        error, = e.args

    finally:
        cursor.close()

# #--------------------------------------------------------------------------------------------

def trigger_verificar_formato_dni(conn):
    try:
        cursor = conn.cursor()

        # Código del trigger en SQL: verifica que el DNI se introduce con formato
        trigger_sql = """
        CREATE OR REPLACE TRIGGER verificar_formato_dni
        BEFORE INSERT OR UPDATE ON empleado
        FOR EACH ROW
        BEGIN
            IF :NEW.dni IS NULL OR NOT REGEXP_LIKE(:NEW.dni, '^[0-9]{8}[A-Z]$') THEN
                RAISE_APPLICATION_ERROR(-20010, 'Error: El DNI debe tener 8 números seguidos de 1 letra mayúscula.');
            END IF;
        END;
        """

        # Ejecutar el SQL para crear el trigger
        cursor.execute(trigger_sql)

    except oracledb.DatabaseError as e:
        error, = e.args

    finally:
        cursor.close()

# #--------------------------------------------------------------------------------------------

def trigger_verificar_formato_tlf_empleado(conn):
    try:
        cursor = conn.cursor()

        # Código del trigger en SQL: antes de eliminar de empleado, contar los repartos asignados
        trigger_sql = """
        CREATE OR REPLACE TRIGGER verificar_formato_tlf
        BEFORE INSERT OR UPDATE ON empleado
        FOR EACH ROW
        BEGIN
            IF :NEW.telefono IS NULL OR NOT REGEXP_LIKE(:NEW.telefono, '^\\+?[0-9]{1,3}?[0-9]{1,20}$') THEN
                RAISE_APPLICATION_ERROR(-20011, 'Error: El teléfono debe ser un número válido con un prefijo opcional.');
            END IF;
        END;
        """

        # Ejecutar el SQL para crear el trigger
        cursor.execute(trigger_sql)

    except oracledb.DatabaseError as e:
        error, = e.args

    finally:
        cursor.close()

#--------------------------------------------------------------------------------------------
#DISPARADORES SUBSISTEMA DE PROVEEDORES
#--------------------------------------------------------------------------------------------

def trigger_verificar_formato_telefono_proveedor(conn):

    try:

        cursor = conn.cursor()

        trigger_sql = """
        CREATE OR REPLACE TRIGGER trigger_verificar_formato_telefono_proveedor
        BEFORE INSERT 
        ON proveedor
        FOR EACH ROW
        BEGIN
            IF NOT REGEXP_LIKE(:NEW.telefono, '^\+?\d+$') THEN
                RAISE_APPLICATION_ERROR(-20020, 'Error: El número debe comenzar con un "+" opcional, seguido solo de dígitos.');
            END IF;
        END;
        """

        # Ejecutar el SQL para crear el trigger
        cursor.execute(trigger_sql)

    except oracledb.DatabaseError as e:
        error, = e.args

    finally:
        cursor.close()

#--------------------------------------------------------------------------------------------
def trigger_verificar_formato_correo_proveedor(conn):

    try:

        cursor = conn.cursor()

        # Código del trigger en SQL: antes de dar de alta un proveedor
        trigger_sql = """
        CREATE OR REPLACE TRIGGER trigger_verificar_formato_correo_proveedor
        BEFORE INSERT 
        ON proveedor
        FOR EACH ROW
        BEGIN
            -- Verificar que contenga el carácter '@'
            IF INSTR(:NEW.correo, '@') = 0 THEN
                RAISE_APPLICATION_ERROR(-20021, 'Error: El correo debe contener un carácter @.');            
            END IF;

            -- Verificar que haya al menos un carácter antes y después del '@'
            IF INSTR(:NEW.correo, '@') = 1 OR INSTR(:NEW.correo, '@') = LENGTH(:NEW.correo) THEN                
                RAISE_APPLICATION_ERROR(-20022, 'Error: El correo debe contener al menos un carácter antes y después del @.');
            END IF;
        END;
        """

        # Ejecutar el SQL para crear el trigger
        cursor.execute(trigger_sql)

    except oracledb.DatabaseError as e:
        error, = e.args

    finally:
        cursor.close()

#--------------------------------------------------------------------------------------------

# def trigger_verificar_que_no_existen_pedidos_activos_de_proveedor (conn):

#     try:
        
#         cursor = conn.cursor()

#         trigger_sql ="""
#         CREATE OR REPLACE TRIGGER trigger_verificar_que_no_existen_pedidos_activos_de_proveedor
#         BEFORE DELETE 
#         ON asociado
#         FOR EACH ROW
#         DECLARE
#             contador NUMBER;
#         BEGIN
#             -- Contar cuántos pedidos de este proveedor están en estado 'ACTIVO'
#             SELECT COUNT(*)
#             INTO contador
#             FROM pedido_proveedor pp
#             WHERE pp.cif = :OLD.cif 
#             AND pp.estado = 'ACTIVO';

#             -- Si existen pedidos activos, lanzar un error y evitar la eliminación
#             IF contador > 0 THEN
#                 RAISE_APPLICATION_ERROR(-20024, 'Error: Existen pedidos activos de este proveedor.');
#             END IF;
#         END;
#         """
#         # Ejecutar el SQL para crear el trigger
#         cursor.execute(trigger_sql)
#         conn.commit()

#     except oracledb.DatabaseError as e:
#         error, = e.args

#     finally:
#         cursor.close()

#--------------------------------------------------------------------------------------------
def trigger_verificar_producto_existe(conn):

    try:
        
        cursor = conn.cursor()

        trigger_sql ="""

        CREATE OR REPLACE TRIGGER trigger_verificar_producto_existe
        BEFORE INSERT OR UPDATE 
        ON tiene
        FOR EACH ROW
        DECLARE
            contador NUMBER;  
        BEGIN
            -- Verificar si el producto existe en la tabla víveres
            SELECT COUNT(*)
            INTO contador
            FROM viveres
            WHERE codigo = :NEW.codigo;

            IF contador = 0 THEN
                RAISE_APPLICATION_ERROR(-20025, 'Error: El producto proporcionado no existe en la base de datos.');
            END IF;
        END;
        """
        # Ejecutar el SQL para crear el trigger
        cursor.execute(trigger_sql)
        conn.commit()

    except oracledb.DatabaseError as e:
        error, = e.args

    finally:
        cursor.close()


#--------------------------------------------------------------------------------------------
#DISPARADORES PEDIDOS ONLINE
#--------------------------------------------------------------------------------------------

#disparador comprobar que un usuario no tiene pedidos asociados
def trigger_verificar_pedidos_antes_de_eliminar(conn):
    try:
        cursor = conn.cursor()

        # Código del trigger en SQL: antes de eliminar de usuario, contar los pedidos pendientes
        trigger_sql = """
        CREATE OR REPLACE TRIGGER verificar_pedidos_antes_de_eliminar
        BEFORE DELETE ON usuario
        FOR EACH ROW
        DECLARE
            pedidos_pendientes INT;
        BEGIN
            -- Contar los pedidos pendientes asociados al usuario
            SELECT COUNT(*)
            INTO pedidos_pendientes
            FROM pedido p
            JOIN realiza r ON p.id_pedido = r.id_pedido
            WHERE r.telefono = :OLD.telefono
            AND p.estado = 'PENDIENTE';

            -- Si hay pedidos pendientes, lanzar un error
            IF pedidos_pendientes > 0 THEN
                RAISE_APPLICATION_ERROR(-20031, 'No se puede eliminar el usuario porque tiene pedidos pendientes.');
            ELSE
               DELETE FROM realiza WHERE telefono = :OLD.telefono;
            END IF;
        END;"""

        # Ejecutar el SQL para crear el trigger
        cursor.execute(trigger_sql)

    except oracledb.DatabaseError as e:
        error, = e.args

    finally:
        cursor.close()

#--------------------------------------------------------------------------------------------
#trigger_verificar_si_es_repartidor
def trigger_verificar_si_es_repartidor(conn):
    try:
        cursor = conn.cursor()

        # Código del trigger en SQL: antes de eliminar de usuario, contar los pedidos pendientes
        trigger_sql = """
        CREATE OR REPLACE TRIGGER verificar_si_es_repartidor
        BEFORE INSERT ON reparte
        FOR EACH ROW
        DECLARE
             cargo_empleado VARCHAR(20);
        BEGIN
            -- obtener el cargo
            SELECT cargo
            INTO cargo_empleado
            FROM empleado
            WHERE dni = :NEW.dni;

            -- Si el empleado es repartidor
            IF cargo_empleado != 'REPARTIDOR' THEN
                RAISE_APPLICATION_ERROR(-20032, 'El empleado no es repartidor.');
            END IF;
        END;"""

        # Ejecutar el SQL para crear el trigger
        cursor.execute(trigger_sql)


    except oracledb.DatabaseError as e:
        error, = e.args

    finally:
        cursor.close()

#--------------------------------------------------------------------------------------------
#trigger_verificar_si_pedido_pendiente
def trigger_verificar_si_pedido_pendiente(conn):
    try:
        cursor = conn.cursor()

        # Código del trigger en SQL: comprobar si un pedido existe y está pendiente
        trigger_sql = """
        CREATE OR REPLACE TRIGGER verificar_si_pedido_pendiente
        BEFORE INSERT ON reparte
        FOR EACH ROW
        DECLARE
            estado_pedido VARCHAR(20);
        BEGIN
            -- obtener el cargo
            SELECT estado
            INTO estado_pedido
            FROM pedido
            WHERE id_pedido = :NEW.id_pedido;

            -- Si el pedido no pendiente
            IF estado_pedido != 'PENDIENTE' THEN
                RAISE_APPLICATION_ERROR(-20033, 'El pedido no existe o no está pendiente.');
            END IF;
        END;"""

        # Ejecutar el SQL para crear el trigger
        cursor.execute(trigger_sql)


    except oracledb.DatabaseError as e:
        error, = e.args

    finally:
        cursor.close()

#--------------------------------------------------------------------------------------------
#trigger verificar si el telefono del usuario existe en la base de datos antes de realizar pedido
def trigger_verificar_si_tlf_usuario_existe(conn):
    try:
        cursor = conn.cursor()
        # Código del trigger en SQL: comprobar si un pedido existe y está pendiente
        trigger_sql ="""
        CREATE OR REPLACE TRIGGER trigger_verificar_si_tlf_usuario_existe
        BEFORE INSERT ON realiza
        FOR EACH ROW
        DECLARE
            nombre_asoc VARCHAR(20);
        BEGIN
            
            -- Comprobar si el número de teléfono existe en la tabla usuario
            BEGIN
                SELECT nombre
                INTO nombre_asoc
                FROM usuario
                WHERE telefono = :NEW.telefono;

            EXCEPTION WHEN NO_DATA_FOUND THEN
                -- Si el teléfono no existe, lanzar una excepción
                RAISE_APPLICATION_ERROR(-20034, 'El número de teléfono no pertenece a ningún usuario');

            END;
        END;
        """
        # Ejecutar el SQL para crear el trigger
        cursor.execute(trigger_sql)
        conn.commit()

    except oracledb.DatabaseError as e:
        error, = e.args

    finally:
        cursor.close()



#----------------------------------------------------------------------------------------
#trigger verificar si el pedido existe en la base de datos
def trigger_verificar_si_cod_prod_existe(conn):
    try:
        cursor = conn.cursor()

        # Define el código del trigger
        trigger_sql = """
        CREATE OR REPLACE TRIGGER trigger_verificar_si_cod_prod_existe
        BEFORE INSERT ON contiene
        FOR EACH ROW
        DECLARE
            nombre_asoc VARCHAR(20);

        BEGIN
            -- Comprobar si el número de producto existe en la tabla producto
            BEGIN
                SELECT nombre
                INTO nombre_asoc
                FROM producto
                WHERE id_producto = :NEW.id_producto;

            EXCEPTION
                WHEN NO_DATA_FOUND THEN
                    -- Si no existe, lanzar una excepción
                    RAISE_APPLICATION_ERROR(-20035, 'El código no identifica a ningún producto');

            END;
        END;
        """

        # Ejecutar el SQL para crear el procedimiento
        cursor.execute(trigger_sql)
        conn.commit()


    except oracledb.DatabaseError as e:
        error, = e.args

    
    finally:
        cursor.close()  


#-------------------------------------------------------------------------------------------
#trigger empleado registrado en la base de datos
def trigger_verificar_si_empleado_existe(conn):
    try:
        cursor = conn.cursor()

        # Define el código del procedimiento
        trigger = """
        CREATE OR REPLACE TRIGGER trigger_verificar_si_empleado_existe
        BEFORE INSERT ON reparte
        FOR EACH ROW
        DECLARE
            nombre_asoc VARCHAR(20);

        BEGIN
            -- Comprobar si el dni de empleado existe en la tabla empleado
            BEGIN
                SELECT nombre
                INTO nombre_asoc
                FROM empleado
                WHERE dni = :NEW.dni;

            EXCEPTION
                WHEN NO_DATA_FOUND THEN
                    -- Si no existe, lanzar una excepción
                    RAISE_APPLICATION_ERROR(-20036, 'No existe un empleado con el dni proporcionado');

            END;
        END;
        """

        # Ejecutar el SQL para crear el procedimiento
        cursor.execute(procedure_sql)
        conn.commit()


    except oracledb.DatabaseError as e:
        error, = e.args
    
    finally:
        cursor.close() 
#-------------------------------------------------------------------------------------------
#trigger pedido en la base de datos
def trigger_verificar_si_pedido_existe(conn):
    try:
        cursor = conn.cursor()

        # Define el código del procedimiento
        trigger_sql = """
        CREATE OR REPLACE TRIGGER trigger_verificar_si_pedido_existe
        BEFORE INSERT ON reparte
        FOR EACH ROW
        DECLARE
            estado_ped VARCHAR(50);

        BEGIN
            -- Comprobar si el dni de empleado existe en la tabla empleado
            BEGIN
                SELECT estado
                INTO estado_ped
                FROM pedido
                WHERE id_pedido = :NEW.id_pedido;

            EXCEPTION
                WHEN NO_DATA_FOUND THEN
                    -- Si no existe, lanzar una excepción
                    RAISE_APPLICATION_ERROR(-20037, 'No existe pedido con identificador asociado');

            END;
        END;
        """

        # Ejecutar el SQL para crear el procedimiento
        cursor.execute(trigger_sql)
        conn.commit()


    except oracledb.DatabaseError as e:
        error, = e.args
    
    finally:
        cursor.close() 


#--------------------------------------------------------------------------------------------
#trigger_verificar_si_pedido_pendiente --- kessler
def trigger_verificar_si_mesas_asociadas(conn):
    try:
        cursor = conn.cursor()

        # Código del trigger en SQL: comprobar si una mesa está disponible
        trigger_sql = """
        CREATE OR REPLACE TRIGGER verificar_si_mesas_asociadas
        BEFORE INSERT ON asignado
        FOR EACH ROW
        DECLARE
            estado_mesa VARCHAR(20);
        BEGIN
            -- obtener el cargo
            SELECT estado
            INTO estado_mesa
            FROM mesa
            WHERE id_mesa = :NEW.id_mesa;

            -- Si la mesa no esta activa
            IF estado_mesa != 'Disponible' THEN
                RAISE_APPLICATION_ERROR(-20033, 'El mesa no está disponible.');
            END IF;
        END;"""

        # Ejecutar el SQL para crear el trigger
        cursor.execute(trigger_sql)


    except oracledb.DatabaseError as e:
        error, = e.args

    finally:
        cursor.close()

#===================================================================================
# Triggers reservas
def trigger_validar_numero_personas_reserva(conn):
    try:
        cursor = conn.cursor()

        # Código del trigger en SQL: verifica el número de personas en la tabla reserva
        trigger_sql = """
        CREATE OR REPLACE TRIGGER validar_numero_personas_reserva
        BEFORE INSERT OR UPDATE ON reserva
        FOR EACH ROW
        BEGIN
            IF :NEW.numero_personas < 1 THEN
                RAISE_APPLICATION_ERROR(-20038, 'El número de personas en una reserva debe ser mayor o igual a 1.');
            END IF;
        END;
        """

        # Ejecutar el SQL para crear el trigger
        cursor.execute(trigger_sql)
        conn.commit()
        print("Trigger 'validar_numero_personas_reserva' creado con éxito.")

    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error al crear el trigger: {error.message}")
        conn.rollback()

    finally:
        cursor.close()

def trigger_validar_fecha_reserva_posterior(conn):
    try:
        cursor = conn.cursor()

        # Código del trigger en SQL: verifica que la fecha de la reserva es posterior a la actual
        trigger_sql = """
        CREATE OR REPLACE TRIGGER validar_fecha_reserva_posterior
        BEFORE INSERT OR UPDATE ON reserva
        FOR EACH ROW
        BEGIN
            IF :NEW.fecha <= SYSDATE THEN
                RAISE_APPLICATION_ERROR(-20039, 'La fecha de la reserva debe ser posterior a la fecha actual.');
            END IF;
        END;
        """

        # Ejecutar el SQL para crear el trigger
        cursor.execute(trigger_sql)
        conn.commit()
        print("Trigger 'validar_fecha_reserva_posterior' creado con éxito.")

    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error al crear el trigger: {error.message}")
        conn.rollback()

    finally:
        cursor.close()

def trigger_validar_formato_telefono_reserva(conn):
    try:
        cursor = conn.cursor()

        # Código del trigger en SQL: verifica que el teléfono tenga un formato válido
        trigger_sql = """
        CREATE OR REPLACE TRIGGER validar_formato_telefono_reserva
        BEFORE INSERT OR UPDATE ON reserva
        FOR EACH ROW
        BEGIN
            IF :NEW.telefono IS NULL OR NOT REGEXP_LIKE(:NEW.telefono, '^[0-9]{9}$') THEN
                RAISE_APPLICATION_ERROR(-20041, 'El teléfono debe tener exactamente 9 dígitos.');
            END IF;
        END;
        """

        # Ejecutar el SQL para crear el trigger
        cursor.execute(trigger_sql)
        conn.commit()
        print("Trigger 'validar_formato_telefono_reserva' creado con éxito.")

    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error al crear el trigger: {error.message}")
        conn.rollback()

    finally:
        cursor.close()

def trigger_validar_valores_lugar_reserva(conn):
    try:
        cursor = conn.cursor()

        # Código del trigger en SQL: verifica que el valor de lugar sea 0 o 1
        trigger_sql = """
        CREATE OR REPLACE TRIGGER validar_valores_lugar_reserva
        BEFORE INSERT OR UPDATE ON reserva
        FOR EACH ROW
        BEGIN
            IF :NEW.lugar NOT IN (0, 1) THEN
                RAISE_APPLICATION_ERROR(-20042, 'El valor de lugar debe ser 0 (dentro) o 1 (fuera).');
            END IF;
        END;
        """

        # Ejecutar el SQL para crear el trigger
        cursor.execute(trigger_sql)
        conn.commit()
        print("Trigger 'validar_valores_lugar_reserva' creado con éxito.")

    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error al crear el trigger: {error.message}")
        conn.rollback()

    finally:
        cursor.close()

############################################################################################
# DISPARADORES GESTIÓN DE MESAS
############################################################################################

# Este trigger está porque en la base de datos, al poner una mesa como ocupada, se crea una nueva entrada en la tabla de comanda de esa mesa.
# No queremos tener dos comandas activas al mismo tiempo en esa mesa.

def trigger_no_activar_mesa_ocupada(conn):
    try:
        cursor = conn.cursor()

        trigger_sql = """
        CREATE OR REPLACE TRIGGER no_activar_mesa_ocupada
        BEFORE UPDATE ON mesa
        FOR EACH ROW
        BEGIN
            IF (:OLD.estado = 'Ocupada' AND :NEW.estado = 'Ocupada') THEN
                RAISE_APPLICATION_ERROR(-20043, 'Para ocupar una mesa, esta no debe estar ocupada');
            END IF;
        END;
        """

        cursor.execute(trigger_sql)
        conn.commit()
        print("Trigger 'no_activar_mesa_ocupada' creado con éxito")

    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error al crear el trigger: {error.message}")
        conn.rollback()

    finally:
        cursor.close()

def trigger_eliminar_entrada_si_cero(conn):
    try:
        cursor = conn.cursor()

        trigger_sql = """
        CREATE OR REPLACE TRIGGER eliminar_entrada_si_cero
        AFTER UPDATE ON entrada_comanda
        FOR EACH ROW
        BEGIN
            IF (:NEW.num_consumidores = 0) THEN
                DELETE FROM formado_por WHERE (id_mesa = :NEW.id_mesa AND id_comanda = :NEW.id_comanda AND id_entrada = :NEW.id_entrada);
                DELETE FROM entrada_comanda WHERE (id_mesa = :NEW.id_mesa AND id_entrada = :NEW.id_entrada AND id_comanda = :NEW.id_comanda);
            END IF;
        END;
        """

        cursor.execute(trigger_sql)
        conn.commit()
        print("Trigger 'eliminar_entrada_si_cero' activado")

    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error al crear el trigger: {error.message}")
        conn.rollback()

    finally:
        cursor.close()



#===================================================================================
# Función para crear triggers
#===================================================================================
def crear_triggers(conn):

    # disparadores subsistema empleados 
    trigger_verificar_mesas_antes_de_eliminar(conn)
    trigger_verificar_repartos_antes_de_eliminar(conn)
    trigger_verificar_salario_positivo(conn)
    trigger_verificar_formato_dni(conn)
    trigger_verificar_formato_tlf_empleado(conn)

    # triggers subsistema de proveedores 
    
    trigger_verificar_formato_telefono_proveedor(conn)
    trigger_verificar_formato_correo_proveedor(conn)
    # trigger_verificar_que_no_existen_pedidos_activos_de_proveedor(conn)
    trigger_verificar_producto_existe(conn)

    #triggers subsistema pedidos online
    trigger_verificar_pedidos_antes_de_eliminar(conn)
    trigger_verificar_si_es_repartidor(conn)
    trigger_verificar_si_pedido_pendiente(conn)
    trigger_verificar_si_tlf_usuario_existe(conn)
    trigger_verificar_si_cod_prod_existe(conn)
    trigger_verificar_si_pedido_existe(conn)


    #triggers subsistema reservas
    trigger_validar_numero_personas_reserva(conn)
    trigger_validar_fecha_reserva_posterior(conn)
    trigger_validar_formato_telefono_reserva(conn)
    trigger_validar_valores_lugar_reserva(conn)

    # disparadores subsistema mesas
    trigger_no_activar_mesa_ocupada(conn)

    #otro
    trigger_verificar_si_mesas_asociadas(conn)
    trigger_eliminar_entrada_si_cero(conn)

#========================================================================================
#FUNCIONES SUBSISTEMA GESTIÓN EMPLEADOS
#========================================================================================
#ALTA EMPLEADO
def dar_de_alta_empleado(conn):
    cursor = conn.cursor()

    dni_jefe = input("Introduzca su DNI (jefe): ")
    # cursor.callproc("comprobar_si_jefe", [dni_jefe])
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    dni_empleado = input("DNI: ") # se comprueba con un trigger que el formato sea el correcto
    tlf = input("Telefono: ") # se comprueba con un trigger que el formato sea el correcto
    cargo = input("Cargo: ")
    ss = input("Número de la seguridad social: ")
    salario = input("Salario: ") # se comprueba con un trigger que no sea negativo

    cursor.execute("INSERT INTO empleado (dni, nombre, apellido, cargo, telefono, num_ss, salario) VALUES (:1, :2, :3, :4, :5, :6, :7)", (dni_empleado, nombre, apellido, cargo, tlf, ss, salario))
    print("Se ha dado de alta al empleado correctamente")
    conn.commit()

#----------------------------------------------------------------------------------------

def dar_de_baja_empleado(conn):
    try:
        cursor = conn.cursor()
        dni_jefe = input("Introduzca su DNI (jefe): ")
        # cursor.callproc("comprobar_si_jefe", [dni_jefe])
        dni_empleado = input("DNI del empleado a borrar: ")
        # cursor.callproc("comprobar_dni_empleado", [dni_empleado])

        # borrado en cascada manual 
        cursor.execute("DELETE FROM hace WHERE dni = :dni", {"dni": dni_empleado})
        cursor.execute("DELETE FROM encargado_de WHERE dni_empleado = :dni", {"dni": dni_empleado})
        cursor.execute("DELETE FROM reporta WHERE dni = :dni", {"dni": dni_empleado})

        # al borrar, se ejecuta el trigger que comprueba que el empleado no tenga repartos asignados
        # al borrar, se ejecuta el trigger que comprueba que el empleado no tenga mesas asignadas
        cursor.execute("DELETE FROM empleado WHERE dni = :dni", {"dni":dni_empleado})
        print("Se ha eliminado el empleado correctamente")
        conn.commit()
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error: {error.message}")

#----------------------------------------------------------------------------------------

def modificar_datos_empleado(conn):
    try:
        cursor = conn.cursor()
        dni_jefe = input("Introduzca su DNI (jefe): ")
        # cursor.callproc("comprobar_si_jefe", [dni_jefe])
        dni_empleado = input("DNI del empleado a modificar: ")
        # cursor.callproc("comprobar_dni_empleado", [dni_empleado])

        comprobacion_tlf = input("¿Quiere modificar el teléfono del empleado? (S sí, N no): ")
        if (comprobacion_tlf == "S" or comprobacion_tlf == "s"):
            tlf = input("Introduzca el nuevo teléfono: ")
            # habría que poner tlf y num_ss como unique keys segun lo q habiamos puesto en practicas anteriores creo
            cursor.execute("UPDATE empleado SET telefono = :tlf WHERE dni = :dni", {"tlf": tlf, "dni": dni_empleado})
            conn.commit()
        
        comprobacion_nombre = input("¿Quiere modificar el nombre del empleado? (S sí, N no): ")
        if (comprobacion_nombre == "S" or comprobacion_nombre == "s"):
            nombre = input("Introduzca el nuevo nombre: ")
            cursor.execute("UPDATE empleado SET nombre = :nombre WHERE dni = :dni", {"nombre": nombre, "dni": dni_empleado})
            conn.commit()
        
        comprobacion_apellido = input("¿Quiere modificar el apellido del empleado? (S sí, N no): ")
        if (comprobacion_apellido == "S" or comprobacion_apellido == "s"):
            apellido = input("Introduzca el nuevo apellido: ")
            cursor.execute("UPDATE empleado SET apellido = :apellido WHERE dni = :dni", {"apellido": apellido, "dni": dni_empleado})
            conn.commit()
        
        comprobacion_salario = input("¿Quiere modificar el salario del empleado? (S sí, N no): ")
        if (comprobacion_salario == "S" or comprobacion_salario == "s"):
            salario = input("Introduzca el nuevo salario: ")
            cursor.execute("UPDATE empleado SET salario = :salario WHERE dni = :dni", {"salario": salario, "dni": dni_empleado})
            conn.commit()

        print("Se han modificado los datos del empleado")
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error: {error.message}")    

#----------------------------------------------------------------------------------------

def listar_empleados(conn):
    cursor = conn.cursor()
    dni_jefe = input("Introduzca su DNI (jefe): ")
    # cursor.callproc("comprobar_si_jefe", [dni_jefe])
    cargo = input("Introduzca el cargo por el que quiere filtrar (JEFE, REPARTIDOR). Si quiere verlos todos, introduzca -1: ")
    salario = input("Introduzca el salario a partir del cual quiere filtrar. Si quiere verlos todos, introduzca -1: ")
    
    if cargo == "-1" and salario == "-1":
        # Mostrar todos los empleados
        cursor.execute("""
        SELECT *
        FROM empleado
        -- JOIN contiene c ON p.id_pedido = c.id_pedido
        -- JOIN producto pr ON c.id_producto = pr.id_producto
        ORDER BY empleado.apellido
        """)
    elif cargo == "-1":
        # Mostrar los empleados con un salario mayor que "salario"
        cursor.execute("""
        SELECT *
        FROM empleado
        -- JOIN contiene c ON p.id_pedido = c.id_pedido
        -- JOIN producto pr ON c.id_producto = pr.id_producto
        WHERE salario > :salario
        ORDER BY empleado.apellido
        """, {"salario": float(salario)})
    elif salario == "-1": 
        # Mostrar los empleados con un cargo particular
        cursor.execute("""
        SELECT *
        FROM empleado
        -- JOIN contiene c ON p.id_pedido = c.id_pedido
        -- JOIN producto pr ON c.id_producto = pr.id_producto
        WHERE cargo = :cargo
        ORDER BY empleado.apellido
        """, {"cargo": cargo})
    else:
        # Mostrar los empleados con un cargo particular y un salario mayor que "salario"
        cursor.execute("""
        SELECT *
        FROM empleado
        -- JOIN contiene c ON p.id_pedido = c.id_pedido
        -- JOIN producto pr ON c.id_producto = pr.id_producto
        WHERE cargo = :cargo AND salario > :salario
        ORDER BY empleado.apellido
        """, {"cargo": cargo, "salario": salario})
    
    # Mostrar los resultados
    print ("\n\t DNI | Nombre | Apellido | Cargo | Telefono | Num_SS | Salario")
    for row in cursor:
        print("\t", row)

#----------------------------------------------------------------------------------------

def reporta_incidencia(conn):
    cursor = conn.cursor()
    dni = input("Introduzca su DNI: ")
    # cursor.callproc("comprobar_dni_empleado", [dni])

    cursor.execute("""
    SELECT COUNT(*)
    FROM incidencia
    """
    )
    id_incidencia = cursor.fetchone()[0]+1
    descripcion = input("Describa lo ocurrido: ")    

    cursor.execute("INSERT INTO incidencia VALUES (:1, SYSDATE, :2)", (id_incidencia, descripcion))
    cursor.execute("INSERT INTO reporta VALUES(:1, :2)", (dni, id_incidencia))
    conn.commit()


#========================================================================================
#FUNCIONES SUBSISTEMA GESTION PROVEEDORES
#========================================================================================
#----------------------------------------------------------------------------------------
# DAR DE ALTA A UN PROVEEDOR

def dar_de_alta_proveedor(conn):

    try: 
        cursor = conn.cursor()

        cif = input("CIF: ")
        # un disparador comprueba el formato del correo
        correo = input("Correo electronico: ")
        telefono = input("Telefono: ")
        nombre = input("Nombre: ")
        cursor.execute("INSERT INTO proveedor (cif, correo, telefono, nombre) VALUES (:1, :2, :3, :4)", (cif, correo, telefono, nombre))
        
        print("Se ha dado de alta al proveedor")
        conn.commit()

    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error: {error.message}")

#----------------------------------------------------------------------------------------
# DAR DE BAJA A UN PROVEEDOR

def dar_de_baja_proveedor(conn):

    try:
        cursor = conn.cursor()
        cif = input("Introduzca el CIF del proveedor que desea que sea borrado: ")
        
        # de la propia existencia del CIF se encarga la sentencia DELETE de SQL
        # un disparador debería comprobar que no existan pedidos activos de dicho proveedor
        # pero está comentado, no logré que funcionara

        cursor.execute("DELETE FROM asociado WHERE cif = :cif", {"cif":cif})
        cursor.execute("DELETE FROM proveedor WHERE cif = :cif", {"cif":cif})
        conn.commit()

    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error: {error.message}")

#----------------------------------------------------------------------------------------
# LISTADO POR CIF SIN PEDIDOS

def listado_por_cif_sin_pedidos(conn):

    cursor = conn.cursor()
    cif = input("Introduzca CIF del proveedor (si quiere verlos todos, introduzca -1): ")

    if cif == "-1":
        cursor.execute("""
        SELECT p.cif, p.correo, p.telefono, p.nombre
        FROM proveedor p
        ORDER BY p.nombre
        """)
    else:
        cursor.execute("""
        SELECT p.cif, p.correo, p.telefono, p.nombre
        FROM proveedor p
        WHERE p.cif = :cif
        """, {"cif": cif})
    
    # Mostrar los resultados
    print ("\n\t CIF | CORREO | TELÉFONO | NOMBRE")
    for row in cursor:
        print("\t", row)

#----------------------------------------------------------------------------------------
# LISTADO POR CIF CON PEDIDOS

def listado_por_cif_con_pedidos(conn):

    cursor = conn.cursor()
    cif = input("Introduzca CIF del proveedor (si quiere verlos todos, introduzca -1): ")

    if cif == "-1":
        cursor.execute("""
        SELECT p.cif, p.correo, p.telefono, p.nombre, pp.id, pp.estado, pp.fecha
        FROM proveedor p
        JOIN asociado a ON a.cif = p.cif
        JOIN pedido_proveedor pp ON a.id = pp.id
        ORDER BY p.nombre
        """)
    else:
        cursor.execute("""
        SELECT p.cif, p.correo, p.telefono, p.nombre, pp.id, pp.estado, pp.fecha
        FROM proveedor p
        JOIN asociado a ON a.cif = p.cif
        JOIN pedido_proveedor pp ON a.id = pp.id
        WHERE p.cif = :cif
        ORDER BY pp.id
        """, {"cif": cif})
    
    # Mostrar los resultados
    print ("\n\t CIF | CORREO | TELÉFONO | NOMBRE | ID_PEDIDO | ESTADO | FECHA")
    for row in cursor:
        print("\t", row)

#----------------------------------------------------------------------------------------
# HACER PEDIDO A UN PROVEEDOR

def hacer_pedido(conn):

    try:
        
        cursor = conn.cursor()

        dni = input("Introduzca dni (JEFE): ")
        # Verificar si el usuario es jefe
        cursor.execute("SELECT cargo FROM empleado WHERE dni = :dni", {"dni": dni})
        resultado = cursor.fetchone()

        if not resultado or resultado[0] != 'JEFE':
            print("Solo un empleado con cargo JEFE puede realizar esta acción.")
            return

        cif = input("CIF: ")
        cursor.execute("SELECT MAX(id) + 1 FROM pedido_proveedor")
        id_pedido = cursor.fetchone()[0]
        estado = 'ACTIVO'

        cursor.execute("INSERT INTO pedido_proveedor (id, estado, fecha) VALUES (:1, :2, SYSDATE)", (id_pedido, estado))
        cursor.execute("INSERT INTO asociado (cif, id) VALUES (:1, :2)", (cif, id_pedido))
        cursor.execute("INSERT INTO hace (id, dni) VALUES (:1, :2)", (id_pedido, dni))

        cod_prod = 1
        while (cod_prod != "-1"):

            aniadir = input ("Decida como añadir el producto: \na) Por nombre\nb) Por código\n---> ")
            while (aniadir != 'a' and aniadir != 'b'):
                aniadir = input ("Decida como añadir el producto: \na) Por nombre\nb) Por código\n---> ")

            if (aniadir == 'a'):
                
                nombre = input("Introduzca el nombre del producto: ")
                cantidad = int( input("Cantidad del producto: "))
                while (cantidad <= 0): cantidad = int(input("Introduzca cantidad positiva: "))
                cursor.execute("SELECT codigo FROM viveres WHERE nombre = :nombre ", {"nombre": nombre})
                cod_prod = cursor.fetchone()
                if cod_prod :
                    cod = cod_prod[0]
                    # disparador comprueba que el producto existe
                    cursor.execute("INSERT INTO tiene (id, codigo, cantidad) VALUES (:1, :2, :3)",(id_pedido, cod, cantidad))
                else :
                    print ("Producto no encontrado")

            elif (aniadir == 'b'):

                cod_prod = input("Introduzca el código del producto: ")
                cantidad = int( input("Cantidad del producto: "))
                while (cantidad < 0): cantidad = int(input("Introduzca cantidad positiva: "))
                # disparador comprueba que el producto existe
                cursor.execute("INSERT INTO tiene (id, codigo, cantidad) VALUES (:1, :2, :3)",(id_pedido, cod_prod, cantidad))

            cod_prod = input ("Para salir introduzca -1, para seguir 0: ")
        
        print ("Su pedido tiene identificador :", id_pedido)
        conn.commit()
        
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error: {error.message}")
        

#----------------------------------------------------------------------------------------
# CANCELAR PEDIDO DE UN PROVEEDOR

def cancelar_pedido(conn):

    try:
        
        cursor = conn.cursor()

        dni = input("Introduzca dni (JEFE): ")
        # Verificar si el usuario es jefe
        cursor.execute("SELECT cargo FROM empleado WHERE dni = :dni", {"dni": dni})
        resultado = cursor.fetchone()

        if not resultado or resultado[0] != 'JEFE':
            print("Solo un empleado con cargo JEFE puede realizar esta acción.")
            return
       
        identificador = input ("Identificador del pedido a cancelar: ")

        # debe haber un disparador que comprueba que la fecha límite no se ha pasado (no se implementa)
        # diparador comprueba que dicho pedido existe
        
        nuevo_estado = 'FINALIZADO'
        cursor.execute("""
        UPDATE pedido_proveedor
        SET estado = :1
        WHERE id = :2""", (nuevo_estado, identificador))
        
        conn.commit()
        
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error: {error.message}")


#========================================================================================
#FUNCIONES SUBSISTEMA GESTION PEDIDOS ONLINE
#========================================================================================
#----------------------------------------------------------------------------------------
#DAR DE ALTA USUARIO
def dar_de_alta_usuario(conn):
    try:
        cursor = conn.cursor()
        telefono = input("Telefono: ")
        correo = input("Correo electronico: ")
        nombre = input ("Nombre: ")
        apellido = input ("Apellido: ")
        
        permiso = input("¿Está de acuerdo con que sus datos sean registrados en nuestra base de datos? (S/N)")
        if (permiso == 'S' or permiso == 's'):
            cursor.execute("INSERT INTO usuario (telefono, correo, nombre, apellido) VALUES (:1, :2, :3, :4)", (telefono, correo, nombre, apellido))
            print ("Usuario registrado con éxito")
            conn.commit()

    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error: {error.message}")

#----------------------------------------------------------------------------------------
#DAR DE BAJA USUARIO
def dar_de_baja_usuario(conn):
    try:
        cursor = conn.cursor()
        telefono = input("Telefono: ")
        #disparador para comprobar que el teléfono está en la base de datos
        #aqui actúa un disparador para comprobar que no se borra un cliente con pedidos activos
        cursor.execute("DELETE FROM usuario WHERE telefono = :telefono", {"telefono":telefono})
        
        print("Se ha eliminado el usuario")
        conn.commit()
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error: {error.message}")

#----------------------------------------------------------------------------------------
#HACER PEDIDO ONLINE
def hacer_pedido_online(conn):
    try:
        
        cursor = conn.cursor()
        telefono = input("Telefono: ")
        direccion = input("Direccion: ")
        cursor.execute("SELECT COUNT (*) FROM pedido")
        id_pedido = cursor.fetchone()[0]+1
        estado = "PENDIENTE"
        cursor.execute("INSERT INTO pedido (id_pedido, estado, direccion) VALUES (:1, :2,:3)", (id_pedido,estado,direccion))
        

        cursor.execute("INSERT INTO realiza (telefono, id_pedido) VALUES (:1, :2)", (telefono, id_pedido))
        print ("Su pedido tiene identificador :", id_pedido)
        cod_pro = input ("Codigo producto. Para salir pulse 0: ")
        
        while (cod_pro != "0"):
            #disparador que controla que los productos existen
            cantidad = int(input("Introduzca cantidad positiva: "))
            
            while (cantidad <0):
                cantidad = int(input("Introduzca cantidad positiva: "))
            #disparador que controla que los productos existen
            cursor.execute("INSERT INTO contiene (id_pedido, id_producto, cantidad) VALUES (:1, :2, :3)",(id_pedido, cod_pro, cantidad))
            cod_pro = input ("Codigo producto. Para salir pulse 0: ")
        
        conn.commit()
        
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error: {error.message}")
        


def listado_por_filtros(conn):
    cursor = conn.cursor()
    cod_ped = input("Introduzca código pedido. Si no existe el pedido, no saldrá nada. Si quiere verlos todos, introduzca -1: ")
    
    if cod_ped == "-1":
        # Mostrar todos los pedidos y los productos que contienen
        cursor.execute("""
        SELECT p.id_pedido, pr.nombre, pr.precio, c.cantidad
        FROM pedido p
        JOIN contiene c ON p.id_pedido = c.id_pedido
        JOIN producto pr ON c.id_producto = pr.id_producto
        ORDER BY p.id_pedido
        """)
    else:
        # Mostrar un pedido específico y los productos que contiene
        cursor.execute("""
        SELECT p.id_pedido, pr.nombre, pr.precio, c.cantidad
        FROM pedido p
        JOIN contiene c ON p.id_pedido = c.id_pedido
        JOIN producto pr ON c.id_producto = pr.id_producto
        WHERE p.id_pedido = :cod_ped
        ORDER BY p.id_pedido
        """, {"cod_ped": int(cod_ped)})
    
    # Mostrar los resultados
    for row in cursor:
        print ("\tid_pedido|nombre_producto|precio|cantidad")
        print("\t", row)
    
    
#----------------------------------------------------------------------------------------
#ASIGNAR REPARTIDOR
def asignar_repartidor(conn):
    try:
        cursor = conn.cursor()
        dni= input("Introduza su DNI: ")
         # Solicitar datos al usuario

        # Verificar si el usuario es jefe
        cursor.execute("SELECT cargo FROM empleado WHERE dni = :dni", {"dni": dni})
        resultado = cursor.fetchone()

        if not resultado or resultado[0] != 'JEFE':
            print("Solo un empleado con cargo JEFE puede realizar esta acción.")
            return

        dni_empleado = input("DNI repartidor: ")
        #disparador que controle si corresponde a un repartidor
        #disparador que compruebe si es empleado
        #disparador que compruebe si existe el pedido
        id_pedido = input("id_pedido: ")
        cursor.callproc("comprobar_pedido", [id_pedido])
        cursor.execute("INSERT INTO reparte(id_pedido,dni)VALUES (:1,:2)",(id_pedido,dni_empleado))
        conn.commit()
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error: {error.message}")
        

############################################################################################
#========================================================================================
#FUNCIONES SUBSISTEMA GESTION DE MESAS
#========================================================================================
############################################################################################

def activar_mesa(conn):
    try:
        cursor = conn.cursor()

        # Para activar una mesa, solamente se debe meter el identificador de la mesa que se quiera activar
        numero = input("Por favor, introduzca el número de la mesa: ")

        cursor.execute("""
            UPDATE mesa
            SET estado = 'Ocupada'
            WHERE id_mesa = :identif
        """, {"identif": numero})

        cursor.execute("""
            SELECT COUNT (*)
            FROM comanda
        """)

        numero_comanda = cursor.fetchone()[0]+1

        cursor.execute("""
            INSERT INTO comanda (id_comanda, id_mesa, estado, fecha_entrada)
            VALUES (:1, :2, :3, SYSDATE)   
        """, (numero_comanda, numero, 'ACTIVO'))

        print("Se ha activado la mesa correctamente")

    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error en la base de datos: {error.message}")
    
    finally:
        cursor.close()

    # HACER DISPARADOR QUE IMPIDA QUE SE ACTIVE DOS MESAS OCUPADAS

############################################################################################

def aniadir_pedido(conn):
    try:
        cursor = conn.cursor()

        # Añadir pedido funciona de la siguiente forma: se introduce el número de la mesa, el identificador de la comida que se vaya a tomar nota y
        # el número de consumiciones de esta

        numero_mesa = input("Por favor, introduzca el número de la mesa: ")
        comida = input("Por favor, introduzca el ID de la comida: ")
        n_cons = input("Por favor, introduzca el número de consumiciones a pedir: ")

        cursor.execute("""
            SELECT id_comanda
            FROM comanda
            WHERE (id_mesa = :identif AND estado = 'ACTIVO')
        """, {"identif": numero_mesa})

        comprobador = cursor.fetchone()
        if (comprobador is None):
            print("No hay ninguna comanda activa en esta mesa")
            return
        
        numero_comanda = comprobador[0]
        cursor.execute("""
            SELECT id_entrada, num_consumidores
            FROM entrada_comanda NATURAL JOIN (SELECT * FROM formado_por WHERE id_producto = :identif_producto)
            WHERE (id_mesa = :identif_mesa AND id_comanda = :identif_comanda)
        """, {"identif_mesa": numero_mesa, "identif_comanda": numero_comanda, "identif_producto": comida})

        resultado = cursor.fetchone()
 
        if (resultado is None):

            cursor.execute("""
                SELECT id_entrada
                FROM entrada_comanda
                WHERE id_entrada = (SELECT MAX(id_entrada) FROM entrada_comanda WHERE (id_mesa = :identif_mesa AND id_comanda = :identif_com))
            """, {"identif_mesa": numero_mesa, "identif_com": numero_comanda})

            comprobador = cursor.fetchone()
            if (comprobador is None):
                num_entrada = 1
            else:
                num_entrada = int(comprobador[0])+1

            cursor.execute("""
                INSERT INTO entrada_comanda (id_mesa, id_comanda, id_entrada, num_consumidores)
                VALUES (:1, :2, :3, :4)
            """, (numero_mesa, numero_comanda, num_entrada, n_cons))

            cursor.execute("""
                INSERT INTO formado_por (id_entrada, id_mesa, id_comanda, id_producto)
                VALUES (:1, :2, :3, :4)
            """, (num_entrada, numero_mesa, numero_comanda, comida))
        
        else:
            num_entrada, num_cons_act = resultado

            cursor.execute("""
                UPDATE entrada_comanda
                SET num_consumidores = :nuevo_valor
                WHERE (id_mesa = :identif_mesa AND id_comanda = :identif_com AND id_entrada = :identif_ent)
            """, {"nuevo_valor": num_cons_act+int(n_cons), "identif_mesa": numero_mesa, "identif_com": numero_comanda, "identif_ent": num_entrada})

        print("El pedido se ha añadido correctamente")

    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error en la base de datos: {error.message}")
    
    finally:
        cursor.close()

############################################################################################

def eliminar_pedido(conn):
    try:
        cursor = conn.cursor()

        numero_mesa = input("Por favor, introduzca el número de la mesa: ")
        comida = input("Por favor, introduzca el ID de la comida: ")
        n_consumiciones = input("Por favor, introduzca el número de consumiciones a eliminar: ")

        cursor.execute("""
            SELECT id_comanda
            FROM comanda
            WHERE (id_mesa = :identif AND estado = 'ACTIVO')
        """, {"identif": numero_mesa})

        comprobador = cursor.fetchone()
        if (comprobador is None):
            print("No hay ninguna comanda activa en esta mesa")
            return
        
        numero_comanda = comprobador[0]

        cursor.execute("""
            SELECT id_entrada, num_consumidores
            FROM entrada_comanda NATURAL JOIN (SELECT * FROM formado_por WHERE id_producto = :ident_prod)
            WHERE (id_mesa = :identif_mesa AND id_comanda = :identif_comanda)
        """, {"identif_mesa": numero_mesa, "identif_comanda": numero_comanda, "ident_prod": comida})

        resultado = cursor.fetchone()

        if (resultado is not None):
            n_entrada, n_cons_act = resultado

            cursor.execute("""
                UPDATE entrada_comanda
                SET num_consumidores = :nuevo_numero
                WHERE (id_mesa = :ident_mesa AND id_comanda = :ident_com AND id_entrada = :ident_ent)
            """, {"nuevo_numero": n_cons_act-int(n_consumiciones), "ident_mesa": numero_mesa, "ident_com": numero_comanda, "ident_ent": n_entrada})

            print("Se ha eliminado correctamente el producto")

        else:
            print("Dicho producto no ha sido pedido")

    # HACER UN DISPARADOR QUE COMPRUEBE QUE CUANDO UN PEDIDO ES 0, BORRE LAS TUPLAS

    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error en la base de datos: {error.message}")
    
    finally:
        cursor.close()

############################################################################################

def consultar_pedido(conn):
    try:
        cursor = conn.cursor()

        numero = input("Por favor, introduzca el número de la mesa: ")
        decision = input("¿Quiere ver todos los pedidos de esta mesa? (Marcar S/s para sí o N/n para ver solo el actual (si es posible)): ")

        if (decision.upper() == 'S'):
            cursor.execute("""
                SELECT to_char(c.fecha_entrada, 'DD/MON/YYYY HH24:MI:SS'), c.id_mesa, c.id_comanda, e.id_entrada, e.num_consumidores, p.id_producto, p.nombre, p.precio
                FROM comanda c
                JOIN entrada_comanda e ON c.id_mesa = e.id_mesa and c.id_comanda = e.id_comanda
                JOIN formado_por f ON e.id_mesa = f.id_mesa AND e.id_comanda = f.id_comanda AND e.id_entrada = f.id_entrada
                JOIN producto p ON p.id_producto = f.id_producto
                WHERE (c.id_mesa = :ident_mesa)
            """, {"ident_mesa": numero})

        elif (decision.upper() == 'N'):
            cursor.execute("""
                SELECT to_char(c.fecha_entrada, 'DD/MON/YYYY HH24:MI:SS'), c.id_mesa, c.id_comanda, e.id_entrada, e.num_consumidores, p.id_producto, p.nombre, p.precio
                FROM comanda c
                JOIN entrada_comanda e ON c.id_mesa = e.id_mesa and c.id_comanda = e.id_comanda
                JOIN formado_por f ON e.id_mesa = f.id_mesa AND e.id_comanda = f.id_comanda AND e.id_entrada = f.id_entrada
                JOIN producto p ON p.id_producto = f.id_producto
                WHERE (c.id_mesa = :ident_mesa AND c.estado = 'ACTIVO')
            """, {"ident_mesa": numero})

        for row in cursor:
            print(row)

    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error en la base de datos: {error.message}")
    
    finally:
        cursor.close()

############################################################################################

def solicitar_cuenta(conn):
    try:
        cursor = conn.cursor()

        numero_mesa = input("Por favor, introduzca el número de la mesa solicitante de la cuenta: ")

        cursor.execute("""
            SELECT id_comanda, to_char(fecha_entrada, 'DD/MON/YYYY HH24:MI:SS')
            FROM comanda
            WHERE (id_mesa = :identif AND estado = 'ACTIVO')
        """, {"identif": numero_mesa})

        comprobador = cursor.fetchone()

        if (comprobador is None):
            print("No hay ninguna comanda activa para esta mesa")
            return
        
        else:
            numero_comanda, fecha = comprobador
            print(fecha)
            print(f"Recibo de la mesa {numero_mesa}")
            print(f"ID recibo {numero_comanda}")

            print("Nº \tNombre \tPrecio \tConsum. \tTotal")

            cursor.execute("""
                SELECT p.nombre, p.precio, e.num_consumidores
                FROM entrada_comanda e
                JOIN formado_por f ON e.id_mesa = f.id_mesa AND e.id_comanda = f.id_comanda AND e.id_entrada = f.id_entrada
                JOIN producto p ON f.id_producto = p.id_producto
                WHERE (e.id_mesa = :ident_mesa AND e.id_comanda = :ident_comanda)
            """, {"ident_mesa": numero_mesa, "ident_comanda": numero_comanda})

            i = 1
            importe_total = 0
            for row in cursor:
                print(f"{i} \t{row[0]} \t{row[1]} \t{row[2]} \t{row[2]*row[1]}")
                i+=1
                importe_total+=row[2]*row[1]

            print(f"\nTOTAL: {importe_total}")

    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error en la base de datos: {error.message}")
    
    finally:
        cursor.close()

############################################################################################

def registrar_pago(conn):
    try:
        cursor = conn.cursor()

        # Al registrar el pago de una mesa, tenemos que poner el identificador de la mesa que debe pagar
        numero = input("Por favor, introduzca el número de la mesa: ")

        cursor.execute("""
            UPDATE mesa
            SET estado = 'Disponible'
            WHERE id_mesa = :identif
        """, {"identif": numero})

        cursor.execute("""
            UPDATE comanda
            SET estado = 'PAGADO'
            WHERE (estado = 'ACTIVO' AND id_mesa = :identif)
        """, {"identif": numero})

        print("El pago ha sido registrado correctamente")

    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error en la base de datos: {error.message}")
    
    finally:
        cursor.close()


############################################################################################
#========================================================================================
#FUNCIONES SUBSISTEMA GESTION RESERVAS
#========================================================================================
############################################################################################

def crear_reserva(conn):
    try:
        cursor = conn.cursor()
        
        # Pedir datos al usuario
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        telefono = input("Teléfono: ")
        fecha = input("Fecha (formato ejemplo 24-12-2003): ")
        hora = input("Hora (formato HH:MM, ejemplo 14:30): ")
        numero = input("Número de personas: ")
        lugar = input("Dentro o fuera (0 o 1): ")
        
        # Validar permiso del usuario
        permiso = input("¿Está de acuerdo con que sus datos sean registrados en nuestra base de datos? (S/N): ")
        if permiso.upper() != 'S':
            print("Debe aceptar los términos para realizar una reserva.")
            return
        
        # Validar y transformar la fecha y hora
        try:
            # Validar fecha
            fecha_formateada = datetime.datetime.strptime(fecha, "%d-%m-%Y").strftime("%d-%m-%Y")
            
            # Validar hora
            hora_formateada = datetime.datetime.strptime(hora, "%H:%M").strftime("%H:%M")
            
            # Combinar fecha y hora
            fecha_hora = f"{fecha_formateada} {hora_formateada}"
        except ValueError:
            print("La fecha o la hora ingresadas no son válidas. Asegúrate de usar los formatos DD-MM-YYYY y HH:MM.")
            return
        
        # Validar número y lugar como enteros
        try:
            numero = int(numero)
            lugar = int(lugar)
        except ValueError:
            print("Número de personas y lugar deben ser valores numéricos.")
            return
        
        # Ejecutar la consulta con marcadores de nombres
        sql = """
            INSERT INTO reserva (fecha, telefono, nombre, apellido, numero_personas, lugar) 
            VALUES (TO_DATE(:fecha_hora, 'DD-MM-YYYY HH24:MI'), :telefono, :nombre, :apellido, :numero_personas, :lugar)
        """
        cursor.execute(sql, {
            'fecha_hora': fecha_hora,
            'telefono': telefono,
            'nombre': nombre,
            'apellido': apellido,
            'numero_personas': numero,
            'lugar': lugar
        })
        conn.commit()
        print("Reserva creada con éxito.")
    
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error en la base de datos: {error.message}")
    
    finally:
        cursor.close()


def modificar_reserva(conn):
    try:
        cursor = conn.cursor()
        telefono = input("Teléfono: ")
        fecha = input("Fecha (formato ejemplo 24-12-2003): ")
        hora = input("Hora (formato HH:MM, ejemplo 14:30): ")
        # Validar y transformar la fecha y hora
        try:
            # Validar fecha
            fecha_formateada = datetime.datetime.strptime(fecha, "%d-%m-%Y").strftime("%d-%m-%Y")
            
            # Validar hora
            hora_formateada = datetime.datetime.strptime(hora, "%H:%M").strftime("%H:%M")
            
            # Combinar fecha y hora
            fecha_hora = f"{fecha_formateada} {hora_formateada}"
        except ValueError:
            print("La fecha o la hora ingresadas no son válidas. Asegúrate de usar los formatos DD-MM-YYYY y HH:MM.")
            return
        
        comprobacion_nombre = input("¿Quiere modificar el nombre asociado a la reserva? (S sí, N no): ")
        if comprobacion_nombre.lower() == "s":
            nombre = input("Introduzca el nuevo nombre: ")
            cursor.execute("""
            UPDATE reserva
            SET nombre = :nuevo_nombre
            WHERE telefono = :telefono AND fecha = TO_DATE(:fecha_hora_formateada, 'DD-MM-YYYY HH24:MI')
            """, {
                "nuevo_nombre": nombre,
                "telefono": telefono,
                "fecha_hora_formateada": fecha_hora
            })

        comprobacion_apellido = input("¿Quiere modificar el apellido asociado a la reserva? (S sí, N no): ")
        if comprobacion_apellido.lower() == "s":
            apellido_nuevo = input("Introduzca el nuevo apellido: ")
            cursor.execute("""
            UPDATE reserva
            SET apellido = :apellido_nuevo
            WHERE telefono = :telefono AND fecha = TO_DATE(:fecha_hora_formateada, 'DD-MM-YYYY HH24:MI')
            """, {
                "apellido_nuevo": apellido_nuevo,
                "telefono": telefono,
                "fecha_hora_formateada": fecha_hora
            })

        comprobacion_num_personas = input("¿Quiere modificar el num_personas asociado a la reserva? (S sí, N no): ")
        if comprobacion_num_personas.lower() == "s":
            num_personas_nuevo = input("Introduzca el nuevo num_personas: ")
            cursor.execute("""
            UPDATE reserva
            SET numero_personas = :num_personas_nuevo
            WHERE telefono = :telefono AND fecha = TO_DATE(:fecha_hora_formateada, 'DD-MM-YYYY HH24:MI')
            """, {
                "num_personas_nuevo": num_personas_nuevo,
                "telefono": telefono,
                "fecha_hora_formateada": fecha_hora
            })

        conn.commit()
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error: {error.message}")

def anular_reserva(conn):
    try:
        cursor = conn.cursor()

        # Solicitar datos al usuario
        telefono = input("Introduzca el número de teléfono asociado a la reserva: ").strip()
        fecha = input("Introduzca la fecha de la reserva (formato DD-MM-YYYY): ").strip()
        hora = input("Hora (formato HH:MM, ejemplo 14:30): ").strip()

        # Validar y transformar la fecha y hora
        try:
            fecha_formateada = datetime.datetime.strptime(fecha, "%d-%m-%Y").strftime("%d-%m-%Y")
            hora_formateada = datetime.datetime.strptime(hora, "%H:%M").strftime("%H:%M")
            fecha_hora = f"{fecha_formateada} {hora_formateada}"
        except ValueError:
            print("La fecha o la hora ingresadas no son válidas. Asegúrate de usar los formatos DD-MM-YYYY y HH:MM.")
            return

        # Confirmar que la reserva existe
        cursor.execute("""
            SELECT COUNT(*)
            FROM reserva
            WHERE telefono = :telefono AND fecha = TO_DATE(:fecha_hora, 'DD-MM-YYYY HH24:MI')
        """, {"telefono": telefono, "fecha_hora": fecha_hora})

        if cursor.fetchone()[0] == 0:
            print("La reserva no existe. Verifique los datos ingresados.")
            return

        # Eliminar la reserva
        cursor.execute("""
            DELETE FROM encargado_de
            WHERE tlf = :telefono AND fecha = TO_DATE(:fecha_hora, 'DD-MM-YYYY HH24:MI')
        """, {"telefono": telefono, "fecha_hora": fecha_hora})

        cursor.execute("""
            DELETE FROM reserva
            WHERE telefono = :telefono AND fecha = TO_DATE(:fecha_hora, 'DD-MM-YYYY HH24:MI')
        """, {"telefono": telefono, "fecha_hora": fecha_hora})

        conn.commit()
        print("Reserva anulada con éxito.")
    
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error al anular la reserva: {error.message}")
        conn.rollback()
    
    finally:
        cursor.close()

def asignar_empleado(conn):
    try:
        cursor = conn.cursor()
        
        # Solicitar datos al usuario
        dni_jefe = input("Introduzca el DNI del USUARIO REALIZANDO LA ASIGNACION: ").strip()

        # Verificar si el usuario es jefe
        cursor.execute("SELECT cargo FROM empleado WHERE dni = :dni", {"dni": dni_jefe})
        resultado = cursor.fetchone()

        if not resultado or resultado[0] != 'JEFE':
            print("Solo un empleado con cargo JEFE puede realizar esta acción.")
            return

        telefono = input("Introduzca el número de teléfono asociado a la reserva: ").strip()
        fecha = input("Introduzca la fecha de la reserva (formato DD-MM-YYYY): ").strip()
        hora = input("Hora (formato HH:MM, ejemplo 14:30): ").strip()
        dni_empleado = input("Introduzca el DNI del empleado a asignar: ").strip()

        
        # Validar y transformar la fecha y hora
        try:
            # Validar fecha
            fecha_formateada = datetime.datetime.strptime(fecha, "%d-%m-%Y").strftime("%d-%m-%Y")
            
            # Validar hora
            hora_formateada = datetime.datetime.strptime(hora, "%H:%M").strftime("%H:%M")
            
            # Combinar fecha y hora
            fecha_hora = f"{fecha_formateada} {hora_formateada}"
        except ValueError:
            print("La fecha o la hora ingresadas no son válidas. Asegúrate de usar los formatos DD-MM-YYYY y HH:MM.")
            return
        # Intentar la inserción en la tabla encargado_de
        cursor.execute("""
            INSERT INTO encargado_de (dni_empleado, fecha, tlf)
            VALUES (:dni_empleado, TO_DATE(:fecha, 'DD-MM-YYYY HH24:MI'), :telefono)
        """, {"dni_empleado": dni_empleado, "fecha": fecha_hora, "telefono": telefono})
        
        # Confirmar cambios
        conn.commit()
        print("Empleado asignado correctamente.")
    
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error al asignar empleado: {error.message}")
        conn.rollback()
    finally:
        cursor.close()

def listado_reserva(conn):
    try:
        cursor = conn.cursor()
        # Pedir al usuario si quiere filtrar por teléfono
        filtro_telefono = input("¿Desea filtrar por teléfono? (S/N): ").strip().upper()
        
        if filtro_telefono == 'N':
            filtro_telefono_fecha = input("¿Desea filtrar por teléfono Y fecha? (S/N): ").strip().upper()
        else:
            filtro_telefono_fecha = 'N'

        if filtro_telefono == 'S':
            telefono = input("Introduzca el número de teléfono: ")
            # Consulta con filtro por teléfono
            cursor.execute("""
                SELECT r.fecha, r.telefono, r.nombre, r.apellido, r.numero_personas, 
                       r.lugar, e.dni_empleado
                FROM reserva r
                LEFT JOIN encargado_de e ON r.fecha = e.fecha AND r.telefono = e.tlf
                WHERE r.telefono = :telefono
                ORDER BY r.fecha
            """, {"telefono": telefono})
        elif filtro_telefono_fecha == 'S':
            telefono = input("Introduzca el número de teléfono: ")
            fecha = input("Fecha (formato ejemplo 24-12-2003): ")
            hora = input("Hora (formato HH:MM, ejemplo 14:30): ")
            # Validar y transformar la fecha y hora
            try:
                # Validar fecha
                fecha_formateada = datetime.datetime.strptime(fecha, "%d-%m-%Y").strftime("%d-%m-%Y")
                
                # Validar hora
                hora_formateada = datetime.datetime.strptime(hora, "%H:%M").strftime("%H:%M")
                
                # Combinar fecha y hora
                fecha_hora = f"{fecha_formateada} {hora_formateada}"
            except ValueError:
                print("La fecha o la hora ingresadas no son válidas. Asegúrate de usar los formatos DD-MM-YYYY y HH:MM.")
                return
            cursor.execute("""
            SELECT r.fecha, r.telefono, r.nombre, r.apellido, r.numero_personas, 
                r.lugar, e.dni_empleado
            FROM reserva r
            LEFT JOIN encargado_de e ON r.fecha = e.fecha AND r.telefono = e.tlf
            WHERE r.telefono = :telefono AND r.fecha = TO_DATE(:fecha, 'DD-MM-YYYY HH24:MI')
            ORDER BY r.fecha
            """, {"telefono": telefono, "fecha": fecha_hora})

        else:
            # Consulta sin filtro
            cursor.execute("""
                SELECT r.fecha, r.telefono, r.nombre, r.apellido, r.numero_personas, 
                       r.lugar, e.dni_empleado
                FROM reserva r
                LEFT JOIN encargado_de e ON r.fecha = e.fecha AND r.telefono = e.tlf
                ORDER BY r.fecha
            """)

        # Imprimir resultados
        print("\nListado de Reservas:")
        print("Fecha | Teléfono | Nombre | Apellido | Número de Personas | Lugar | DNI Empleado Encargado")
        print("-" * 80)
        for row in cursor:
            fecha, telefono, nombre, apellido, num_personas, lugar, dni_encargado = row
            lugar_str = "Dentro" if lugar == 0 else "Fuera"
            print(f"{fecha} | {telefono} | {nombre} | {apellido} | {num_personas} | {lugar_str} | {dni_encargado or 'N/A'}")
    
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error al listar reservas: {error.message}")
    finally:
        cursor.close()


#========================================================================================
#MEŃÚS
#========================================================================================
#MENU GESTIÓN EMPLEADOS
def gestion_empleado(conn):
    while True:
        print("\n--- SELECCIÓN OPCION ---")
        print("1. Dar de alta empleado")
        print("2. Dar de baja empleado")
        print("3. Modificar datos empleado")
        print("4. Listar empleados")
        print("5. Reporta incidencia")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == '1':
            dar_de_alta_empleado(conn)
        elif opcion == '2':
            dar_de_baja_empleado(conn)
        elif opcion == '3':
            modificar_datos_empleado(conn)
        elif opcion == '4':
            listar_empleados(conn)
        elif opcion == '5':
            reporta_incidencia(conn)
        elif opcion =='6':
            conn.commit()
            return
        else:
            print("Opción no válida.")

#MENU GESTIÓN PROVEEDORES
def gestion_proveedor(conn):
    while True:
        print("\n--- SELECCIÓN OPCION ---")
        print("1. Dar de alta proveedor")
        print("2. Dar de baja proveedor")
        print("3. Listado por CIF (solo proveedores)")
        print("4. Listado por CIF (proveedores con pedidos)")
        print("5. Hacer pedido")
        print("6. Cancelar pedido")
        print("7. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == '1':
            dar_de_alta_proveedor(conn)
        elif opcion == '2':
            dar_de_baja_proveedor(conn)
        elif opcion == '3':
            listado_por_cif_sin_pedidos(conn)
        elif opcion == '4':
            listado_por_cif_con_pedidos(conn)
        elif opcion == '5':
            hacer_pedido(conn)
        elif opcion == '6':
            cancelar_pedido(conn)
        elif opcion =='7':
            conn.commit()
            return
        else:
            print("Opción no válida.")

#MENU GESTIÓN USUARIOS
def gestion_pedidos_online(conn):
    while True:
        print("\n--- SELECCIÓN OPCION ---")
        print("1. Dar de alta usuario")
        print("2. Dar de baja usuario")
        print("3. Hacer pedidos online")
        print("4. Listado por filtros")
        print("5. Asignar repartidor")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == '1':
            dar_de_alta_usuario(conn)
        elif opcion == '2':
            dar_de_baja_usuario(conn)
        elif opcion == '3':
            hacer_pedido_online(conn)
        elif opcion == '4':
            listado_por_filtros(conn)
        elif opcion == '5':
            asignar_repartidor(conn)
        elif opcion == '6':
            conn.commit()
            return
        else:
            print("Opción no válida.")

#MENU GESTIÓN MESAS
def gestion_mesas(conn):
    while True:
        print("\n--- SELECCIÓN OPCION ---")
        print("1. Activar mesa")
        print("2. Aniadir pedido")
        print("3. Eliminar pedido")
        print("4. Consultar pedido")
        print("5. Solicitar cuenta")
        print("6. Registrar pago")
        print("7. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == '1':
            activar_mesa(conn)
        elif opcion == '2':
            aniadir_pedido(conn)
        elif opcion == '3':
            eliminar_pedido(conn)
        elif opcion == '4':
            consultar_pedido(conn)
        elif opcion == '5':
            solicitar_cuenta(conn)
        elif opcion == '6':
            registrar_pago(conn)
        elif opcion == '7':
            conn.commit()
            return
        else:
            print("Opción no válida.")

#MENU GESTIÓN RESERVAS
def gestion_reservas(conn):
    while True:
        print("\n--- SELECCIÓN OPCION ---")
        print("1. Crear reserva")
        print("2. Anular reserva")
        print("3. Modificar reserva")
        print("4. Asignar empleado")
        print("5. Listado reservas")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == '1':
            crear_reserva(conn)
        elif opcion == '2':
            anular_reserva(conn)
        elif opcion == '3':
            modificar_reserva(conn)
        elif opcion == '4':
            asignar_empleado(conn)
        elif opcion == '5':
            listado_reserva(conn)
        elif opcion == '6':
            conn.commit()
            return
        else:
            print("Opción no válida.")


# Mostrar el contenido de las tablas
def mostrar_tablas(conn):
    try:
        cursor = conn.cursor()
        print("\nTabla Proveedor:")
        cursor.execute("SELECT * FROM proveedor")
        for row in cursor:
            print(row)
        
        print("\nTabla pedido_proveedor:")
        cursor.execute("SELECT * FROM pedido_proveedor")
        for row in cursor:
            print(row)
        
        print("\nTabla asociado:")
        cursor.execute("SELECT * FROM asociado")
        for row in cursor:
            print(row)

        print("\nTabla usuario:")
        cursor.execute("SELECT * FROM usuario")
        for row in cursor:
            print(row)
        
        print("\nTabla pedido:")
        cursor.execute("SELECT * FROM pedido")
        for row in cursor:
            print(row)
        
        print("\nTabla realiza:")
        cursor.execute("SELECT * FROM realiza")
        for row in cursor:
            print(row)
        
        print("\nTabla empleado:")
        cursor.execute("SELECT * FROM empleado")
        for row in cursor:
            print(row)
        

        print("\nTabla hace:")
        cursor.execute("SELECT * FROM hace")
        for row in cursor:
            print(row)
        
        print("\nTabla encargado_de:")
        cursor.execute("SELECT * FROM encargado_de")
        for row in cursor:
            print(row)
        
        print("\nTabla reparte:")
        cursor.execute("SELECT * FROM reparte")
        for row in cursor:
            print(row)
        
        print("\nTabla viveres:")
        cursor.execute("SELECT * FROM viveres")
        for row in cursor:
            print(row)
        
        print("\nTabla tiene:")
        cursor.execute("SELECT * FROM tiene")
        for row in cursor:
            print(row)
        
        print("\nTabla incidencia:")
        cursor.execute("SELECT * FROM incidencia")
        for row in cursor:
            print(row)


        print("\nTabla reporta:")
        cursor.execute("SELECT * FROM reporta")
        for row in cursor:
            print(row)
        
        print("\nTabla producto:")
        cursor.execute("SELECT * FROM producto")
        for row in cursor:
            print(row)
        
        print("\nTabla contiene:")
        cursor.execute("SELECT * FROM contiene")
        for row in cursor:
            print(row)
        
        print("\nTabla mesa:")
        cursor.execute("SELECT * FROM mesa")
        for row in cursor:
            print(row)
        
        print("\nTabla reserva:")
        cursor.execute("SELECT * FROM reserva")
        for row in cursor:
            print(row)

        print("\nTabla asignado:")
        cursor.execute("SELECT * FROM asignado")
        for row in cursor:
            print(row)
        
        print("\nTabla comanda:")
        cursor.execute("SELECT id_mesa, id_comanda, estado, to_char(fecha_entrada, 'DD/MON/YYYY HH24:MI:SS') FROM comanda")
        for row in cursor:
            print(row)
        
        print("\nTabla entrada_comanda:")
        cursor.execute("SELECT * FROM entrada_comanda")
        for row in cursor:
            print(row)
        
        print("\nTabla formado_por:")
        cursor.execute("SELECT * FROM formado_por")
        for row in cursor:
            print(row)
        

    except oracledb.DatabaseError as e:
        print("Error al mostrar el contenido de las tablas:", e)

#============================================================================
# Menú principal
#============================================================================
def mostrar_triggers(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT trigger_name, trigger_type, triggering_event, table_name, status
        FROM user_triggers
    """)

    for row in cursor:
        print(f"Nombre: {row[0]} // Evento activante: {row[2]} // Tabla: {row[3]} // Estado: {row[4]}")


def menu_principal(conn):
    while True:

        print("\n--- SELECCIÓN SUBSISTEMA ---")
        print("1. EMPLEADOS")
        print("2. PROVEEDOR")
        print("3. PEDIDOS ONLINE")
        print("4. MESAS")
        print("5. RESERVAS")
        print("6. Mostrar Tablas")
        print("7. Eliminar y crear tablas")
        print("8. Salir")
        opcion = input("Seleccione una opción: ")


        if opcion == '1':
            gestion_empleado(conn)
            mostrar_tablas(conn)
        elif opcion == '2':
            gestion_proveedor(conn)
            mostrar_tablas(conn)
        elif opcion == '3':
            gestion_pedidos_online(conn)
            mostrar_tablas(conn)
        elif opcion == '4':
            gestion_mesas(conn)
            mostrar_tablas(conn)
        elif opcion == '5':
            gestion_reservas(conn)
            mostrar_tablas(conn)
        elif opcion == '6':
            mostrar_tablas(conn)
        elif opcion == '7':
            crear_tablas(conn)
        elif opcion == '8':
            conn.close()
            print("Conexión cerrada. Salir del programa.")
            break
        else:
            mostrar_triggers(conn)
            print("Opción no válida.")

if __name__ == "__main__":
    conn = conectar_bd()
    if conn:
        crear_triggers(conn)
        mostrar_tablas(conn)
        menu_principal(conn)