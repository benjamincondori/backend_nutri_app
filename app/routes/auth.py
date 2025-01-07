from functools import wraps
from flask import Blueprint, jsonify, request, current_app
import jwt
import os
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash
from dotenv import load_dotenv

from app.models.user import User
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

auth_bp = Blueprint("auth", __name__, url_prefix="/api")


def generate_jwt(user_id):
    """
    Genera un token JWT con una duración de 1 hora.
    """
    expiration = datetime.utcnow() + timedelta(hours=1)
    token = jwt.encode({
        'user_id': user_id,
        'exp': expiration
    }, SECRET_KEY, algorithm='HS256')

    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Verifica si el token está en las cabeceras
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Decodifica el token usando la clave secreta
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user_id = data['user_id']
            # Aquí podrías buscar al usuario en la base de datos si es necesario
            user = User.query.get(current_user_id)  # Descomenta si necesitas la instancia del usuario
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        # Llama a la función decorada
        return f(current_user_id, *args, **kwargs)

    return decorated


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Inicio de sesión de usuario.
    ---
    tags:
      - Autenticacion  # Agrupación opcional
    parameters:
      - name: credenciales
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: Email del usuario
              example: user@example.com
            password:
              type: string
              description: Contraseña del usuario
              example: pass123
    responses:
      200:
        description: Login exitoso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Inicio de sesión exitoso!"
            token:
              type: string
              description: JWT token
              example: 87f5a2d1cf621f7c48702982a8e3d3247c3e06fc7de9957f2b6d

      400:
        description: Todos los campos son requeridos.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Todos los campos son requeridos."
      404:
        description: Usuario no encontrado.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Usuario no encontrado."
      401:
        description: Contraseña incorrecta.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Contraseña incorrecta."
    """
    data = request.get_json()

    # Campos requeridos
    required_fields = ['email', 'password']

    if not all(field in data for field in required_fields):
        return jsonify({"message": "Todos los campos son requeridos."}), 400

    email = data['email']
    password = data['password']
    print(email)
    print(password)
    # Busca el usuario en la base de datos
    user_login = User.query.filter_by(email=email).first()

    if user_login is None:
        return jsonify({"message": "Usuario no encontrado."}), 404

    # # Verifica la contraseña
    if not check_password_hash(user_login.password, password):
        return jsonify({"message": "Contraseña incorrecta."}), 401
    # if user_login.password != password:
    #     return jsonify({"message": "Contraseña incorrecta."}), 401

    # Obtiene el tipo de usuario
    user_type = user_login.type

    # Genera el token JWT
    token = generate_jwt(user_login.id)

    return jsonify({
        "message": "Inicio de sesión exitoso!",
        "token": token,
        "user_id": user_login.id,
        "user_type": user_type
    }), 200


@auth_bp.route('/verify-token', methods=['GET'])
def verify_token():
    token = None

    # Verifica si el token está en las cabeceras
    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].split(" ")[1]

    if not token:
        return jsonify({'message': 'Token is missing!'}), 401

    try:
        # Decodifica el token usando la clave secreta
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return jsonify({'message': 'Token is valid!', 'data': data}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token!'}), 401
