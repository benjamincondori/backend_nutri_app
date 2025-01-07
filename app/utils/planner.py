import sys
import os
import pandas as pd
import random
import joblib
from sklearn.preprocessing import LabelEncoder
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.models.food import Food
from app.routes.plan import *
from app.routes.meal import save_meal, save_plan_meal

MODELO = joblib.load("templates/modelo_momento.pkl")
SCALER = joblib.load("templates/scaler.pkl")
LE_MOMENTO = joblib.load("templates/label_encoder_momento.pkl")
LE_CATEGORY = joblib.load("templates/label_encoder_category.pkl")
DF_FOOD = pd.read_pickle("templates/df_food.pkl")


class Planner:
    def __init__(self):
        """
        Constructor del Planificador de comidas.

        Args:
            df_food (DataFrame): Datos de alimentos.
            le_momento (LabelEncoder): Codificador de etiquetas para 'Momento'.
            le_category (LabelEncoder): Codificador de etiquetas para 'category'.
        """

        df_food = DF_FOOD
        le_momento = LabelEncoder()
        le_momento.fit(["desayuno", "almuerzo", "cena"])

        le_category = LabelEncoder()
        le_category.fit(DF_FOOD["category"].unique())

        self.df_food = df_food
        self.le_momento = le_momento
        self.le_category = le_category
        self.calories_t = 0

    # 1. Calcular la TMB (Tasa Metabólica Basal)
    def tmb(self, peso, altura, edad, genero, objetivo, PAL):
        """
        Calcula la Tasa Metabólica Basal (TMB) y el Total Daily Energy Expenditure (TDEE).

        Args:
            peso (float): Peso en kg.
            altura (float): Altura en cm.
            edad (int): Edad en años.
            genero (str): Género ('masculino' o 'femenino').
            objetivo (str): Objetivo ('perder peso', 'mantener peso', 'ganar masa muscular').
            PAL (float): Nivel de actividad física (valor de 1.2 a 2.5).

        Returns:
            float: Calorías necesarias para el objetivo.
        """
        if genero == 'Masculino':
            tmb = 10 * peso + 6.25 * altura - 5 * edad + 5
        elif genero == 'Femenino':
            tmb = 10 * peso + 6.25 * altura - 5 * edad - 161
        else:
            raise ValueError("Género no válido. Debe ser 'masculino' o 'femenino'.")

        # Ajuste por nivel de actividad física (PAL)
        tdee = tmb * PAL

        # Ajuste por objetivo
        if objetivo == 'Perder peso':
            tdee -= 500  # Déficit calórico
        elif objetivo == 'Ganar masa muscular':
            tdee += 500  # Superávit calórico
        elif objetivo != 'Mantener peso':
            raise ValueError("Objetivo no válido. Debe ser 'perder peso', 'mantener peso' o 'ganar masa muscular'.")

        return tdee

    # 2. Función para predecir las calorías necesarias para el plan nutricional
    def calories(self, peso, altura, edad, genero, objetivo, PAL, dias):
        """
        Calcula las calorías totales necesarias para el plan nutricional según el TDEE.

        Args:
            peso (float): Peso en kg.
            altura (float): Altura en cm.
            edad (int): Edad en años.
            genero (str): Género ('masculino' o 'femenino').
            objetivo (str): Objetivo ('perder peso', 'mantener peso', 'ganar masa muscular').
            PAL (float): Nivel de actividad física.
            dias (int): Número de días del plan nutricional.

        Returns:
            float: Calorías totales para el plan de días.
        """
        # Calcular el TDEE
        tdee = self.tmb(peso, altura, edad, genero, objetivo, PAL)
        print(f"Calorías necesarias para el plan nutricional por día: {tdee}")

        # Calcular calorías totales para los días del plan
        calorias_totales = tdee * dias
        print(f"Calorías totales para el plan de {dias} días: {calorias_totales}")

        return calorias_totales

    def armar_comida_ajustada(self, momento, calorias_objetivo, proporciones_macros, plan_id):
        """
        Arma una comida ajustada a las calorías objetivo y proporciones de macronutrientes, basándose en la categoría.
        """
        # print(f"\nMomento: {momento}, Calorías objetivo: {calorias_objetivo}")
        print(f"\nMomento: {momento}")
        momento_transformado = self.le_momento.transform([momento])[0]

        # Filtrar alimentos para el momento específico
        df_momento = self.df_food[self.df_food["Momento"] == momento_transformado]

        if df_momento.empty:
            print(f"No hay alimentos disponibles para el momento: {momento}")
            return []

        seleccion = []
        total_calorias = 0
        alimentos_usados = set()

        # Definir categorías de alimentos y sus unidades
        categorias_unidad = {
            "frutas": "unidad",  # Se mide por unidad (manzana, plátano, etc.)
            "huevos": "unidad",  # Se mide por unidad
            "frutos secos": "gramo",  # Se mide por gramos
            "quesos": "gramo",  # Se mide por gramos
            "lacteos": "mililitro",  # Se mide por gramos
            "carnes": "gramo",  # Se mide por gramos
            "pescados": "gramo",  # Se mide por gramos
            "verduras/hortalizas": "gramo",  # Se mide por gramos
            "legumbres": "gramo",  # Se mide por gramos
            "cereales y derivados": "gramo",  # Se mide por gramos
            "grasas": "gramo"  # Se mide por gramos
        }

        while total_calorias < calorias_objetivo * 0.9:
            alimento_seleccionado = df_momento.sample(1).iloc[0]
            food = Food.query.filter_by(name=alimento_seleccionado["name"]).first()

            if alimento_seleccionado["name"] in alimentos_usados:
                continue

            # Cálculo de la cantidad necesaria según las calorías por unidad
            calorias_por_gramo = alimento_seleccionado["calories"] / 100  # Suponiendo que la medida está en 100 gramos
            cantidad_requerida = min(
                (calorias_objetivo - total_calorias) / calorias_por_gramo,
                100  # Limitar a la cantidad original por unidad (suponiendo que se mide en 100 gramos)
            )

            if cantidad_requerida <= 0:
                break

            # Obtener la categoría del alimento
            categoria = food.category

            # Verificar si la categoría tiene una unidad específica (gramos o unidad)
            if categoria in categorias_unidad:
                unidad = food.measure
            else:
                # Si no está en las categorías definidas, usamos la unidad por defecto (gramos)
                unidad = "gramo"

            if unidad == "unidad":
                # Si el alimento está en una categoría de unidad (como frutas), asigna la cantidad a 1
                cantidad_final = 1

            if unidad == None:
                unidad = "gramo"
            else:
                # Si no es una unidad, calcula según los gramos
                if unidad == "gramo":
                    cantidad_final = round(cantidad_requerida, 2)
                elif unidad == "mililitro":
                    cantidad_final = round(cantidad_requerida, 2)  # Para líquidos
                else:
                    cantidad_final = cantidad_requerida  # Si la unidad no se encuentra, tomar el valor por defecto

            # Agregar alimento a la selección
            seleccion.append({
                "alimento": alimento_seleccionado["name"],
                "cantidad": cantidad_final,
                "unidad": unidad
            })
            total_calorias += cantidad_final * calorias_por_gramo
            self.calories_t = total_calorias
            alimentos_usados.add(alimento_seleccionado["name"])

            # Limitar la cantidad de alimentos por comida para mayor simplicidad
            if len(seleccion) >= 5:
                break

        if not seleccion:
            print(f"No se pudieron encontrar alimentos válidos para el momento: {momento}")
        else:

            print(f"Comida armada: {seleccion}, Calorías totales: {total_calorias:.2f}")

        return seleccion

    def distribuir_comidas(self, calorias_totales, dias, objetivo, plan_id):
        calorias_diarias = calorias_totales / dias
        print(f"Calorías diarias para el plan: {calorias_diarias}")

        proporciones_comidas = {
            "desayuno": 0.25,
            "almuerzo": 0.40,
            "cena": 0.35
        }

        macronutrientes = {
            "Perder peso": {"proteinas": 0.40, "grasas": 0.30, "carbohidratos": 0.30},
            "Mantener peso": {"proteinas": 0.30, "grasas": 0.25, "carbohidratos": 0.45},
            "Ganar masa muscular": {"proteinas": 0.35, "grasas": 0.20, "carbohidratos": 0.45}
        }

        if objetivo not in macronutrientes:
            raise ValueError(f"Objetivo '{objetivo}' no es válido.")

        proporciones_macros = macronutrientes[objetivo]
        date = datetime.now()

        plan_comidas = []

        for day in range(dias):
            comidas_dia = {}
            for momento, proporcion_comida in proporciones_comidas.items():
                calorias_objetivo = calorias_diarias * proporcion_comida
                comida = self.armar_comida_ajustada(momento, calorias_objetivo, proporciones_macros, plan_id)
                print(f"----------------------------------")
                print(comida)
                print(f"----------------------------------")

                # registra la comida y los alimentos que pertenecen a ella
                meal = save_meal(objetivo, momento, self.calories_t, comida, plan_id)

                # guarda la relacion de las comidas con el plan (el plan ya se creó)
                # plan_meal= save_plan_meal(meal, plan_id, date, day)
                plan_meal = save_plan_meal(meal, plan_id, date.strftime('%Y-%m-%d %H:%M:%S'), day + 1)

                # date = date.strftime('%Y-%m-%d %H:%M:%S')

                comidas_dia[momento] = comida

            date += timedelta(days=1)
            plan_comidas.append(comidas_dia)

        return plan_comidas

