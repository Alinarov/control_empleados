#!/usr/bin/env python
# 
# Este codigo de el instalador ya esta completado 
#
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image
import customtkinter as ctk  # Asegúrate de tener esta biblioteca instalada
import pyodbc
from comunicacion import SQLServerManager, SQLServerConnector, verificador
from get_hostname import obtener_nombre_servidor  # GET_HOSTNAME.PY
from app import *
import threading
import sys
from tkinter import messagebox as mensaje
import codificador_descodificador 


y = 310

def escritura_configuracion(dbName, entrada):
	# Leer las configuraciones existentes
	try:
		with open("configuracion_comunicacion.json", "r", encoding="utf-8") as archivo:
			try:
				datos = json.load(archivo)
			except json.JSONDecodeError:
				datos = {}  # Si el archivo está vacío o tiene contenido no válido, inicializamos con un diccionario vacío
	except FileNotFoundError:
		datos = {}  # Si el archivo no existe, iniciamos con un diccionario vacío
	
	# Imprimir las configuraciones actuales
	print("Configuraciones actuales:", datos)
	
	# Actualizar las configuraciones según dbName y entrada
	if dbName == "s":
		# Si "server" no está en datos, inicializarlo como una lista vacía
		if "servidores" not in datos:
			datos["servidores"] = []
		
		# Agregar el nuevo nombre del servidor a la lista
		if entrada not in datos["servidores"]:
			datos["servidores"].append(entrada)
		else:
			print(f"El servidor '{entrada}' ya está en la lista.")
	elif dbName == "db":
		# Actualizar o agregar la configuración de la base de datos
		datos["nombre_database"] = entrada
	else: 
		print("Nada que crear")
		return  # Salimos de la función si no hay nada que actualizar

	# Escribir las configuraciones actualizadas en el archivo JSON
	with open("configuracion_comunicacion.json", "w", encoding="utf-8") as archivo:
		json.dump(datos, archivo, ensure_ascii=False, indent=4)
	
	print("Configuraciones escritas en configuraciones_comunicacion.json")

class Setup(MainApp):
	"""Clase para la configuración del instalador"""
	def __init__(self, parent):
		super().__init__(parent)
		self.dataConfig = configuraciones()
		ctk.set_appearance_mode("dark")
		self.parent = parent
		self.parent.title("Instalador del programa")
		self.parent.geometry("600x400+400+110")
		self.parent.resizable(False, False)
		self.parent.iconbitmap("setup_installer/setup.ico")
		self.frames = {}
		self.current_frame_index = 0

		self.frame_imagen_banner = ctk.CTkFrame(self.parent, height=40)
		self.frame_imagen_banner.pack(fill="x")

		self.cuerpo_ventana = ctk.CTkFrame(self.parent)
		self.cuerpo_ventana.pack(fill="both", expand=True)

		#self.footer = ctk.ctkframe(self.cuerpo_ventana)
		#self.footer.grid(row=1, col)

		# [+] Banner
		self.banner = ctk.CTkLabel(
			self.frame_imagen_banner,
			text="",
			image=ctk.CTkImage(
				light_image=Image.open("banner.jpg"),
				size=(600, 50)
			)
		)
		self.banner.pack()

		# Define los pasos (frames) en el instalador
		steps = [StartPage, StepZero, StepOne, StepTwo, StepThree, StepFour, FinishPage]

		for F in steps:
			page_name = F.__name__
			frame = F(parent=self.cuerpo_ventana, controller=self)
			self.frames[page_name] = frame
			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame("StartPage")

		# Configura el grid para que los frames ocupen todo el espacio
		self.cuerpo_ventana.grid_rowconfigure(0, weight=1)
		self.cuerpo_ventana.grid_columnconfigure(0, weight=1)

		for frame in self.frames.values():
			frame.grid(row=0, column=0)

		# ew


	def show_frame(self, page_name):
		frame = self.frames[page_name]
		frame.tkraise()

	def next_frame(self):
		self.current_frame_index += 1
		if self.current_frame_index >= len(self.frames):
			self.current_frame_index = len(self.frames) - 1
		page_name = list(self.frames.keys())[self.current_frame_index]
		self.show_frame(page_name)

	def previous_frame(self):
		self.current_frame_index -= 1
		if self.current_frame_index < 0:
			self.current_frame_index = 0
		page_name = list(self.frames.keys())[self.current_frame_index]
		self.show_frame(page_name)

