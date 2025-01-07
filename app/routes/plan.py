from flask import Blueprint, jsonify, request
from datetime import datetime

from app.database import db
from app.models.meal import Meal
from app.models.food import Food
from app.models.plan import Plan
from app.models.plan_meal import PlanMeal
from app.models.health_profile import HealthProfile
from app.models.physical_activity import PhysicalActivity

from app.utils.functions import convertir_a_json
from app.utils.planner import Planner

from app.utils.nutrion_model import *
from app.routes.auth import token_required

plan_meal_bp = Blueprint("plan_meal", __name__, url_prefix="/api/plan-meal")


# con ia (token muy limitados)
@plan_meal_bp.route("/generate-plan", methods=["POST"])
@token_required
def generate_plan():
    data = request.get_json()
    required_fields = ["id", "objective", "number-days"]

    if not all(field in data for field in required_fields):
        return jsonify({"message": "Todos los campos son requeridos."}), 400

    # Extraer parámetros
    client_id = data["id"]
    objective = data["objective"]
    numbers_days = data["number-days"]
    print("client_id", client_id)
    print("objective", objective)
    print("numbers_days", numbers_days)

    return generate_plan_nutritional(client_id, numbers_days, objective)


# con modelo de regresion
@plan_meal_bp.route("/generate-plan1", methods=["POST"])
@token_required
def generate_plan_1(current_user_id):
    """
    Generar un plan de comidas personalizado para un usuario específico. 
    Esta ruta recibe los datos del usuario y genera un plan de comidas basado 
    en sus necesidades calóricas, objetivos y número de días del plan. 
    La información generada incluye el perfil de salud,
    la actividad física y las comidas distribuidas. 
    ---
    tags:
      - Plan Nutricional
    parameters:
      - name: Parámetros
        in: body
        required: true
        schema:
            type: object
            properties:
                objective:
                    type: string
                    description: El objetivo del plan (por ejemplo, "Perder peso")
                    example: "Perder peso"
                number-days:
                    type: int
                    description: El número de días para el plan.
                    example: 7
    responses:
        200:
            description: Plan de comidas generado con éxito
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Plan de comidas generado con éxito!"
                    plan:
                        type: object
                        description: Plan de comidas detallado generado
        500:
            description: Error al generar el plan de comidas
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Error al generar el plan de comidas"
    """
    data = request.get_json()
    objective = data["objective"]
    numbers_days = data["number-days"]
    planner = Planner()

    healt_profile = HealthProfile.query.filter_by(user_id=current_user_id).first()
    pal = PhysicalActivity.query.filter_by(id=healt_profile.physical_activity_id).first()
    # Calcular las calorías necesarias para el plan completo
    calories_total = planner.calories(healt_profile.weight,
                                      healt_profile.height * 100,
                                      healt_profile.age,
                                      healt_profile.gender,
                                      objective, pal.PAL,
                                      numbers_days)
    print(f"calories_total: {calories_total}")
    plan = create_plan(objective, calories_total, current_user_id)

    # Ya se tiene DataFrame df_food con los alimentos disponibles
    plan_comidas = planner.distribuir_comidas(calories_total, numbers_days, objective, plan.id)
    # plan_comidas = planner.distribuir_comidas( calories_total, numbers_days, objective, 1)

    # actualizar la cantidad de calorias del plan
    calories_t = calculate_total_calories(plan.id)
    plan.calories = calories_t
    db.session.commit()
    print(f"calories oficiales. {plan.calories}", )
    # Convertir el plan de comidas a JSON
    plan_json = convertir_a_json(plan_comidas)
    if plan_json is None:
        return jsonify({"message": "Error al generar el plan de comidas"}), 500
    return jsonify({
        "message": "Plan de comidas generado con éxito!",
        "plan": plan_json
    }), 200


def create_plan(objective, calories, user_id):
    # Crear un plan nutricional
    plan = Plan(name=objective,
                calories=calories,
                date_generation=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                status="en progreso",
                user_id=user_id)
    db.session.add(plan)
    db.session.commit()
    return plan


