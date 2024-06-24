:: ldc2 -shared -of codificador_decodificador.so codificador_decodificador.d
::dmd -m64 -shared -ofcodificador.dll codificador_decodificador.d
:: pip install CTkListbox
:: pip install reportlab
::pip install pyinstaller


rem pip install tkinter
rem pip install  pillow 
rem pip install tkcalendar
rem pip install  customtkinter
rem pip install  pyodbc

rem pip install --upgrade tkinter 
rem pip install --upgrade pillow
rem pip install --upgrade tkcalendar
rem pip install --upgrade customtkinter
rem pip install --upgrade pyodbc
rem pip install --upgrade babel

rem pip show babel
rem pip install auto-py-to-exe
where python
:: C:\Users\dani\AppData\Local\Programs\Python\Python312\Lib\site-packages\babel
:: C:\Users\dani\AppData\Local\Programs\Python\Python312\Lib\site-packages\tkcalendar

rem pyinstaller --onefile login.py

pyinstaller --onefile --windowed --add-data "C:/Users/dani/AppData/Local/Programs/Python/Python312/Lib/site-packages/tkcalendar;tkcalendar" --add-data "C:/Users/dani/AppData/Local/Programs/Python/Python312/Lib/site-packages/babel;babel" login.py


rem pyinstaller --onefile --windowed --add-data "C:\Users\dani\AppData\Local\Programs\Python\Python312\Lib\site-packages\tkcalendar;tkcalendar" --add-data "C:\Ruta\Al\Python\Lib\site-packages\babel;babel" archivo_principal.py




::pip install ctypes 




