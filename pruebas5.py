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

		self.empleados = []  # Lista de empleados obtenidos de la base de datos
		self.nombres_empleados = []  # Lista para almacenar nombres de empleados

		self.pagina_actual_empleado = 0
		self.opciones_registros_empleado = ['10', '15', '20', '25', '30']  # Opciones de cantidad de registros por página
		self.registros_por_pagina = tk.IntVar(value=int(self.opciones_registros_empleado[0]))  # Valor inicial por defecto

		# Frames principales
		self.framePanelIzquierdo = ctk.CTkFrame(self.content_frame,
												fg_color=self.dataConfig["tema_2"]["colorbg"])
		self.framePanelIzquierdo.pack(side="left", fill="both")

		self.framePanelRegistrosEmpleados = ctk.CTkFrame(self.content_frame,
														 fg_color=self.dataConfig["tema_3"]["colorbg"])
		self.framePanelRegistrosEmpleados.pack(fill="both", expand=True)

		# Contenido del panel izquierdo
		self.labelTituloSeleccionarEmpleado = ctk.CTkLabel(self.framePanelIzquierdo, text="Seleccionar un Empleado",
														   text_color=self.dataConfig["tema_2"]["colordes"],
														   font=("Cascadia Code", 16, "bold"))
		self.labelTituloSeleccionarEmpleado.pack(padx=10, pady=10)

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
										   text_color="#F1F8E8", hover_color="#497174", fg_color="#C8CFA0", 
										   border_color="#78ABA8", button_color="#78ABA8", font=("", 16))
		self.lb_empleados.pack(padx=0, pady=10, expand=True, fill="both")

		# Opciones de paginación para empleados
		self.frm_opciones_empleado = ctk.CTkFrame(self.framePanelRegistrosEmpleados, fg_color="#9DDE8B", 
												  border_color="#006769", border_width=3)
		self.frm_opciones_empleado.pack(padx=0, pady=0, fill="x")

		self.opcion_seleccionada_empleado = tk.StringVar(self.framePanelRegistrosEmpleados)
		self.opcion_seleccionada_empleado.set(self.opciones_registros_empleado[1])  # Valor inicial por defecto
		ctk.CTkOptionMenu(self.frm_opciones_empleado, variable=self.opcion_seleccionada_empleado, 
						  values=self.opciones_registros_empleado, command=self.cambiar_registros_por_pagina_empleado).pack(padx=10, pady=5, side="left")
		
		ctk.CTkButton(self.frm_opciones_empleado, text="Anterior", command=self.pagina_anterior_empleado).pack(padx=10, pady=5, side="left")
		ctk.CTkButton(self.frm_opciones_empleado, text="Siguiente", command=self.pagina_siguiente_empleado).pack(padx=10, pady=5, side="left")

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

# Ejemplo de inicialización
if __name__ == "__main__":
	root = ctk.CTk()
	app = MenuRegistradora(root)
	root.mainloop()