# @plan_meal_bp.route("/get-plan/<int:user_id>", methods=["GET"])
@plan_meal_bp.route("/get-plan", methods=["GET"])
@token_required
def get_plan_by_user(current_user_id):
    """
    Obtener el plan de comidas actual para un usuario específico.
    Esta ruta devuelve el plan de comidas en progreso del usuario actual.
    Si no hay un plan activo, se devuelve un mensaje de error.
    ---
    tags:
      - Plan Nutricional
    parameters:
      - name: current_user_id
        in: path
        required: true
        description: ID del usuario actual obtenido del token.
        type: integer
        example: 1
    responses:
      200:
        description: Plan de comidas obtenido exitosamente.
        schema:
          type: object
          properties:
            plan_id:
              type: integer
              example: 1
            name:
              type: string
              example: "Plan semanal de pérdida de peso"
            calories:
              type: float
              example: 1800.0
            date_generation:
              type: string
              format: date-time
              example: "2025-01-01T10:00:00"
            status:
              type: string
              example: "En progreso"
            meals:
              type: array
              items:
                type: object
                properties:
                  meal_id:
                    type: integer
                    example: 2
                  meal_status:
                    type: boolean
                    example: true | false
                  name:
                    type: string
                    example: "Desayuno"
                  meal_type:
                    type: string
                    example: "Comida principal"
                  total_calories:
                    type: float
                    example: 400.0
                  total_proteins:
                    type: float
                    example: 25.0
                  total_fats:
                    type: float
                    example: 15.0
                  total_carbohydrates:
                    type: float
                    example: 50.0
                  day:
                    type: integer
                    example: 1
                  date:
                    type: string
                    format: date-time
                    example: "2025-01-01T08:00:00"
                  foods:
                    type: array
                    items:
                      type: object
                      properties:
                        food_id:
                          type: integer
                          example: 1
                        name:
                          type: string
                          example: "Huevos"
                        description:
                          type: string
                          example: "Huevos cocidos"
                        calories:
                          type: float
                          example: 70.0
                        proteins:
                          type: float
                          example: 6.0
                        fats:
                          type: float
                          example: 5.0
                        carbohydrates:
                          type: float
                          example: 1.0
                        quantity:
                          type: float
                          example: 2
                        type_quantity:
                          type: string
                          example: "Unidades"
                        category:
                          type: string
                          example: "Proteínas"
                        benefits:
                          type: string
                          example: "Fuente de proteínas"
                        image_url:
                          type: string
                          example: "https://example.com/huevos.jpg"
      404:
        description: No se encontró un plan activo para el usuario.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "No hay planes activos"
    """
    # Obtener el plan actual con status "en progreso"
    current_plan = Plan.query.filter_by(user_id=current_user_id, status="en progreso").first()

    if not current_plan:
        return jsonify({"error": "No hay planes activos"}), 404

    # Construir el JSON de respuesta
    response = {
        "plan_id": current_plan.id,
        "name": current_plan.name,
        "calories": current_plan.calories,
        "date_generation": current_plan.date_generation.isoformat(),
        "status": current_plan.status,
        "meals": []
    }

    # Obtener las comidas asociadas al plan
    for plan_meal in current_plan.plan_meal:
        meal = plan_meal.meal
        meal_data = {
            "meal_id": meal.id,
            "name": meal.name,
            "meal_type": meal.meal_type,
            "meal_status": meal.status,
            "total_calories": meal.total_calories,
            "total_proteins": meal.total_proteins,
            "total_fats": meal.total_fats,
            "total_carbohydrates": meal.total_carbohydrates,
            "day": plan_meal.day,  # Día de la comida
            "date": plan_meal.date.isoformat(),  # Fecha de la comida
            "foods": []
        }

        # Obtener los alimentos asociados a la comida
        for meal_food in meal.meal_food:
            food = meal_food.food
            food_data = {
                "food_id": food.id,
                "name": food.name,
                "description": food.description,
                "calories": food.calories,
                "proteins": food.proteins,
                "fats": food.fats,
                "carbohydrates": food.carbohydrates,
                "quantity": meal_food.quantity,
                "type_quantity": meal_food.type_quantity,
                "category": food.category,
                "benefits": food.benefits,
                "image_url": food.image_url
            }
            meal_data["foods"].append(food_data)

        response["meals"].append(meal_data)

    return jsonify(response)


