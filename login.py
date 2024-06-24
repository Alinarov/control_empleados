#!/usr/bin/env python
# Registro de Pesos: Control de cargas de Empleados
import app
from app import *
from tkinter import messagebox as mensaje
from comunicacion import SQLServerManager, SQLServerConnector, verificador
import codificador_descodificador 
import threading
import menu_administrador
import menu_registradora


class Login(app.MainApp):
	def __init__(self, parent):
		super().__init__(parent)
		self.dataConfig = configuraciones()
		ctk.set_appearance_mode("dark")  
		self.parent = parent
		self.parent.title("Aministrador de la empresa")
		self.parent.geometry(f"440x440+300+100")
		self.parent.resizable(False, False)
		self.parent.iconbitmap("setup_installer/icono.ico")  # Asegúrate de que la ruta sea correcta

		self.fondo_menu_image = Image.open("login.jpg")  
		self.fondo_menu_image_tk = ImageTk.PhotoImage(self.fondo_menu_image)  


		self.fondo_menu_label = ctk.CTkLabel(
			self.parent,
			image=self.fondo_menu_image_tk, 
			text="",
			font=("", 40, "bold"),
			text_color="#9AD0C2"
		)
		self.fondo_menu_label.place(x=0, y=0, relwidth=1, relheight=1)

		self.mensaje = ctk.CTkLabel(
			self.fondo_menu_label,
			text="¡Bienvenido al Panel de Control de Cargas de Empleados! \nSimplifica la gestión de tareas y supervisa el rendimiento de tu equipo de manera eficiente. \n (C) 2005 Alina Krasnaya https://alinakrasnaya.itch.io/",
			fg_color="#F1FADA", text_color="#2D9596", bg_color="#9AD0C2", justify=tk.CENTER,
			font=("", 11), cursor = "hand2", corner_radius = 16
		)
		self.mensaje.place(relx=0.5, rely= 0.9, anchor = "center")
		self.mensaje.bind("<Button-1>", lambda e: webbrowser.open_new("https://alinakrasnaya.itch.io/"))
		self.parent.bind("<Configure>", self.resize_image)


		self.username_entry = ctk.CTkEntry(self.parent, placeholder_text="Nombre de Usuario",
											border_width=1, border_color="#2D9596", corner_radius=8,
											width=208, font=("", 12), bg_color="#3C5B6F")
		self.username_entry.place(relx=0.29, rely=0.329)

		self.password_entry = ctk.CTkEntry(self.parent, placeholder_text="Contraseña",
											border_width=1, border_color="#2D9596", corner_radius=8,
											width=208, show="*", font=("", 12), bg_color="#3C5B6F")
		self.password_entry.place(relx=0.2, rely=0.488)




		self.boton1 = ctk.CTkButton(self.parent, text="LOGIN", fg_color="#fff", compound="top", 
									text_color="#111", font=("Cascadia Code", 19, "bold"), bg_color="#58A399",
									width = 230, height = 39, command = self.start_login)
		self.boton1.place(relx=0.48, rely=0.732, anchor='center')


		self.last_width = self.parent.winfo_width()
		self.last_height = self.parent.winfo_height()

		self.informacion = ctk.CTkButton(self.parent, text="", 
			command= lambda: mensaje.showinfo(
				message=(
					"Para iniciar sesión, por favor asegúrate de cumplir con las siguientes condiciones:\n\n"
					"1. El usuario y la contraseña no deben estar vacíos.\n"
					"2. El usuario y la contraseña no deben contener espacios.\n"
					"3. El usuario debe tener al menos 3 caracteres.\n"
					"4. La contraseña debe tener al menos 6 caracteres.\n"
					"5. El nombre de usuario debe ser alfanumérico (solo letras y números).\n\n"
					"# --------------- NO TE PREOCUPES ---------------\n"
					"Si te has equivocado de contraseña o no estás seguro de la contraseña que has ingresado, "
					"puedes registrarte de nuevo con el mismo usuario y la contraseña se reemplazará por la nueva."
				), title="Condiciones para iniciar sesión"
			),
			fg_color = "#fff", font = ("",14, "bold"), image = ctk.CTkImage (
				light_image=Image.open("setup_installer/informacion.png"),
				size=(30, 30)
				),
			width = 30, height = 30, bg_color = "#547c7b"
			)
		self.informacion.place(x = 360, y = 270)

		self.ocultar_mostrar_contra = ctk.CTkButton(self.parent, text="", 
			command= self.mostrar_ocultar_contra ,
			font = ("",14, "bold"), image = ctk.CTkImage (
				light_image=Image.open("setup_installer/ocultar-contrasena.png"),
				size=(30, 30)
				),
			width = 30, height = 30, bg_color = "#41aea9", fg_color = "#FCDC94"
			)
		self.ocultar_mostrar_contra.place(x = 360, y = 210)



	def start_login(self):
		# Iniciar el proceso de configuración en un hilo separado
		threading.Thread(target=lambda : mensaje.showinfo(message="Un ratito estoy verificando para iniciar sesion en la cuenta, esto no tardara mucho :3", title = "Iniciando sesion")).start()
		threading.Thread(target=self.login).start()



	def login(self):
		usuario = self.username_entry.get().strip()
		usuario_codificado = codificador_descodificador.codificar_base64(usuario)

		contrasenia = self.password_entry.get().strip()
		contrasenia_codificada = codificador_descodificador.codificar_base64(contrasenia)

		if not usuario or not contrasenia:
			mensaje.showerror(message="Necesitas proporcionar credenciales válidas.\nPor favor, ingrese un usuario y una contraseña.", title="Error de login")
		elif " " in usuario or " " in contrasenia:
			mensaje.showerror(message="El usuario y la contraseña no deben contener espacios.", title="Error de login")
		elif not usuario.isalnum():
			mensaje.showerror(message="El nombre de usuario debe ser alfanumérico.", title="Error de login")
		else:
			print(f"Usuario: {usuario}")
			print(f"Contraseña: {contrasenia}")

			verificador_respuesta = verificador(usuario_codificado, contrasenia_codificada)
			
			if verificador_respuesta:
				if "A" in verificador_respuesta:
					mensaje.showinfo(message="¡Bienvenido Admin al Panel de Control de Cargas de Empleados :3", title="Mensaje de bienvenida :) al admin")
					self.parent.withdraw()  # Ocultar la ventana actual
					admin_window = menu_administrador.Menu_administrador(self.parent)
					admin_window.deiconify()  # Mostrar la ventana de administrador
				elif "U" in verificador_respuesta:
					mensaje.showinfo(message="¡Bienvenido Usuario al Panel de Control de Cargas de Empleados :3", title="Mensaje de bienvenida :) al registrador")
					self.parent.withdraw()  # Ocultar la ventana actual
					user_window = menu_registradora.Menu_registradora(self.parent)
					user_window.deiconify()  # Mostrar la ventana de usuario
				else:
					mensaje.showerror(message="Al parecer las credenciales que has ingresado no son las correctas, vuelve por favor a ingresar nuevamente", title="Error de inicio de sesion de la cuenta")
			else:
				mensaje.showerror(message="Al parecer las credenciales que has ingresado no son las correctas, vuelve por favor a ingresar nuevamente", title="Error de inicio de sesion de la cuenta")



	def mostrar_ocultar_contra(self):
		if self.password_entry.cget('show') == '':
			self.password_entry.configure(show='*')
			self.ocultar_mostrar_contra.configure(image = ctk.CTkImage (
				light_image=Image.open("setup_installer/mostrar-contrasena.png"),
				size=(30, 30)
				),
				fg_color = "#55AD9B"
			)
		else:
			self.password_entry.configure(show='')
			self.ocultar_mostrar_contra.configure(image = ctk.CTkImage (
				light_image=Image.open("setup_installer/ocultar-contrasena.png"),
				size=(30, 30)
				),
				fg_color = "#FCDC94",
			)

	def resize_image(self, event):
		width = event.width
		height = event.height

		# Se verifica si el cambio en el tamaño de la ventana es significativo
		if abs(width - self.last_width) > 10 or abs(height - self.last_height) > 10:
			resized_image = self.fondo_menu_image.resize((width, height))
			self.fondo_menu_image_tk = ImageTk.PhotoImage(resized_image)
			self.fondo_menu_label.configure(image=self.fondo_menu_image_tk)

			# Se actualizan las dimensiones anteriores
			self.last_width = width
			self.last_height = height


if __name__ == '__main__':
	root = ctk.CTk()
	menu_dueno = Login(root)
	menu_dueno.pack(fill='both', expand=True)  
	root.bind("<Escape>", exit)
	root.bind("<F5>", reinicio)
	root.mainloop()
