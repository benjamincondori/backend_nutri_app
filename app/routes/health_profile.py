from flask import Blueprint, jsonify, request

from datetime import datetime


from app.models.health_profile import HealthProfile
from app.models.physical_activity import PhysicalActivity

from app.database import db

from app.routes.auth import generate_jwt


health_profile_bp = Blueprint("health_profile", __name__, url_prefix="/api/health-profile")

@health_profile_bp.route("/create", methods=["POST"])
def create():
    """
    2do registro de usuario (datos corporales).
    ---
    tags:
      - Registro  # Agrupación opcional
    parameters:
      - name: Parámetros
        in: body
        required: true
        schema:
          type: object
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
            birthday:
              type: date
              description: fecha de nacimiento del usuario
              example: 1994-01-01
            gender:
              type: string
              description: lista desplegable con las siguientes opociones de género (Masculino, Femenino)
              example: Masculino
            physical_activity:
              type: string
              description: lista desplegable con las siguientes opociones de condición física (Sedentario, Actividad Ligera, Actividad Moderada, Actividad Intensa, Atleta)
              example: Sedentario
            health_restrictions:
              type: string
              description: lista desplegable con las siguientes opociones de restriccioes de salud (Ninguna, Diabetes, Hipertensión, Asma, Alergias, Enfermedad cardíaca, Problemas articulares, Sobrepeso, Bajo peso, Trastornos alimenticios, Problemas de movilidad, Enfermedades respiratorias, Cáncer, Enfermedades neurológicas)
              example: Enfermedad cardíaca
            user_id:
                type: int
                description: id del usuario
                example: 1
    responses:
      201:
        description: Registro datos corporales exitoso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Perfil de salud creado con éxito!"
            token:
              type: string
              description: "token del usuario" 
              example: 87f5a2d1cf621f7c48702982a8e3d3247c3e06fc7de9957f2b6d
      400:
        description: Todos los campos son requeridos.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Todos los campos son requeridos."
      500:
        description: Error al crear el perfil de salud.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Ocurrió un error al crear el perfil de salud"
    """
    data = request.get_json()

    required_fields = ['age','weight','height','physical_activity_id','health_restrictions','user_id','birthday','gender',]

    if not all(field in data for field in required_fields):
        return jsonify({"message": "Todos los campos son requeridos."}), 400
    
    age = data['age']
    weight = data['weight'] 
    height = data['height']
    physical_activity_id = data['physical_activity_id']
    health_restrictions = data['health_restrictions']
    update_date = datetime.now().replace(microsecond=0)
    user_id = data['user_id']
    birthday = data['birthday']
    gender = data['gender']

    new_health_profile = HealthProfile(
        age=age,
        weight=weight,
        height=height,
        physical_activity_id=physical_activity_id,
        health_restrictions=health_restrictions,
        update_date=update_date,
        user_id=user_id,
        birthday = birthday,
        gender = gender
    )

    try:
        db.session.add(new_health_profile)
        db.session.commit()
        id_user = str(user_id)
        token = generate_jwt(id_user)

        return jsonify({
            "message": "Perfil de salud creado con éxito!",
            "token": token
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message":f"Ocurrió un error al crear el perfil de salud: {str(e)}"}), 500




