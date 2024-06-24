import tkinter as tk
from tkinter import ttk
import app
from app import *
import random
from datetime import datetime as dt
from comunicacion import SQLServerConnector
import threading
import os

class MenuRegistradora:
	def __init__(self, parent):
		self.parent = parent
		self.parent.title("Menu Registradora")
		self.content_frame = ctk.CTkFrame(self.parent)
		self.content_frame.pack(fill="both", expand=True)
		
		self.dataConfig = {
			"tema_2": {"colordes": "#FFFFFF", "colorbg": "#333333"},
			"tema_3": {"colorcp": "#CCCCCC", "colorbg": "#666666"}
		}
		
		self.show_dashboard_v2()

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
		self.framePanelIzquierdo.pack(side="left", fill="both")

		self.framePanerRegistrosCargas = ctk.CTkFrame(self.content_frame,
													  fg_color=self.dataConfig["tema_3"]["colorbg"])
		self.framePanerRegistrosCargas.pack(fill="both", expand=True)

		# Contenido del panel izquierdo
		self.labelTituloSeleccionarFecha = ctk.CTkLabel(self.framePanelIzquierdo, text="Seleccionar una Fecha",
														text_color=self.dataConfig["tema_2"]["colordes"],
														font=("Cascadia Code", 16, "bold"))
		self.labelTituloSeleccionarFecha.pack(padx=10, pady=10)

		# Contenido del panel de simulación de registros
		ctk.CTkLabel(self.framePanerRegistrosCargas, text="Registros de las cargas hechas en la fecha",
					 text_color=self.dataConfig["tema_2"]["colordes"], font=("", 20, "bold")).pack(fill="x", side="top")

		self.frameBuscar = ctk.CTkFrame(self.framePanerRegistrosCargas)
		self.frameBuscar.pack(fill="x")

		# Campo de búsqueda
		self.name_var_fecha = tk.StringVar()
		self.name_var_fecha.trace_add('write', self.debounce(self.actualizar_resultados_fechas, 100))

		ctk.CTkEntry(self.frameBuscar, validate='key', placeholder_text="Buscar fecha (dd-mm-yyyy)",
					 placeholder_text_color=self.dataConfig["tema_2"]["colordes"],
					 fg_color=self.dataConfig["tema_3"]["colorcp"], font=("", 16),
					 text_color="#01204E", textvariable=self.name_var_fecha).pack(padx=10, fill="x", side="left", expand=True)

		# Botón de búsqueda con imagen
		ctk.CTkButton(self.frameBuscar, text="Buscar", command=self.actualizar_resultados_fechas,
					  image=ctk.CTkImage(light_image=Image.open("lupa.png"), size=(20, 20))).pack(side="right", pady=3, padx=10)

		# Lista de fechas
		self.lb_fechas = CTkListbox(self.framePanerRegistrosCargas, 
									text_color="#F1F8E8", hover_color="#497174", fg_color="#C8CFA0", 
									border_color="#78ABA8", button_color="#78ABA8", font=("", 16, "bold"))
		self.lb_fechas.pack(padx=0, pady=10, expand=True, fill="both")
		self.lb_fechas.configure(font=("", 16, "bold"), text_color="#102C57")

		# Opciones de paginación
		self.frm_opciones_fecha = ctk.CTkFrame(self.framePanerRegistrosCargas, fg_color="#9DDE8B", 
											   border_color="#006769", border_width=3)
		self.frm_opciones_fecha.pack(padx=0, pady=0, fill="x")

		self.opcion_seleccionada = tk.StringVar(self.framePanerRegistrosCargas)
		self.opcion_seleccionada.set(self.opciones_registros_fecha[1])  # Valor inicial por defecto
		ctk.CTkOptionMenu(self.frm_opciones_fecha, variable=self.opcion_seleccionada, 
						  values=self.opciones_registros_fecha, command=self.cambiar_registros_por_pagina_fecha).pack(padx=10, pady=5, side="left")
		
		ctk.CTkButton(self.frm_opciones_fecha, text="Anterior", command=self.pagina_anterior_fecha).pack(padx=10, pady=5, side="left")
		ctk.CTkButton(self.frm_opciones_fecha, text="Siguiente", command=self.pagina_siguiente_fecha).pack(padx=10, pady=5, side="left")

		# Iniciar hilo para obtener fechas
		hilo = threading.Thread(target=self.obtener_fechas_db)
		hilo.start()

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
			for resultado in resultados:
				self.lb_fechas.insert(tk.END, resultado)
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
			self.show_dashboard_v2()			
			mb.showinfo(message=f"Error al procesar datos de fechas: {e}", title="Error")
		self.loadingTK.after(0, self.cosa_carga.stop_loading)
		self.content_frame.after(0, self.cargar_fechas)


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

# Ejemplo de inicialización
if __name__ == "__main__":
	root = ctk.CTk()
	app = MenuRegistradora(root)
	root.mainloop()