class StartPage(tk.Frame):
	def __init__(self, parent, controller):
		super().__init__(parent)
		self.controller = controller

		# [+] Foto del empleado
		self.imagenBienvenida = ctk.CTkLabel(
			self, 
			text = "",
			image = ctk.CTkImage(
				light_image=Image.open("setup_installer/bienvenida.jpg"),
				size=(600,296)
				)
			)
		self.imagenBienvenida.place(x = 0, y=0)

		self.next_button = ctk.CTkButton(self, text="Siguiente", command=controller.next_frame,
			fg_color = "#018574", font = ("",14, "bold"))
		self.next_button.place(x = 10, y = y)

class StepZero(tk.Frame):
	def __init__(self, parent, controller):
		super().__init__(parent)
		self.controller = controller

		self.escaneo_server_label = ctk.CTkLabel(self,
			text = "",
			image = ctk.CTkImage (
				light_image=Image.open("setup_installer/paso0.jpg"),
				size=(600, 296)
				))  
		self.escaneo_server_label.place(x=0, y=0)


		self.entry_text = tk.StringVar()
		self.ctk_entry = ctk.CTkEntry(self, textvariable=self.entry_text, width=300, height=30)
		self.ctk_entry.place(x=60, y=210)

		# Insert a long text into the CTkEntry widget
		long_text = "controlEmpleados"
		self.entry_text.set(long_text)

		# Disable the entry to make it read-only
		self.ctk_entry.configure(state="normal")

		registrar_nombre = ctk.CTkButton(self, text="Registrar nombre", command=self.def_name_database,
			fg_color="#DD5746", font=("", 14, "bold"))
		registrar_nombre.place(x=410, y=210)


		self.next_button = ctk.CTkButton(self, text="Siguiente", command=controller.next_frame,
			fg_color = "#018574", font = ("",14, "bold"), state = "disabled")
		self.next_button.place(x = 10, y = y)

		back_button = ctk.CTkButton(self, text="Atrás", command=controller.previous_frame,
			fg_color = "#ec984a", font = ("",14, "bold"))
		back_button.place(x = 155, y = y)
	
	# (+) Esta funcion verifica si el nombre de la base de datos que se ingresara es un nombre 
	# 		valido y si lo es, dejara continuar
	def def_name_database(self):
		nombre_database = self.ctk_entry.get()

		if " " in nombre_database:              # -- retorna que esta mal 
			mensaje.showerror(message = "El nombre de la base de datos tiene espacios que no deberia de tener", title = "Error")
			self.next_button.configure(state="disabled")
		elif nombre_database.isalnum():         # -- retorna que esta bien
			escritura_configuracion("db", nombre_database)
			mensaje.showinfo(message = "El nombre esta bien escrito: "+ nombre_database+ "\npuedes continuar", title = "Bien hecho :)")
			self.next_button.configure(state="normal")
		else:                                   # -- retorna que esta mal el texto
			mensaje.showerror(message = "El nombre no es un texto alfanumerico valido, solo deben ir numeros y letras", title = "Error")
			self.next_button.configure(state="disabled")

		return nombre_database

