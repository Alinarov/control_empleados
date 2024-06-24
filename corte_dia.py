#!/usr/bin/env python
import app
from app import * # aqui estoy importanto todas las funciones de mi ventana padre
import menu_registradora

class CorteDia(app.MainApp, tk.Toplevel):
	def __init__(self, parent, *args, **kargs):
		super().__init__(parent, configuraciones(), *args, **kargs)
		ctk.set_appearance_mode("dark") # tema principal
		self.parent = parent # 
		self.parent.title("Corte del dia")
		
				# Frames principales
		self.framePanelIzquierdo = ctk.CTkFrame(self.parent,
												 fg_color=self.dataConfig["tema_2"]["colorbg"]
												 )
		self.framePanelIzquierdo.pack(side="left", fill="both")

		self.framePanerRegistrosCargas = ctk.CTkFrame(self.parent,
													  fg_color=self.dataConfig["tema_3"]["colorbg"]
													  )
		self.framePanerRegistrosCargas.pack(fill="both", expand=True)

		# {+} Contenido frame izquierdo
		Imagen = ctk.CTkLabel(self.framePanelIzquierdo, text = "", image = CTkImage(light_image=Image.open("ventana.jpg"), 
			size=(200,200)))
		Imagen.pack(padx = 10, pady = 10)

		self.boton_menu = ctk.CTkButton(self.framePanelIzquierdo, text = "Menu", font = ("Cascadia Code", 24),
			image = CTkImage(light_image=Image.open("home.png"), size = (30,30)), command = lambda: self.volver())
		self.boton_menu.pack(side = "bottom", pady = 10)
		self.boton_menu.configure(width = (self.boton_menu.winfo_width() + 170))



		# {+} Contenido de los registros de los empleados que hicieron los cortes en un dia
		self.labelTituloCortesDia = ctk.CTkLabel(self.framePanerRegistrosCargas, 
			text="Corte del dia: xx/xx/xx Hora inicio: xx:xx Hora corte: xx:xx",
			text_color=self.dataConfig["tema_2"]["colordes"],
			font=("Cascadia Code", 16, "bold")
			)

		self.labelTituloCortesDia.pack(fill = "x")

		self.frameBuscar = ctk.CTkFrame(self.framePanerRegistrosCargas)
		self.frameBuscar.pack(fill = "x")

		self.inputBuscarEmpleado = ctk.CTkEntry(self.frameBuscar,
			validate='key', placeholder_text="Ingresar nombre del empleado",
			text_color= self.dataConfig["tema_2"]["colordes"],
							fg_color=self.dataConfig["tema_3"]["colorcp"]
			)
		self.inputBuscarEmpleado.pack(padx = 10, fill="x", side = "left", expand = True)

		# Imagen del botón de búsqueda
		self.boton_busqueda = ctk.CTkButton(self.frameBuscar, text="Buscar", 
			image = ctk.CTkImage(
				light_image=Image.open("lupa.png"),
				size=(20,20)
				),
			)
		self.boton_busqueda.pack(side="right", pady = 3, padx = 10)



		self.activar_scrollbar(self.framePanerRegistrosCargas)
		for i in range(50):
			self.boton= ctk.CTkButton(self.contenidoCanva, text=f"Registro {i} en la fecha: xx/xx/xxxx", 
				font = ("", self.dataConfig["tamanoLetraRegistrosHistorialCarga"]),
				anchor = "w",
				fg_color = self.dataConfig["tema_2"]["colorbg"],
				text_color = self.dataConfig["tema_2"]["colordes"]
				)
			self.boton.pack(padx = 10, pady = 3, fill = "x", expand = True)
			self.boton.bind("<MouseWheel>", self._on_mousewheel)



	def _on_mousewheel(self, event):
		# Realizar el desplazamiento cuando se utiliza la rueda del mouse
		self.canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

	def volver(self):
		print("ojpads")
		menu_registradora.Menu_registradora(self.parent)
		self.destroy()
		##self.parent.deiconify()
		##self.destroy()

if __name__ == '__main__':
	root = ctk.CTk()
	menu_dueno = CorteDia(root)
	menu_dueno.pack()
	root.bind("<Escape>", exit)
	root.bind("<F5>", reinicio)
	root.mainloop()
