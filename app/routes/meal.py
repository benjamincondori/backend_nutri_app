from datetime import datetime
from flask import Blueprint, jsonify, request

from app.database import db
from app.models.meal import Meal
from app.models.food import Food
from app.models.meal_food import MealFood
from app.models.plan import Plan
from app.models.plan_meal import PlanMeal

from app.routes.auth import token_required
from app.utils.nutrion_model import *

meal_bp = Blueprint("meal", __name__, url_prefix="/api/meal")


@meal_bp.route('/generate-plan', methods=['POST'])
def generate_plan():
    data = request.get_json()
    required_fields = ['id', 'objective', 'number-days']

    if not all(field in data for field in required_fields):
        return jsonify({"message": "Todos los campos son requeridos."}), 400

    # Extraer parámetros
    client_id = data['id']
    objective = data['objective']
    numbers_days = data['number-days']

    return generate_plan_nutritional1(client_id, numbers_days, objective)


@meal_bp.route('/meals/', methods=['GET'])
def get_meal_by_objective():
    """
    Retrieves one breakfast, one lunch, and one dinner with their associated foods.
    """
    try:
        # Query the database for one breakfast, one lunch, and one dinner
        breakfasts = (
            Meal.query.filter_by(meal_type="desayuno", status=True)
            .first()
        )
        lunches = (
            Meal.query.filter_by(meal_type="almuerzo", status=True)
            .first()
        )
        dinners = (
            Meal.query.filter_by(meal_type="cena", status=True)
            .first()
        )

        # Format meals and their related foods into JSON format
        meals = {
            "breakfast": format_meal_with_foods(breakfasts) if breakfasts else None,
            "lunch": format_meal_with_foods(lunches) if lunches else None,
            "dinner": format_meal_with_foods(dinners) if dinners else None,
        }
        return jsonify(meals), 200
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "Unable to fetch meals"}), 500


def format_meal_with_foods(meal):
    """
    Helper function to format a meal with its associated foods.
    """
    if not meal:
        return None

    # Fetch associated foods through the MealFood relationship
    foods = (
        MealFood.query.filter_by(meal_id=meal.id)
        .join(Food, MealFood.food_id == Food.id)
        .all()
    )

    return {
        "id": meal.id,
        "name": meal.name,
        "meal_type": meal.meal_type,
        "total_calories": meal.total_calories,
        "total_proteins": meal.total_proteins,
        "total_fats": meal.total_fats,
        "total_carbohydrates": meal.total_carbohydrates,
        "foods": [
            {
                "name": food.food.name,
                "quantity": food.quantity,
                "type_quantity": food.type_quantity,
                "calories": food.food.calories,
                "proteins": food.food.proteins,
                "fats": food.food.fats,
                "carbohydrates": food.food.carbohydrates,
            }
            for food in foods
        ],
    }


def save_meal(objective, type, calories, food, plan_id):
    """
    Create a new meal with the provided parameters.
    """
    proteins = float(calculate_proteins(food))
    fats = float(calculate_fats(food))
    carbohydrates = float(calculate_carbohydrates(food))
    print("proteins", proteins)
    print("fats", fats)
    print("carbohydrates", carbohydrates)
    meal = Meal(
        name=type,
        status=False,
        meal_type=type,
        total_calories=float(calories),
        total_proteins=proteins,
        total_fats=fats,
        total_carbohydrates=carbohydrates,
    )

    db.session.add(meal)
    db.session.commit()

    save_food(food, meal)

    return meal


def save_food(food, meal):
    for foo in food:
        foo['cantidad'] = float(foo['cantidad'])  # Conversión aquí

        f = Food.query.filter_by(name=foo['alimento']).first()
        meal_food = MealFood(meal_id=meal.id,
                             food_id=f.id,
                             quantity=foo['cantidad'],
                             type_quantity=foo['unidad'])
        db.session.add(meal_food)
    db.session.commit()


