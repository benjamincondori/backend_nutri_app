from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from app.models.user import User
from app.routes.auth import token_required

from app.models.food import Food
from app.models.meal import Meal
from app.models.meal_food import MealFood

from app.schemas.user import UserSchema

from app.database import db

user_bp = Blueprint("user", __name__, url_prefix="/api/user")


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

@user_bp.route("/profile", methods=["PUT"])
@token_required
def update_personal_profile(current_user_id):
    """
    Editar los datos personales de un usuario.
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
      - in: body
        name: body
        required: true
        description: Datos personales a actualizar
        schema:
          type: object
          properties:
            name:
              type: string
              description: Nombre del usuario
              example: Juan
            lastname:
              type: string
              description: Apellido del usuario
              example: Pérez
            telephone:
              type: string
              description: Teléfono del usuario
              example: 74646527
            url_image:
              type: string
              description: URL de la imagen del perfil
              example: https://res.cloudinary.com/image/upload/v1234567890/user.jpg
    responses:
      200:
        description: Datos personales actualizados correctamente
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Datos personales actualizados correctamente."
      404:
        description: Usuario no encontrado
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Usuario no encontrado."
      400:
        description: Error en los datos proporcionados
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Datos inválidos."
    """
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "Usuario no encontrado."}), 404

    data = request.get_json()
    if not data:
        return jsonify({"message": "Datos inválidos."}), 400

    # Actualizar campos personales
    user.name = data.get("name", user.name)
    user.lastname = data.get("lastname", user.lastname)
    user.telephone = data.get("telephone", user.telephone)
    user.url_image = data.get("url_image", user.url_image)

    # Guardar cambios
    try:
        db.session.commit()
        return jsonify({"message": "Datos personales actualizados correctamente."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error al actualizar los datos: {str(e)}"}), 500
