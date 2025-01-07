import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash

from app.models.plan import Plan
from app.models.user import User
from app.routes.auth import token_required

from app.models.food import Food
from app.models.meal import Meal
from app.models.meal_food import MealFood

from app.schemas.user import UserSchema

from app.database import db

user_bp = Blueprint("user", __name__, url_prefix="/api/user")

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración de Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

@user_bp.route("/create", methods=["POST"])
def create():
    """
    1er registro de usuario (datos básicos).
    ---
    tags:
      - Registro  # Agrupación opcional
    parameters:
      - name: credenciales
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: nombre del usuario
              example: juan carlos
            lastname:
              type: string
              description: apellido del usuario
              example: gonzales perez
            telephone:
              type: string
              description: teléfono del usuario
              example: 74646527
            email:
              type: string
              description: correo del usuario
              example: juan@gmail.com
            password:
              type: string
              description: contraseña del usuario
              example: pass123
    responses:
      201:
        description: Registro exitoso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Usuario creado con éxito!"
            user_id:
              type: int
              description: "id del usuario" 
              example: 1
      400:
        description: Todos los campos son requeridos.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Todos los campos son requeridos."
      500:
        description: Error al crear el usuario.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Ocurrió un error al crear el usuario."
    """
    data = request.get_json()  # Obtener datos JSON del cuerpo de la solicitud

    # Validar que todos los campos requeridos están presentes
    required_fields = ['name', 'lastname', 'telephone', 'email', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Todos los campos son requeridos."}), 400

    name = data['name']
    lastname = data['lastname']
    telephone = data['telephone']
    email = data['email']
    password = data['password']

    # URL fija para la imagen de usuario
    url_image = "https://res.cloudinary.com/dnkvrqfus/image/upload/v1700017356/user_zmcosz.jpg"

    # Encriptar la contraseña antes de almacenarla
    password_hash = generate_password_hash(password)

    # Crear un nuevo usuario
    new_user = User(
        name=name,
        lastname=lastname,
        telephone=telephone,
        email=email,
        password=password_hash,  # Almacenar la contraseña encriptada
        url_image=url_image
    )

    # Guardar en la base de datos
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Usuario creado con éxito!", "user_id": new_user.id}), 201  # 201 Created
    except Exception as e:
        db.session.rollback()  # Hacer rollback en caso de error
        return jsonify({"message": f"Ocurrió un error al crear el usuario: {str(e)}"}), 500  # 500 Internal Server Error


@user_bp.route("/profile", methods=["GET"])
@token_required
def get_profile(current_user_id):
    """
    Obtener el perfil de un usuario.
    ---
    tags:
      - Usuarios
    parameters:
      - name: Authorization
        in: header
        required: true
        type: string
        description: Token JWT del usuario
        example: "Bearer <tu_token_aqui>"   
    responses:
      200:
        description: uusario encontrado
        schema:
          type: object
          properties:
            message:
              type: UserSchema()
              example:
                id:
              type: integer
              description: ID del usuario
              example: 2
            name:
              type: string
              description: Nombre del usuario
              example: juan marcos
            lastname:
              type: string
              description: Apellido del usuario
              example: gonzales perez
            telephone:
              type: string
              description: Teléfono del usuario
              example: 74646527
            email:
              type: string
              description: Correo electrónico del usuario
              example: juan@gmail.com
            url_image:
              type: string
              description: URL de la imagen del perfil
              example: https://res.cloudinary.com/dnkvrqfus/image/upload/v1700017356/user_zmcosz.jpg
            health_profile:
              type: object
              description: Perfil de salud del usuario
              properties:
                age:
                  type: int
                  description: edad del usuario
                  example: 27
                weight:
                  type: float
                  description: peso del usuario
                  example: 70.5
                height:
                  type: float
                  description: altura del usuario
                  example: 1.60
                physical_activity:
                  type: string
                  description: lista desplegable con las siguientes opociones de condición física (Sedentario, Actividad Ligera, Actividad Moderada, Actividad Intensa, Atleta)
                  example: Sedentario
                health_restrictions:
                  type: string
                  description: lista desplegable con las siguientes opociones de restriccioes de salud (Ninguna, Diabetes, Hipertensión, Asma, Alergias, Enfermedad cardíaca, Problemas articulares, Sobrepeso, Bajo peso, Trastornos alimenticios, Problemas de movilidad, Enfermedades respiratorias, Cáncer, Enfermedades neurológicas)
                  example: Enfermedad cardíaca    
      404:
        description: Error al crear el perfil de salud.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Usuario no encontrado" 
    """
    user = User.query.get(current_user_id)
    if user:
        return UserSchema().dump(user), 200
    return jsonify({"message": "Usuario no encontrado."}), 404


@user_bp.route("/profile/nutritionist", methods=["GET"])
@token_required
def get_nutritionist_profile(current_user_id):
    """
    Obtener el perfil de un nutricionista.
    ---
    tags:
      - Usuarios
    parameters:
      - name: Authorization
        in: header
        required: true
        type: string
        description: Token JWT del usuario
        example: "Bearer <tu_token_aqui>"
    responses:
      200:
        description: Nutricionista encontrado
        schema:
          type: object
          properties:
            message:
              type: object
              properties:
                id:
                  type: integer
                  description: ID del nutricionista
                  example: 2
                name:
                  type: string
                  description: Nombre del nutricionista
                  example: "Juan Marcos"
                lastname:
                  type: string
                  description: Apellido del nutricionista
                  example: "Gonzales Pérez"
                telephone:
                  type: string
                  description: Teléfono del nutricionista
                  example: "74646527"
                email:
                  type: string
                  description: Correo electrónico del nutricionista
                  example: "juan@gmail.com"
                url_image:
                  type: string
                  description: URL de la imagen del perfil
                  example: "https://res.cloudinary.com/dnkvrqfus/image/upload/v1700017356/user_zmcosz.jpg"
                role:
                  type: string
                  description: Rol del usuario
                  example: "nutritionist"
      404:
        description: Error al obtener el perfil.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Nutricionista no encontrado"
    """
    user = User.query.get(current_user_id)

    if user and user.type == "nutritionist":
        return jsonify({
            "id": user.id,
            "name": user.name,
            "lastname": user.lastname,
            "telephone": user.telephone,
            "email": user.email,
            "url_image": user.url_image,
            "type": user.type
        }), 200

    return jsonify({"message": "Nutricionista no encontrado."}), 404

@user_bp.route("/update", methods=["PUT"])
@token_required
def update_user(current_user_id):
    """
    Actualizar los datos del usuario.
    ---
    tags:
      - Usuarios
    parameters:
      - name: Authorization
        in: header
        required: true
        type: string
        description: Token JWT del usuario
        example: "Bearer <tu_token_aqui>"
      - name: datos
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: Nombre del usuario
              example: "Juan Carlos"
            lastname:
              type: string
              description: Apellido del usuario
              example: "Gonzales Perez"
            telephone:
              type: string
              description: Teléfono del usuario
              example: "74646527"
            email:
              type: string
              description: Correo electrónico del usuario
              example: "juan@gmail.com"
            health_profile:
              type: object
              description: Perfil de salud del usuario (solo para tipo 'user')
              properties:
                age:
                  type: int
                  description: Edad del usuario
                  example: 30
                weight:
                  type: float
                  description: Peso del usuario
                  example: 75.5
                height:
                  type: float
                  description: Altura del usuario
                  example: 1.75
                physical_activity:
                  type: string
                  description: Nivel de actividad física
                  example: "Actividad Moderada"
                health_restrictions:
                  type: string
                  description: Restricciones de salud
                  example: "Ninguna"
    responses:
      200:
        description: Usuario actualizado correctamente
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Usuario actualizado con éxito."
      404:
        description: Usuario no encontrado
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Usuario no encontrado."
      400:
        description: Datos inválidos
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Datos proporcionados no son válidos."
    """
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "Usuario no encontrado."}), 404

    # Obtener los datos del formulario
    name = request.form.get("name")
    lastname = request.form.get("lastname")
    telephone = request.form.get("telephone")
    email = request.form.get("email")
    image = request.files.get("image")
    age = request.form.get("age")
    weight = request.form.get("weight")
    height = request.form.get("height")
    physical_activity_id = request.form.get("physical_activity_id")
    health_restrictions = request.form.get("health_restrictions")

    try:
        # Actualizar campos comunes
        if name:
            user.name = name
        if lastname:
            user.lastname = lastname
        if telephone:
            user.telephone = telephone
        if email:
            user.email = email
        if image:
            # Subir imagen a Cloudinary
            upload_result = cloudinary.uploader.upload(image, folder='users')
            user.url_image = upload_result.get("secure_url")

        # Actualizar perfil de salud si el usuario es de tipo 'user'
        if user.type == "user":
            if age:
                user.health_profile.age = age
            if weight:
                user.health_profile.weight = weight
            if height:
                user.health_profile.height = height
            if physical_activity_id:
                user.health_profile.physical_activity_id = physical_activity_id
            if health_restrictions:
                user.health_profile.health_restrictions = health_restrictions

        # Solo datos básicos si es 'nutritionist'
        if user.type == "nutritionist":
            # No se actualiza health_profile para nutritionist
            pass

        db.session.commit()
        return jsonify({"message": "Usuario actualizado con éxito."}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error al actualizar el usuario: {str(e)}"}), 500


@user_bp.route("/users", methods=["GET"])
@token_required
def get_users(current_user_id):
    """
    Obtener todos los usuarios de tipo 'user'.
    ---
    tags:
      - Usuarios
    parameters:
      - name: Authorization
        in: header
        required: true
        type: string
        description: Token JWT del usuario
        example: "Bearer <tu_token_aqui>"
    responses:
      200:
        description: Lista de usuarios de tipo 'user'
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: ID del usuario
                example: 1
              name:
                type: string
                description: Nombre del usuario
                example: "Juan Carlos"
              lastname:
                type: string
                description: Apellido del usuario
                example: "Gonzales Perez"
              telephone:
                type: string
                description: Teléfono del usuario
                example: "74646527"
              email:
                type: string
                description: Correo electrónico del usuario
                example: "juan@gmail.com"
              url_image:
                type: string
                description: URL de la imagen del perfil
                example: "https://res.cloudinary.com/dnkvrqfus/image/upload/v1700017356/user_zmcosz.jpg"
      404:
        description: No se encontraron usuarios
        schema:
          type: object
          properties:
            message:
              type: string
              example: "No se encontraron usuarios."
    """
    # Consultar todos los usuarios de tipo 'user'
    users = User.query.filter_by(type="user").all()

    # Si no se encuentran usuarios
    if not users:
        return jsonify({"message": "No se encontraron usuarios."}), 404

    # Serializar los usuarios usando UserSchema
    users_data = UserSchema(many=True).dump(users)

    return jsonify(users_data), 200


@user_bp.route("/totals", methods=["GET"])
@token_required
def get_totals(current_user_id):
    """
    Obtener el total de usuarios, comidas, alimentos y planes generados.
    ---
    tags:
      - Estadísticas
    parameters:
      - name: Authorization
        in: header
        required: true
        type: string
        description: Token JWT del usuario
        example: "Bearer <tu_token_aqui>"
    responses:
      200:
        description: Totales obtenidos correctamente
        schema:
          type: object
          properties:
            total_users:
              type: integer
              description: Total de usuarios de tipo 'user'
              example: 100
            total_meals:
              type: integer
              description: Total de comidas
              example: 50
            total_foods:
              type: integer
              description: Total de alimentos
              example: 200
            total_plans:
              type: integer
              description: Total de planes generados
              example: 30
      500:
        description: Error al obtener los totales.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Ocurrió un error al obtener los totales."
    """
    try:
        # Contar usuarios de tipo 'user'
        total_users = User.query.filter_by(type='user').count()

        # Contar comidas
        total_meals = Meal.query.count()

        # Contar alimentos
        total_foods = Food.query.count()

        # Contar planes generados
        total_plans = Plan.query.count()

        # Devolver los resultados
        return jsonify({
            "total_users": total_users,
            "total_meals": total_meals,
            "total_foods": total_foods,
            "total_plans": total_plans
        }), 200
    except Exception as e:
        return jsonify({"message": f"Ocurrió un error al obtener los totales: {str(e)}"}), 500