@plan_meal_bp.route("/get-plans", methods=["GET"])
@token_required
def get_plans(current_user_id):
    """
    Obtener todos los planes de un usuario
    ---
    tags:
      - Plan Nutricional
    responses:
      200:
        description: Lista de planes del usuario.
        schema:
          type: array
          items:
            type: object
            properties:
              plan_id:
                type: integer
                example: 1
              name:
                type: string
                example: "Plan semanal de pérdida de peso"
              calories:
                type: float
                example: 1800.0
              date_generation:
                type: string
                format: date-time
                example: "2025-01-01T10:00:00"
              status:
                type: string
                example: "En progreso | terminado"
      404:
        description: El usuario no tiene planes.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "el usuario no tiene planes"
    """
    plans = Plan.query.filter_by(user_id=current_user_id).all()
    if not plans:
        return jsonify({"error": "el usuario no tiene planes"}), 404

    # Crear la respuesta JSON
    response = []
    for plan in plans:
        plan_data = {
            "plan_id": plan.id,
            "name": plan.name,
            "calories": plan.calories,
            "date_generation": plan.date_generation.isoformat(),
            "status": plan.status,
        }
        response.append(plan_data)

    return jsonify(response), 200


# @plan_meal_bp.route("/finish-plan", methods=["POST"])
# @token_required
# def finish_plan(current_user_id):
#     """
#     Finalizar un plan de comidas en progreso.
#     Esta ruta cambia el estado de un plan activo a "terminado".
#     ---
#     tags:
#       - Plan Nutricional
#     parameters:
#       - in: body
#         name: body
#         description: ID del plan a finalizar.
#         required: true
#         schema:
#           type: object
#           properties:
#             plan_id:
#               type: integer
#               example: 1
#     responses:
#       200:
#         description: Plan finalizado con éxito.
#         schema:
#           type: object
#           properties:
#             message:
#               type: string
#               example: "Plan finalizado con éxito."
#       404:
#         description: No se encontró un plan activo para el usuario.
#         schema:
#           type: object
#           properties:
#             error:
#               type: string
#               example: "No hay planes activos"
#     """
#     # Obtener los datos de la solicitud
#     data = request.get_json()
#
#     # Validar que se haya proporcionado el plan_id
#     plan_id = data.get("plan_id")
#     if not plan_id:
#         return jsonify({"error": "El campo 'plan_id' es requerido."}), 400
#
#     # Obtener el plan actual con status "en progreso"
#     current_plan = Plan.query.filter_by(id=plan_id, user_id=current_user_id, status="en progreso").first()
#     if not current_plan:
#         return jsonify({"error": "No hay planes activos"}), 404
#
#     # Cambiar el estado del plan a "terminado"
#     current_plan.status = "terminado"
#     db.session.commit()
#
#     return jsonify({"message": "Plan finalizado con éxito."}), 200

