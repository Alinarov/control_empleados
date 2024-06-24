#!/usr/bin/env python
#
#	Modulo donde se tienen los codigos de comunicacion con la base de datos
#
import socket
import pyodbc
import json
import concurrent.futures
import threading

"""
def __init__(self, server, database):
def connect(self):
def create_database(self, database_name):
def create_table(self, query):
def close_connection(self):
def get_host_name(self):
def __init__(self):
def configuraciones(self):
def connect(self):
def execute_query(self, query):
def close_connection(self):
def verificador(usuario_codificado, contrasenia_codificada):
"""





# Este clase 
class SQLServerManager:
	def __init__(self, server, database):
		self.server = server
		self.database = database
		self.conn = None
		self.cursor = None

	def connect(self):
		try:
			print("Intentando conectar a SQL Server...")
			self.conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={self.server};DATABASE=master;Trusted_Connection=yes;')
			self.conn.autocommit = True
			self.cursor = self.conn.cursor()
			
		except pyodbc.Error as e:
			print("Error al conectar a SQL Server: \n\n")


	def create_database(self, database_name):
		try:
			print("Creando la base de datos...")
			self.cursor.execute(f"CREATE DATABASE {database_name}")
			print("Base de datos creada exitosamente")
		except pyodbc.Error as e:
			print("Error al crear la base de datos:", e)


	def create_table(self, query):
		try:
			self.cursor.execute(f"USE {self.database}")
			print("Creando la tabla usuarios...")

			print("Query recibido: " + query)
			self.cursor.execute(query)

			print("Tabla creada exitosamente")
		except pyodbc.Error as e:
			return e
			print("Error al crear la tabla:", e)

	def close_connection(self):
		if self.conn:
			self.conn.close()
			print("Conexión cerrada")

	def get_host_name(self):
		# 
		#	GET_HOSTNAME.PY
		# 
		# Llamada a la función para obtener el nombre del servidor
		try:
			nombre_servidor = socket.gethostname()
			return nombre_servidor
		except Exception as e:
			print("Error al obtener el nombre del servidor:", e)
			return None





class SQLServerConnector(object):
	_instance = None
	_lock = threading.Lock()

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			with cls._lock:
				if not cls._instance:
					cls._instance = super(SQLServerConnector, cls).__new__(cls, *args, **kwargs)
		return cls._instance

	def __init__(self):
		if not hasattr(self, 'initialized'):  # Evitar re-inicialización
			self._data_config = self.configuraciones()
			self.servers = self._data_config["servidores"]
			self.database = self._data_config["nombre_database"]
			self.conn = None
			self.initialized = True  # Marcar como inicializado

	def configuraciones(self):
		with open("configuracion_comunicacion.json", "r") as fileConfig:
			data = json.load(fileConfig)
		return data

	def try_connect(self, server):
		try:
			print(f"Intentando conectar a servidor: {server} ...")
			conn_str = (
				f'DRIVER={{SQL Server}};'
				f'SERVER={server};'
				f'DATABASE={self.database};'
				f'Trusted_Connection=True;'
				f'Connection Timeout=5;'  # Reducir el tiempo de espera para cada intento de conexión
			)

			conn = pyodbc.connect(conn_str)
			conn.autocommit = True
			print(f"Conexión exitosa a {server}")
			return conn
		except pyodbc.Error as e:
			print(f"Error al conectar a {server}: {e}")
			return None

	def connect(self):
		if self.conn:
			print("Ya existe una conexión activa.")
			return
		
		with concurrent.futures.ThreadPoolExecutor() as executor:
			future_to_server = {executor.submit(self.try_connect, server): server for server in self.servers}
			for future in concurrent.futures.as_completed(future_to_server):
				server = future_to_server[future]
				try:
					conn = future.result()
					if conn:
						self.conn = conn
						print(f"Conectado a {server}")
						return
				except Exception as e:
					print(f"Error en el intento de conexión con {server}: {e}")

		print("Error al conectar a SQL Server: - revisa el nombre de la base de datos y la configuración del servidor")


	def execute_query(self, query):
		if not self.conn:
			print("No hay conexión establecida.")
			return None

		try:
			print("\nQuery a ejecutar:", query)  # Imprimir el query a ejecutar
			cursor = self.conn.cursor()
			cursor.execute(f"use {self.database}")
			cursor.execute(query)
			try:
				rows = cursor.fetchall()
			except:
				rows = cursor.fetchone()
			print("Consulta ejecutada con éxito")
			return rows
		except pyodbc.Error as e:
			print("Error al ejecutar la consulta:", e)
			print("Pero si el query es una dml entonces no hay problema con tal que este bien hecha")
			return None
		finally:
			cursor.close()

	def close_connection(self):
		if self.conn:
			self.conn.close()
			print("Conexión cerrada")


