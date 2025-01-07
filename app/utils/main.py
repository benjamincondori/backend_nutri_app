import json
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

from planner import Planner

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app import create_app

from app.models.food import Food
from app.utils.functions import convertir_a_json

MODELO = joblib.load("templates/modelo_momento.pkl")
SCALER = joblib.load("templates/scaler.pkl")
LE_MOMENTO = joblib.load("templates/label_encoder_momento.pkl")
LE_CATEGORY = joblib.load("templates/label_encoder_category.pkl")
DF_FOOD = pd.read_pickle("templates/df_food.pkl")

app = create_app()


#def main():
with app.app_context():

# Codificadores de etiquetas
    le_momento = LabelEncoder()
    le_momento.fit(["desayuno", "almuerzo", "cena"])

    le_category = LabelEncoder()
    le_category.fit(DF_FOOD["category"].unique())


    # Crear instancia del planificador
   # planner = Planner(DF_FOOD, le_momento, le_category)
    planner = Planner()

 
    # Ejemplo de uso
    peso = 70  # en kg
    altura = 170  # en cm
    edad = 30  # en años
    genero = 'Masculino'
    objetivo = 'Perder peso'  # o 'ganar' o 'perder'
    pal = 1.55  # Nivel de actividad física
    dias = 3  # Duración del plan (en días)

    # Calcular las calorías necesarias para el plan completo
    calorias_totales = planner.calories(peso, altura, edad, genero, objetivo, pal, dias)

    # Suponiendo que ya tienes el DataFrame df_food con los alimentos disponibles
    plan_comidas = planner.distribuir_comidas( calorias_totales, dias, objetivo)

    # Convertir el plan de comidas a JSON
    plan_json = convertir_a_json(plan_comidas)

    print(plan_json)