class StepOne(tk.Frame):
	def __init__(self, parent, controller):
		super().__init__(parent)
		self.controller = controller

		self.escaneo_server_label = ctk.CTkLabel(self,
			text = "",
			image = ctk.CTkImage (
				light_image=Image.open("setup_installer/paso1.jpg"),
				size=(600, 296)
				))  
		self.escaneo_server_label.place(x=0, y=0)


		# Create a ScrolledText widget
		self.scrolled_text = ctk.CTkTextbox(self, wrap=tk.WORD, width=400, height=140)
		self.scrolled_text.place(x=30, y = 130)

		# Insert a long text into the ScrolledText widget
		long_text = (
			"Haz click en el boton 'Escanear'")# Repeat the text to make it long

		self.scrolled_text.insert(tk.END, long_text)
		self.scrolled_text.configure(state='normal')  # Make the text read-only

		escaneo_server_boton = ctk.CTkButton(self, text="Escanear", command=self.escaneo_server,
			fg_color = "#DD5746", font = ("",14, "bold"))
		escaneo_server_boton.place(x = 435, y = 140)


		self.next_button = ctk.CTkButton(self, text="Siguiente", command=controller.next_frame,
			fg_color = "#018574", font = ("",14, "bold"), state = "disabled")
		self.next_button.place(x = 10, y = y)

		back_button = ctk.CTkButton(self, text="Atrás", command=controller.previous_frame,
			fg_color = "#ec984a", font = ("",14, "bold"))
		back_button.place(x = 155, y = y)

	def escaneo_server(self):
		self.scrolled_text.insert(tk.END, "\nEscaneando ... ")
		nombre_servidor = SQLServerManager.get_host_name(None)
		escritura_configuracion("s", nombre_servidor)
		self.scrolled_text.insert(tk.END, 
			( 
				"\n ------------------------------------------------"
				"\n El nombre del servidor es: "+nombre_servidor +
				"\n ================================================"+
				"\n Ya puedes presionar el boton de \"Siguiente\""
			)
		)
		self.next_button.configure(state="normal")

class StepTwo(tk.Frame):
	def __init__(self, parent, controller):
		super().__init__(parent)
		self.controller = controller

		self.escaneo_server_label = ctk.CTkLabel(self,
			text = "",
			image = ctk.CTkImage (
				light_image=Image.open("setup_installer/paso2.jpg"),
				size=(600, 296)
				))  
		self.escaneo_server_label.place(x=0, y=0)


		# Create a ScrolledText widget
		self.scrolled_text = ctk.CTkTextbox(self, wrap=tk.WORD, width=535, height=160)
		self.scrolled_text.place(x=39, y = 110)

		# Insert a long text into the ScrolledText widget
		long_text = (
			"Haz click en el boton 'Configurar base de datos' para crear la base de datos y las tablas de registros")# Repeat the text to make it long

		self.scrolled_text.insert(tk.END, long_text)
		self.scrolled_text.configure(state='normal')  # Make the text read-only


		configurar_database = ctk.CTkButton(self, text="Configurar base de datos", command=self.start_setup,
			fg_color = "#8B322C", font = ("",14, "bold"))
		configurar_database.place(x = 45, y = 70)


		# = --------------- Botones --------------------
		self.next_button = ctk.CTkButton(self, text="Siguiente", command=controller.next_frame,
			fg_color = "#018574", font = ("",14, "bold"), state = "normal")
		self.next_button.place(x = 10, y = y)

		back_button = ctk.CTkButton(self, text="Atrás", command=controller.previous_frame,
			fg_color = "#ec984a", font = ("",14, "bold"))
		back_button.place(x = 155, y = y)
	
	def start_setup(self):
		# Iniciar el proceso de configuración en un hilo separado
		threading.Thread(target=self.setup_database_structure).start()

	def setup_database_structure(self):
		self.insert_text("\n(+) Configurando ...")
		dato = SQLServerConnector.configuraciones(None)

		self.insert_text(str("\n\nEl nombre del servidor es: " + dato["servidores"][0] + "\nEl nombre de la base de datos es: \n" + dato["nombre_database"]))
		manager = SQLServerManager(dato["servidores"][0], dato["nombre_database"])

		self.insert_text("\n\n(+) Intentando conectar a SQL Server...")
		manager.connect()

		self.insert_text("\n(+) Creando la base de datos...")
		manager.create_database(dato["nombre_database"])
		self.insert_text("\n(!) Base de datos creada exitosamente")

		# =================================================================

		self.insert_text("\n(+) Conexión cerrada")
		manager.close_connection()

		self.insert_text("\n\n(+) Intentando conectar a SQL Server...")
		manager.connect()

		self.insert_text("\n(+) Creando la tabla de registro de empleados...")
		manager.create_table("""CREATE TABLE registro_empleados (
			    id_registro_personal INT IDENTITY(1,1) PRIMARY KEY,
			    nombre_empleado VARCHAR(100) NOT NULL,
			    apellidos_empleado VARCHAR(100) NOT NULL,
			    dni_empleado CHAR(8) NOT NULL,
			    sexo CHAR(1) NOT NULL,
			    telefono CHAR(9) NOT NULL,
			    fecha_nacimiento DATE NOT NULL,
			    email VARCHAR(100),
			    direccion VARCHAR(120),
			    fecha_contrato DATE,
			    estado VARCHAR(20) DEFAULT 'activo' -- Nuevo campo para el estado del empleado
			);
			""")

		self.insert_text("\n(+) Creando la tabla de empleados...")
		manager.create_table("""CREATE TABLE empleado (id_empleado INT IDENTITY(1,1) PRIMARY KEY,id_registro_personal INT NOT NULL,CONSTRAINT unique_employee UNIQUE (id_registro_personal), FOREIGN KEY (id_registro_personal) REFERENCES registro_empleados(id_registro_personal));""")
	
		self.insert_text("\n(+) Creando la tabla de las fechas de carga...")
		manager.create_table("""CREATE TABLE fecha_carga (id_fecha_carga DATE PRIMARY KEY,hora_inicio TIME(0),hora_corte TIME(0));""")

		self.insert_text("\n(+) Creando la tabla de las cargas...")
		manager.create_table("""
			CREATE TABLE cargas (
				id_cargas int  IDENTITY(1,1) PRIMARY KEY , 
				hora_entrega TIME(0),
				peso_carga DECIMAL(4,2),
				id_empleado INT,
				FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado),
				id_fecha_carga date,
				foreign key (id_fecha_carga) references fecha_carga (id_fecha_carga)
			);""")

		self.insert_text("\n(+) Creando la tabla de los administradores...")
		manager.create_table("""
			CREATE TABLE Administrador (
				id INT PRIMARY KEY IDENTITY(1,1),
				usuario NVARCHAR(50) NOT NULL UNIQUE,
				contrasenia NVARCHAR(255) NOT NULL
			);
			""")

		self.insert_text("\n(+) Creando la tabla de los mortales...")
		manager.create_table("""
			CREATE TABLE Usuario (
				id INT PRIMARY KEY IDENTITY(1,1),
				usuario NVARCHAR(50) NOT NULL UNIQUE,
				contrasenia NVARCHAR(255) NOT NULL
			);""")

		self.insert_text("\n(+) Tabla creada exitosamente \n(!) Conexión cerrada")
		manager.close_connection()
		self.insert_text(
			"\n\n==================================================================="+
			" \nConfiguracion satisfecha puedes presionar el boton de \"Siguiente\""+
			"\n====================================================================="
			)
		self.next_button.configure(state = "normal")

	def insert_text(self, text):
		self.scrolled_text.insert(tk.END, text)
		self.scrolled_text.see(tk.END)

