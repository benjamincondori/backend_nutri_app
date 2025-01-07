from flask import Flask
from flasgger import Swagger
from flask.cli import with_appcontext

from app.routes.user import user_bp
from app.routes.health_profile import health_profile_bp
from app.routes.health_objective import health_objective_bp
from app.routes.food import food_bp
from app.routes.physical_activity import physical_activity_bp
from app.routes.meal import meal_bp
from app.routes.plan import plan_meal_bp
from app.routes.meal_food import meal_food_bp

from app.extensions import ma
from app.routes.auth import auth_bp
from app.database import create_database, configure_app
from app.seed import seed_data, seed_users_health_profile, seed_food, seed_meal, seed_food_measures


def create_app():
    """
    Crea y configura la aplicación Flask.

    Returns:
        Flask: Instancia de la aplicación Flask configurada.
    """
    app = Flask(__name__)

    # Configurar Swagger
    Swagger(app)

    # Inicializar la base de datos y configuración
    create_database()  # Crear la base de datos si no existe
    configure_app(app)  # Configurar la base de datos para la app

    # Registrar extensiones
    ma.init_app(app)  # Inicializar la extensión Marshmallow

    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(health_profile_bp)
    app.register_blueprint(health_objective_bp)
    app.register_blueprint(food_bp)
    app.register_blueprint(physical_activity_bp)
    app.register_blueprint(meal_bp)
    app.register_blueprint(meal_food_bp)
    app.register_blueprint(plan_meal_bp)

    # Registrar comandos CLI
    register_cli_commands(app)

    return app


def register_cli_commands(app):
    """
    Registra comandos CLI personalizados para la aplicación.

    Args:
        app (Flask): Instancia de la aplicación Flask.
    """

    @app.cli.command("seed-physical-activities-db")
    @with_appcontext
    def seed_physical_activities_db():
        """
        Comando CLI para inicializar la base de datos con datos de actividades físicas.
        """
        seed_data()
        print("Base de datos inicializada con datos de actividades físicas.")

    @app.cli.command("seed-users-health-profiles-db")
    @with_appcontext
    def seed_users_health_profiles_db():
        """
        Comando CLI para inicializar la base de datos con usuarios y perfiles de salud.
        """
        seed_users_health_profile()
        print("Base de datos inicializada con usuarios y perfiles de salud.")

    @app.cli.command("seed-food-db")
    @with_appcontext
    def seed_food_db():
        """
        Comando CLI para inicializar la base de datos con alimentos.
        """
        seed_food()
        print("Base de datos inicializada con alimentos.")

    @app.cli.command("seed-meal-db")
    @with_appcontext
    def seed_meal_db():
        """
        Comando CLI para inicializar la base de datos con alimentos.
        """
        seed_meal()
        print("Base de datos inicializada con alimentos.")
    
    @app.cli.command("seed-measure-food-db")
    @with_appcontext
    def seed_measure_food_db():
        """
        Comando CLI para cargar la columna "measure" de la tabla Food.
        """
        seed_food_measures()
        print("Base de datos inicializada con alimentos.")