@plan_meal_bp.route("/finish-plan", methods=["POST"])
@token_required
def finish_plan(current_user_id):
    """
    Finalizar o reiniciar un plan de comidas en función de su estado actual.
    Si el plan está "en progreso", se cambia a "terminado".
    Si el plan está "terminado", se cambia a "en progreso".
    ---
    tags:
      - Plan Nutricional
    parameters:
      - in: body
        name: body
        description: ID del plan a modificar.
        required: true
        schema:
          type: object
          properties:
            plan_id:
              type: integer
              example: 1
    responses:
      200:
        description: Plan modificado con éxito.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Plan modificado con éxito."
      404:
        description: No se encontró un plan para el usuario.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "No se encontró un plan con ese ID."
    """
    # Obtener los datos de la solicitud
    data = request.get_json()

    # Validar que se haya proporcionado el plan_id
    plan_id = data.get("plan_id")
    if not plan_id:
        return jsonify({"error": "El campo 'plan_id' es requerido."}), 400

    # Obtener el plan con el ID proporcionado
    current_plan = Plan.query.filter_by(id=plan_id, user_id=current_user_id).first()
    if not current_plan:
        return jsonify({"error": "No se encontró un plan con ese ID."}), 404

    # Cambiar el estado del plan según su estado actual
    if current_plan.status == "en progreso":
        current_plan.status = "terminado"
        message = "Plan finalizado con éxito."
    elif current_plan.status == "terminado":
        current_plan.status = "en progreso"
        message = "Plan reiniciado a 'en progreso'."
    else:
        return jsonify({"error": "El estado del plan es desconocido."}), 400

    # Guardar los cambios en la base de datos
    db.session.commit()

    return jsonify({"message": message}), 200

@plan_meal_bp.route("/update-plan-status", methods=["POST"])
@token_required
def update_plan_status(current_user_id):
    """
    Verificar el estado de las comidas asociadas al plan y actualizar el estado del plan.
    Si todas las comidas están en 'True', el plan se marca como 'terminado'.
    Si alguna comida está en 'False', el plan se marca como 'en progreso'.
    ---
    tags:
      - Plan Nutricional
    parameters:
      - in: body
        name: body
        description: ID del plan a verificar y actualizar.
        required: true
        schema:
          type: object
          properties:
            plan_id:
              type: integer
              example: 1
    responses:
      200:
        description: Estado del plan actualizado con éxito.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Estado del plan actualizado con éxito."
      404:
        description: No se encontró un plan o comidas asociadas al plan.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "No se encontró un plan o comidas asociadas al plan."
    """
    # Obtener los datos de la solicitud
    data = request.get_json()

    # Validar que se haya proporcionado el plan_id
    plan_id = data.get("plan_id")
    if not plan_id:
        return jsonify({"error": "El campo 'plan_id' es requerido."}), 400

    # Obtener el plan con el ID proporcionado
    current_plan = Plan.query.filter_by(id=plan_id, user_id=current_user_id).first()
    if not current_plan:
        return jsonify({"error": "No se encontró un plan con ese ID."}), 404

    # Obtener las comidas asociadas al plan mediante la tabla intermedia `PlanMeal`
    plan_meals = PlanMeal.query.filter_by(plan_id=plan_id).all()
    if not plan_meals:
        return jsonify({"error": "No se encontraron comidas asociadas al plan."}), 404

    # Verificar el estado de las comidas
    all_meals_completed = True
    for plan_meal in plan_meals:
        meal = plan_meal.meal
        if meal.status != True:  # Si alguna comida tiene estado False
            all_meals_completed = False
            break

    # Si todas las comidas están completas, marcar el plan como "terminado"
    if all_meals_completed:
        current_plan.status = "terminado"
        message = "Plan finalizado con éxito."
    else:
        # Si alguna comida está incompleta, marcar el plan como "en progreso"
        current_plan.status = "en progreso"
        message = "Plan reiniciado a 'en progreso'."

    # Guardar los cambios en la base de datos
    db.session.commit()

    return jsonify({"message": message, "success": all_meals_completed}), 200

# @plan_meal_bp.route("/act-calories", methods=["POST"])
# @token_required

# Extrae la lógica de cálculo a una función independiente
def calculate_total_calories(plan_id):
    """
    Calcula las calorías totales de un plan dado su ID.
    """
    meals = PlanMeal.query.filter_by(plan_id=plan_id).all()
    if not meals:
        return None  # Retorna None si no hay comidas asociadas al plan

    total_calories = 0.00
    for meal in meals:
        me = Meal.query.filter_by(id=meal.meal_id).first()
        if me:
            total_calories += me.total_calories
    return total_calories