def verificador(usuario_codificado, contrasenia_codificada):
	connector = SQLServerConnector()
	connector.connect()
	queryUsr = f"""SELECT COUNT(*) FROM Usuario WHERE usuario = '{usuario_codificado}' AND contrasenia = '{contrasenia_codificada}';"""
	User_verificacion = connector.execute_query(queryUsr)

	connector.connect()
	queryAdmin = f"""SELECT COUNT(*) FROM Administrador WHERE usuario = '{usuario_codificado}' AND contrasenia = '{contrasenia_codificada}';"""
	Admin_verificacion = connector.execute_query(queryAdmin)

	if any(1 in item for item in Admin_verificacion):
		print("\n \nYa existe")
		return (True, "A")
	elif any(1 in item for item in User_verificacion): 
		print("\n \nYa existe")
		return (True, "U")
	else:
		return False




'''
if __name__ == "__main__":
	connector = SQLServerConnector()
	insercion = """
	INSERT INTO registro_empleados (nombre_empleado, apellidos_empleado, dni_empleado, sexo, telefono, fecha_nacimiento, email, direccion, fecha_contrato)
	VALUES ('Carlos', 'Garcia', '34567890', 'M', '555555555', '1993-06-12', 'carlos@example.com', 'Avenida 789', '2024-05-09');
	"""
	perfiles_empleados = """SELECT * from registro_empleados order by id_registro_personal"""
	# Ejecutar la consulta de inserción
	result = connector.execute_query("select * from prueba1")
	print('Respuesta del servidor:', result)

'''


# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

"""
|=================================================
| COMANDOS PARA LAS VENTANAS
|_________________________________________________
-- CORTE DEL DIA : listado de cargas que hicieron los empleados en un dia de cargas
"""
corte_dia = """
SELECT e.nombre_empleado, e.apellidos_empleado, e.dni_empleado, c.id_cargas, c.peso_carga, c.id_fecha_carga, fc.hora_inicio, fc.hora_corte, c.hora_entrega
FROM empleado em
INNER JOIN registro_empleados e ON em.id_registro_personal = e.id_registro_personal
INNER JOIN cargas c ON em.id_empleado = c.id_empleado
INNER JOIN fecha_carga fc ON c.id_fecha_carga = fc.id_fecha_carga
WHERE c.id_fecha_carga = '2024-03-22'
ORDER BY c.id_cargas--e.nombre_empleado, e.apellidos_empleado;--"""

"""
-- PERFILES EMPLEADOS: listado de datos personales de los empleados
"""
perfiles_empleados = """SELECT * from registro_empleados order by id_registro_personal"""


"""-- ADMINISTRACION EMPLEADOS: listado de los empleados registrados"""
administracion_empleados = """
SELECT nombre_empleado, apellidos_empleado, dni_empleado from registro_empleados order by id_registro_personal"""

"""-- HISTORIAL DE CARGAS"""
historial_cargas = """SELECT * from fecha_carga"""

"""-- SEGUIMIENTO DE CARGA EMPLEADO: lista las cargas realizadas en un dia de un empleado"""
seguimiento_carga = """SELECT e.nombre_empleado, e.apellidos_empleado, e.dni_empleado, c.id_cargas, c.peso_carga, c.id_fecha_carga, fc.hora_inicio, fc.hora_corte, c.hora_entrega
FROM empleado em
INNER JOIN registro_empleados e ON em.id_registro_personal = e.id_registro_personal
INNER JOIN cargas c ON em.id_empleado = c.id_empleado
INNER JOIN fecha_carga fc ON c.id_fecha_carga = fc.id_fecha_carga
WHERE c.id_fecha_carga = '2024-03-22' -- Filtra por la fecha de carga deseada
AND em.id_empleado = 4 -- Filtra por el ID del empleado deseado
ORDER BY c.id_cargas;"""
