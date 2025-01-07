from flask import jsonify
import pandas as pd
import google.generativeai as genai
import anthropic
#import openai
import os
from dotenv import load_dotenv
import json

from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from app.database import db
from app.models.food import Food
from app.models.user import User
from app.models.health_profile import HealthProfile

from app.utils.meals import plan_nutricional_ganar_peso_1dia, plan_nutricional_ganar_peso_3dias,plan_nutricional_perder_peso_1dia,plan_nutricional_perder_peso_3dias

API_GEMINI = os.getenv('GEMINI_API_KEY')
#CHATGPT_API_KEY = os.getenv('CHATGPT_API_KEY')
#client = anthropic.Anthropic(api_key='CLAUDE_API_KEY')  
#client = anthropic.Anthropic(api_key='CLAUDE_API_KEY')  


#openai.api_key = CHATGPT_API_KEY


def get_user_health_data(user_id):
    # Lógica para obtener datos del usuario desde la base de datos (por ejemplo)
    health_data_profile = db.session.query(HealthProfile).filter_by(user_id=user_id).first()
    if not health_data_profile:
        return ValueError("datos de usuario no encontrado")
    return {
        "genero": health_data_profile.gender,
        "edad": health_data_profile.age,
        "peso": health_data_profile.weight,
        "altura": health_data_profile.height,
        "restriccion":health_data_profile.health_restrictions
    }


def get_food_data():
    # Obtener los alimentos y sus características (calorías, nutrientes, etc.)
    foods = Food.query.all()
    food_data = [
        {
            "name": food.name,
            # "calories": food.calories,
            # "proteins": food.proteins,
            # "fats": food.fats,
            # "carbohydrates": food.carbohydrates,
        }
        for food in foods
    ]
    return pd.DataFrame(food_data)

def generate_plan_nutritional1(id, number_days, objective):
    if (objective == "Ganar masa muscular" and number_days == 1):
        return jsonify(plan_nutricional_ganar_peso_1dia)
    
    if (objective == "Ganar masa muscular" and number_days == 3):
        return jsonify(plan_nutricional_ganar_peso_3dias)

    if (objective == "Perder peso" and number_days == 1):
        return jsonify(plan_nutricional_perder_peso_1dia)

    if (objective == "Perder peso" and number_days == 3):
        return jsonify(plan_nutricional_perder_peso_3dias)

    return jsonify(plan_nutricional_ganar_peso_1dia)

def generate_plan_nutritional(id, number_days, objective):
    try:
        # Obtener los datos del usuario
        user_data = get_user_health_data(id)
        if not user_data:
            return {"message": "Datos de usuario no encontrados"}, 404
        foods = get_food_data()

        food_json = foods.to_json(orient='records') #orient='records' crea una lista de diccionarios
        json_ejemplo = {
            "dias": [
                {
                    "dia": 1,
                    "comidas": [
                        {"nombre": "nonbre para el desayuno", "tipo_comida": "desayuno", "alimentos": [{"alimento": "Huevos", "cantidad": 2, "unidad": "unidades"}]},
                        {"nombre": "nombre para el Almuerzo", "tipo_comida": "almuerzo", "alimentos": [{"alimento": "Pollo", "cantidad": 150, "unidad": "gramos"}]},
                        {"nombre": "nombre para la cena", "tipo_comida": "cena", "alimentos": [{"alimento": "Salmón", "cantidad": 120, "unidad": "gramos"}]}
                    ]
                }
            ]
        }
        json_ejemplo_str = json.dumps(json_ejemplo, indent=2)
        prompt = f"""Quiero que me generes un plan de comidas para 
                {number_days} días para el objetivo de {objective}, a partir de la 
                siguiente información:

                Edad: {user_data['edad']}
                Peso: {user_data['peso']}
                Altura: {user_data['altura']}
                Género: {user_data['genero']}
                Restricciones dietéticas: {user_data['restriccion']}

                Usa la siguiente lista de alimentos para crear el plan de comidas:
                ```json
                {food_json}
                ```

                El plan de comidas debe tener el siguiente formato JSON:

                ```json
                {json_ejemplo_str}
                ```
                Teniendo en cuenta las restricciones de enfermedades especificadas, 
                Quiero que generes UN SOLO objeto JSON con la estructura dada. No me 
                generes parrafos de texto luego del objeto JSON ni Nota, solo el objeto
                JSON. 

                En cada comida, solo debes listar 1 sola vez un alimento, no repitas, y no 
                ignores los demas datos de cada alimento, como cantidad y unidad. Puede haber
                mas de un 1 alimento por comida, pero no repitas el mismo alimento en la misma
                comida. 
            """
        genai.configure(api_key=API_GEMINI) 
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = None

        # Verificar la respuesta del modelo
        # if response is None:
        #     return {"message": "No se pudo obtener una respuesta del modelo."}, 500
        
        response = model.generate_content(prompt)
        print(response.text)
        
        response_text = response.text.strip()
       
        if response_text.startswith("```json"):
            response_text = response_text[7:] 
        if response_text.endswith("```"):
            response_text = response_text[:-3]

        if not response_text:
            return {"message": "El modelo no generó una respuesta"}, 500

        try:
            response_json = json.loads(response_text)

            #Validación adicional (opcional pero recomendado)
            validate_json(response_json)

            return response_json
        except json.JSONDecodeError as e:
            print(f"Error JSONDecodeError: {e}, Respuesta del modelo:\n{response}")
            return {"message": "Error al procesar la respuesta del modelo"}, 500
      
        except ValueError as e: #Captura otras excepciones de la validación
            print(f"Error validando JSON: {e}, Respuesta del modelo:\n{response}")
            return {"message": "Error al procesar la respuesta del modelo"}, 500
        
    except Exception as e:
        print(f"Error al parsear el JSON: {e}, respuesta del modelo: {response}")
        return {"message": f"Error al generar el plan: {e}"}, 500
  

def validate_json(data):
    """Valida la estructura del JSON recibido para asegurar que cumple con el formato esperado."""
    if not isinstance(data, dict):
        raise ValueError("El JSON de respuesta no es un diccionario.")
    if "dias" not in data or not isinstance(data["dias"], list):
        raise ValueError("El JSON de respuesta no contiene la clave 'dias' o no es una lista.")
    # Agregar más validaciones según la estructura JSON esperada...  Por ejemplo:
    for dia in data["dias"]:
        if "comidas" not in dia or not isinstance(dia["comidas"], list):
            raise ValueError("Un elemento de 'dias' no contiene la clave 'comidas' o no es una lista.")
   

def train_nutrition_model(user_data):
    # Preprocesar los datos del usuario (peso, altura, etc.)
    X = user_data[['age', 'weight', 'height', 'activity_level']]  # Características del usuario
    y = user_data['calories']  # Calorías necesarias

    # Estandarizar los datos
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Entrenar el modelo de regresión lineal
    model = LinearRegression()
    model.fit(X_scaled, y)

    return model

def predict_calories_for_user(user_data, model):
    # Predecir las calorías necesarias para un nuevo usuario
    X_scaled = StandardScaler().fit_transform(user_data[['age', 'weight', 'height', 'activity_level']])
    predicted_calories = model.predict(X_scaled)
    return predicted_calories