@plan_meal_bp.route("/get-plan/<int:plan_id>", methods=["GET"])
@token_required
def get_plan_by_id(current_user_id, plan_id):
    """
    Obtener un plan de comidas específico por su ID.
    Esta ruta devuelve un plan de comidas basado en el ID proporcionado.
    Si no se encuentra el plan o no pertenece al usuario, se devuelve un mensaje de error.
    ---
    tags:
      - Plan Nutricional
    parameters:
      - name: plan_id
        in: path
        required: true
        description: ID del plan de comidas.
        type: integer
        example: 1
    responses:
      200:
        description: Plan de comidas obtenido exitosamente.
        schema:
          type: object
          properties:
            plan_id:
              type: integer
              example: 1
            name:
              type: string
              example: "Plan semanal de pérdida de peso"
            calories:
              type: float
              example: 1800.0
            date_generation:
              type: string
              format: date-time
              example: "2025-01-01T10:00:00"
            status:
              type: string
              example: "En progreso"
            meals:
              type: array
              items:
                type: object
                properties:
                  meal_id:
                    type: integer
                    example: 2
                  meal_status:
                    type: boolean
                    example: true
                  name:
                    type: string
                    example: "Desayuno"
                  meal_type:
                    type: string
                    example: "Comida principal"
                  total_calories:
                    type: float
                    example: 400.0
                  total_proteins:
                    type: float
                    example: 25.0
                  total_fats:
                    type: float
                    example: 15.0
                  total_carbohydrates:
                    type: float
                    example: 50.0
                  day:
                    type: integer
                    example: 1
                  date:
                    type: string
                    format: date-time
                    example: "2025-01-01T08:00:00"
                  foods:
                    type: array
                    items:
                      type: object
                      properties:
                        food_id:
                          type: integer
                          example: 1
                        name:
                          type: string
                          example: "Huevos"
                        description:
                          type: string
                          example: "Huevos cocidos"
                        calories:
                          type: float
                          example: 70.0
                        proteins:
                          type: float
                          example: 6.0
                        fats:
                          type: float
                          example: 5.0
                        carbohydrates:
                          type: float
                          example: 1.0
                        quantity:
                          type: float
                          example: 2
                        type_quantity:
                          type: string
                          example: "Unidades"
                        category:
                          type: string
                          example: "Proteínas"
                        benefits:
                          type: string
                          example: "Fuente de proteínas"
                        image_url:
                          type: string
                          example: "https://example.com/huevos.jpg"
      404:
        description: No se encontró un plan con el ID proporcionado.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "No se encontró el plan"
    """
    # Obtener el plan específico por ID
    plan = Plan.query.filter_by(id=plan_id, user_id=current_user_id).first()

    if not plan:
        return jsonify({"error": "No se encontró el plan"}), 404

    # Construir el JSON de respuesta
    response = {
        "plan_id": plan.id,
        "name": plan.name,
        "calories": plan.calories,
        "date_generation": plan.date_generation.isoformat(),
        "status": plan.status,
        "meals": []
    }

    # Obtener las comidas asociadas al plan
    for plan_meal in plan.plan_meal:
        meal = plan_meal.meal
        meal_data = {
            "meal_id": meal.id,
            "name": meal.name,
            "meal_type": meal.meal_type,
            "meal_status": meal.status,
            "total_calories": meal.total_calories,
            "total_proteins": meal.total_proteins,
            "total_fats": meal.total_fats,
            "total_carbohydrates": meal.total_carbohydrates,
            "day": plan_meal.day,
            "date": plan_meal.date.isoformat(),
            "foods": []
        }

        # Obtener los alimentos asociados a la comida
        for meal_food in meal.meal_food:
            food = meal_food.food
            food_data = {
                "food_id": food.id,
                "name": food.name,
                "description": food.description,
                "calories": food.calories,
                "proteins": food.proteins,
                "fats": food.fats,
                "carbohydrates": food.carbohydrates,
                "quantity": meal_food.quantity,
                "type_quantity": meal_food.type_quantity,
                "category": food.category,
                "benefits": food.benefits,
                "image_url": food.image_url
            }
            meal_data["foods"].append(food_data)

        response["meals"].append(meal_data)

    return jsonify(response)