class StepThree(tk.Frame):
	def __init__(self, parent, controller):
		super().__init__(parent)
		self.controller = controller

		self.escaneo_server_label = ctk.CTkLabel(
			self,
			text="",
			image=ctk.CTkImage(
				light_image=Image.open("setup_installer/admin_register.jpg"),
				size=(600, 296)
			)
		)
		self.escaneo_server_label.place(x=0, y=0)

		# Campos de entrada para el usuario y la contraseña
		self.usuario_entry = ctk.CTkEntry(
			self, width=225, placeholder_text="Usuario:", font = ("", 15), bg_color = "#a1afb8",
			text_color = "#fff", fg_color = "#5f666b"
			)
		self.usuario_entry.place(x=200, y=115)

		self.contrasenia_entry = ctk.CTkEntry(
			self, 
			show="*",
			width=225, placeholder_text="Contraseña:", font = ("", 15), bg_color = "#a1afb8",
			text_color = "#fff", fg_color = "#5f666b"
			)
		self.contrasenia_entry.place(x=200, y=165)

		# Botón para registrar la cuenta de administrador
		self.registrar_button = ctk.CTkButton(
			self, text="Registrar Administrador", command=self.registrar_administrador,
			fg_color="#26ada6", font=("", 14, "bold"), width = 280, height = 40,
			bg_color="#26ada6", hover_color = "#018574", text_color = "#4c5a65"
		)
		self.registrar_button.place(x=160, y=211)

		self.informacion = ctk.CTkButton(self, text="", 
			command= lambda : mensaje.showinfo(
				message=(
                "Para crear una cuenta, por favor asegúrate de cumplir con las siguientes condiciones:\n\n"
                "1. El usuario y la contraseña no deben estar vacíos.\n"
                "2. El usuario y la contraseña no deben contener espacios.\n"
                "3. El usuario debe tener al menos 3 caracteres.\n"
                "4. La contraseña debe tener al menos 6 caracteres.\n"
                "5. El nombre de usuario debe ser alfanumérico (solo letras y números).\n\n"
                "# ---------------- NO TE PREOCUPES ----------------\n\n"
                "Si te has equivocado de contraseña o no estás seguro de la contraseña que has ingresado, "
                "puedes registrarte de nuevo con el otro usuario y contraseña para poderla editar la que te has equivocado."
            ),
			title = "Condiciones para Crear una Cuenta"
			),
			fg_color = "#fff", font = ("",14, "bold"), image = ctk.CTkImage (
				light_image=Image.open("setup_installer/informacion.png"),
				size=(30, 30)
				),
			width = 30, height = 30, bg_color = "#405a6b"
			)
		self.informacion.place(x = 490, y = 220)

		self.ocultar_mostrar_contra = ctk.CTkButton(self, text="", 
			command= self.mostrar_ocultar_contra ,
			font = ("",14, "bold"), image = ctk.CTkImage (
				light_image=Image.open("setup_installer/ocultar-contrasena.png"),
				size=(30, 30)
				),
			width = 30, height = 30, bg_color = "#405a6b", fg_color = "#FCDC94"
			)
		self.ocultar_mostrar_contra.place(x = 490, y = 170)

		# = --------------- Botones --------------------
		self.next_button = ctk.CTkButton(self, text="Siguiente", command=controller.next_frame,
			fg_color = "#018574", font = ("",14, "bold"), state = "disabled")
		self.next_button.place(x = 10, y = y)

		back_button = ctk.CTkButton(self, text="Atrás", command=controller.previous_frame,
			fg_color = "#ec984a", font = ("",14, "bold"))
		back_button.place(x = 155, y = y)

	def mostrar_ocultar_contra(self):
		if self.contrasenia_entry.cget('show') == '':
			self.contrasenia_entry.configure(show='*')
			self.ocultar_mostrar_contra.configure(image = ctk.CTkImage (
				light_image=Image.open("setup_installer/mostrar-contrasena.png"),
				size=(30, 30)
				),
				fg_color = "#55AD9B"
			)
		else:
			self.contrasenia_entry.configure(show='')
			self.ocultar_mostrar_contra.configure(image = ctk.CTkImage (
				light_image=Image.open("setup_installer/ocultar-contrasena.png"),
				size=(30, 30)
				),
				fg_color = "#FCDC94",
			)


	def registrar_administrador(self):
		usuario = self.usuario_entry.get().strip()
		contrasenia = self.contrasenia_entry.get().strip()

		if not usuario or not contrasenia:
			mensaje.showerror(message="Necesitas proporcionar credenciales válidas.\nPor favor, ingrese un usuario y una contraseña.", title="Error para registrar")
			self.next_button.configure(state="disabled")

		elif " " in usuario or " " in contrasenia:
			mensaje.showerror(message="El usuario y la contraseña no deben contener espacios.", title="Error para registrar")
			self.next_button.configure(state="disabled")

		elif len(usuario) < 3 or len(contrasenia) < 6:
			mensaje.showerror(message="El usuario debe tener al menos 3 caracteres y la contraseña al menos 6 caracteres.", title="Error para registrar")
			self.next_button.configure(state="disabled")

		elif not usuario.isalnum():
			mensaje.showerror(message="El nombre de usuario debe ser alfanumérico.", title="Error para registrar")
			self.next_button.configure(state="disabled")

		else:
			usuario_codificado = codificador_descodificador.codificar_base64(usuario)
			contrasenia_codificada = codificador_descodificador.codificar_base64(contrasenia)

			# Lógica para registrar el administrador
			print(f"Registrando usuario: {usuario_codificado}")
			print(f"Contraseña: {contrasenia_codificada}")

			if verificador(usuario_codificado, contrasenia_codificada):
				mensaje.showerror(
					message="Ya existe una cuenta registrada, elige otras credenciales válidas", 
					title = "Error"
					)
			else:

				connector = SQLServerConnector()
				connector.connect()
				query = f"INSERT INTO Administrador (usuario, contrasenia) VALUES ('{usuario_codificado}', '{contrasenia_codificada}')"
				connector.execute_query(query)

				self.next_button.configure(state="normal")
				mensaje.showinfo(message="Cuenta registrada exitosamente", title="Bien hecho señor Administrador")

			
