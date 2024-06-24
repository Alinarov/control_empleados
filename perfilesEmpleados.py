#!/usr/bin/env python
import app
from app import * # aqui estoy importanto todas las funciones de mi ventana padre


class FormPerfilesEmpleados(app.MainApp, tk.Toplevel):
	def __init__(self, parent, *args, **kargs):
		super().__init__(parent, configuraciones())
		ctk.set_appearance_mode("dark") # tema principal
		self.parent = parent # 
		self.parent.geometry(f"{self.ancho - 140}x{self.alto - 160}+300+100")
		# {+} Frames principales de la ventana
			# [+] Frame de opciones CRUD 
		self.frameOpciones = ctk.CTkFrame(parent, fg_color = self.dataConfig["tema_1"]["colorbg"])
		self.frameOpciones.pack(fill = "both", side = "left")

			# [+] Frame de formulario de los empleados
		self.frameFormulario = ctk.CTkFrame(parent, fg_color = self.dataConfig["tema_2"]["colorbg"],
			bg_color = self.dataConfig["tema_2"]["colorbg"])
		self.frameFormulario.pack(fill = "both", expand = True)

			# [+] Este frame es para que aparezca el email y la direccion del empleado
			# y como los textbox son largos y el self.frameFormulario esta en grid entonces por eso
			# este nuevo frame debe estar aparte
		self.frameFormularioOpcional = ctk.CTkFrame(parent, fg_color = self.dataConfig["tema_2"]["colorbg"], 
			bg_color = self.dataConfig["tema_2"]["colorbg"]
			)
		self.frameFormularioOpcional.pack(fill = "both")
			# [+] Frame footer

		self.frameFooter = ctk.CTkFrame(parent, fg_color=self.dataConfig["tema_3"]["colorbg"])
		self.frameFooter.pack(fill = "both", expand = True)

		# {-} Frames principales de la ventana


		# 
		# {+} Contenido de frame CRUD con la foto del empleado
			# [+] Foto del empleado
		self.fotoEmpleado = ctk.CTkLabel(
			self.frameOpciones, 
			text = "",
			image = ctk.CTkImage(
				light_image=Image.open("nuevoEmpleado.png"),
				size=(180,180)
				)
			)
		self.fotoEmpleado.grid(column = 0, row = 0, pady = 50, padx = 50)
			# [+] Botones CRUD
		
		self.botonRegistrar = ctk.CTkButton(self.frameOpciones, text = "Registrar Empleado")
		self.botonDespedir = ctk.CTkButton(self.frameOpciones, text = "Despedir")
		self.botonEditarDatos = ctk.CTkButton(self.frameOpciones, text = "Editar Datos")
		self.botonRegresarMenu = ctk.CTkButton(self.frameOpciones, text = "Regresar Menu")

		self.botones = (self.botonRegistrar, self.botonEditarDatos, self.botonDespedir, 
			self.botonRegresarMenu
		)

		nPosicionBoton = 0
		for botones in self.botones:
			nPosicionBoton = nPosicionBoton + 1
			botones.configure(font = ("", 19))
			botones.grid(row = nPosicionBoton, pady = 10)
		# {-} Contenido de frame CRUD con la foto del empleado

		# {+} Contenido de frame de formulario para los datos de los empleados

		# [+] Casillas de datos personales
			# (+) Columna 1
		self.labelNombre = ctk.CTkLabel(self.frameFormulario, text="Nombres")
		self.textNombre = ctk.CTkEntry(self.frameFormulario, placeholder_text="Ingresar Nombres")
		self.labelDni = ctk.CTkLabel(self.frameFormulario, text="Dni")
		self.textDni = ctk.CTkEntry(self.frameFormulario, placeholder_text="Ingresar DNI")
		self.labelFechaNacimiento = ctk.CTkLabel(self.frameFormulario, text="Fecha de nacimiento")
		self.textFechaNacimiento = DateEntry(self.frameFormulario)
		self.textFechaNacimiento.grid(row = 5)
		self.labelSexo = ctk.CTkLabel(self.frameFormulario, text="Sexo")
			# (+) Columna 2
		self.labelApellidos = ctk.CTkLabel(self.frameFormulario, text="Apellidos")
		self.textApellido = ctk.CTkEntry(self.frameFormulario, placeholder_text="Ingresar apellidos")
		self.labelTelefono1 = ctk.CTkLabel(self.frameFormulario, text="Ingresar telefono 1")		
				# (+) entradas de solo numeros para los telefonos
		vcmd = (self.frameFormulario.register(enter_only_digits), '%P', '%d')
		self.textTelenfono1 = ctk.CTkEntry(self.frameFormulario,
			validate='key', validatecommand=vcmd,  placeholder_text="Ingresar telefono 1")

		self.labelTelefono2 = ctk.CTkLabel(self.frameFormulario, text="Ingresar telefono 2")
		self.textTelenfono2 = ctk.CTkEntry(self.frameFormulario, placeholder_text="Ingresar telefono 2",
			validate='key', validatecommand=vcmd)
				# (-) entradas de solo numeros para los telefonos		
		self.labelFechaContrato = ctk.CTkLabel(self.frameFormulario, text="Fecha de contrato")
		self.textFechaContrato = DateEntry(self.frameFormulario)
		self.textFechaContrato.grid(row = 8, column = 1)
			# (+) Radio buton de sexo
		# [+] Radio buton del sexo
		self.radio_sexo = tk.IntVar(value=0)

		self.radiobutton_hombre = ctk.CTkRadioButton(self.frameFormulario, text="Hombre",
													 variable=self.radio_sexo,
													 text_color = self.dataConfig["tema_2"]["colordes"],
													 value=1)
		self.radiobutton_hombre.grid(row=8, column=0, sticky="w", padx = 10)  # Ajusta la posición como necesites

		self.radiobutton_mujer = ctk.CTkRadioButton(self.frameFormulario, text="Mujer",
													 variable=self.radio_sexo, 
													 text_color = self.dataConfig["tema_2"]["colordes"],
													 value=2)
		self.radiobutton_mujer.grid(row=9, column=0, sticky="w", padx = 10)  # Ajusta la posición como necesites



		# Agregar el último label de sexo y los radio botones a columna1
		self.columna1 = (
			self.labelNombre, self.textNombre, self.labelDni, self.textDni, 
			self.labelFechaNacimiento, self.textFechaNacimiento, self.labelSexo
		)
		self.nPosicionColumna1 = 0

		self.columna2 = (
			self.labelApellidos, self.textApellido, self.labelTelefono1, self.textTelenfono1,
			self.labelTelefono2, self.textTelenfono2, self.labelFechaContrato#, self.textFechaContrato
		)
		self.nPosicionColumna2 = 1

		self.textBox = (
			self.textNombre, self.textDni, self.textFechaNacimiento, self.textApellido,
			self.textTelenfono1, self.textTelenfono2, self.textFechaContrato
		)
		self.labeles = (
			self.labelNombre,
			self.labelDni,
			self.labelFechaNacimiento,
			self.labelApellidos,
			self.labelTelefono1,
			self.labelTelefono2,
			self.labelSexo,
			self.labelFechaContrato
		)
		nFila = 1
		# Configurar la altura de todas las textBoxes fuera del ciclo
		for textBox in self.textBox:
			try:
				textBox.configure(height=1, fg_color="white", text_color="black")
			except:
				pass
				

		# Configurar los colores de los labeles fuera del ciclo
		for label in self.labeles:
			label.configure(text_color= self.dataConfig["tema_2"]["colordes"],
							fg_color=self.dataConfig["tema_3"]["colorcp"])

		# Iterar sobre las listas
		for columna1, columna2 in zip(self.columna1, self.columna2):
			try: 
				columna1.grid(column=self.nPosicionColumna1, row=nFila, pady=5, padx = 10, sticky = "w")
				columna2.grid(column=self.nPosicionColumna2, row=nFila, padx=10, sticky = "w")
			except:
				pass
			nFila += 1
		

		# [+] Formulario opcional
		self.labelEmail = ctk.CTkLabel(self.frameFormularioOpcional, text="Email", anchor = "w",
			text_color=self.dataConfig["tema_2"]["colordes"],
			fg_color=self.dataConfig["tema_3"]["colorcp"],
			)
		self.labelEmail.pack(fill = "x", padx = 10)

		self.textEmail = ctk.CTkEntry(self.frameFormularioOpcional, placeholder_text = "Ingresar el correo electronico",
			fg_color = "white", text_color = "black")
		self.textEmail.pack(padx = 10, expand=True, fill="x") 

		self.labelDireccion = ctk.CTkLabel(self.frameFormularioOpcional, text="Direccion", 
			anchor = "w",
			text_color=self.dataConfig["tema_2"]["colordes"],
			fg_color=self.dataConfig["tema_3"]["colorcp"]
			)
		self.labelDireccion.pack(fill = "x", padx = 10)

		self.textDireccion = ctk.CTkEntry(self.frameFormularioOpcional, placeholder_text = "Ingresar direccion domiciliaria",
			fg_color = "white", text_color = "black")
		self.textDireccion.pack(padx = 10, expand=True, fill="x") 
		# [-] Formulario opcional

		# {+} Footer
			# [+] Boton de regresar al menu
		
		self.boton_regresar = ctk.CTkButton(
			self.frameFooter, 
			text = "Regresar",
			image = ctk.CTkImage(
				light_image=Image.open("home.png"),
				size=(30,30)
				),
			font = ("", 15,"bold")
			)
		self.boton_regresar.pack(padx = 10, pady = 10, side = "left")
		






if __name__ == '__main__':
	root = ctk.CTk()
	menu_dueno = FormPerfilesEmpleados(root)
	menu_dueno.pack()
	root.bind("<Escape>", exit)
	root.bind("<F5>", reinicio)
	root.mainloop()