def save_plan_meal(meal, plan_id, date, day):
    """
    Crea un plan de comida con el id del plan y el id de la comida.
    """
    plan_meal = PlanMeal(plan_id=plan_id, meal_id=meal.id, date=date, day=day)
    db.session.add(plan_meal)
    db.session.commit()

    return plan_meal


@meal_bp.route("/calculate-calories/<int:id>", methods=["GET"])
def get_calories_plan(id):
    """
    Calcula las calorías totales de un plan.
    ---
    tags:
      - Plan Nutricional
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del plan nutricional.
    responses:
      200:
        description: Calorías totales calculadas exitosamente.
        schema:
          type: object
          properties:
            total_calories:
              type: number
              format: float
              example: 4500.75
      404:
        description: No se encontraron comidas para el plan especificado.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "No se encontraron comidas para el plan especificado."
    """
    meals = PlanMeal.query.filter_by(plan_id=id).all()
    if not meals:
        return jsonify({"error": "No se encontraron comidas para el plan especificado."}), 404

    total_calories = 0.00
    for meal in meals:
        me = Meal.query.filter_by(id=meal.meal_id).first()
        total_calories += me.total_calories
    return jsonify({"total_calories": total_calories}), 200


def calculate_proteins(food):
    print("comida recibida:", food)
    pro = 0
    for foo in food:
        if 'alimento' not in foo:
            print("Key 'alimento' no se encuentra en el item:", foo)
            continue
        pro_food = Food.query.filter_by(name=foo['alimento']).first()
        if pro_food:
            pro += pro_food.proteins
        else:
            print(f"Food '{foo['alimento']}' no encontrado en la base de datos.")
    return pro


def calculate_fats(food):
    print("comida recibida:", food)
    fats = 0
    for foo in food:
        if 'alimento' not in foo:
            print("Key 'alimento' no se encuentra en el item:", foo)
            continue
        fats_food = Food.query.filter_by(name=foo['alimento']).first()
        if fats_food:
            fats += fats_food.fats
        else:
            print(f"Food '{foo['alimento']}' no encontrado en la base de datos.")
    return fats


def calculate_carbohydrates(food):
    print("comida recibida:", food)
    carbohydrates = 0
    for foo in food:
        if 'alimento' not in foo:
            print("Key 'alimento' no se encuentra en el item:", foo)
            continue
        carbohydrates_food = Food.query.filter_by(name=foo['alimento']).first()
        if carbohydrates_food:
            carbohydrates += carbohydrates_food.carbohydrates
        else:
            print(f"Food '{foo['alimento']}' no encontrado en la base de datos.")
    return carbohydrates


# @meal_bp.route("/finish-meal", methods=["POST"])
# @token_required
# def finish_meal(current_user_id):
#     """
#     Finalizar una comida.
#     Cambia el estado de la comida especificada a True y actualiza las calorías totales del plan asociado.
#     ---
#     tags:
#       - Comidas
#     parameters:
#       - in: body
#         name: body
#         description: ID de la comida que se desea finalizar.
#         required: true
#         schema:
#           type: object
#           properties:
#             meal_id:
#               type: integer
#               example: 1
#     responses:
#       200:
#         description: Estado de la comida cambiado exitosamente y calorías del plan actualizadas.
#         schema:
#           type: object
#           properties:
#             message:
#               type: string
#               example: "Estado de comida cambiada a True."
#       400:
#         description: El campo 'meal_id' no fue proporcionado.
#         schema:
#           type: object
#           properties:
#             error:
#               type: string
#               example: "El campo 'meal_id' es requerido."
#       404:
#         description: No se encontró una comida con el ID especificado y estado False.
#         schema:
#           type: object
#           properties:
#             error:
#               type: string
#               example: "No existe la comida con id: 1 y estado: False"
#     """
#     # Obtener los datos de la solicitud
#     data = request.get_json()
#     meal_id = data.get("meal_id")
#
#     if not meal_id:
#         return jsonify({"error": "El campo 'meal_id' es requerido."}), 400
#
#     meal = Meal.query.filter_by(id=meal_id, status=False).first()
#
#     if not meal:
#         return jsonify({"error": "No existe la comida con id: {meal_id} y estado: False"}), 404
#
#     # Cambiar el estado del plan a True
#     meal.status = True
#     db.session.commit()
#
#     # obtener el plan al que pertenece la comida
#     plan = PlanMeal.query.filter_by(meal_id=meal_id).first()
#
#     # al cambiar el estado de la comida se actualiza el total de calorias del plan
#     act_calories(meal.total_calories, plan.plan_id)
#
#     return jsonify({"message": "estado de comida cambiada a True."}), 200


