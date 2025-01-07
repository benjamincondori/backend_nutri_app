from datetime import datetime
from flask import Blueprint, jsonify, request

from app.database import db

from app.models.user import User
from app.models.health_objective import HealthObjective
from app.models.health_profile import HealthProfile

from app.routes.auth import token_required

health_objective_bp = Blueprint("healt_objective", __name__,  url_prefix="/api/health-objective")

@health_objective_bp.route("/create", methods=["POST"])
@token_required
def create(current_user_id):
    """
    Registro de objetivo de salud
    ---
    tags:
      - Objetivo de salud  # Agrupación opcional
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: Objetivos posibles (Pérdida de peso, Aumento de peso, Mantenimiento del peso, Mejorar la salud general, Manejar la diabetes, Controlar la hipertensión, Mejorar los niveles de colesterol, Mejorar el rendimiento deportivo, Mejorar la salud digestiva, Aliviar síntomas de alergias, Aliviar intolerancias alimentarias, Otro)
              example: Aumento de peso
            other_objetive:
              type: string
              description: Campo de texto libre para especificar otro objetivo si no está en la lista.
              example: Sanar de una infección en el estómago
            number_days:
              type: integer
              description: Cantidad de días para cumplir el objetivo (3, 5, 7)
              example: 3
    responses:
      201:
        description: Registro de objetivo de salud exitoso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Objetivo de salud creado con éxito!"
            health_objective:
              type: object
              properties:
                name:
                  type: string
                  example: "Aumento de peso"
                other_objetive:
                  type: string
                  example: "Sanar de una infección en el estómago"
                update_date:
                  type: string
                  format: date-time
                  example: "2024-10-23T12:00:00"
                number_days:
                  type: integer
                  example: 3
            health_profile:
              type: object
              properties:
                age:
                  type: integer
                  example: 30
                weight:
                  type: number
                  format: float
                  example: 70.5
                height:
                  type: number
                  format: float
                  example: 1.75
                physical_activity:
                  type: string
                  example: "Moderada"
                update_date:
                  type: string
                  format: date-time
                  example: "2024-10-23T12:00:00"
                health_restrictions:
                  type: string
                  items:
                    type: string
                  example: "Diabetes"
      400:
        description: Todos los campos son requeridos a excepcion de other_objective.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Todos los campos son requeridos."
      500:
        description: Error al crear el objetivo de salud.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Ocurrió un error al crear el objetivo de salud"
    """
    data = request.get_json()

    # Campos requeridos
    required_fields = ['name','number_days']

    if not all(field in data for field in required_fields):
        return jsonify({"message": "Todos los campos son requeridos."}), 400    

    # Asignar datos desde la solicitud
    name = data['name'] 
    other_objetive = data['other_objective']
    update_date = datetime.now().replace(microsecond=0)
    number_days = data['number_days']

    # Obtener el usuario y el perfil de salud
    user = User.query.filter_by(id=current_user_id).first()
    health_profile = HealthProfile.query.filter_by(user_id=user.id).first()

    if health_profile is None:
        return jsonify({"message": "Perfil de salud no encontrado."}), 404

    health_profile_id = health_profile.id

    # Crear un nuevo objetivo de salud
    new_health_objective = HealthObjective(
        name=name,
        other_objetive=other_objetive,
        update_date=update_date,
        number_days=number_days,
        health_profile_id=health_profile_id
    )

    try:
        # Agregar y confirmar la nueva instancia
        db.session.add(new_health_objective)
        db.session.commit()
        return jsonify({
            "message": "Objetivo de salud creado con éxito!",
            'health_objective': {
                "name": new_health_objective.name,
                "other_objetive": new_health_objective.other_objetive,
                "update_date": new_health_objective.update_date.isoformat(),
                "number_days": new_health_objective.number_days
            },
            'health_profile': {
                "age": health_profile.age,
                "weight": health_profile.weight,
                "height": health_profile.height,
                "physical_activity": health_profile.physical_activity,
                "update_date": health_profile.update_date.isoformat(),
                "health_restrictions": health_profile.health_restrictions
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Ocurrió un error al crear el objetivo de salud: {str(e)}"}), 500