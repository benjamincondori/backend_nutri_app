from flask import Blueprint, jsonify, request

from app.database import db

from app.models.physical_activity import PhysicalActivity


physical_activity_bp = Blueprint("physical_activity", __name__,  url_prefix="/api/physical-activity")

@physical_activity_bp.route("/physical-activities", methods=["GET"])
def get_all_physical_activities():
    """
    Obtener todas las actividades físicas
    ---
    tags:
      - Actividades físicas
    responses:
      200:
        description: Lista de todas las actividades físicas con sus perfiles de salud asociados.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              name:
                type: string
                example: "Correr"
              description:
                type: string
                example: "Actividad aeróbica de alta intensidad."
              PAL:
                type: float
                example: 1.75
              health_profile:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  age:
                    type: integer
                    example: 30
                  weight:
                    type: float
                    example: 70.5
                  height:
                    type: float
                    example: 1.75
                  physical_activity:
                    type: string
                    example: "Moderada"
    """
    physical_activities = PhysicalActivity.query.all()
    result = [
        {
            "id": activity.id,
            "name": activity.name,
            "description": activity.description,
            "PAL": activity.PAL,
            # "health_profile": {
            #     "id": activity.health_profile.id if activity.health_profile else None,
            #     "age": activity.health_profile.age if activity.health_profile else None,
            #     "weight": activity.health_profile.weight if activity.health_profile else None,
            #     "height": activity.health_profile.height if activity.health_profile else None,
            #     "physical_activity": activity.health_profile.physical_activity if activity.health_profile else None,
            # } if activity.health_profile else None
        }
        for activity in physical_activities
    ]
    return jsonify(result), 200

@physical_activity_bp.route("/physical-activities/<int:id>", methods=["GET"])
def get_physical_activity_by_id(id):
    """
    Obtener una actividad física por ID
    ---
    tags:
      - Actividades físicas
    parameters:
      - name: id
        in: path
        required: true
        type: integer
        description: ID de la actividad física.
        example: 1
    responses:
      200:
        description: Detalles de la actividad física con el perfil de salud asociado.
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: "Correr"
            description:
              type: string
              example: "Actividad aeróbica de alta intensidad."
            PAL:
              type: float
              example: 1.75
            health_profile:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                age:
                  type: integer
                  example: 30
                weight:
                  type: float
                  example: 70.5
                height:
                  type: float
                  example: 1.75
                physical_activity:
                  type: string
                  example: "Moderada"
      404:
        description: Actividad física no encontrada.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Actividad física no encontrada."
    """
    physical_activity = PhysicalActivity.query.get(id)
    if not physical_activity:
        return jsonify({"message": "Actividad física no encontrada."}), 404

    result = {
        "id": physical_activity.id,
        "name": physical_activity.name,
        "description": physical_activity.description,
        "PAL": physical_activity.PAL,
        "health_profile": {
            "id": physical_activity.health_profile.id if physical_activity.health_profile else None,
            "age": physical_activity.health_profile.age if physical_activity.health_profile else None,
            "weight": physical_activity.health_profile.weight if physical_activity.health_profile else None,
            "height": physical_activity.health_profile.height if physical_activity.health_profile else None,
            "physical_activity": physical_activity.health_profile.physical_activity if physical_activity.health_profile else None,
        } if physical_activity.health_profile else None
    }
    return jsonify(result), 200
