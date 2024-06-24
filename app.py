#!/usr/bin/env python
## *******************************
## | Este archivo solo sirve para generar las ventanas, es la **ventana Padre**
## | 
## |____________________________ 
import sys
import tkinter as tk
from tkinter import ttk, PhotoImage, messagebox as mb
import json
import customtkinter as ctk
from customtkinter import CTkImage, CTkProgressBar
from PIL import Image, ImageTk
from tkcalendar import DateEntry, Calendar
#import pyodbc
import webbrowser
from CTkListbox import CTkListbox
import datetime
from decimal import Decimal
import time 

import random
from datetime import datetime as dt
from comunicacion import SQLServerConnector
import threading
import os

# configuraciones para la ventana
def configuraciones():
	with open("settings.json","r") as fileConfig:
		data = json.load(fileConfig)
	return data


class MainApp(tk.Frame):

	def __init__(self, parent, *args, **kwargs):
		super().__init__(parent, *args, **kwargs)
		self.dataConfig = configuraciones()
		self.parent = parent
		self.ancho = self.dataConfig["ancho_ventana"]
		self.alto = self.dataConfig["alto_ventana"]

		self.parent.iconbitmap("setup_installer/icono.ico")


		self.parent.geometry(f"{self.ancho}x{self.alto}+300+50")
		self.parent.title("Menu")
		self.parent.configure(fg_color=self.dataConfig["tema_1"]["colorac"])

	def get_dataConfig(self):
		return self.dataConfig

	def activar_scrollbar(self, master):
		# Contenido de registros en un canvas con scrollbar
		colorFondoRegistros = self.dataConfig["tema_2"]["colorbg"]
		self.canvas = tk.Canvas(master, bg = colorFondoRegistros)
		self.canvas.pack(side="left", fill="both", expand=True)

		self.scrollbar = ttk.Scrollbar(master, orient="vertical", command=self.canvas.yview)
		self.scrollbar.pack(side="right", fill="y")

		self.canvas.configure(yscrollcommand=self.scrollbar.set)

		self.contenidoCanva = ctk.CTkFrame(self.canvas, fg_color = self.dataConfig["tema_1"]["colorbg"], 
			)
		self.canvas.create_window((0, 0), window=self.contenidoCanva, anchor="nw", 
			width = "15c")

		# Configurar el canvas para que se expanda con el contenido
		self.contenidoCanva.bind("<Configure>", lambda event, canvas=self.canvas: canvas.configure(
			scrollregion=canvas.bbox("all")))

		# Vincular eventos de desplazamiento del mouse al canvas y al frame
		self.canvas.bind("<MouseWheel>", self._on_mousewheel)
		self.contenidoCanva.bind("<MouseWheel>", self._on_mousewheel)

	def obtener_ancho_marco(self, event):
		ancho_marco = self.frame_tabla_registro.winfo_width()
		self.tree.column("Peso_carga", width=ancho_marco // 2)
class DateEntry(DateEntry):
	def __init__(self, master=None, **kw):
		super().__init__(master, **kw)
		self.config(
			date_pattern='yyyy-mm-dd',  # Patrón de fecha personalizado
			selectbackground='sky blue', # Color de fondo al seleccionar una fecha
			selectforeground='#111',     # Color de texto al seleccionar una fecha
			background='#638889'            # Color de fondo de la ventanita del DateEntry
		)
		#self.bind("<KeyPress>", lambda e: "break")  # Bloquear la entrada de teclado

class Kalendario(Calendar, MainApp):
	def __init__(self, master=None, **kw):
		super().__init__(master, **kw)
		dataConfig = configuraciones()
		self.config(
			selectbackground='sky blue',
			selectforeground='#111',
			background= dataConfig["tema_3"]["colorcp"],
			foreground= dataConfig["tema_3"]["colorac"],
			bordercolor= dataConfig["tema_3"]["colordes"],
			headersbackground= dataConfig["tema_2"]["colorbg"]
		)
		# Bind the click event to the date_selected method
		self.bind("<<CalendarSelected>>", self.date_selected)
	
		
	def get_date(self):
		return self.selection_get()  # This gets the selected date

	def date_selected(self, event):
		# Get the selected date
		selected_date = self.get_date()
		print(f"Selected date: {selected_date}")		

class Paginador:
	def __init__(self, master, color_fondo = None):
		self.master = master
		self.pagina_actual = 1

		self.frame = ctk.CTkFrame(master, fg_color = color_fondo, bg_color = "#fff")
		self.frame.pack()

		self.label = ctk.CTkLabel(self.frame, text_color = "#111")
		self.label.grid(row=0, column=0, columnspan=3)

		self.anterior_button = ctk.CTkButton(self.frame, text="Atrás", command=self.pagina_anterior, width = 20)
		self.anterior_button.grid(row=1, column=0)

		self.entry = ctk.CTkEntry(self.frame)
		self.entry.grid(row=1, column=1)
		self.entry.bind('<Return>', self.actualizar_pagina)

		self.siguiente_button = ctk.CTkButton(self.frame, text="Siguiente", command=self.pagina_siguiente, width = 20)
		self.siguiente_button.grid(row=1, column=2)

		self.actualizar_etiqueta()

	def actualizar_etiqueta(self):
		self.label.configure(text=f"Página {self.pagina_actual}")

	def actualizar_pagina(self, event=None):
		try:
			nueva_pagina = int(self.entry.get())
			if nueva_pagina >= 0:
				self.pagina_actual = nueva_pagina
				self.actualizar_etiqueta()
		except ValueError:
			pass
		finally:
			self.entry.delete(0, ctk.END)
			self.entry.insert(0, str(self.pagina_actual))

	def pagina_anterior(self):
		if self.pagina_actual > 0:
			self.pagina_actual -= 1
			self.actualizar_etiqueta()
			self.entry.delete(0, ctk.END)
			self.entry.insert(0, str(self.pagina_actual))

	def pagina_siguiente(self):
		self.pagina_actual += 1
		self.actualizar_etiqueta()
		self.entry.delete(0, ctk.END)
		self.entry.insert(0, str(self.pagina_actual))

# {+} Estas funciones no estan en funcionamiento pero si funcionan para el resize 
def _on_frame_configure(self, event):
	self.canvas.configure(scrollregion=self.canvas.bbox("all"))

def resize_frame(self, event):
	width = event.width
	height = event.height

	# Verificar si el cambio en el tamaño de la ventana es significativo
	if abs(width - self.last_width) > 10 or abs(height - self.last_height) > 10:
		self.canvas.config(width=width, height=height)
		self.canvas.itemconfig(self.inner_frame_id, width=width)
		self.canvas.itemconfig(self.inner_frame_id, height=height)

		# Actualizar las dimensiones anteriores
		self.last_width = width
		self.last_height = height


class TimeInputWidget:
	def __init__(self, master):
		self.frame = ctk.CTkFrame(master)
		self.frame.place(x=0,y=0)

		self.label = ctk.CTkLabel(self.frame, text="Hora:", font = ("", 16))
		self.label.grid(row=0, column=0, padx=5, pady=5)

		self.hour_var = tk.StringVar()
		self.hour_spinbox = tk.Spinbox(self.frame, from_=0, to=23, width=2, textvariable=self.hour_var,
			font = ("", 13)
			)
		self.hour_spinbox.grid(row=0, column=1, padx=5, pady=5)

		self.label_separator = ctk.CTkLabel(self.frame, text=":", font = ("", 16, "bold"))
		self.label_separator.grid(row=0, column=2, padx=5, pady=5)

		self.minute_var = tk.StringVar()
		self.minute_spinbox = tk.Spinbox(self.frame, from_=0, to=59, width=2, textvariable=self.minute_var,
			font = ("", 13)
			)
		self.minute_spinbox.grid(row=0, column=3, padx=5, pady=5)

		self.btn_now = ctk.CTkButton(self.frame, text="Ahora", command=self.set_current_time, 
			fg_color = "#445D48", text_color = "#D6CC99", font = ("", 14, "bold"))
		self.btn_now.grid(row=0, column=4, padx=5, pady=5)

	def set_current_time(self):
		now = datetime.datetime.now()
		self.hour_var.set(now.hour)
		self.minute_var.set(now.minute)

	def get_time(self):
		hour = int(self.hour_var.get())
		minute = int(self.minute_var.get())
		return f"{hour:02}:{minute:02}"


# esta funcion hace que la entrada de datos sea solo con numeros 
def enter_only_digits(entry, action_type) -> bool:
	if action_type == '1' and not entry.isdigit():
		return False

	if len(entry) > 9:
		return False
	return True


def exit(event):
	sys.exit()

def reinicio(event):
	print("\n Recargando ventana ... ")
	python = sys.executable # declaro de una instancia 
	os.execl(python, python, *sys.argv) # funcion de systema que reinicia el programa



class IndicadorCarga:
	def __init__(self, root):
		self.root = root
		self.root.title("Indicador de carga")
		self.root.geometry("300x100+500+300")
		self.root.iconbitmap("setup_installer/setup.ico")
		
		# Crear el indicador de carga personalizado
		self.progressbar = CTkProgressBar(master=self.root, mode="indeterminate")
		self.progressbar.pack(padx=20, pady=10)
		
		self.label = ctk.CTkLabel(self.root, text="Cargando, por favor espere...", fg_color = "#111", corner_radius = 4)
		self.label.pack(pady=10)

		self.start_loading()
			
	def start_loading(self):
		self.progressbar.start()  # Configurar la velocidad de animación

	def stop_loading(self):
		self.progressbar.stop()
		self.label.configure(text="Carga completa")
		self.root.after(1000, self.root.destroy)  




# ------------------------------------------------------------------------------------------------------------------------
# 
# Aqui esta todo lo que es referente a la convercion y reporte de los resultados de las cargas que 
# se hicieron en una fecha
# ------------------------------------------------------------------------------------------------------------------------


import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black

def crear_pdf_desde_json(data, archivo_salida):
	c = canvas.Canvas(archivo_salida, pagesize=letter)
	y_position = 750  # Posición vertical inicial
	page_height = letter[1]

	# Ordenar fechas de carga
	fechas_ordenadas = sorted(data.keys())

	# Título en la primera página
	c.setFont("Helvetica-Bold", 14)
	c.drawString(100, y_position, "Registros de las cargas hechas en la fecha")
	y_position -= 30  # Espacio después del título

	first_page = True

	for fecha in fechas_ordenadas:
		empleados = data[fecha]

		for dni in sorted(empleados.keys()):
			detalles = empleados[dni]

			# Datos del empleado
			empleado_info = [
				f"FECHA: {fecha}",
				f"NOMBRES: {detalles['nombres_apellidos']}",
				f"TOTAL DE CARGA EN EL DIA: {detalles['total_carga']} Kg",
				f"DNI: {dni}",
				f"N CARGAS: {detalles['n_cargas']}"
			]

			# Verificar espacio necesario para los datos del empleado
			espacio_necesario = (len(empleado_info) + 2) * 20 + 100
			if not first_page and y_position - espacio_necesario < 80:
				c.showPage()
				y_position = page_height - 120  # Reiniciar posición vertical

			# Escribir datos del empleado con tamaño de letra 11
			c.setFont("Helvetica", 11)
			for line in empleado_info:
				c.drawString(100, y_position, line)
				y_position -= 18  # Espacio de línea para tamaño de letra 11

			# Encabezados de la tabla con tamaño de letra 11
			c.setFont("Helvetica-Bold", 11)
			c.drawString(100, y_position - 15, "PESO DE CARGA")
			c.drawString(250, y_position - 15, "HORA DE REGISTRO")
			y_position -= 10

			# Líneas horizontales del encabezado de la tabla
			c.setLineWidth(0.5)
			c.line(80, y_position + 10, 500, y_position + 10)  # Línea superior
			c.line(80, y_position - 10, 500, y_position - 10)  # Línea inferior

			y_position -= 20

			# Escribir datos de la tabla con tamaño de letra 11
			c.setFont("Helvetica", 11)
			for carga in detalles["cargas"]:
				if y_position < 100:
					c.showPage()
					y_position = page_height - 120  # Reiniciar posición vertical

				c.drawString(100, y_position - 5, str(carga[0]) + " Kg")  # Peso de carga
				c.drawString(250, y_position - 5, carga[1])  # Hora de registro

				# Líneas horizontales de la tabla
				c.line(80, y_position - 10, 500, y_position - 10)

				y_position -= 18  # Espacio de línea para tamaño de letra 11

			y_position -= 20  # Espacio después de la tabla

			# Indicador de separación de registros de empleados
			if not first_page and y_position < 100:
				c.showPage()
				y_position = page_height - 120  # Reiniciar posición vertical

			draw_fancy_line(c, y_position + 10)
			y_position -= 20  # Espacio después del indicador

			first_page = False

	c.save()
	# Abrir automáticamente el PDF generado
	os.startfile(archivo_salida)

def draw_fancy_line(canvas, y_position):
	# Dibujar línea decorativa
	canvas.setStrokeColor(black)
	canvas.setLineWidth(1)
	canvas.line(80, y_position, 100, y_position)  # Línea izquierda
	canvas.drawString(100, y_position, "] ------ [")
	text_width = canvas.stringWidth("] ------ [", "Helvetica", 10)
	canvas.line(100 + text_width, y_position, 500, y_position)  # Línea derecha

def conversion_a_json_respuesta(respuesta_sql):
	# Estructura de datos para almacenar la información
	data = {}

	# Procesar cada fila de la respuesta SQL
	for nombre, apellidos, dni, peso_carga, id_fecha_carga, hora_entrega in respuesta_sql:
		if id_fecha_carga not in data:
			data[id_fecha_carga] = {}
		
		if dni not in data[id_fecha_carga]:
			data[id_fecha_carga][dni] = {
				"nombres_apellidos": f"{nombre} {apellidos}",
				"total_carga": 0,
				"n_cargas": 0,
				"cargas": []
			}
		
		# Actualizar el total de carga y el número de cargas
		data[id_fecha_carga][dni]["total_carga"] += float(peso_carga)
		data[id_fecha_carga][dni]["n_cargas"] += 1
		
		# Agregar carga a la lista de cargas
		data[id_fecha_carga][dni]["cargas"].append([float(peso_carga), hora_entrega])

	return data


if __name__ == '__main__':
	dataConfig = configuraciones()
	root = ctk.CTk()
	#root = tk.Tk()
	MainApp(root, dataConfig).pack()
	root.bind("<Escape>",exit)
	root.bind("<F5>", reinicio)
	root.mainloop()
























