import json
from decimal import Decimal

import tkinter
import time 
from app import IndicadorCarga
import customtkinter as ctk
from comunicacion import SQLServerConnector

import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkcalendar import Calendar

class CustomCalendar(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Custom Calendar")
        self.geometry("300x250")

        self.calendar = Calendar(self, selectmode='day', date_pattern='dd/MM/yyyy')
        self.calendar.pack(padx=10, pady=10)

        self.button = ttk.Button(self, text="Select Date", command=self.get_selected_date)
        self.button.pack(pady=5)

        self.selected_date_label = ttk.Label(self, text="")
        self.selected_date_label.pack(pady=5)

    def get_selected_date(self):
        selected_date = self.calendar.get_date()
        self.selected_date_label.config(text=f"Selected Date: {selected_date}")

class MenuAdministrador(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Administrador")
        self.geometry("800x600")
        self.iconbitmap("setup_installer/icono.ico")

        self.open_calendar_button = ttk.Button(self, text="Open Calendar", command=self.open_calendar)
        self.open_calendar_button.pack(pady=20)

    def open_calendar(self):
        calendar_window = CustomCalendar(self)
        calendar_window.grab_set()  # Bloquea la ventana principal mientras está abierta la ventana del calendario
        calendar_window.wait_window()  # Espera hasta que se cierre la ventana del calendario

if __name__ == "__main__":
    app = MenuAdministrador()
    app.mainloop()


# con = SQLServerConnector()
# con.connect()


# respuesta_sql = con.execute_query("""INSERT INTO fecha_carga (id_fecha_carga, hora_inicio, hora_corte)
# VALUES 
#        ('2024-03-24', '08:15:00', '17:15:00'),
#        ('2024-03-25', '09:45:00', '18:45:00'),
#        ('2024-03-26', '07:00:00', '16:00:00'),
#        ('2024-03-27', '11:00:00', '20:00:00'),
#        ('2024-03-28', '08:30:00', '17:30:00'),
#        ('2024-03-29', '09:30:00', '18:30:00'),
#        ('2024-03-30', '07:45:00', '16:45:00'),
#        ('2024-03-31', '10:45:00', '19:45:00'),
#        ('2024-04-01', '08:00:00', '17:00:00'),
#        ('2024-04-02', '09:00:00', '18:00:00'),
#        ('2024-04-03', '07:30:00', '16:30:00'),
#        ('2024-04-04', '10:30:00', '19:30:00'),
#        ('2024-04-05', '08:15:00', '17:15:00'),
#        ('2024-04-06', '09:45:00', '18:45:00'),
#        ('2024-04-07', '07:00:00', '16:00:00'),
#        ('2024-04-08', '11:00:00', '20:00:00');
# """)




# print(respuesta_sql)

