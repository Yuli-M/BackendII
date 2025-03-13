import mysql.connector
import csv

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="establecimientosBC_db"
)
cursor = conexion.cursor()

tablas = {
    "establecimientos": {
        "columns": ["id", "nom_estab", "latitud", "longitud", "ubicacion"],
        "types": ["INT", "VARCHAR", "DECIMAL", "DECIMAL", "POINT"]
    },
    "direcciones": {
        "columns": ["id_establecimiento", "raz_social", "cod_postal", "id_actividad", "id_tipo_vialidad", "nom_vial", "numero_ext", "edificio", "edificio_e", "id_tipo_asent", "nomb_asent", "id_municipio", "id_localidad", "fecha_alta"],
        "types": ["INT", "VARCHAR", "INT", "INT", "INT", "VARCHAR", "VARCHAR", "VARCHAR", "VARCHAR", "INT", "VARCHAR", "INT", "INT", "DATE"]
    },
    "contactos": {
        "columns": ["id_establecimiento", "telefono", "correoelec", "www", "nivel_contacto"],
        "types": ["INT", "JSON", "JSON", "JSON", "TINYINT"]
    },
    "localidades": {
        "columns": ["id_localidad", "localidad"],
        "types": ["INT", "VARCHAR"]
    },
    "actividades": {
        "columns": ["id_actividad", "nombre_act"],
        "types": ["INT", "VARCHAR"]
    },
    "vialidades": {
        "columns": ["id_tipo_vialidad", "tipo_vialidad"],
        "types": ["INT", "VARCHAR"]
    },
    "municipios": {
        "columns": ["id_municipio", "municipio"],
        "types": ["INT", "VARCHAR"]
    },
    "asentamientos": {
        "columns": ["id_tipo_asent", "tipo_asent"],
        "types": ["INT", "VARCHAR"]
    }
}

tabla_seleccionada = "direcciones"  #######
csv_file = f"{tabla_seleccionada}.csv"
# num_registros = 10  # pruebas

try:
    with open(csv_file, mode='r') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)
        columnas = ', '.join(headers)
        valores = []

        for index, row in enumerate(csv_reader):
            # pruebas
            # if index >= num_registros:
            #     break
            
            if not row:  # saltar vacias
                continue
            
            formatted_values = []
            for i, valor in enumerate(row):
                tipo = tablas[tabla_seleccionada]["types"][i]

                ##valor = valor.strip('"').replace("'", "''")
                valor = valor.strip().strip('"').replace("'", "''")

                if tipo == "VARCHAR":
                    formatted_values.append(valor)
                elif tipo == "JSON":
                    if valor == "0" or not valor: 
                        formatted_values.append('[]')  # array vacio
                    else:
                        formatted_values.append(f'["{valor}"]') #array JSON (?)
                elif tipo == "POINT":
                    latitud = row[2]  
                    longitud = row[3] 
                    formatted_values.append(f"POINT({longitud} {latitud})")
                elif tipo == "DATE":
                    #DD/MM/YYYY a YYYY-MM-DD
                    if "/" in valor:
                        dia, mes, anio = valor.split("/")
                        valor = f"{anio}-{mes.zfill(2)}-{dia.zfill(2)}"
                    formatted_values.append(valor)
                elif tipo == "INT":
                    if valor == "" or not valor.isdigit(): # or valor == "0"
                        formatted_values.append(None)  # NULL, 
                    else:
                        formatted_values.append(int(valor))  # int

            #print(f"Cantidad de columnas: {len(row)}, Valores formateados: {len(formatted_values)}")
            valores.append(tuple(formatted_values))
            ## print({valores})
            
        # placeholders
        placeholders = ', '.join(['%s'] * len(headers))

        #point
        if "POINT" in tablas[tabla_seleccionada]["types"]:
            index_point = tablas[tabla_seleccionada]["types"].index("POINT")
            placeholders_list = ['%s'] * len(headers)
            placeholders_list[index_point] = "ST_GeomFromText(%s)"
            placeholders = ', '.join(placeholders_list)

        query = f"INSERT INTO {tabla_seleccionada} ({columnas}) VALUES ({placeholders})"
        print(f"Query: {query}")
        print(valores)
        try:
            cursor.executemany(query, valores)
            conexion.commit()
            print( {cursor} )
            print(f"Se insertaron {cursor.rowcount} registros, en la tabla {tabla_seleccionada}")
        except mysql.connector.Error as e:
            print(f"Error al insertar en la tabla {tabla_seleccionada}: {e}")
finally:
    cursor.close()
    conexion.close()
