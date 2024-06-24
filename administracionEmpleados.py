#!/usr/bin/env python
import app
from app import *
from PIL import Image

class MenuDueno(app.MainApp, tk.Toplevel):
	def __init__(self, parent, *args, **kargs):
		super().__init__(parent, configuraciones())
		ctk.set_appearance_mode("dark") # tema principal
		self.parent = parent
		color_fondo = self.dataConfig["tema_2"]["colorbg"]

		# Frames principales de la ventana
		self.frameBusqueda = ctk.CTkFrame(self.parent)
		self.frameBusqueda.configure(fg_color=self.dataConfig["tema_1"]["colorbg"])
		self.frameBusqueda.pack(fill="x")

		self.framePanelControl = ctk.CTkFrame(self.parent)
		self.framePanelControl.configure(fg_color= color_fondo)
		self.framePanelControl.pack(fill="both", expand=True)


		self.frameFooter = ctk.CTkFrame(self.parent)
		self.frameFooter.configure(fg_color=self.dataConfig["tema_3"]["colorbg"])
		self.frameFooter.pack(fill="both")

		# Elementos del sistema
		self.tituloVentana = ctk.CTkLabel(
			self.frameBusqueda,
			text="Administracion de empleados en la empresa",
			font=("Cascadia Code", 20, "bold")
		)
		self.tituloVentana.pack(padx=10, pady=5)

		self.casilla_busqueda = ctk.CTkEntry(
			self.frameBusqueda,
			height=1,
			font = ("", 16, "bold"),
			placeholder_text = "Ingresar el nombre de un empleado"
		)
		self.casilla_busqueda.pack(padx=10, pady=(5, 5), side="left", fill="x", expand=True)

		imagen_boton = ctk.CTkImage(
			light_image=Image.open("lupa.png"),
			size=(20, 20)
		)

		self.boton_busqueda = ctk.CTkButton(
			self.frameBusqueda,
			image=imagen_boton,
			text="Buscar",
			fg_color=self.dataConfig["tema_2"]["colordes"],
			text_color=self.dataConfig["tema_1"]["colordes"]
		)
		self.boton_busqueda.pack(side="right", padx=(0, 5))


		# {++++} Panel donde se ven los registros 
		self.inner_frame = ctk.CTkFrame(self.framePanelControl, fg_color = color_fondo)
		self.inner_frame.pack(fill = "both", expand = True)


		for i in range(13):
			ctk.CTkButton(self.inner_frame, text=f"hola {i}", 
				anchor="w", 
				font = ("", 16, "bold"),
				width = self.inner_frame.winfo_width()).pack(padx=10, pady=3, expand = True, fill = "x")

		# (+) Este es el paginador de la tabla
		Paginador(self.frameFooter, self.dataConfig["tema_3"]["colorbg"])

		# {++++} Frame de pie de página
		self.botonRegistrarNuevoEmpleado = ctk.CTkButton(
			self.frameFooter,
			text="Registrar nuevo empleado",
			image=ctk.CTkImage(
				light_image=Image.open("nuevoEmpleado.png"),
				size=(20, 20)
			)
		)
		self.botonRegistrarNuevoEmpleado.pack(padx=10, pady=10, side="right")

		self.boton_regresar = ctk.CTkButton(
			self.frameFooter,
			text="Regresar",
			image=ctk.CTkImage(
				light_image=Image.open("home.png"),
				size=(20, 20)
			)
		)
		self.boton_regresar.pack(padx=10, pady=10, side="left")
		# {++++} Frame de pie de página

if __name__ == '__main__':
	root = ctk.CTk()
	menu_dueno = MenuDueno(root)
	menu_dueno.pack()
	root.bind("<Escape>", exit)
	root.bind("<F5>", reinicio)
	root.mainloop()