class StepFour(tk.Frame):
	def __init__(self, parent, controller):
		super().__init__(parent)
		self.controller = controller

		self.escaneo_server_label = ctk.CTkLabel(
			self,
			text="",
			image=ctk.CTkImage(
				light_image=Image.open("setup_installer/usuario_register.jpg"),
				size=(600, 296)
			)
		)
		self.escaneo_server_label.place(x=0, y=0)

		# Campos de entrada para el usuario y la contrasenia
		self.usuario_entry = ctk.CTkEntry(
			self, width=180, placeholder_text="Usuario:", bg_color = "#e8eed4",
			text_color = "#5b5150", fg_color = "#e5eec1", placeholder_text_color = "#69635d"
			)
		self.usuario_entry.place(x=210, y=160)

		self.contrasenia_entry = ctk.CTkEntry(
			self, 
			show="*",
			 width=180, placeholder_text="Contraseña:", bg_color = "#e8eed4",
			text_color = "#5b5150", fg_color = "#e5eec1", placeholder_text_color = "#69635d"
			)
		self.contrasenia_entry.place(x=210, y=197)

		# Botón para registrar la cuenta de administrador
		self.registrar_button = ctk.CTkButton(
			self, text="Registrar Usuario", command=self.start_registrar_administrador,
			fg_color="#26ada6", font=("", 14, "bold"), width = 180, height = 25,
			bg_color="#d4d8c1", hover_color = "#018574", text_color = "#fff"
		)
		self.registrar_button.place(x=210, y=240)

		self.informacion = ctk.CTkButton(self, text="", 
			command= lambda: mensaje.showinfo(
				message=(
                "Para crear una cuenta, por favor asegúrate de cumplir con las siguientes condiciones:\n\n"
                "1. El usuario y la contraseña no deben estar vacíos.\n"
                "2. El usuario y la contraseña no deben contener espacios.\n"
                "3. El usuario debe tener al menos 3 caracteres.\n"
                "4. La contraseña debe tener al menos 6 caracteres.\n"
                "5. El nombre de usuario debe ser alfanumérico (solo letras y números).\n\n"
                "# ---------------- NO TE PREOCUPES ----------------\n\n"
                "Si te has equivocado de contraseña o no estás seguro de la contraseña que has ingresado, "
                "el administrador podra cambiar tus credenciales o sino puedes tu crear una nueva cuenta para poder acceder."
            ),
			title = "Condiciones para Crear una Cuenta"
			),
			fg_color = "#fff", font = ("",14, "bold"), image = ctk.CTkImage (
				light_image=Image.open("setup_installer/informacion.png"),
				size=(30, 30)
				),
			width = 30, height = 30, bg_color = "#547c7b"
			)
		self.informacion.place(x = 490, y = 220)

		self.ocultar_mostrar_contra = ctk.CTkButton(self, text="", 
			command= self.mostrar_ocultar_contra ,
			font = ("",14, "bold"), image = ctk.CTkImage (
				light_image=Image.open("setup_installer/ocultar-contrasena.png"),
				size=(30, 30)
				),
			width = 30, height = 30, bg_color = "#41aea9", fg_color = "#FCDC94"
			)
		self.ocultar_mostrar_contra.place(x = 490, y = 170)

		# = --------------- Botones --------------------
		self.next_button = ctk.CTkButton(self, text="Siguiente", command=controller.next_frame,
			fg_color = "#018574", font = ("",14, "bold"), state = "disabled")
		self.next_button.place(x = 10, y = y)

		back_button = ctk.CTkButton(self, text="Atrás", command=controller.previous_frame,
			fg_color = "#ec984a", font = ("",14, "bold"))
		back_button.place(x = 155, y = y)


	def mostrar_ocultar_contra(self):
		if self.contrasenia_entry.cget('show') == '':
			self.contrasenia_entry.configure(show='*')
			self.ocultar_mostrar_contra.configure(image = ctk.CTkImage (
				light_image=Image.open("setup_installer/mostrar-contrasena.png"),
				size=(30, 30)
				),
				fg_color = "#55AD9B"
			)
		else:
			self.contrasenia_entry.configure(show='')
			self.ocultar_mostrar_contra.configure(image = ctk.CTkImage (
				light_image=Image.open("setup_installer/ocultar-contrasena.png"),
				size=(30, 30)
				),
				fg_color = "#FCDC94",
			)

	def start_registrar_administrador(self):
		# Iniciar el proceso de configuración en un hilo separado
		threading.Thread(target=self.registrar_administrador).start()

	def registrar_administrador(self):
		usuario = self.usuario_entry.get().strip()
		contrasenia = self.contrasenia_entry.get().strip()

		if not usuario or not contrasenia:
			mensaje.showerror(message="Necesitas proporcionar credenciales válidas.\nPor favor, ingrese un usuario y una contraseña.", title="Error para registrar")
			self.next_button.configure(state="disabled")
		elif " " in usuario or " " in contrasenia:
			mensaje.showerror(
				message="El usuario y la contraseña no deben contener espacios.", 
				title="Error para registrar"
				)
			self.next_button.configure(state="disabled")
		elif len(usuario) < 3 or len(contrasenia) < 6:
			mensaje.showerror(
				message="El usuario debe tener al menos 3 caracteres y la contraseña al menos 6 caracteres.", 
				title="Error para registrar"
				)
			self.next_button.configure(state="disabled")
		elif not usuario.isalnum():
			mensaje.showerror(message="El nombre de usuario debe ser alfanumérico.", title="Error para registrar")
			self.next_button.configure(state="disabled")
		else:
			usuario_codificado = codificador_descodificador.codificar_base64(usuario)
			contrasenia_codificada = codificador_descodificador.codificar_base64(contrasenia)

			# Lógica para registrar el administrador
			print(f"Registrando usuario: {usuario_codificado}")
			print(f"Contraseña: {contrasenia_codificada}")

			if verificador(usuario_codificado, contrasenia_codificada):
				mensaje.showerror(
					message="Ya existe una cuenta registrada, elige otras credenciales válidas", 
					title = "Error"
					)
			else:
				connector = SQLServerConnector()
				connector.connect()
				query = f"INSERT INTO Usuario (usuario, contrasenia) VALUES ('{usuario_codificado}', '{contrasenia_codificada}')"
				connector.execute_query(query)

				self.next_button.configure(state="normal")
				mensaje.showinfo(message="Cuenta registrada exitosamente", title="Bien hecho señor Administrador")


class FinishPage(tk.Frame):
	def __init__(self, parent, controller):
		super().__init__(parent)
		self.controller = controller


		self.escaneo_server_label = ctk.CTkLabel(self,
			text = "",
			image = ctk.CTkImage (
				light_image=Image.open("setup_installer/instalacion_completada.jpg"),
				size=(600, 296)
				))  
		self.escaneo_server_label.place(x=0, y=0)

		back_button = ctk.CTkButton(self, text="Atrás", command=controller.previous_frame,
			fg_color = "#ec984a", font = ("",14, "bold"))
		back_button.place(x = 155, y = y)

		finish_button = ctk.CTkButton(self, text="Finish", command= sys.exit,
			fg_color = "#028391", font = ("",14, "bold"))
		finish_button.place(x = 10, y = y)


if __name__ == '__main__':
	root = ctk.CTk()
	setupDatabase = Setup(root)
	root.bind("<Escape>", exit)
	root.bind("<F5>", reinicio)
	root.mainloop()


"""

if __name__ == "__main__":
	server_name = 'DESKTOP-E09IF8K'
	database_name = 'controlEmpleados'

"""