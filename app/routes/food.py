from datetime import datetime
import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv
from flask import Blueprint, jsonify, request

from app.database import db
from app.models.food import Food

food_bp = Blueprint("food", __name__, url_prefix="/api/food")

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración de Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)


@food_bp.route("/foods", methods=["GET"])
def get_all_foods():
    """
    Obtener todos los alimentos
    ---
    tags:
      - Alimentos
    responses:
      200:
        description: Lista de todos los alimentos.
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
                example: "Manzana"
              description:
                type: string
                example: "Fruta fresca y dulce, rica en fibra y vitaminas."
              calories:
                type: float
                example: 52
              proteins:
                type: float
                example: 0.3
              fats:
                type: float
                example: 0.2
              carbohydrates:
                type: float
                example: 14
              image_url:
                type: string
                example: "https://example.com/images/manzana.jpg"
              category:
                type: string
                example: "frutas"
              benefits:
                type: string
                example: "Ayuda a mantener el sistema digestivo saludable."
    """
    foods = Food.query.all()
    result = [
        {
            "id": food.id,
            "name": food.name,
            "description": food.description,
            "calories": food.calories,
            "proteins": food.proteins,
            "fats": food.fats,
            "carbohydrates": food.carbohydrates,
            "image_url": food.image_url,
            "category": food.category,
            "benefits": food.benefits
        }
        for food in foods
    ]
    return jsonify(result), 200


@food_bp.route('/foods/category/<string:category>', methods=['GET'])
def get_foods_by_category(category):
    foods = Food.query.filter_by(category=category).all()
    if not foods:
        return jsonify({"error": "No se encontraron alimentos para la categoría especificada"}), 404

    result = [
        {
            "id": food.id,
            "name": food.name,
            "description": food.description,
            "calories": food.calories,
            "proteins": food.proteins,
            "fats": food.fats,
            "carbohydrates": food.carbohydrates,
            "image_url": food.image_url,
            "category": food.category,
            "benefits": food.benefits
        }
        for food in foods
    ]
    return jsonify(result), 200


@food_bp.route('/foods/<int:id>', methods=['GET'])
def get_food_by_id(id):
    """
    Obtener un alimento por ID
    ---
    tags:
      - Alimentos
    parameters:
      - name: id
        in: path
        required: true
        type: integer
        description: ID del alimento.
        example: 1
    responses:
      200:
        description: Detalles del alimento especificado.
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: "Manzana"
            description:
              type: string
              example: "Fruta fresca y dulce, rica en fibra y vitaminas."
            calories:
              type: float
              example: 52
            proteins:
              type: float
              example: 0.3
            fats:
              type: float
              example: 0.2
            carbohydrates:
              type: float
              example: 14
            image_url:
              type: string
              example: "https://example.com/images/manzana.jpg"
            category:
              type: string
              example: "frutas"
            benefits:
              type: string
              example: "Ayuda a mantener el sistema digestivo saludable."
      404:
        description: Alimento no encontrado.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Alimento no encontrado."
    """
    food = Food.query.get(id)
    if not food:
        return jsonify({"error": "Alimento no encontrado"}), 404

    result = {
        "id": food.id,
        "name": food.name,
        "description": food.description,
        "calories": food.calories,
        "proteins": food.proteins,
        "fats": food.fats,
        "carbohydrates": food.carbohydrates,
        "image_url": food.image_url,
        "category": food.category,
        "benefits": food.benefits
    }
    return jsonify(result), 200