@meal_bp.route("/finish-meal", methods=["POST"])
@token_required
def finish_meal(current_user_id):
    """
    Finalizar o desmarcar una comida.
    Cambia el estado de la comida especificada a True (consumida) o False (desmarcada) y actualiza las calorías del plan asociado.
    ---
    tags:
      - Comidas
    parameters:
      - in: body
        name: body
        description: ID de la comida que se desea finalizar o desmarcar.
        required: true
        schema:
          type: object
          properties:
            meal_id:
              type: integer
              example: 1
    responses:
      200:
        description: Estado de la comida cambiado exitosamente y calorías del plan actualizadas.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Estado de comida cambiada a True."
      400:
        description: El campo 'meal_id' no fue proporcionado.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "El campo 'meal_id' es requerido."
      404:
        description: No se encontró una comida con el ID especificado y estado False.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "No existe la comida con id: 1 y estado: False"
    """
    # Obtener los datos de la solicitud
    data = request.get_json()
    meal_id = data.get("meal_id")

    if not meal_id:
        return jsonify({"error": "El campo 'meal_id' es requerido."}), 400

    # Buscar la comida por ID y su estado
    meal = Meal.query.filter_by(id=meal_id).first()

    if not meal:
        return jsonify({"error": f"No existe la comida con id: {meal_id}"}), 404

    # Si la comida está marcada como consumida (status=True), desmarcarla (status=False)
    if meal.status:
        meal.status = False
        db.session.commit()

        # Obtener el plan asociado a la comida y actualizar las calorías
        # plan = PlanMeal.query.filter_by(meal_id=meal_id).first()
        # if plan:
        #     act_calories(meal.total_calories, plan.plan_id)  # Se suman las calorías al plan

        return jsonify({"message": "Comida desmarcada y calorías actualizadas."}), 200

    # Si la comida no está marcada como consumida, cambiarla a consumida (status=True)
    meal.status = True
    db.session.commit()

    # Obtener el plan asociado a la comida y actualizar las calorías
    # plan = PlanMeal.query.filter_by(meal_id=meal_id).first()
    # if plan:
    #     act_calories(-meal.total_calories, plan.plan_id)  # Se restan las calorías al plan

    return jsonify({"message": "Comida marcada como consumida y calorías actualizadas."}), 200


# actualiza las calorías del plan
def act_calories(cal, plan_id):
    plan = Plan.query.filter_by(id=plan_id).first()

    if not plan:
        return jsonify({"error": "No existe el plan"}), 404

    plan.calories = plan.calories + cal  # Se suma o resta dependiendo de la acción
    db.session.commit()


@meal_bp.route('/meals/all', methods=['GET'])
def get_all_meals():
    """
    Endpoint para obtener todas las comidas.
    """
    try:
        # Obtener todas las comidas de la base de datos
        meals = Meal.query.all()

        # Formatear las comidas en un JSON
        meals_list = [
            {
                "id": meal.id,
                "name": meal.name,
                "status": meal.status,
                "meal_type": meal.meal_type,
                "total_calories": meal.total_calories,
                "total_proteins": meal.total_proteins,
                "total_fats": meal.total_fats,
                "total_carbohydrates": meal.total_carbohydrates,
            }
            for meal in meals
        ]

        return jsonify(meals_list), 200
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "Error al obtener las comidas"}), 500


