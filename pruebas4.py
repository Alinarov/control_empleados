import json
from decimal import Decimal

# Respuesta de la consulta SQL
respuesta_sql = [
    ('Ana', 'Martinez', '98765432', Decimal('30.00'), '2024-03-20', '11:00:00'),
    ('Ana', 'Martinez', '98765432', Decimal('55.25'), '2024-03-20', '14:00:00'),
    ('Ana', 'Martinez', '98765432', Decimal('35.00'), '2024-03-20', '18:00:00'),
    ('Ana', 'Martinez', '98765432', Decimal('50.00'), '2024-03-20', '20:00:00'),
    ('Juan', 'Perez', '12345678', Decimal('20.50'), '2024-03-20', '08:00:00'),
    ('Juan', 'Perez', '12345678', Decimal('40.75'), '2024-03-20', '15:00:00'),
    ('Juan', 'Perez', '12345678', Decimal('90.25'), '2024-03-20', '17:00:00'),
    ('Juan', 'Perez', '12345678', Decimal('75.50'), '2024-03-20', '22:00:00'),
    ('Maria', 'Gonzalez', '87654321', Decimal('50.75'), '2024-03-20', '09:00:00'),
    ('Maria', 'Gonzalez', '87654321', Decimal('70.00'), '2024-03-20', '12:00:00'),
    ('Maria', 'Gonzalez', '87654321', Decimal('25.75'), '2024-03-20', '19:00:00'),
    ('Maria', 'Gonzalez', '87654321', Decimal('65.25'), '2024-03-20', '21:00:00'),
    ('Pedro', 'Lopez', '23456789', Decimal('80.25'), '2024-03-20', '10:00:00'),
    ('Pedro', 'Lopez', '23456789', Decimal('45.50'), '2024-03-20', '13:00:00'),
    ('Pedro', 'Lopez', '23456789', Decimal('60.50'), '2024-03-20', '16:00:00'),
    ('Pedro', 'Lopez', '23456789', Decimal('85.25'), '2024-03-20', '23:00:00')
]

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
            "dni": dni,
            "n_cargas": 0,
            "cargas": []
        }
    
    # Actualizar el total de carga y el número de cargas
    data[id_fecha_carga][dni]["total_carga"] += float(peso_carga)
    data[id_fecha_carga][dni]["n_cargas"] += 1
    
    # Agregar carga a la lista de cargas
    data[id_fecha_carga][dni]["cargas"].append([float(peso_carga), hora_entrega])

# Convertir a formato JSON
json_data = json.dumps(data, indent=4)

# Imprimir el JSON resultante
print(json_data)
