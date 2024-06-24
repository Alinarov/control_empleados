import tkinter as tk
from tkinter import ttk
import app
from app import *
import random
from datetime import datetime as dt
from comunicacion import SQLServerConnector
import threading
import os

class Menu_administrador(ctk.CTkToplevel, app.MainApp):
	def __init__(self, parent, *args, **kwargs):
		super().__init__(parent, *args, **kwargs)
		ctk.set_appearance_mode("dark")
		self.parent = parent # Enlazar con la ventana padre (no necesitas self.parent = self)
		self.parent.title("Dashboard v2")
		self.geometry("1200x600+100+50")
		self.after(250,lambda: self.iconbitmap("setup_installer/icono.ico"))  # Asegúrate de que la ruta sea correcta
		self.dataConfig = configuraciones()

		self.color_menu = "#222831"
		self.color_boton = "#50727B"
		self.color_texto_boton = "#EEEEEE"
		self.color_hover_boton = "#254336"

		# Create the PanedWindow
		self.paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL)
		self.paned_window.pack(fill=tk.BOTH, expand=True)

		# Create the left menu frame
		self.menu_frame = ctk.CTkFrame(self.paned_window, bg_color= self.color_menu, width = 300)
		self.paned_window.add(self.menu_frame, minsize=200)

		# Create the main content frame
		self.content_frame = ctk.CTkFrame(self.paned_window, bg_color='#ecf0f1')
		self.paned_window.add(self.content_frame)


		self.nombres_empleados = []  # Lista para almacenar nombres de empleados desde el JSON


		# Populate the menu frame with buttons
		self.create_menu()

		# Populate the content frame with default content
		self.show_dashboard_v1()

	def create_menu(self):
		user_info = ctk.CTkLabel(self.menu_frame, text="github.com/walter8wagner", bg_color= self.color_menu, 
			fg_color=self.color_menu, font=('Helvetica', 22, "bold"), image = ctk.CTkImage(
				light_image=Image.open("fondo_panel.png"),
				size=(300,80)
				), text_color = "#FED9ED"
			)
		user_info.pack(pady=0, fill = "both")

		self.create_menu_button("Inicio", self.show_dashboard_v1, "home.png")
		self.create_menu_button("Historial de cargas. 1", self.show_dashboard_v2, "anotar.png")
		self.create_menu_button("Adminis. de empleados. 2", self.show_dashboard_v3, "admini_empleados.png")
		self.create_menu_button("Registrar nuevo empleado", self.show_dashboard_v6, "historial.png")
		self.create_menu_button("Configuraciones", self.show_dashboard_v5, "configuracion.png")

	def create_menu_button(self, text, command, imagen):
		button = ctk.CTkButton(self.menu_frame, text=text, command=command, bg_color= self.color_menu, 
			fg_color = self.color_boton, hover_color = self.color_hover_boton, font=('Arial', 20, "bold"), 
			text_color = self.color_texto_boton, image = ctk.CTkImage(
				light_image=Image.open(imagen),
				size=(20,20)
				), compound = "left", anchor = "w", height = 40
			)
		button.pack(fill=tk.X, padx=10, pady=5)

	def clear_content(self):
		for widget in self.content_frame.winfo_children():
			widget.destroy()


	def leer_desde_json(self):
		try:
			with open('temp.json', 'r', encoding='utf-8') as archivo:
				datos = json.load(archivo)
				self.nombres_empleados = datos.get('datos_temporales', [])  # Obtener lista de nombres de empleados
			return datos
		except FileNotFoundError:
			print(f"El archivo 'temp.json' no existe. Creando archivo nuevo...")
			with open('temp.json', 'w', encoding='utf-8') as archivo:
				json.dump({}, archivo)  # Crear archivo JSON vacío
			return {}
		except json.JSONDecodeError as e:
			print(f"Error al decodificar JSON en 'temp.json': {e}")
			return None
		except Exception as e:
			print(f"Error al leer desde 'temp.json': {e}")
			return None

	def escribir_en_json(self, datos):
		# Crear el diccionario con la estructura deseada
		data = {"datos_temporales": datos}
		try:
			if os.path.exists('temp.json'):
				os.remove('temp.json')  # Eliminar el archivo existente si está presente
				print("Creando un nuevo archivo 'temp.json'...")


			with open('temp.json', 'w', encoding='utf-8') as archivo:
				json.dump(data, archivo, indent=4, ensure_ascii=False)
			print(f"Datos escritos correctamente en 'temp.json'.")
		except Exception as e:
			print(f"Error al escribir en 'temp.json': {e}")
	# ############################################################################################################
	# 
	# Pagina de inicio
	# 
	def show_dashboard_v1(self):
		self.clear_content()
		self.parent.title("Aministrador de la empresa")

		self.fondo_menu_label = ctk.CTkLabel(
			self.content_frame,
			image = ctk.CTkImage(
				light_image=Image.open("fondo5.jpg"),
				size=(1245, 750)
			),  
			text="Panel de Control de Cargas: \nGestión de Actividades\n\n\n\n\n\n\n\n",
			font=("", 40, "bold"),
			text_color="#CABFAB"
		)
		self.fondo_menu_label.place(x=0, y=0, relwidth=1, relheight=1)

		self.mensaje = ctk.CTkLabel(
			self.fondo_menu_label,
			text="¡Supervisa y gestiona las cargas de trabajo de tus empleados con facilidad! \nMantén un control eficiente y promueve un ambiente laboral saludable. \n(C) 2005 Alina Krasnaya https://alinakrasnaya.itch.io/",
			fg_color="#DFD8C8", text_color="#52575D", bg_color="#212A31", justify=tk.CENTER,
			font=("", 19), cursor = "hand2", corner_radius = 16
		)
		self.mensaje.place(relx=0.5, rely= 0.38, anchor = "center")
		self.mensaje.bind("<Button-1>", lambda e: webbrowser.open_new("https://alinakrasnaya.itch.io/"))

		imagen1 = Image.open("admini_empleados.png")
		imagen1 = imagen1.resize((100, 100))
		imagen1 = ImageTk.PhotoImage(imagen1)

		imagen2 = Image.open("configuracion.png")
		imagen2 = imagen2.resize((100, 100))
		imagen2 = ImageTk.PhotoImage(imagen2)

		imagen3 = Image.open("historial.png")  # Reemplaza "tercer_imagen.jpg" con el nombre de tu tercera imagen
		imagen3 = imagen3.resize((100, 100))
		imagen3 = ImageTk.PhotoImage(imagen3)

		self.boton1 = ctk.CTkButton(self.content_frame, text="Configuraciones", fg_color="#fff", compound="top", 
									image=imagen2, text_color="#111", font=("", 16, "bold"), bg_color="#58A399", command = self.show_dashboard_v5)
		self.boton1.place(relx=0.19, rely=0.7, anchor='center')

		self.boton2 = ctk.CTkButton(self.content_frame, text="Administrar empleados", fg_color="#fff", compound="top", 
									image=imagen1, text_color="#111", font=("", 16, "bold"), bg_color="#58A399", command = self.show_dashboard_v3)
		self.boton2.place(relx=0.47, rely=0.7, anchor='center')

		self.boton3 = ctk.CTkButton(self.content_frame, text="Historial de cargas", fg_color="#fff", compound="top", 
									image=imagen3, text_color="#111", font=("", 16, "bold"), bg_color="#948979", command = self.show_dashboard_v2)
		self.boton3.place(relx=0.76, rely=0.7, anchor='center')

	################################################################################################### 	
	#
	# Pagina donde se seleccionara las cargas que se hicieron
	# 

	def show_dashboard_v2(self):
		self.clear_content()

		self.registros_fechas_completas = []  # Lista de registros obtenidos de la base de datos
		self.nombres_fechas = []  # Lista para almacenar nombres de fechas

		self.pagina_actual_fecha = 0
		self.opciones_registros_fecha = ['10', '15', '20', '25', '30']  # Opciones de cantidad de registros por página
		self.registros_por_pagina = tk.IntVar(value=int(self.opciones_registros_fecha[0]))  # Valor inicial por defecto

		# Frames principales
		self.framePanelIzquierdo = ctk.CTkFrame(self.content_frame,
												fg_color=self.dataConfig["tema_2"]["colorbg"])
		self.framePanelIzquierdo.pack(side="right", fill="both")

		self.framePanerRegistrosCargas = ctk.CTkFrame(self.content_frame,
													  fg_color=self.dataConfig["tema_3"]["colorbg"])
		self.framePanerRegistrosCargas.pack(fill="both", expand=True)

		# Contenido del panel izquierdo
		self.labelTituloSeleccionarFecha = ctk.CTkLabel(self.framePanelIzquierdo, text="Descripcion de la pagina: \n Cargas hechas",
														text_color=self.dataConfig["tema_2"]["colordes"],
														font=("Cascadia Code", 16, "bold"))
		self.labelTituloSeleccionarFecha.pack(padx=10, pady=10)


		kalendario = Kalendario(self.framePanelIzquierdo)
		kalendario.pack()

		ctk.CTkLabel(self.framePanelIzquierdo, text = (
			'Funcionalidades:\n'+
			'1. Selección de Fecha: Usa \nel calendario\n'+
			'2. Visualización: La lista \nmuestra registros \ndel día seleccionado.\n'+
			'3. Navegación:\n'+
			'   a. Inicio: Página principal.\n'+
			'   b. Historial: Registros \nanteriores.\n'+
			'   c. Búsqueda: Encuentra \nregistros.\n'+
			'4. Uso:\n'+
			'   a. Fecha: Clic en una fecha.\n'+
			'   b. Revisa: Se crea un PDF.\n'),
			text_color="#113946",
			font=("Cascadia Code", 13, "bold"),

			anchor='w',  # Alinea el texto a la izquierda
			justify='left'  # Justifica el texto a la izquierda
			).pack(padx=10, pady=10)

		# Contenido del panel de simulación de registros
		ctk.CTkLabel(self.framePanerRegistrosCargas, text="Registros de las cargas hechas en la fecha",
					 text_color=self.dataConfig["tema_2"]["colordes"], font=("", 20, "bold")).pack(fill="x", side="top")

		self.frameBuscar = ctk.CTkFrame(self.framePanerRegistrosCargas)
		self.frameBuscar.pack(fill="x")

		# Campo de búsqueda
		self.name_var_fecha = tk.StringVar()
		self.name_var_fecha.trace_add('write', self.debounce_fecha(self.actualizar_resultados_fechas, 100))

		ctk.CTkEntry(self.frameBuscar, validate='key', placeholder_text="Buscar fecha (dd-mm-yyyy)",
					 placeholder_text_color=self.dataConfig["tema_2"]["colordes"],
					 fg_color=self.dataConfig["tema_3"]["colorcp"], font=("", 16),
					 text_color="#01204E", textvariable=self.name_var_fecha).pack(padx=10, fill="x", side="left", expand=True)

		# Botón de búsqueda con imagen
		ctk.CTkButton(self.frameBuscar, text="Buscar", command=self.actualizar_resultados_fechas,
					  image=ctk.CTkImage(light_image=Image.open("lupa.png"), size=(20, 20))).pack(side="right", pady=3, padx=10)

		# Lista de fechas
		self.lb_fechas = CTkListbox(self.framePanerRegistrosCargas, 
									text_color="#F1F8E8", hover_color="#497174", fg_color="#C8CFA0", command = self.realizar_reporte,
									border_color="#78ABA8", button_color="#78ABA8", font=("", 16, "bold"))
		self.lb_fechas.pack(padx=0, pady=10, expand=True, fill="both")
		self.lb_fechas.configure(font=("", 16, "bold"), text_color="#102C57")

		# Opciones de paginación
		self.frm_opciones_fecha = ctk.CTkFrame(self.framePanerRegistrosCargas,fg_color="#C8CFA0", 
			border_color="#78ABA8", border_width=3)
		self.frm_opciones_fecha.pack(padx=0, pady=0, fill="x")

		self.opcion_seleccionada = tk.StringVar(self.framePanerRegistrosCargas)
		self.opcion_seleccionada.set(self.opciones_registros_fecha[1])  # Valor inicial por defecto
		ctk.CTkOptionMenu(self.frm_opciones_fecha, variable=self.opcion_seleccionada, 
						  values=self.opciones_registros_fecha, command=self.cambiar_registros_por_pagina_fecha).pack(padx=10, pady=5, side="left")
		
		ctk.CTkButton(self.frm_opciones_fecha, text="Anterior", text_color = "#01204E", fg_color = "#028391", font = ("", 16, "bold"),
			command=self.pagina_anterior_fecha).pack(padx=10, pady=5, side="left")
		ctk.CTkButton(self.frm_opciones_fecha, text="Siguiente", text_color = "#01204E", fg_color = "#028391",font = ("", 16, "bold"),
			command=self.pagina_siguiente_fecha).pack(padx=10, pady=5, side="left")
		ctk.CTkButton(self.frm_opciones_fecha, text="Siguiente", text_color = "#01204E", fg_color = "#028391",font = ("", 16, "bold"),
			command=self.pagina_siguiente_fecha).pack(padx=10, pady=5, side="left")
		# Iniciar hilo para obtener fechas
		hilo = threading.Thread(target=self.obtener_fechas_db)
		hilo.start()

	def realizar_reporte(self, fecha_seleccionada):
		# Obtener los primeros 10 dígitos de fecha_seleccionada
		fecha_formateada = fecha_seleccionada[:10]

		con = SQLServerConnector()
		con.connect()

		respuesta_sql = con.execute_query(f"""
		SELECT e.nombre_empleado, e.apellidos_empleado, e.dni_empleado, c.peso_carga, c.id_fecha_carga, c.hora_entrega
		FROM empleado em
		INNER JOIN registro_empleados e ON em.id_registro_personal = e.id_registro_personal
		INNER JOIN cargas c ON em.id_empleado = c.id_empleado
		INNER JOIN fecha_carga fc ON c.id_fecha_carga = fc.id_fecha_carga
		WHERE c.id_fecha_carga = '{fecha_formateada}'
		ORDER BY e.nombre_empleado;
			""")
		print(respuesta_sql)

		data = conversion_a_json_respuesta(respuesta_sql)
		archivo = f"reporte-{fecha_formateada}.pdf"
		ruta_escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
		archivo_salida = os.path.join(ruta_escritorio, archivo)


		crear_pdf_desde_json(data, archivo_salida)


	def clear_content(self):
		for widget in self.content_frame.winfo_children():
			widget.destroy()

	def cargar_fechas(self):
		inicio = self.pagina_actual_fecha * self.registros_por_pagina.get()
		fin = inicio + self.registros_por_pagina.get()
		fechas_pagina = self.nombres_fechas[inicio:fin]
		
		self.lb_fechas.delete(0, tk.END)
		for fecha in fechas_pagina:
			self.lb_fechas.insert(tk.END, fecha)

	def pagina_anterior_fecha(self):
		if self.pagina_actual_fecha > 0:
			self.pagina_actual_fecha -= 1
			self.cargar_fechas()
		else:
			mb.showinfo("Información", "Ya estás en la primera página")

	def pagina_siguiente_fecha(self):
		if (self.pagina_actual_fecha + 1) * self.registros_por_pagina.get() < len(self.nombres_fechas):
			self.pagina_actual_fecha += 1
			self.cargar_fechas()
		else:
			mb.showinfo("Información", "Ya estás en la última página")

	def cambiar_registros_por_pagina_fecha(self, event):
		self.registros_por_pagina.set(int(self.opcion_seleccionada.get()))
		self.pagina_actual_fecha = 0  # Reiniciar a la primera página al cambiar el número de registros por página
		self.cargar_fechas()

	def buscar_fechas(self, patron_busqueda):
		resultados = []

		for fecha in self.nombres_fechas:
			if patron_busqueda.lower() in fecha.lower():
				resultados.append(fecha)

		return resultados


	def actualizar_resultados_fechas(self, *args):
		patron_busqueda = self.name_var_fecha.get().strip()  # Obtener el patrón de búsqueda y quitar espacios en blanco
		resultados = self.buscar_fechas(patron_busqueda)

		self.lb_fechas.delete(0, tk.END)  # Limpiar la lista

		if patron_busqueda:
			# Caso 1: Cuando hay un patrón de búsqueda
			try:
				for resultado in resultados:
					self.lb_fechas.insert(tk.END, resultado)
			except Exception as e:
				self.actualizar_resultados_fechas()
		else:
			# Caso 2: Cuando no hay patrón de búsqueda (mostrar todos los registros)
			inicio = self.pagina_actual_fecha * self.registros_por_pagina.get()
			fin = inicio + self.registros_por_pagina.get()
			fechas_pagina = self.nombres_fechas[inicio:fin]

			try:
				for fecha in fechas_pagina:
					self.lb_fechas.insert(tk.END, fecha)
			except:
				self.actualizar_resultados_fechas()


	def obtener_fechas_db(self):
		try:
			self.loadingTK = ctk.CTk()
			self.cosa_carga = IndicadorCarga(self.loadingTK)

			# Iniciar hilo para obtener fechas desde la base de datos
			hilo_fechas_db = threading.Thread(target=self.get_fechas_db)
			hilo_fechas_db.start()

			self.loadingTK.mainloop()

		except Exception as e:
			mb.showinfo(message=f"Error al procesar datos de fechas: {e}", title="Error")

	def get_fechas_db(self):
		try:
			# Conexión y consulta a la base de datos
			conector = SQLServerConnector()
			conector.connect()
			lista_fechas_cargas = conector.execute_query("SELECT * FROM fecha_carga ORDER BY id_fecha_carga DESC;")

			# Procesamiento de resultados
			for fecha_carga, hora_inicio, hora_corte in lista_fechas_cargas:
				nombre_fecha = f"{fecha_carga} {hora_inicio} {hora_corte}"
				self.nombres_fechas.append(nombre_fecha)

			# Escritura en archivo JSON
			self.escribir_en_json(self.nombres_fechas)

			# Cargar las fechas en el ListBox
			self.cargar_fechas()

		except Exception as e:
			mb.showinfo(message=f"Error al procesar datos de fechas: {e}", title="Error")
			self.show_dashboard_v2()
		self.loadingTK.after(0, self.cosa_carga.stop_loading)
		self.content_frame.after(0, self.cargar_fechas)


	def debounce_fecha(self, func, wait):
		"""Debounce function to prevent multiple rapid calls"""
		def debounced(*args, **kwargs):
			def call_it():
				func(*args, **kwargs)
				self._last_call = None  # Reiniciar _last_call después de ejecutar func

			if hasattr(self, "_last_call") and self._last_call is not None:
				try:
					self.parent.after_cancel(self._last_call)
				except ValueError:
					pass  # Ignorar el error si el identificador no es válido

			self._last_call = self.parent.after(wait, call_it)

		return debounced


	# #############################################################################################################################
	# 
	# Pagina para mostrar la lista de los empleados
	# ##############################################################################################################################

	def show_dashboard_v3(self, root=None):
		self.clear_content()
		self.parent.title("Corte del dia")
		ctk.set_appearance_mode("dark")  # Tema principal

		self.clear_content()

		self.empleados = []  # Lista de empleados obtenidos de la base de datos
		self.nombres_empleados = []  # Lista para almacenar nombres de empleados

		self.pagina_actual_empleado = 0
		self.opciones_registros_empleado = ['10', '15', '20', '25', '30']  # Opciones de cantidad de registros por página
		self.registros_por_pagina = tk.IntVar(value=int(self.opciones_registros_empleado[0]))  # Valor inicial por defecto

		# Frames principales
		self.framePanelIzquierdo = ctk.CTkFrame(self.content_frame,
												fg_color=self.dataConfig["tema_2"]["colorbg"])
		self.framePanelIzquierdo.pack(side="right", fill="both")

		self.framePanelRegistrosEmpleados = ctk.CTkFrame(self.content_frame,
														 fg_color=self.dataConfig["tema_3"]["colorbg"])
		self.framePanelRegistrosEmpleados.pack(fill="both", expand=True)

		# Contenido del panel izquierdo
		self.labelTituloSeleccionarEmpleado = ctk.CTkLabel(self.framePanelIzquierdo, text="Detalles de los Empleados",
														   text_color=self.dataConfig["tema_2"]["colordes"],
														   font=("Cascadia Code", 16, "bold"))
		self.labelTituloSeleccionarEmpleado.pack(padx=10, pady=10)
		ctk.CTkLabel (
			self.framePanelIzquierdo,
			text = "",
			image = ctk.CTkImage(
				light_image=Image.open("datos-laborales.jpg"),
				size=(300,210)
				)
			).pack()
		ctk.CTkLabel(
			self.framePanelIzquierdo,
			text=(
				'Funcionalidades:\n'
				'1. Selección de Empleado: Usa\n la lista para elegir un empleado.\n'
				'2. Visualización: Muestra los\n registros del empleado\n 	seleccionado.\n'
				'3. Navegación:\n'
				'   a. Buscar: Encuentra empleados.\n'
				'   b. Anterior/Siguiente: Cambia\n 	de página.'
				'4. Uso:\n'
				'   a. Selecciona un Empleado:\n 	Haz clic en un nombre de \n 	la lista.\n'
				'   b. Revisa los Datos personales:\n 	Detalles del empleado \n 	aparecerán.\n'
			),
			text_color="#113946",
			font=("Cascadia Code", 13, "bold"),
			anchor='w',  # Alinea el texto a la izquierda
			justify='left'  # Justifica el texto a la izquierda
		).pack(pady=5, padx=10, fill='both', expand=True)

		# Contenido del panel de registros de empleados
		ctk.CTkLabel(self.framePanelRegistrosEmpleados, text="Registros de empleados",
					 text_color=self.dataConfig["tema_2"]["colordes"], font=("", 20, "bold")).pack(fill="x", side="top")

		self.frameBuscarEmpleado = ctk.CTkFrame(self.framePanelRegistrosEmpleados)
		self.frameBuscarEmpleado.pack(fill="x")

		# Campo de búsqueda de empleados
		self.name_var_empleado = tk.StringVar()
		self.name_var_empleado.trace_add('write', self.debounce(self.actualizar_resultados_empleados, 100))

		ctk.CTkEntry(self.frameBuscarEmpleado, validate='key', placeholder_text="Buscar empleado por nombre",
					 placeholder_text_color=self.dataConfig["tema_2"]["colordes"],
					 fg_color=self.dataConfig["tema_3"]["colorcp"], font=("", 16),
					 text_color="#01204E", textvariable=self.name_var_empleado).pack(padx=10, fill="x", side="left", expand=True)

		# Botón de búsqueda con imagen
		ctk.CTkButton(self.frameBuscarEmpleado, text="Buscar", command=self.actualizar_resultados_empleados,
					  image=ctk.CTkImage(light_image=Image.open("lupa.png"), size=(20, 20))).pack(side="right", pady=3, padx=10)

		# Lista de empleados
		self.lb_empleados = CTkListbox(self.framePanelRegistrosEmpleados, 
									 text_color="#F1F8E8", hover_color="#497174", fg_color="#C8CFA0", border_color="#78ABA8", 
									 button_color="#78ABA8", command=self.imprimir_seleccion, font=("", 16, "bold"))
		self.lb_empleados.pack(padx=0, pady=10, expand=True, fill="both")
		self.lb_empleados.configure(font=("", 16, "bold"), text_color="#102C57")   
		
		# Opciones de paginación para empleados
		self.frm_opciones_empleado = ctk.CTkFrame(self.framePanelRegistrosEmpleados,fg_color="#C8CFA0", 
			border_color="#78ABA8", border_width=3)
		self.frm_opciones_empleado.pack(padx=0, pady=0, fill="x")

		self.opcion_seleccionada_empleado = tk.StringVar(self.framePanelRegistrosEmpleados)
		self.opcion_seleccionada_empleado.set(self.opciones_registros_empleado[1])  # Valor inicial por defecto
		ctk.CTkOptionMenu(self.frm_opciones_empleado, variable=self.opcion_seleccionada_empleado, 
						  values=self.opciones_registros_empleado, command=self.cambiar_registros_por_pagina_empleado).pack(padx=10, pady=5, side="left")
		
		ctk.CTkButton(self.frm_opciones_empleado, text="Anterior",text_color = "#01204E", fg_color = "#028391",font = ("", 16, "bold"),
		 command=self.pagina_anterior_empleado).pack(padx=10, pady=5, side="left")
		ctk.CTkButton(self.frm_opciones_empleado, text="Siguiente", text_color = "#01204E", fg_color = "#028391",font = ("", 16, "bold"),
			command=self.pagina_siguiente_empleado).pack(padx=10, pady=5, side="left")

		# Iniciar hilo para obtener empleados
		hilo = threading.Thread(target=self.obtener_empleados_db)
		hilo.start()

	def clear_content(self):
		for widget in self.content_frame.winfo_children():
			widget.destroy()

	def cargar_empleados(self):
		inicio = self.pagina_actual_empleado * self.registros_por_pagina.get()
		fin = inicio + self.registros_por_pagina.get()
		empleados_pagina = self.nombres_empleados[inicio:fin]
		
		self.lb_empleados.delete(0, tk.END)
		for empleado in empleados_pagina:
			self.lb_empleados.insert(tk.END, empleado)

	def pagina_anterior_empleado(self):
		if self.pagina_actual_empleado > 0:
			self.pagina_actual_empleado -= 1
			self.cargar_empleados()
		else:
			mb.showinfo("Información", "Ya estás en la primera página")

	def pagina_siguiente_empleado(self):
		if (self.pagina_actual_empleado + 1) * self.registros_por_pagina.get() < len(self.nombres_empleados):
			self.pagina_actual_empleado += 1
			self.cargar_empleados()
		else:
			mb.showinfo("Información", "Ya estás en la última página")

	def cambiar_registros_por_pagina_empleado(self, event):
		self.registros_por_pagina.set(int(self.opcion_seleccionada_empleado.get()))
		self.pagina_actual_empleado = 0  # Reiniciar a la primera página al cambiar el número de registros por página
		self.cargar_empleados()

	def buscar_empleados(self, patron_busqueda):
		resultados = []

		for empleado in self.nombres_empleados:
			if patron_busqueda.lower() in empleado.lower():
				resultados.append(empleado)

		return resultados

	def actualizar_resultados_empleados(self, *args):
		patron_busqueda = self.name_var_empleado.get().strip()  # Obtener el patrón de búsqueda y quitar espacios en blanco
		resultados = self.buscar_empleados(patron_busqueda)

		self.lb_empleados.delete(0, tk.END)  # Limpiar la lista

		if patron_busqueda:
			# Caso 1: Cuando hay un patrón de búsqueda
			for resultado in resultados:
				self.lb_empleados.insert(tk.END, resultado)
		else:
			# Caso 2: Cuando no hay patrón de búsqueda (mostrar todos los registros)
			inicio = self.pagina_actual_empleado * self.registros_por_pagina.get()
			fin = inicio + self.registros_por_pagina.get()
			empleados_pagina = self.nombres_empleados[inicio:fin]

			try:
				for empleado in empleados_pagina:
					self.lb_empleados.insert(tk.END, empleado)
			except:
				self.actualizar_resultados_empleados()

	def obtener_empleados_db(self):
		# Iniciar la cosa de carga
		self.loadingTK = ctk.CTk()
		self.cosa_carga = IndicadorCarga(self.loadingTK)

		# Realizar la operación de base de datos en un hilo separado
		hilo_nombres_db = threading.Thread(target=self.get_nombres_db)
		hilo_nombres_db.start()

		# Iniciar el bucle principal en el hilo principal
		self.loadingTK.mainloop()

	def get_nombres_db(self, comando=None):
		nombres_completos = []
		self.conector = SQLServerConnector()
		
		try:
			self.conector.connect()

			# Realizar la consulta a la base de datos
			if comando is None: 
				lista_db_empleados = self.conector.execute_query("""
					SELECT nombre_empleado, apellidos_empleado, dni_empleado
					FROM registro_empleados 
					ORDER BY id_registro_personal
				""")
			else:
				lista_db_empleados = self.conector.execute_query(comando)
				
			# Formatear nombres completos
			for nombre, apellido, dni_empleado in lista_db_empleados:
				nombre_completo = f"{nombre} {apellido} : {dni_empleado}"
				nombres_completos.append(nombre_completo)

			# Informar que la operación fue exitosa
			print("Nombres de empleados obtenidos correctamente")
			self.nombres_empleados = nombres_completos  # Actualizar la lista de nombres
			self.escribir_en_json(nombres_completos)

		except Exception as e:
			mb.showinfo(message=f"Error al procesar datos de empleados: {e}", title="Error")

		# Detener el indicador de carga y cerrar la ventana de carga
		self.loadingTK.after(0, self.cosa_carga.stop_loading)

		# Actualizar la lista de nombres en la interfaz principal
		self.framePanelRegistrosEmpleados.after(0, self.cargar_empleados)


	def debounce(self, func, wait):
		"""Debounce function to prevent multiple rapid calls"""
		def debounced(*args, **kwargs):
			def call_it():
				func(*args, **kwargs)
				self._last_call = None  # Reiniciar _last_call después de ejecutar func

			if hasattr(self, "_last_call") and self._last_call is not None:
				try:
					self.parent.after_cancel(self._last_call)
				except ValueError:
					pass  # Ignorar el error si el identificador no es válido

			self._last_call = self.parent.after(wait, call_it)

		return debounced


	def imprimir_seleccion(self, opcion_seleccionada_lista_box):
		print(opcion_seleccionada_lista_box)
		self.show_dashboard_v4(opcion_seleccionada_lista_box)

	# ###############################################################################################################################
	# 
	# Pagina para ver la informacion de los empleados 
	#
	def show_dashboard_v4(self, args = ""):
		self.clear_content()
		ctk.set_appearance_mode("dark") # tema principal

		if args != "":	
			try: 
				ultimo_espacio = args.rfind(" ")
				dni_empleado = args[ultimo_espacio + 1:]
				empleado = self.obtener_datos(dni_empleado)

				print("\n\n\n", empleado)
			except:
				pass

		# Crear el frame del formulario de empleados
		self.frameFormulario = ctk.CTkFrame(self.content_frame, fg_color="#717469", bg_color="#717469")
		self.frameFormulario.pack(expand=True, fill="both")

		ctk.CTkLabel(self.frameFormulario, text = "Formulario de datos de empleados", 
			font = ("Helvetica", 25, "bold"), text_color = "#113946", fg_color = "#BCA37F", corner_radius = 4

		).pack(pady = 20)

		# Frame del formulario de datos personales
		self.frameDatosPersonales = ctk.CTkFrame(self.frameFormulario, fg_color="#538392")
		self.frameDatosPersonales.pack(expand=True, fill="both", padx=20, pady=20)


		self.labelFormulario = ctk.CTkLabel(self.frameDatosPersonales, text="", image=ctk.CTkImage(
			light_image=Image.open("fondo4.jpg"),
			size=(1245, 750)
		))
		self.labelFormulario.place(x=-50, y=-50)

		# Configurar columnas
		for i in range(4):
			self.frameDatosPersonales.columnconfigure(i, weight=1)

		# Columna 1
		self.labelNombre = ctk.CTkLabel(self.frameDatosPersonales, text="Nombres (Obli.)")
		self.labelNombre.grid(row=0, column=0, padx=3, pady=10, sticky="w")

		self.textNombre = ctk.CTkEntry(self.frameDatosPersonales, placeholder_text="Ingresar Nombres", font=("", 15, "bold"), bg_color ="#538392")
		self.textNombre.grid(row=0, column=1, padx=3, pady=3, sticky="ew")

		self.labelDni = ctk.CTkLabel(self.frameDatosPersonales, text="DNI (Obli.)")
		self.labelDni.grid(row=1, column=0, padx=3, pady=10, sticky="w")

		vcmd = (self.frameDatosPersonales.register(enter_only_digits), '%P', '%d')
		self.textDni = ctk.CTkEntry(self.frameDatosPersonales, font=("", 15, "bold"), validate='key', validatecommand=vcmd)
		self.textDni.grid(row=1, column=1, padx=3, pady=3, sticky="ew")

		self.labelFechaNacimiento = ctk.CTkLabel(self.frameDatosPersonales, text="Fecha de nacimiento (Obli.)")
		self.labelFechaNacimiento.grid(row=2, column=0, padx=3, pady=10, sticky="w")

		self.textFechaNacimiento = DateEntry(self.frameDatosPersonales, font=("", 11, "bold"), bg_color ="#538392")
		self.textFechaNacimiento.grid(row=2, column=1, padx=3, pady=10, sticky="ew")

		self.labelSexo = ctk.CTkLabel(self.frameDatosPersonales, text="Sexo (Obli.)")
		self.labelSexo.grid(row=3, column=0, padx=3, pady=10, sticky="w")

		self.radio_sexo = tk.IntVar(value=0)
		self.radiobutton_hombre = ctk.CTkRadioButton(self.frameDatosPersonales, text="Hombre", variable=self.radio_sexo, text_color="#005C78", font=("", 14, "bold"), value=1, bg_color ="#538392")
		self.radiobutton_hombre.grid(row=3, column=1, padx=0, pady=10, sticky="w")

		self.radiobutton_mujer = ctk.CTkRadioButton(self.frameDatosPersonales, text="Mujer", variable=self.radio_sexo, text_color="#005C78", font=("", 14, "bold"), value=2, bg_color ="#538392")
		self.radiobutton_mujer.grid(row=3, column=1, padx=0, pady=10, sticky="e")

		# Columna 2
		self.labelApellidos = ctk.CTkLabel(self.frameDatosPersonales, text="Apellidos (Obli.)")
		self.labelApellidos.grid(row=0, column=2, padx=3, pady=10, sticky="w")

		self.textApellido = ctk.CTkEntry(self.frameDatosPersonales, placeholder_text="Ingresar Apellidos",
		 bg_color ="#538392", font=("", 15, "bold")
		 )
		self.textApellido.grid(row=0, column=3, padx=3, pady=10, sticky="ew")

		self.labelTelefono1 = ctk.CTkLabel(self.frameDatosPersonales, text="Teléfono 1 (Obli.)")
		self.labelTelefono1.grid(row=1, column=2, padx=3, pady=10, sticky="w")

		self.textTelefono1 = ctk.CTkEntry(self.frameDatosPersonales, validate='key', validatecommand=vcmd, placeholder_text="Ingresar Teléfono 1", font=("", 15, "bold"), bg_color ="#538392")
		self.textTelefono1.grid(row=1, column=3, padx=3, pady=10, sticky="ew")




		self.label_estado_empleado = ctk.CTkLabel(self.frameDatosPersonales, text="Estado")
		self.label_estado_empleado.grid(row=2, column=2, padx=3, pady=10, sticky="w")

		self.estado_empleado_option_menu = ['activo', 'despedido']
		self.opcion_seleccionada = tk.StringVar(self.frameDatosPersonales)
		self.opcion_seleccionada.set(self.estado_empleado_option_menu[0])  # Se corrige aquí el valor inicial

		self.option_menu = ctk.CTkOptionMenu(self.frameDatosPersonales, variable=self.opcion_seleccionada,
											 values=self.estado_empleado_option_menu, bg_color ="#538392")
		self.option_menu.grid(row=2, column=3, padx=3, pady=10, sticky="ew")



		self.labelFechaContrato = ctk.CTkLabel(self.frameDatosPersonales, text="Fecha de contrato (Opci.)")
		self.labelFechaContrato.grid(row=3, column=2, padx=3, pady=10, sticky="w")

		self.textFechaContrato = DateEntry(self.frameDatosPersonales, font=("", 11, "bold"), bg_color ="#538392")
		self.textFechaContrato.grid(row=3, column=3, padx=3, pady=10, sticky="ew")

		# Columna 3 (Formulario opcional)
		self.labelEmail = ctk.CTkLabel(self.frameDatosPersonales, text="Email (Campo Opcional)", anchor="w")
		self.labelEmail.grid(row=4, column=0, padx=3, pady=10, sticky="w")

		self.textEmail = ctk.CTkEntry(self.frameDatosPersonales, placeholder_text="Ingresar el correo electrónico (Opci.)", fg_color="white", text_color="black", font=("", 15, "bold"), bg_color ="#538392")
		self.textEmail.grid(row=4, column=1, padx=3, pady=10, columnspan=3, sticky="ew")

		self.labelDireccion = ctk.CTkLabel(self.frameDatosPersonales, text="Dirección (Campo Opcional)", anchor="w")
		self.labelDireccion.grid(row=5, column=0, padx=3, pady=10, sticky="w")

		self.textDireccion = ctk.CTkEntry(self.frameDatosPersonales, placeholder_text="Ingresar dirección domiciliaria (Opci.)", fg_color="white", text_color="black", font=("", 15, "bold"), bg_color ="#538392")
		self.textDireccion.grid(row=5, column=1, padx=3, pady=10, columnspan=3, sticky="ew")


		# ---------------------------------------------------------------------------------------------------------------------
		# Crear el frame de opciones en la parte inferior
		self.frameOpciones = ctk.CTkFrame(self.content_frame, fg_color="#DFD0B8")
		self.frameOpciones.pack(side="bottom", fill="x")

		# Configurar columnas del frame de opciones
		self.frameOpciones.columnconfigure(0, weight=1)
		self.frameOpciones.columnconfigure(1, weight=1)
		self.frameOpciones.columnconfigure(2, weight=1)

		# Foto del empleado en la parte izquierda
		self.fotoEmpleado = ctk.CTkLabel(
			self.frameOpciones, 
			text="",
			image=ctk.CTkImage(
				light_image=Image.open("nuevoEmpleado.png"),
				size=(180, 180)
			)
		)
		self.fotoEmpleado.grid(column=0, row=0, pady=10, padx=10, rowspan=4, sticky="w")

		# Label con funcionalidades y detalles
		ctk.CTkLabel(
			self.frameOpciones,
			text=(
				'Funcionalidades:\n'
				'    1. Registro de Empleados y Visualización de \n       Información.\n'
				'    2. Botones cambian según la operación (registro o \n       visualización).\n'
				'    3. Entradas Obligatorias: Nombre completo, fecha de \n       nacimiento y puesto.\n'
				'    4. Casillas Opcionales: Teléfono, dirección, correo \n       electrónico.\n'
				'Importante: Completa las entradas obligatorias antes \n       de registrar.\n'
			),
			text_color="#113946",
			font=("Cascadia Code", 13, "bold"),
			anchor='w',  # Alinea el texto a la izquierda
			justify='left'  # Justifica el texto a la izquierda
		).grid(column=1, row=0, rowspan=4, pady=10, padx=10, sticky="nsew")  # Ajusta el rowspan y el espaciado

		# Botones CRUD en la parte derecha
		self.botonRegistrar = ctk.CTkButton(self.frameOpciones, text="Registrar Empleado", command=self.crear_empleado)
		self.botonEditarDatos = ctk.CTkButton(self.frameOpciones, text="Editar datos", command=self.editar)

		self.botonRegistrar.configure(font=("", 19))
		self.botonEditarDatos.configure(font=("", 19))

		# Posicionamiento de los botones
		self.botonRegistrar.grid(column=2, row=0, pady=20, padx=10, sticky="ew")
		self.botonEditarDatos.grid(column=2, row=1, pady=20, padx=10, sticky="ew")


		# Configurar las entradas de texto
		self.textBox = (
			self.textNombre, self.textDni, self.textApellido, self.textTelefono1, 
			self.textEmail, self.textDireccion
		)

		# Configurar los colores de las etiquetas
		self.labeles = (
			self.labelNombre, self.labelDni, self.labelFechaNacimiento, self.labelSexo,
			self.labelApellidos, self.labelTelefono1, self.label_estado_empleado,
			self.labelFechaContrato, self.labelEmail, self.labelDireccion
		)

		for label in self.labeles:
			label.configure(text_color=self.dataConfig["tema_2"]["colordes"], bg_color ="#538392",
				fg_color=self.dataConfig["tema_3"]["colorcp"], font = ("", 14, "bold"), corner_radius = 3)
			
		for textBox in self.textBox:
			textBox.configure(fg_color="white", bg_color ="#538392", text_color="black")

		try:
			# Insertar datos en los campos correspondientes
			self.textNombre.insert(0, empleado[0][1])  # Nombres
			self.textApellido.insert(0, empleado[0][2])  # Apellidos
			self.textDni.insert(0, empleado[0][3])  # DNI
			self.textFechaNacimiento.set_date(empleado[0][6])  # Fecha de nacimiento
			self.radio_sexo.set(1 if empleado[0][4] == "M" else 2)  # Sexo
			self.textTelefono1.insert(0, empleado[0][5])  # Teléfono 1
			self.textFechaContrato.set_date(empleado[0][9])  # Fecha de contrato (Opcional)
			self.textEmail.insert(0, empleado[0][7])  # Email (Opcional)
			self.textDireccion.insert(0, empleado[0][8])  # Dirección (Opcional)
			print("Estado: ", empleado[0][10])
			self.opcion_seleccionada.set(empleado[0][10])


		except Exception as e:
			print(e)
			pass #mb.showinfo(message=e, title="Error")

		if args != "":
			self.botonRegistrar.configure(state = "disabled")
			self.botonEditarDatos.configure(state="normal")

		else:		

			self.botonEditarDatos.configure(state="disabled")
			self.botonRegistrar.configure(state = "normal")			


	
	def obtener_datos(self, dni):

		self.conector = SQLServerConnector()
		self.conector.connect()
		
		try:
			r = self.conector.execute_query(f"SELECT * from registro_empleados where dni_empleado = '{dni}'")
			return r
	
		except Exception as e:
			mb.showinfo(message = f"Error al procesar datos de empleados: {e}", title = "Error")


	def validar_campos(self):
		# Obtener el contenido de las casillas obligatorias
		nombre = self.textNombre.get()
		apellidos = self.textApellido.get()
		dni = self.textDni.get()
		fecha_nacimiento = self.textFechaNacimiento.get()
		sexo = self.radio_sexo.get()
		telefono1 = self.textTelefono1.get()

		# Validar que los campos obligatorios no estén vacíos
		if not nombre or not apellidos or not dni or not fecha_nacimiento or sexo == 0:
			mb.showerror("Error", "Todos los campos obligatorios deben estar llenos.")
			return False

		# Validar que el DNI tenga exactamente 8 dígitos
		if len(dni) != 8 or not dni.isdigit():
			mb.showerror("Error", "El DNI debe tener exactamente 8 dígitos.")
			return False

		# Validar que el Teléfono 1 tenga exactamente 9 dígitos si no está vacío
		if telefono1 and (len(telefono1) != 9 or not telefono1.isdigit()):
			mb.showerror("Error", "El Teléfono 1 debe tener exactamente 9 dígitos.")
			return False

		# Si todas las validaciones pasan
		mb.showinfo("Éxito", "Todos los campos están correctamente llenos.")
		return True

	def capturar_entradas(self):
		# Obtener el contenido de todas las casillas del formulario
		nombre = self.textNombre.get()
		apellidos = self.textApellido.get()
		dni = self.textDni.get()
		fecha_nacimiento = self.textFechaNacimiento.get()
		sexo = self.radio_sexo.get()
		telefono1 = self.textTelefono1.get()
		fecha_contrato = self.textFechaContrato.get()
		email = self.textEmail.get()
		direccion = self.textDireccion.get()
		estado = self.opcion_seleccionada.get()

		# Crear una tupla con los valores capturados
		datos_empleado = (
			nombre,
			apellidos,
			dni,
			fecha_nacimiento,
			"M" if sexo == 1 else "F",
			telefono1,
			fecha_contrato,
			email,
			direccion,
			estado
		)

		return datos_empleado



	def empleado_existe(self,dni):
		try:
			con = SQLServerConnector()
			con.connect()
			
			result = self.conector.execute_query(f"SELECT COUNT(*) FROM registro_empleados WHERE dni_empleado = '{dni}'")
			existe = result[0][0] > 0
			
			return existe
		except Exception as e:
			mb.showerror("Error", f"No se pudo verificar la existencia del empleado: {e}")
			return False



	def crear_empleado(self):
		if self.validar_campos() and not self.empleado_existe(self.textDni.get()):
			datos = self.capturar_entradas()
			print("Los datos que he recibido son:")
			print(datos)

			try:
				con = SQLServerConnector()
				con.connect()

				query = f"""
					INSERT INTO registro_empleados 
					(
						nombre_empleado, 
						apellidos_empleado, 
						dni_empleado, 
						sexo, 
						telefono, 
						fecha_nacimiento, 
						email, 
						direccion, 
						fecha_contrato
					)
					VALUES (
						'{datos[0]}', '{datos[1]}', '{datos[2]}', '{datos[4]}',
						'{datos[5]}', '{datos[3]}', '{datos[7]}', '{datos[8]}', '{datos[6]}'
					)
				"""
				con.execute_query(query)

				id_empleado = con.execute_query(f"SELECT id_registro_personal FROM registro_empleados WHERE dni_empleado = '{datos[2]}'")
				
				if id_empleado:
					con.execute_query(f"INSERT INTO empleado (id_registro_personal) VALUES ({id_empleado[0][0]})")

				mb.showinfo("Éxito", "Empleado creado correctamente.")

				# Habilitar todos los botones después de crear el empleado exitosamente
				self.botonRegistrar.configure(state="normal")
				
				self.botonEditarDatos.configure(state="normal")

			except Exception as e:
				mb.showerror("Error", f"No se pudo crear el empleado: {e}")
		else:
			mb.showerror("Error", "No se puede crear el empleado. Verifique los campos o el DNI ya existe.")


	def editar(self):
		if self.validar_campos() and self.empleado_existe(self.textDni.get()):
			datos = self.capturar_entradas()
			print("Los datos que he recibido son:")
			print(datos)

			try:
				con = SQLServerConnector()
				con.connect()

				id_empleado = con.execute_query(f"SELECT id_registro_personal FROM registro_empleados WHERE dni_empleado = '{datos[2]}'")
				
				query = f"""
					UPDATE registro_empleados
					SET nombre_empleado = '{datos[0]}',
						apellidos_empleado = '{datos[1]}',
						dni_empleado = '{datos[2]}',
						sexo = '{datos[4]}',
						telefono = '{datos[5]}',
						fecha_nacimiento = '{datos[3]}',
						email = '{datos[7]}',
						direccion = '{datos[8]}',
						fecha_contrato = '{datos[6]}',
						estado = '{datos[9]}'
					WHERE id_registro_personal = {id_empleado[0][0]}
				"""
				con.execute_query(query)


				mb.showinfo("Éxito", "Empleado modificado correctamente.")


			except Exception as e:
				mb.showerror("Error", f"No se pudo modificar el empleado: {e}")
		else:
			mb.showerror("Error", "No se puede crear el empleado. Verifique los campos o el DNI ya existe.")

	####### #########################################################################################################################
	#
	#
	#
	#

	def show_dashboard_v5(self):
		self.clear_content()
		ctk.CTkLabel(self.content_frame, text = "LA PAGINA DE Configuraciones AUN NO ESTA DISPONIBLE, PERO ESTOY TRABAJANDO PARA QUE SALGA PRONTO").pack()

	def show_dashboard_v6(self):
		self.clear_content()
		self.show_dashboard_v4()

if __name__ == "__main__":
	root = ctk.CTk()
	app = Menu_administrador(root)
	#app.pack(fill='both', expand=True)  
	root.bind("<Escape>", exit)
	root.bind("<F5>", reinicio)
	root.mainloop()
