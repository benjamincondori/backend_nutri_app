import unittest
import pandas as pd
from app.utils.nutrion_model import train_nutrition_model
from sklearn.linear_model import LinearRegression

class TestNutritionModel(unittest.TestCase):

    def test_train_nutrition_model(self):
        # Datos de entrada simulados
        data = pd.DataFrame({
            'age': [25, 30, 35, 40],
            'weight': [60, 70, 80, 90],
            'height': [1.70, 1.75, 1.80, 1.85],
            'activity_level': [1.375, 1.55, 1.725, 1.9],
            'calories': [2000, 2500, 2800, 3000]
        })
        
        X = data[['age', 'weight', 'height', 'activity_level']]  # Características
        y = data['calories']  # Objetivo (calorías)
        
        # Llamar a la función que entrena el modelo
        model = train_nutrition_model(data)

        # Verificar que el modelo es una instancia de LinearRegression
        self.assertIsInstance(model, LinearRegression, "El modelo no es de tipo LinearRegression.")

        # Verificar que el modelo se ha entrenado correctamente (esto puede variar dependiendo del comportamiento esperado)
        self.assertGreater(model.score(X, y), 0, "El modelo no tiene una buena precisión.")