@food_bp.route("/foods", methods=["POST"])
def add_food():
    """
    Agregar un nuevo alimento
    ---
    tags:
      - Alimentos
    requestBody:
      required: true
      content:
        multipart/form-data:
          schema:
            type: object
            properties:
              name:
                type: string
                example: "Manzana"
              description:
                type: string
                example: "Fruta fresca y dulce, rica en fibra y vitaminas."
              calories:
                type: float
                example: 52
              proteins:
                type: float
                example: 0.3
              fats:
                type: float
                example: 0.2
              carbohydrates:
                type: float
                example: 14
              image:
                type: string
                format: binary
              category:
                type: string
                example: "frutas"
              benefits:
                type: string
                example: "Ayuda a mantener el sistema digestivo saludable."
    responses:
      201:
        description: Alimento creado exitosamente.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Alimento creado exitosamente."
            food:
              type: object
      400:
        description: Error en los datos enviados.
    """
    try:
        name = request.form.get("name")
        description = request.form.get("description")
        calories = request.form.get("calories", type=float)
        proteins = request.form.get("proteins", type=float)
        fats = request.form.get("fats", type=float)
        carbohydrates = request.form.get("carbohydrates", type=float)
        category = request.form.get("category")
        benefits = request.form.get("benefits")
        image = request.files.get("image")

        if not all([name, description, category, proteins, fats, carbohydrates, calories, benefits, image]):
            return jsonify({"error": "Los campos obligatorios son name, description y category"}), 400

        # Subir imagen a Cloudinary
        image_url = None
        if image:
            upload_result = cloudinary.uploader.upload(image, folder=os.getenv("CLOUDINARY_FOLDER"))
            image_url = upload_result.get("secure_url")

        # Crear nuevo alimento
        new_food = Food(
            name=name,
            description=description,
            calories=calories,
            proteins=proteins,
            fats=fats,
            carbohydrates=carbohydrates,
            image_url=image_url,
            category=category,
            benefits=benefits
        )
        db.session.add(new_food)
        db.session.commit()

        return jsonify({
            "message": "Alimento creado exitosamente.",
            "food": {
                "id": new_food.id,
                "name": new_food.name,
                "description": new_food.description,
                "calories": new_food.calories,
                "proteins": new_food.proteins,
                "fats": new_food.fats,
                "carbohydrates": new_food.carbohydrates,
                "image_url": new_food.image_url,
                "category": new_food.category,
                "benefits": new_food.benefits
            }
        }), 201

    except Exception as e:
        return jsonify({"error": f"Ocurrió un error al agregar el alimento: {str(e)}"}), 500


@food_bp.route("/foods/<int:id>", methods=["PUT"])
def update_food(id):
    """
    Actualizar un alimento existente
    ---
    tags:
      - Alimentos
    parameters:
      - name: id
        in: path
        required: true
        type: integer
        description: ID del alimento a actualizar.
    requestBody:
      required: true
      content:
        multipart/form-data:
          schema:
            type: object
            properties:
              name:
                type: string
                example: "Manzana"
              description:
                type: string
                example: "Fruta fresca y dulce, rica en fibra y vitaminas."
              calories:
                type: float
                example: 52
              proteins:
                type: float
                example: 0.3
              fats:
                type: float
                example: 0.2
              carbohydrates:
                type: float
                example: 14
              image:
                type: string
                format: binary
              category:
                type: string
                example: "frutas"
              benefits:
                type: string
                example: "Ayuda a mantener el sistema digestivo saludable."
    responses:
      200:
        description: Alimento actualizado exitosamente.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Alimento actualizado exitosamente."
            food:
              type: object
      404:
        description: Alimento no encontrado.
    """
    try:
        food = Food.query.get(id)
        if not food:
            return jsonify({"error": "Alimento no encontrado"}), 404

        # Obtener los datos del formulario
        name = request.form.get("name")
        description = request.form.get("description")
        calories = request.form.get("calories", type=float)
        proteins = request.form.get("proteins", type=float)
        fats = request.form.get("fats", type=float)
        carbohydrates = request.form.get("carbohydrates", type=float)
        category = request.form.get("category")
        benefits = request.form.get("benefits")
        image = request.files.get("image")

        # Actualizar los campos del alimento
        if name:
            food.name = name
        if description:
            food.description = description
        if calories is not None:
            food.calories = calories
        if proteins is not None:
            food.proteins = proteins
        if fats is not None:
            food.fats = fats
        if carbohydrates is not None:
            food.carbohydrates = carbohydrates
        if category:
            food.category = category
        if benefits:
            food.benefits = benefits

        # Si se proporciona una nueva imagen, cargarla a Cloudinary
        if image:
            upload_result = cloudinary.uploader.upload(image, folder=os.getenv("CLOUDINARY_FOLDER"))
            food.image_url = upload_result.get("secure_url")

        # Guardar los cambios en la base de datos
        db.session.commit()

        return jsonify({
            "message": "Alimento actualizado exitosamente.",
            "food": {
                "id": food.id,
                "name": food.name,
                "description": food.description,
                "calories": food.calories,
                "proteins": food.proteins,
                "fats": food.fats,
                "carbohydrates": food.carbohydrates,
                "image_url": food.image_url,
                "category": food.category,
                "benefits": food.benefits
            }
        }), 200

    except Exception as e:
        return jsonify({"error": f"Ocurri\u00f3 un error al actualizar el alimento: {str(e)}"}), 500
