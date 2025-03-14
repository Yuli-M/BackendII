# Migración de Datos a MySQL (Baja California)

## Descripción
Migrar datos relacionados con la distribución geográfica de las Unidades Económicas en estado de Baja California a una base de datos MySQL. La información incluye datos geográficos, actividades económicas, contactos y más, proporcionando un contexto sobre las unidades económicas del estado.

### Archivos incluidos

- **inegiBCnormalizacion.xlsx:** Ejemplo de normalización de datos en formato Excel. Contiene las ocho tablas, cada una en una hoja diferente.
- **CREATEDATABASE.txt:** Contiene el script SQL para crear la base de datos y las tablas necesarias. La base de datos fue creada utilizando MySQL en un contenedor Docker y gestionada a través de DBeaver.
- **queryInsertCsv.py:** Script en Python que implementa el proceso ETL (Extract, Transform, Load) para cargar los datos en la base de datos.

---

## Proceso ETL (Extract, Transform, Load)
El método utilizado para migrar los datos es el proceso ETL, que se describe a continuación:

### Extract (Extracción)
El script lee los datos desde archivos CSV utilizando el módulo `csv` de Python.

### Transform (Transformación)
Se realizan diversas transformaciones para asegurar la compatibilidad de los datos:
- **Fechas:** Convertir el formato `DD/MM/YYYY` a `YYYY-MM-DD`.
- **Texto (VARCHAR):** Limpiar y formatear cadenas de texto.
- **Números (INT):** Convertir cadenas numéricas o valores nulos a tipos compatibles (INT o NULL).
- **Estructuras espaciales (POINT):** Crear objetos espaciales usando `ST_GeomFromText()`.
- **JSON:** Manejar valores nulos o vacíos como arrays vacíos (`[]`).

### Load (Carga)
Los datos transformados se cargan en la base de datos MySQL utilizando la instrucción `INSERT INTO`, ejecutada mediante `cursor.executemany()`.
Esta técnica permite inserciones masivas, optimizando el rendimiento al evitar realizar inserciones una por una.

---

## Tecnologías Utilizadas
- **Python 3**: Para el procesamiento de datos y migración.
- **MySQL Connector**: Para conectarse a la base de datos y realizar operaciones SQL.
- **Docker**: Para gestionar el entorno de la base de datos.
- **DBeaver**: Interfaz gráfica para administrar la base de datos MySQL.

---

## Instrucciones de Uso

### 1. Preparación del Archivo CSV
Colocar el archivo CSV correspondiente en la misma carpeta donde se encuentra el script. El nombre del archivo debe coincidir con el nombre de la tabla (por ejemplo, `direcciones.csv` para la tabla `direcciones`).

### 2. Configuración del Script
Editar el valor de la variable `tabla_seleccionada` en el script para indicar la tabla que se desea cargar:
```python
tabla_seleccionada = "direcciones"
```

### 3. Ejecución del Script
Ejecutar el script desde un entorno virtual (opcional):
```bash
python3 queryInsertCsv.py
```

El script mostrará el número de registros insertados o los errores encontrados durante el proceso.

---

## Apartado de Tablas
El script utiliza un diccionario para definir la estructura de columnas y tipos de datos de cada tabla:
```python
tablas = {
    "establecimientos": {
        "columns": ["id", "nom_estab", "latitud", "longitud", "ubicacion"],
        "types": ["INT", "VARCHAR", "DECIMAL", "DECIMAL", "POINT"]
    },
    "direcciones": {
        "columns": ["id_establecimiento", "raz_social", "cod_postal", "id_actividad", "id_tipo_vialidad", "nom_vial", "numero_ext", "edificio", "edificio_e", "id_tipo_asent", "nomb_asent", "id_municipio", "id_localidad", "fecha_alta"],
        "types": ["INT", "VARCHAR", "INT", "INT", "INT", "VARCHAR", "VARCHAR", "VARCHAR", "VARCHAR", "INT", "VARCHAR", "INT", "INT", "DATE"]
    }
}
```

### Agregar una Nueva Tabla
Para agregar una nueva tabla, se tiene que añadir una entrada en el diccionario `tablas`, especificando:
1. El nombre de la tabla como clave.
2. Una lista de columnas en el campo `"columns"`.
3. Los tipos de datos correspondientes en el campo `"types"`.

**Ejemplo:**
```python
tablas["nueva_tabla"] = {
    "columns": ["id", "nombre", "fecha_creacion", "descripcion"],
    "types": ["INT", "VARCHAR", "DATE", "TEXT"]
}
```

---

## ¿ placeholders?
Los *placeholders* (`%s`) se usan para evitar ataques de inyección SQL y para manejar los valores de manera dinámica, permite:
- Crear consultas preparadas que se ejecutan con múltiples conjuntos de datos.
- Mejorar el rendimiento al realizar inserciones en bloque con `executemany()`.
- Garantizar la seguridad evitando concatenación de cadenas directamente en la consulta SQL.

---