@meal_bp.route('/meals', methods=['POST'])
def create_meal():
    """
    Endpoint para crear una nueva comida.
    """
    try:
        data = request.get_json()

        # Validar que todos los campos requeridos estén presentes
        required_fields = [
            "name", "status", "meal_type",
            "total_calories", "total_proteins",
            "total_fats", "total_carbohydrates"
        ]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"El campo '{field}' es requerido"}), 400

        # Crear un nuevo objeto Meal
        new_meal = Meal(
            name=data["name"],
            status=data["status"],
            meal_type=data["meal_type"],
            total_calories=data["total_calories"],
            total_proteins=data["total_proteins"],
            total_fats=data["total_fats"],
            total_carbohydrates=data["total_carbohydrates"],
        )

        # Agregar y guardar en la base de datos
        db.session.add(new_meal)
        db.session.commit()

        return jsonify({
            "message": "Comida creada exitosamente",
            "meal": {
                "id": new_meal.id,
                "name": new_meal.name,
                "status": new_meal.status,
                "meal_type": new_meal.meal_type,
                "total_calories": new_meal.total_calories,
                "total_proteins": new_meal.total_proteins,
                "total_fats": new_meal.total_fats,
                "total_carbohydrates": new_meal.total_carbohydrates,
            }
        }), 201
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "Error al crear la comida"}), 500


@meal_bp.route('/meals/<int:meal_id>', methods=['PUT'])
def update_meal(meal_id):
    """
    Endpoint para actualizar una comida existente.
    """
    try:
        data = request.get_json()

        # Buscar la comida por ID
        meal = Meal.query.get(meal_id)
        if not meal:
            return jsonify({"error": "Comida no encontrada"}), 404

        # Actualizar los campos de la comida
        meal.name = data.get("name", meal.name)
        meal.status = data.get("status", meal.status)
        meal.meal_type = data.get("meal_type", meal.meal_type)
        meal.total_calories = data.get("total_calories", meal.total_calories)
        meal.total_proteins = data.get("total_proteins", meal.total_proteins)
        meal.total_fats = data.get("total_fats", meal.total_fats)
        meal.total_carbohydrates = data.get("total_carbohydrates", meal.total_carbohydrates)

        # Guardar los cambios en la base de datos
        db.session.commit()

        return jsonify({
            "message": "Comida actualizada exitosamente",
            "meal": {
                "id": meal.id,
                "name": meal.name,
                "status": meal.status,
                "meal_type": meal.meal_type,
                "total_calories": meal.total_calories,
                "total_proteins": meal.total_proteins,
                "total_fats": meal.total_fats,
                "total_carbohydrates": meal.total_carbohydrates,
            }
        }), 200
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "Error al actualizar la comida"}), 500


@meal_bp.route('/meals/<int:meal_id>/foods/', methods=['GET'])
def get_foods_by_meal(meal_id):
    """
    Endpoint para obtener los alimentos asociados a una comida específica.
    """
    try:
        # Buscar la comida por su ID
        meal = Meal.query.get(meal_id)

        # Validar si existe
        if not meal:
            return jsonify({"error": "Comida no encontrada"}), 404

        # Obtener las relaciones MealFood para esta comida
        meal_foods = MealFood.query.filter_by(meal_id=meal_id).all()

        # Formatear los datos de los alimentos
        foods = [
            {
                "id": meal_food.food.id,
                "name": meal_food.food.name,
                "calories": meal_food.food.calories,
                "proteins": meal_food.food.proteins,
                "fats": meal_food.food.fats,
                "carbohydrates": meal_food.food.carbohydrates,
                "image_url": meal_food.food.image_url,
                "description": meal_food.food.description,
                "benefits": meal_food.food.benefits,
                "category": meal_food.food.category,
                "quantity": meal_food.quantity,
                "type_quantity": meal_food.type_quantity,
            }
            for meal_food in meal_foods
        ]

        return jsonify({
            "meal": {
                "id": meal.id,
                "name": meal.name,
                "meal_type": meal.meal_type,
                "total_calories": meal.total_calories,
                "total_proteins": meal.total_proteins,
                "total_fats": meal.total_fats,
                "total_carbohydrates": meal.total_carbohydrates,
                "status": meal.status,
            },
            "foods": foods
        }), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "Error al obtener los alimentos"}), 500
