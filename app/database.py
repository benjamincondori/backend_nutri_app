import os
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Cargar las configuraciones de la base de datos
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# Inicializar la instancia de SQLAlchemy
db = SQLAlchemy()
migrate = Migrate()
def create_database():
    """Crea la base de datos si no existe.

    Conecta a la base de datos por defecto de PostgreSQL y ejecuta
    un comando SQL para crear la base de datos especificada. 
    Maneja el caso donde la base de datos ya existe.
    """
    try:
        # Conectar a PostgreSQL (sin especificar la base de datos)
        connection = psycopg2.connect(
            dbname="postgres",  # Conectar a la base de datos por defecto
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        connection.autocommit = True  # Permitir autocommit para crear la base de datos
        cursor = connection.cursor()

        # Crear la base de datos si no existe
        cursor.execute(f"CREATE DATABASE {DB_NAME};")
        print(f"Base de datos '{DB_NAME}' creada exitosamente.")
    except psycopg2.errors.DuplicateDatabase:
        # Manejar el caso donde la base de datos ya existe
        print(f"La base de datos '{DB_NAME}' ya existe.")
    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

def configure_app(app):
    """Configura la aplicación Flask con la URI de la base de datos.

    Args:
        app: Instancia de la aplicación Flask que se configurará.
    """
    # Configurar la URI de la base de datos en la aplicación
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Deshabilitar el seguimiento de modificaciones
    db.init_app(app)  # Inicializar SQLAlchemy con la aplicación
    migrate.init_app(app, db)  # Inicializar Flask-Migrate con la aplicación y la instancia de SQLAlchemy