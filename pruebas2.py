import tkinter as tk
from tkinter import Button

class Ventana2(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Ventana 2")
        self.parent = parent
        self.geometry("740x440")
        self.iconbitmap("setup_installer/icono.ico")  # Ruta al icono

        # Botón para cerrar la ventana 2 y volver a la ventana 1
        btn_volver_ventana1 = Button(self, text="Volver a Ventana 1", command=self.volver_ventana1)
        btn_volver_ventana1.pack(pady=20)

    def volver_ventana1(self):
        # Destruye la ventana actual
        self.destroy()
        
        # Muestra la ventana principal nuevamente
        self.parent.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    app = Ventana2(root)
    app.mainloop()


# import app
# from app import *
# from tkinter import messagebox as mensaje
# from comunicacion import SQLServerManager, SQLServerConnector, verificador
# import codificador_descodificador 
# import threading
# import menu_administrador
# import menu_registradora



# class Menu_administrador(ctk.CTkToplevel, app.MainApp):
#     def __init__(self, parent, *args, **kwargs):
#         super().__init__(parent, *args, **kwargs)
#         self.title("Panel de Administración")
#         self.geometry("800x600")
#         ctk.set_appearance_mode("dark")  
#         label = tk.Label(self, text="Bienvenido Admin")
#         label.pack(pady=20)

# class Menu_registradora(tk.Toplevel):
#     def __init__(self, parent, *args, **kwargs):
#         super().__init__(parent, *args, **kwargs)
#         self.title("Panel de Registro")
#         self.geometry("800x600")
#         label = tk.Label(self, text="Bienvenido Usuario")
#         label.pack(pady=20)

# class LoginApp(ctk.CTk):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.geometry("400x300")
#         self.title("Login")
#         self.username_entry = tk.Entry(self)
#         self.username_entry.pack(pady=10)
#         self.password_entry = tk.Entry(self, show="*")
#         self.password_entry.pack(pady=10)
#         self.login_button = tk.Button(self, text="Login", command=self.login)
#         self.login_button.pack(pady=10)

#     def login(self):
#         usuario = "dani"#self.username_entry.get().strip()
#         usuario_codificado = codificador_descodificador.codificar_base64(usuario)

#         contrasenia = "123456"#self.password_entry.get().strip()
#         contrasenia_codificada = codificador_descodificador.codificar_base64(contrasenia)

#         if not usuario or not contrasenia:
#             mensaje.showerror(message="Necesitas proporcionar credenciales válidas.\nPor favor, ingrese un usuario y una contraseña.", title="Error de login")
#         elif " " in usuario or " " in contrasenia:
#             mensaje.showerror(message="El usuario y la contraseña no deben contener espacios.", title="Error de login")
#         elif not usuario.isalnum():
#             mensaje.showerror(message="El nombre de usuario debe ser alfanumérico.", title="Error de login")
#         else:
#             print(f"Usuario: {usuario}")
#             print(f"Contraseña: {contrasenia}")

#             verificador_respuesta = verificador(usuario_codificado, contrasenia_codificada)

#             if verificador_respuesta:
#                 if "A" in verificador_respuesta:
#                     mensaje.showinfo(message="¡Bienvenido Admin al Panel de Control de Cargas de Empleados!", title="Mensaje de bienvenida al admin")
#                     self.withdraw()  # Ocultar la ventana actual
#                     admin_window = menu_administrador.Menu_administrador(self)
#                     admin_window.deiconify()  # Mostrar la ventana de administrador
#                 elif "U" in verificador_respuesta:
#                     mensaje.showinfo(message="¡Bienvenido Usuario al Panel de Control de Cargas de Empleados!", title="Mensaje de bienvenida al registrador")
#                     self.withdraw()  # Ocultar la ventana actual
#                     user_window = menu_registradora.Menu_registradora(self).pack(fill='both', expand=True)  
#                     user_window.deiconify()  # Mostrar la ventana de usuario
#                 else:
#                     mensaje.showerror(message="Credenciales incorrectas. Por favor, vuelve a intentarlo.", title="Error de inicio de sesión")
#             else:
#                 mensaje.showerror(message="Credenciales incorrectas. Por favor, vuelve a intentarlo.", title="Error de inicio de sesión")

# if __name__ == "__main__":
#     app = LoginApp()
#     app.mainloop()
