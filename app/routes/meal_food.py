from flask import Blueprint, jsonify, request

from app.database import db
from app.models.food import Food
from app.models.meal import Meal
from app.models.meal_food import MealFood

meal_food_bp = Blueprint("meal_food", __name__, url_prefix="/api/meal-food")


@meal_food_bp.route('/add', methods=['POST'])
def add_single_meal_food():
    """
    Endpoint para registrar una sola relación entre comida y alimento.
    """
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        # Validar datos requeridos
        meal_id = data.get("meal_id")
        food_id = data.get("food_id")
        quantity = data.get("quantity", 1.0)
        type_quantity = data.get("type_quantity", "unidad")

        if not meal_id or not food_id:
            return jsonify({"error": "meal_id y food_id son obligatorios"}), 400

        existing = MealFood.query.filter_by(meal_id=meal_id, food_id=food_id).first()
        if existing:
            return jsonify({"error": "La relación ya existe"}), 400

        meal = Meal.query.get(meal_id)
        if not meal:
            return jsonify({"error": "No se encontró la comida"}), 404

        food = Food.query.get(food_id)
        if not food:
            return jsonify({"error": "No se encontró el alimento"}), 404

        # Crear instancia de MealFood
        meal_food = MealFood(
            meal_id=meal_id,
            food_id=food_id,
            quantity=quantity,
            type_quantity=type_quantity
        )

        # Agregar a la base de datos
        db.session.add(meal_food)
        db.session.commit()

        # Actualizar los totales de la comida
        # update_meal_totals(meal_id)

        return jsonify({"message": "Relación registrada correctamente"}), 201

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "Error al registrar la relación"}), 500


@meal_food_bp.route('/remove/<int:meal_food_id>', methods=['DELETE'])
def remove_meal_food(meal_food_id):
    """
    Endpoint para eliminar una relación específica entre comida y alimento.
    """
    try:
        # Buscar la relación por su ID
        meal_food = MealFood.query.get(meal_food_id)

        # Validar si existe
        if not meal_food:
            return jsonify({"error": "Relación no encontrada"}), 404

        # Eliminar la relación
        db.session.delete(meal_food)
        db.session.commit()

        # Actualizar los totales de la comida
        # update_meal_totals(meal_food.meal_id)

        return jsonify({"message": "Relación eliminada correctamente"}), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "Error al eliminar la relación"}), 500

@meal_food_bp.route('/remove/<int:meal_id>/<int:food_id>', methods=['DELETE'])
def delete_meal_food(meal_id, food_id):
    """
    Endpoint para eliminar una relación específica entre comida y alimento usando meal_id y food_id.
    """
    try:
        # Buscar la relación entre comida y alimento usando los dos IDs
        meal_food = MealFood.query.filter_by(meal_id=meal_id, food_id=food_id).first()

        # Validar si existe
        if not meal_food:
            return jsonify({"error": "Relación no encontrada"}), 404

        # Eliminar la relación
        db.session.delete(meal_food)
        db.session.commit()

        # Actualizar los totales de la comida
        # update_meal_totals(meal_id)

        return jsonify({"message": "Relación eliminada correctamente"}), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "Error al eliminar la relación"}), 500


def update_meal_totals(meal_id):
    """
    Recalcula y actualiza los totales de calorías, proteínas, grasas y carbohidratos
    para una comida específica basada en los alimentos asociados.
    """
    # Obtener la comida
    meal = Meal.query.get(meal_id)
    if not meal:
        return

    # Calcular los totales a partir de los alimentos asociados
    meal_foods = MealFood.query.filter_by(meal_id=meal_id).all()

    # total_calories = sum([mf.food.calories * mf.quantity for mf in meal_foods])
    total_calories = sum([mf.food.calories for mf in meal_foods])
    total_proteins = sum([mf.food.proteins for mf in meal_foods])
    total_fats = sum([mf.food.fats for mf in meal_foods])
    total_carbohydrates = sum([mf.food.carbohydrates * mf.quantity for mf in meal_foods])

    # Actualizar los campos de la comida
    meal.total_calories = total_calories
    meal.total_proteins = total_proteins
    meal.total_fats = total_fats
    meal.total_carbohydrates = total_carbohydrates

    # Guardar los cambios en la base de datos
    db.session.commit()