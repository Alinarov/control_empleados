import tkinter as tk
from tkinter import ttk
import app
from app import *
import random
from datetime import datetime as dt
from comunicacion import SQLServerConnector
import threading
import time

class Menu_registradora(ctk.CTkToplevel, app.MainApp):
	def __init__(self, parent, *args, **kargs):
		super().__init__(parent, *args, **kargs)
		ctk.set_appearance_mode("dark")
		self.parent = parent # Enlazar con la ventana padre (no necesitas self.parent = self)
		self.parent.title("Registradora")
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
		self.menu_frame = tk.Frame(self.paned_window, bg= self.color_menu, width=300)
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
		self.create_menu_button("Nuevo corte. 1", self.show_dashboard_v4, "anotar.png")
		self.create_menu_button("Anotar carga. 2", self.show_dashboard_v2, "nuevoEmpleado.png")

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
				self.nombres_empleados = datos.get('empleados', [])  # Obtener lista de nombres de empleados
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
		data = {"empleados": datos}
		try:
			with open('temp.json', 'w', encoding='utf-8') as archivo:
				json.dump(data, archivo, indent=4, ensure_ascii=False)
			print(f"Datos escritos correctamente en 'temp.json'.")
		except Exception as e:
			print(f"Error al escribir en 'temp.json': {e}")

	######################################################################################################################################
	# ----------------------------------------------------------------------------------------------
	# Pagina de inicio
	# ______________________________________________________________________________________________
	def show_dashboard_v1(self):
		self.clear_content()
		self.parent.title("Menu")
		self.fondo_menu_label = ctk.CTkLabel(
			self.content_frame,
			image= ctk.CTkImage(
				light_image=Image.open("fondo3.jpg"),
				size=(1245, 750)
			), 
			text="Control de cargas de Empleados \n\n\n\n\n\n\n\n\n",
			font=("", 40, "bold"),
			text_color="#254336"
		)
		self.fondo_menu_label.place(x=0, y=0, relwidth=1, relheight=1)

		self.mensaje = ctk.CTkLabel(
			self.fondo_menu_label,
			text="¡Registra y supervisa los pesos de tus empleados con facilidad! \nMantén un control eficiente y promueve la salud en tu lugar de trabajo. \n(C) 2005 https://alinakrasnaya.itch.io/",
			fg_color="#F9EFDB", text_color="#638889", bg_color="#849166", justify=tk.CENTER,
			font=("", 19), cursor = "hand2", corner_radius = 15
		)
		self.mensaje.place(relx=0.51, rely= 0.36, anchor = "center")
		self.mensaje.bind("<Button-1>", lambda e: webbrowser.open_new("https://alinakrasnaya.itch.io/"))

		imagen1 = Image.open("nuevoEmpleado.png")
		imagen1 = imagen1.resize((100, 100))
		imagen1 = ImageTk.PhotoImage(imagen1)

		imagen2 = Image.open("anotar.png")
		imagen2 = imagen2.resize((100, 100))
		imagen2 = ImageTk.PhotoImage(imagen2)


		self.boton1 = ctk.CTkButton(self.content_frame, text="Nuevo corte.\n 1", fg_color="#fff", compound="top", 
									image=imagen2, text_color="#111", font=("", 16, "bold"), bg_color="#58A399", command = self.show_dashboard_v4)
		self.boton1.place(relx=0.25, rely=0.7, anchor='center')

		self.boton2 = ctk.CTkButton(self.content_frame, text="Registrar carga \nempleado. 2", fg_color="#fff", compound="top", 
									image=imagen1, text_color="#111", font=("", 16, "bold"), bg_color="#58A399", command = self.show_dashboard_v2)
		self.boton2.place(relx=0.75, rely=0.7, anchor='center')


	######################################################################################################################################
	# 	
	# ----------------------------------------------------------------------------------------------
	# Pagina de listado de los empleados para registrar las cargas que hicieron durante el dia
	# ______________________________________________________________________________________________

	def show_dashboard_v2(self):
		self.clear_content()
		self.parent.title("Corte del dia")
		ctk.set_appearance_mode("dark")  # tema principal

		# Frames principales
		self.framePanelIzquierdo = ctk.CTkFrame(self.content_frame,
												fg_color=self.dataConfig["tema_2"]["colorbg"])
		self.framePanelIzquierdo.pack(side="right", fill="both")
		# Contenido del panel izquierdo
		self.labelTituloSeleccionarEmpleado = ctk.CTkLabel(self.framePanelIzquierdo, text="Cargas de Empleados",
														   text_color=self.dataConfig["tema_2"]["colordes"],
														   font=("Cascadia Code", 16, "bold"))
		self.labelTituloSeleccionarEmpleado.pack(padx=10, pady=10)
		ctk.CTkLabel (
			self.framePanelIzquierdo,
			text = "",
			image = ctk.CTkImage(
				light_image=Image.open("empleado-cargando.jpg"),
				size=(300,210)
				)
			).pack()		
		ctk.CTkLabel(
		    self.framePanelIzquierdo,
		    text=(
		        'Funcionalidades:\n'
		        '1. Ver Empleados Activos.\n'
		        '2. Ingreso de Peso de Carga al\n   hacer clic en un empleado.\n'
		        '4. Visualización de registros \n   del empleado seleccionado.\n'
		        '5. Navegación:\n'
		        '   a. Inicio: Página principal.\n'
		        '   b. Historial: Anotar carga \n'
		        '6. Uso:\n'
		        '   a. Primero registra una fecha \n      haciendo clic en Nuevo corte.\n'
		    ),
		    text_color="#113946",
		    font=("Cascadia Code", 13, "bold"),
		    anchor='w',  # Alinea el texto a la izquierda
		    justify='left'  # Justifica el texto a la izquierda
		).pack(padx=10, pady=(10, 0))
			
		self.framePanerRegistrosCargas = ctk.CTkFrame(self.content_frame,
													  fg_color=self.dataConfig["tema_3"]["colorbg"])
		self.framePanerRegistrosCargas.pack(fill="both", expand=True)
		# {+} Contenido de los registros de los empleados que hicieron los cortes en un día
		self.labelTituloCortesDia = ctk.CTkLabel(self.framePanerRegistrosCargas, 
												 text="Corte del día: xx/xx/xx Hora inicio: xx:xx Hora corte: xx:xx",
												 text_color=self.dataConfig["tema_2"]["colordes"],
												 font=("Cascadia Code", 16, "bold"))
		self.labelTituloCortesDia.pack(fill="x")




		self.frameBuscar = ctk.CTkFrame(self.framePanerRegistrosCargas)
		self.frameBuscar.pack(fill="x")

		# [+] Cosa de busqueda
		self.name_var = tk.StringVar()
		self.name_var.trace_add('write', self.actualizar_resultados)

		self.inputBuscarEmpleado = ctk.CTkEntry(self.frameBuscar,
			validate='key', placeholder_text="Ingresar nombre de un empleado para buscar sus datos",
			placeholder_text_color=self.dataConfig["tema_2"]["colordes"],
			fg_color=self.dataConfig["tema_3"]["colorcp"], font=("", 16),
			text_color="#01204E", textvariable=self.name_var
		)
		self.inputBuscarEmpleado.pack(padx=10, fill="x", side="left", expand=True)



		# Imagen del botón de búsqueda
		self.boton_busqueda = ctk.CTkButton(self.frameBuscar, text="Buscar", 
											image=ctk.CTkImage(light_image=Image.open("lupa.png"), size=(20, 20)))
		self.boton_busqueda.pack(side="right", pady=3, padx=10)

		# Iniciar hilo para obtener nombres de empleados
		hilo = threading.Thread(target=self.obtener_nombre_empleados_db)
		hilo.start()

		self.nombres = []
		self.pagina_actual = 0
		self.opciones_registros = ['10', '15', '20', '25', '30']  # Opciones de cantidad de nombres por página
		self.registros_por_pagina = tk.IntVar(value=int(self.opciones_registros[0]))  # Valor inicial por defecto

		# Este es el panel donde aparecen los nombres de 
		self.lb_nombres = CTkListbox(self.framePanerRegistrosCargas, 
									 text_color="#F1F8E8", hover_color="#497174", fg_color="#C8CFA0", border_color="#78ABA8", 
									 button_color="#78ABA8", command=self.imprimir_seleccion, font=("", 16, "bold"))
		self.lb_nombres.pack(padx=0, pady=10, expand=True, fill="both")
		self.lb_nombres.configure(font=("", 16, "bold"), text_color="#102C57")            
		# ------------------------------------------------------------------------------------------

		self.frm_opciones = ctk.CTkFrame(self.framePanerRegistrosCargas,  fg_color="#C8CFA0", 
			border_color="#78ABA8", border_width=3)
		self.frm_opciones.pack(padx=0, pady=0, fill="x")

		# Dropdown list para seleccionar cantidad de registros por página
		self.opcion_seleccionada = tk.StringVar(self.framePanerRegistrosCargas)
		self.opcion_seleccionada.set(self.opciones_registros[1])  # Valor inicial por defecto
		self.option_menu = ctk.CTkOptionMenu(self.frm_opciones, variable=self.opcion_seleccionada, 
											 values=self.opciones_registros, command=self.cambiar_registros_por_pagina)
		self.option_menu.pack(padx=10, pady=5, side="left")
		
		self.btn_anterior = ctk.CTkButton(self.frm_opciones, text_color = "#01204E", fg_color = "#028391",font = ("", 16, "bold"),
		 text="Anterior", command=self.pagina_anterior)
		self.btn_anterior.pack(padx=10, pady=5, side="left")
		
		self.btn_siguiente = ctk.CTkButton(self.frm_opciones, text="Siguiente", text_color = "#01204E", fg_color = "#028391",font = ("", 16, "bold"),
			command=self.pagina_siguiente)
		self.btn_siguiente.pack(padx=10, pady=5, side="left")

		self.cargar_nombres()
		self.leer_desde_json()

	def imprimir_seleccion(self, opcion_seleccionada_lista_box):
		print(opcion_seleccionada_lista_box)
		self.show_dashboard_v3(opcion_seleccionada_lista_box)


	def buscar_empleados(self, patron_busqueda):
		resultados = []

		# Convertir el patrón de búsqueda a minúsculas para hacer la comparación sin distinción de mayúsculas
		patron_busqueda = patron_busqueda.lower()

		# Buscar por nombre completo, DNI o últimos 8 dígitos del DNI
		for empleado in self.nombres_empleados:
			partes = empleado.split(':')
			if len(partes) == 2:
				nombre_completo = partes[0].strip().lower()
				dni_empleado = partes[1].strip()

				# Buscar coincidencias en nombre o DNI
				if patron_busqueda in nombre_completo or patron_busqueda in dni_empleado:
					resultados.append(empleado)
			else:
				nombre_completo = empleado.strip().lower()
				if patron_busqueda in nombre_completo:
					resultados.append(empleado)

		return resultados

	def debounce(self, func, wait):
		"""Debounce function to prevent multiple rapid calls"""
		def debounced(*args, **kwargs):
			def call_it():
				func(*args, **kwargs)
				self._last_call = None
			if hasattr(self, "_last_call"):
				self.after_cancel(self._last_call)
			self._last_call = self.after(wait, call_it)
		return debounced

	def actualizar_resultados(self, *args):
		patron_busqueda = self.inputBuscarEmpleado.get()
		resultados = self.buscar_empleados(patron_busqueda)

		if resultados is None:
			resultados = []

		# Usar threading para actualizar la lista
		threading.Thread(target=self.actualizar_lista, args=(resultados,)).start()

	def actualizar_lista(self, resultados):
		# Usar after para actualizar la lista en el hilo principal
		self.lb_nombres.delete(0, tk.END)  # Limpiar la lista en el hilo principal

		def insert_items():
			# Agregar los resultados a la lista
			for resultado in resultados:
				self.lb_nombres.insert(tk.END, resultado)

			# Actualizar la lista de nombres internos
			self.nombres = resultados

			# Si necesitas cargar nombres en paginación
			self.cargar_nombres()

		self.lb_nombres.after(0, insert_items)
		

	def cargar_nombres(self):
		inicio = self.pagina_actual * self.registros_por_pagina.get()
		fin = inicio + self.registros_por_pagina.get()
		nombres_pagina = self.nombres[inicio:fin]
		
		self.lb_nombres.delete(0, tk.END)
		for nombre in nombres_pagina:
			self.lb_nombres.insert(tk.END, nombre)


	def pagina_anterior(self):
		if self.pagina_actual > 0:
			self.pagina_actual -= 1
			self.cargar_nombres()
		else:
			mb.showinfo("Información", "Ya estás en la primera página")

	def pagina_siguiente(self):
		if (self.pagina_actual + 1) * self.registros_por_pagina.get() < len(self.nombres):
			self.pagina_actual += 1
			self.cargar_nombres()
		else:
			mb.showinfo("Información", "Ya estás en la última página")
	
	def cambiar_registros_por_pagina(self, event):
		self.registros_por_pagina.set(int(self.opcion_seleccionada.get()))
		self.pagina_actual = 0  # Reiniciar a la primera página al cambiar el número de registros por página
		self.cargar_nombres()

	def obtener_nombre_empleados_db(self):
		# Iniciar la cosa de carga
		self.loadingTK = ctk.CTk()
		self.cosa_carga = IndicadorCarga(self.loadingTK)

		# Realizar la operación de base de datos en un hilo separado
		hilo_db = threading.Thread(target=self.get_nombre_db)
		hilo_db.start()

		# Iniciar el bucle principal en el hilo principal
		self.loadingTK.mainloop()

	def get_nombre_db(self):
		nombres_completos = []
		self.conector = SQLServerConnector()
		self.conector.connect()
		
		try:
			# Realizar la consulta a la base de datos
			lista_db_empleados = self.conector.execute_query("""
				SELECT nombre_empleado, apellidos_empleado, dni_empleado
				FROM registro_empleados 
				WHERE estado = 'activo'
				ORDER BY id_registro_personal;

			""")

			# Formatear nombres completos
			for nombre, apellido, dni_empleado in lista_db_empleados:
				nombre_completo = f"{nombre} {apellido} : {dni_empleado}"
				nombres_completos.append(nombre_completo)

			# Informar que la operación fue exitosa
			print("Nombres de empleados obtenidos correctamente")
			self.nombres = nombres_completos  # Actualizar la lista de nombres
			self.escribir_en_json(nombres_completos)

		except Exception as e:
			mb.showinfo(message = f"Error al procesar datos de empleados: {e}", title = "Error")

		# Detener el indicador de carga y cerrar la ventana de carga
		self.loadingTK.after(0, self.cosa_carga.stop_loading)

		# Actualizar la lista de nombres en la interfaz principal
		self.framePanerRegistrosCargas.after(0, self.cargar_nombres)



	######################################################################################################################################

	# ----------------------------------------------------------------------------------------------
	# Pagina de ingresar los pesos de los empleados
	# ______________________________________________________________________________________________

	def show_dashboard_v3(self, nombres_apellidos):
		self.clear_content()
		self.frame_formulario = ctk.CTkFrame(self.content_frame,
												 fg_color=self.dataConfig["tema_2"]["colorbg"]
												 )
		self.frame_formulario.pack(side="left", fill="both")

		self.frame_tabla_registro = ctk.CTkFrame(self.content_frame,
												 fg_color=self.dataConfig["tema_1"]["colorbg"])
		self.frame_tabla_registro.pack(side="left", fill="both", expand=True)



		# {+} Contenido del formulario 
		Imagen = ctk.CTkLabel(self.frame_formulario, text = "", image = CTkImage(light_image=Image.open("ventana.jpg"), 
			size=(270,270))
		)
		Imagen.pack(padx = 100, pady = 24)


		self.nombre_apellidos = ctk.CTkLabel(self.frame_formulario, text = "Nombres y apellidos: " + nombres_apellidos, 
			text_color = self.dataConfig["tema_2"]["colordes"], font = ("", 20)
			)
		self.nombre_apellidos.pack()

		# [+] Parte del formulario donde se ingresan los pesos
		self.form_grid = ctk.CTkFrame(self.frame_formulario, fg_color=self.dataConfig["tema_2"]["colorbg"])
		self.form_grid.pack(pady = 40, padx = 10)

		self.input_peso = ctk.CTkEntry(self.form_grid, font = ("", 20), validate = "key", 
			placeholder_text = "Ingresar peso en Kg"
			)
		self.input_peso.grid(row = 0, column = 0, sticky = "w") 
		self.input_peso.configure(width = self.input_peso.winfo_reqwidth() + 70)


		self.boton_ingresar_carga = ctk.CTkButton(self.form_grid, text = "Registrar carga", anchor = "center",
			font = ("", 18, "bold"), width = 210, height = 40, command=self.verificar_numero
			)
		self.boton_ingresar_carga.grid(row = 1, column = 0, pady = 20)


		self.label_peso_total = ctk.CTkLabel(self.form_grid, text = "Peso total del dia: xx kg",
			fg_color = self.dataConfig["tema_3"]["colorbg"], bg_color = self.dataConfig["tema_2"]["colorbg"],
			text_color = self.dataConfig["tema_1"]["colorbg"], font = ("", 16, "bold"), width = 200, 
			height = 40, anchor = "w"

			)
		self.label_peso_total.grid(row = 1, column = 1, pady = 20, padx = 30)
		# {-} Contenido del formulario 

		# {+} Contenido del frame de las tablas
				# Tabla 

		self.tree = ttk.Treeview(self.frame_tabla_registro)
		self.tree["columns"] = ("Peso_carga", "Hora_registro")

		self.tree.column("#0", width=15)

		# Configuración del ancho de la columna "Peso_carga" al ancho del marco dividido por 2
		self.tree.bind("<Configure>", self.obtener_ancho_marco)
		self.tree.bind("<Configure>", self._on_mousewheel)

		self.tree.column("Peso_carga", width=self.frame_tabla_registro.winfo_reqwidth() // 2)
		self.tree.column("Hora_registro", width=self.frame_tabla_registro.winfo_reqwidth() // 2)

		self.tree.heading("#0", text="ID's")
		self.tree.heading("Peso_carga", text="Peso carga")
		self.tree.heading("Hora_registro", text="Hora de registro")

		# Barra de desplazamiento vertical para la tabla
		scrollbar_y = tk.Scrollbar(self.frame_tabla_registro, orient="vertical", command=self.tree.yview)
		self.tree.configure(yscrollcommand=scrollbar_y.set)

		self.tree.pack(side="left", fill="both", expand=True)
		# Configurar estilo para letras grandes
		style = ttk.Style()
		style.configure("Treeview.Heading", font=("Helvetica", 14))  # Ajusta el tamaño de la fuente aquí
		style.configure("Treeview", font=("Helvetica", 13))  # Cambia el tamaño de la fuente del Treeview

		scrollbar_y.pack(fill="y", side="right")
		

		hilo = threading.Thread(target=self.obtener_pesos)
		hilo.start()


		# for i in range(1, 51):
		# 	peso = random.randint(50, 100)
		# 	hora_registro = dt.now().strftime("%Y-%m-%d %H:%M:%S")
		# 	self.tree.insert("", "end", text=f"ID{i}", values=(peso, hora_registro))

	def _on_mousewheel(self, event):
		# Desplazamiento al utilizar la rueda del mouse
		try:
			self.tree.yview_scroll(int(-1 * (event.delta / 120)), "units")
		except:
			pass

	def verificar_numero(self):
		peso = self.input_peso.get()  # Obtener el texto ingresado en el Entry
		if peso.isdigit():  # Verificar si es un número
			# Aquí puedes hacer lo que necesites con el número, por ejemplo, mostrarlo en la consola
			print("El peso ingresado es:", peso)
			# Si no es un número, mostrar un mensaje de alerta
			confirmacion = mb.askquestion(message="Revise la entrada de pesos antes de continuar. Si es correcta, presione 'Si'.", 
				title="Confirmacion de registro del peso")
			print("la confirmacion" , confirmacion)
			if  "yes" in str(confirmacion):
				print("\n Registrando el peso en la base de datos")
				self.insertar_peso(peso)
				#self.actualizacion_tree()
			else:
				pass
			pass
		else:
			mb.showerror("Alerta", "En la entrada de pesos solo deben ser numero")


	def insertar_peso(self, peso):
		self.conector = SQLServerConnector()
		self.conector.connect()

		texto_completo = self.nombre_apellidos.cget("text")
		dni_empleado = texto_completo[-8:]
		
		try:
			# Realizar la consulta a la base de datos

			# primero obtendremos el id del empleado para poder hacer la insercion
			id_empleado = self.conector.execute_query(f"""select id_registro_personal from registro_empleados where dni_empleado = '{dni_empleado}'""")

			# segundo hacemos la insercion con los datos obtenidos
			lista_db = self.conector.execute_query(f"""
			INSERT INTO cargas (hora_entrega, peso_carga, id_empleado, id_fecha_carga)
			VALUES ('{datetime.datetime.now().strftime('%H:%M:%S')}', {peso}, {id_empleado[0][0]}, '{datetime.datetime.now().strftime("%Y-%m-%d")}');
			""")

			lista_db_pesos = lista_db
			# [(Decimal('30.00'), '2024-03-22', '11:00:00'), (Decimal('55.25'), '2024-03-22', '14:00:00'), (Decimal('35.00'), '2024-03-22', '18:00:00'), (Decimal('50.00'), '2024-03-22', '20:00:00')]

			# aqui agrego los datos de los pesos en la tabla
			try: 

				self.obtener_pesos()
			except Exception as e:
				mb.showinfo(title = "Error", message = "Hubo un error inesperado y creo que es porque no existe un registro de corte para el dia de hoy")
				print(e)


		except Exception as e:
			mb.showinfo(message = f"Error al procesar datos de empleados: {e}", title = "Error")

		
	# Función para borrar todos los datos del Treeview
	def clear_treeview(self):
		treeview = self.tree
		for item in treeview.get_children():
			treeview.delete(item)

	def agregar_datos_tabla(self, data):
		self.clear_treeview()
		for idx, (peso, fecha, hora) in enumerate(data, start=1):
			self.tree.insert("", "end", text=str(idx), values=(str(peso), f"{hora} - {fecha}"))

	def obtener_pesos(self):
		# Iniciar la cosa de carga
		self.loadingTK = ctk.CTk()
		self.cosa_carga = IndicadorCarga(self.loadingTK)

		# Formatear la fecha en el formato deseado
		fecha_formateada = datetime.datetime.now().strftime("%Y-%m-%d")

		# Realizar la operación de base de datos en un hilo separado
		hilo_db = threading.Thread(target=lambda: self.obtener_pesos_db(fecha_formateada))
		hilo_db.start()

		# Iniciar el bucle principal en el hilo principal
		self.loadingTK.mainloop()

	def obtener_pesos_db(self, fecha = None):
		texto_completo = self.nombre_apellidos.cget("text")
		# Obtener los últimos 8 caracteres
		dni_empleado = texto_completo[-8:]
	
		self.conector = SQLServerConnector()
		self.conector.connect()

		lista_db_pesos = []
		
		try:
			# Realizar la consulta a la base de datos
			lista_db = self.conector.execute_query(f"""
				SELECT  c.peso_carga, c.id_fecha_carga, c.hora_entrega
				FROM empleado em
				INNER JOIN registro_empleados e ON em.id_registro_personal = e.id_registro_personal
				INNER JOIN cargas c ON em.id_empleado = c.id_empleado
				INNER JOIN fecha_carga fc ON c.id_fecha_carga = fc.id_fecha_carga
				WHERE c.id_fecha_carga = '{fecha}' -- Filtra por la fecha de carga deseada
				AND e.dni_empleado = '{dni_empleado}' -- Filtra por el ID del empleado deseado
				ORDER BY c.id_cargas;
			""")

			lista_db_pesos = lista_db
			# [(Decimal('30.00'), '2024-03-22', '11:00:00'), (Decimal('55.25'), '2024-03-22', '14:00:00'), (Decimal('35.00'), '2024-03-22', '18:00:00'), (Decimal('50.00'), '2024-03-22', '20:00:00')]

			# aqui agrego los datos de los pesos en la tabla
			try: 
				self.agregar_datos_tabla(lista_db_pesos)
			except Exception as e:
				mb.showinfo(title = "Error", message = "Al parecer no hay ninguna carga registrada")


		except Exception as e:
			mb.showinfo(message = f"Error al procesar datos de empleados: {e}", title = "Error")

		# Detener el indicador de carga y cerrar la ventana de carga
		self.loadingTK.after(0, self.cosa_carga.stop_loading)

		# Actualizar la lista de nombres en la interfaz principal
		self.frame_tabla_registro.after(0, self.agregar_datos_tabla)




	######################################################################################################################################
	# ----------------------------------------------------------------------------------------------
	# Pagina:  Crear el dia de almacenamiento
	# ______________________________________________________________________________________________

	def show_dashboard_v4(self):
		self.clear_content()
		# Obtener la fecha actual
		self.fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y")

		self.content_frame.configure(fg_color = "#001524")

		self.label_registro_dia = ctk.CTkLabel(
			self.content_frame,
			image= ctk.CTkImage(
				light_image=Image.open("fondo4.jpg"),
				size=(1245, 750)
			), 
			text=""
		)
		self.label_registro_dia.place(x=0, y=0, relwidth=1, relheight=1)

		frm_titulo = ctk.CTkFrame(self.label_registro_dia, fg_color = "#72756A", bg_color = "#72756A")
		frm_titulo.place(x=10,y=20)

		# Frames principales
		self.framePanelIzquierdo = ctk.CTkFrame(self.content_frame,
												fg_color=self.dataConfig["tema_2"]["colorbg"])
		self.framePanelIzquierdo.pack(side="right", fill="both")
		# Contenido del panel izquierdo
		self.labelTituloSeleccionarEmpleado = ctk.CTkLabel(self.framePanelIzquierdo, text="Registrar dia de carga",
														   text_color=self.dataConfig["tema_2"]["colordes"],
														   font=("Cascadia Code", 16, "bold"))
		self.labelTituloSeleccionarEmpleado.pack(padx=10, pady=10)
		ctk.CTkLabel (
			self.framePanelIzquierdo,
			text = "",
			image = ctk.CTkImage(
				light_image=Image.open("registrar.jpg"),
				size=(300,200)
				)
			).pack()
		ctk.CTkLabel(
			self.framePanelIzquierdo,
			text=(
	        'Funcionalidades:\n'
	        '1. Registro de Fechas: Establece la \n   fecha y hora de entrada \n   y salida para la carga.\n'
	        '2. Hora de Entrada: Selecciona la\n   hora de inicio de la carga.\n'
	        '3. Hora de Salida: Selecciona la\n   hora de fin de la carga.\n'
	        'Importante: Usa el formato de 24\n   horas.\n'
	        '   Si no estás familiarizado con el\n   formato de 24 horas, simplemente\n   suma 12 a la hora PM para\n   convertirla. Por ejemplo, si deseas\n   ingresar las 10:00 PM, suma 12\n   horas, lo que resulta en 22:00 en\n   formato de 24 horas, que deberás\n   ingresar en la casilla.\n'
	        'Este paso es crucial antes de\n   registrar la carga de un empleado.\n'
			),
			text_color="#497174",
			font=("Cascadia Code", 13, "bold"),
			anchor='w',  # Alinea el texto a la izquierda
			justify='left'  # Justifica el texto a la izquierda
		).pack(pady=0, padx=10, fill='both', expand=True)


		# Label para mostrar la fecha actual
		self.lbl_titulo = ctk.CTkLabel(frm_titulo, text = "Nuevo registro de fecha en formato de \n24 horas para el registro de cargas.", 
			font = ("Helvetica", 20, "bold"), text_color = "#76ABAE", bg_color = "#72756A", 
			fg_color = "#31363F", corner_radius= 5
			)
		self.lbl_titulo.pack(padx = 10, pady = 5)

		self.lbl_fecha = ctk.CTkLabel(self.content_frame, text=f"Fecha (hoy): {self.fecha_actual}", 
			font = ("Helvetica", 18, "bold"), text_color = "#80B9AD", bg_color = "#72756A",
			fg_color = "#31363F", corner_radius= 5
			)
		self.lbl_fecha.place(x=10, y = 80)

		# Frame para las horas de entrada y salida
		frame_horas = ctk.CTkFrame(self.content_frame, bg_color = "#72756A")
		frame_horas.place(y=130, x = 10)

		# TimeInput para la hora de entrada
		lbl_entrada = ctk.CTkLabel(frame_horas, text="Hora de Entrada:", font = ("", 17, "bold"),
			text_color="#76ABAE")
		lbl_entrada.grid(row=0, column=0, padx=10, pady=5)
		self.time_entrada = TimeInputWidget(frame_horas)
		self.time_entrada.frame.grid(row=1, column=0, padx=10, pady=5)

		# TimeInput para la hora de salida
		lbl_salida = ctk.CTkLabel(frame_horas, text="Hora de Salida:", font = ("", 17, "bold"),
			text_color="#76ABAE")
		lbl_salida.grid(row=2, column=0, padx=10, pady=5)
		self.time_salida = TimeInputWidget(frame_horas)
		self.time_salida.frame.grid(row=3, column=0, padx=10, pady=5)

		# Botón para enviar los datos
		btn_enviar = ctk.CTkButton(self.content_frame, text="Enviar", command=self.guardar_registro,
			fg_color = "#445D48", text_color = "#D6CC99", font = ("", 16, "bold") , bg_color = "#72756A"
			)
		btn_enviar.place(y=320, x = 10)

	def guardar_registro(self):
		# Obtener las horas de entrada y salida seleccionadas
		hora_entrada = self.time_entrada.get_time()
		hora_salida = self.time_salida.get_time()

		# Ejemplo: Mostrar los datos ingresados
		respuesta = mb.askokcancel(
			message=(
				f"¿Estás seguro de querer guardar las horas seleccionadas?\n"
				f"Hora de Entrada: {hora_entrada}\n"
				f"Hora de Salida: {hora_salida}\n\n"
				"Presiona 'No' si deseas revisar los datos.\n"
				"¿Deseas continuar?"
			),
			title="Confirmar registro de horas"
		)

		if respuesta:
			print("Si")
			self.conector = SQLServerConnector()
			fecha_actual = dt.strptime(self.fecha_actual, "%d/%m/%Y").strftime("%Y-%m-%d")
			
			# Cambiar cursor a modo carga

			# Iniciar el hilo para la inserción
			threading.Thread(target=lambda: self.insercion_fecha(fecha_actual, hora_entrada, hora_salida)).start()
		else:
			print("no")


	def insercion_fecha(self, fecha_actual, hora_entrada, hora_salida):
		# Iniciar la cosa de carga
		self.loadingTK = ctk.CTk()
		cosa_carga = IndicadorCarga(self.loadingTK)

		# Realizar la operación de base de datos en un hilo separado
		threading.Thread(target=lambda: self.db_operation(cosa_carga, fecha_actual, hora_entrada, hora_salida)).start()
		
		# Iniciar el bucle principal en el hilo principal
		self.loadingTK.mainloop()

	def db_operation(self, cosa_carga, fecha_actual, hora_entrada, hora_salida):
		self.conector.connect()
		# Verificar si ya existe un registro para la fecha actual
		res = self.conector.execute_query(f"""SELECT COUNT(*) FROM fecha_carga WHERE id_fecha_carga = '{fecha_actual}';""")

		if any(1 in item for item in res):
			print("\n \nYa existe")

			# Aquí poner el stop de la carga
			self.loadingTK.after(0, cosa_carga.stop_loading)
			mb.showerror(message="Ya existe un día de cargas registrado")
		else:
			# Realizar la inserción en la base de datos
			self.conector.execute_query(f"""INSERT INTO fecha_carga (id_fecha_carga, hora_inicio, hora_corte) 
			VALUES ('{fecha_actual}', '{hora_entrada}:00', '{hora_salida}:00')""")
			
			# Simulación de tiempo de espera
			
			# Restablecer el cursor y mostrar mensaje de confirmación
			# Aquí poner el stop de la carga
			self.loadingTK.after(0, cosa_carga.stop_loading)
			mb.showinfo(message="La fecha se ha registrado, ya puedes registrar las cargas que harán los empleados", title="Fecha registrada")

# if __name__ == "__main__":
# 	root = ctk.CTk()
# 	app = Menu_registradora(root)
# 	#app.pack(fill='both', expand=True)  
# 	root.bind("<Escape>", exit)
# 	root.bind("<F5>", reinicio)
# 	root.mainloop()
