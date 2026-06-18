Fleet Management API

API REST para la gestión de una flota de taxis y sus trayectorias geográficas, construida con Flask y PostgreSQL. Permite consultar taxis, su historial de ubicaciones por fecha y la última posición registrada de cada vehículo.

El proyecto incluye una suite de pruebas automatizadas (unitarias con pytest y de endpoint con Postman/Newman) que valida el comportamiento de cada endpoint, incluyendo casos de éxito y manejo de errores.


Tecnologías


Python 3 — lenguaje principal
Flask — framework web
Flask-SQLAlchemy — ORM para el acceso a datos
PostgreSQL — base de datos relacional
psycopg — driver de conexión a PostgreSQL
pytest — pruebas unitarias
Postman / Newman — pruebas de endpoint



Modelo de datos

La base de datos contiene dos tablas relacionadas:


taxis: información de cada taxi (id, plate).
trajectories: registros de ubicación de cada taxi (id, taxi_id, date, latitude, longitude), donde taxi_id es una clave foránea que referencia a taxis.id.


La carga inicial incluye 200 taxis y más de 18.000 registros de trayectorias.


Endpoints implementados

1. Listar taxis

GET /taxis

Devuelve el listado de taxis con su id y plate.

Parámetros de consulta (opcionales):


page — número de página (por defecto 1)
limit — resultados por página (por defecto 10)
plate — filtra taxis cuya placa contenga el texto indicado


Ejemplo: GET /taxis?plate=GH&limit=5


2. Historial de ubicaciones de un taxi

GET /trajectories?taxiId={id}&date={DD-MM-AAAA}

Devuelve las trayectorias (latitude, longitude, timestamp) de un taxi en una fecha específica.

Parámetros (obligatorios):


taxiId — id del taxi
date — fecha en formato DD-MM-AAAA


Respuestas:


200 — lista de trayectorias
400 — si falta taxiId o date, o si la fecha tiene formato inválido
404 — si el taxi no existe


Ejemplo: GET /trajectories?taxiId=6418&date=02-02-2008


3. Última ubicación de cada taxi

GET /trajectories/latest

Devuelve la última ubicación registrada de cada taxi, incluyendo id, plate, latitude, longitude y timestamp.


Instalación y ejecución

Requisitos previos


Python 3 instalado
PostgreSQL instalado y en ejecución


Pasos


Clonar el repositorio


bash   git clone https://github.com/estefanymoramellado/fleet-management-api.git
   cd fleet-management-api


Crear y activar un entorno virtual


bash   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate


Instalar las dependencias


bash   pip install -r requirements.txt


Crear la base de datos y cargar los datos

Crear una base de datos PostgreSQL llamada fleet_management.
Crear las tablas taxis y trajectories (ver scripts en la sección Base de datos).
Cargar los archivos SQL de taxis y trayectorias.



Configurar la conexión

Crear un archivo config.py en la raíz con los datos de conexión a la base de datos:





python     from urllib.parse import quote_plus

     DB_USER = "postgres"
     DB_PASSWORD = "tu_contraseña"
     DB_HOST = "localhost"
     DB_PORT = "5432"
     DB_NAME = "fleet_management"

     password_escaped = quote_plus(DB_PASSWORD)
     SQLALCHEMY_DATABASE_URI = (
         f"postgresql+psycopg://{DB_USER}:{password_escaped}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
     )


Nota: config.py está excluido del repositorio (.gitignore) para no exponer credenciales.



Ejecutar el servidor


bash   python app.py

La API quedará disponible en http://127.0.0.1:5000.


Base de datos

Scripts de creación de tablas:

sqlCREATE TABLE taxis (
    id INTEGER PRIMARY KEY,
    plate VARCHAR(10)
);

CREATE TABLE trajectories (
    id SERIAL PRIMARY KEY,
    taxi_id INTEGER REFERENCES taxis(id),
    date TIMESTAMP,
    latitude NUMERIC,
    longitude NUMERIC
);

El orden importa: primero se crea taxis, luego trajectories (que la referencia mediante clave foránea). De igual forma, se cargan primero los datos de taxis y después los de trayectorias.


Pruebas

Pruebas unitarias (pytest)

Con el entorno virtual activo y PostgreSQL en ejecución:

bashpytest -v

La suite cubre 13 pruebas: respuestas exitosas, estructura de los datos devueltos, validaciones de parámetros obligatorios y manejo de errores (400 y 404).

Pruebas de endpoint (Postman)

La carpeta postman/ contiene la colección y el environment. Se pueden ejecutar desde la aplicación Postman importando ambos archivos y activando el environment, o desde la línea de comandos con Newman.


Estado del proyecto

Implementado:


Carga de datos a PostgreSQL
Endpoint de listado de taxis (con paginación y filtro)
Endpoint de historial de ubicaciones por taxi y fecha
Endpoint de última ubicación de cada taxi
Pruebas unitarias y de endpoint para los endpoints anteriores