import joblib

# Cargar el modelo y los objetos necesarios
modelo_momento = joblib.load('templates/modelo_momento.pkl')
scaler = joblib.load('templates/scaler.pkl')
le_momento = joblib.load('templates/label_encoder_momento.pkl')
le_category = joblib.load('templates/label_encoder_category.pkl')

# Ejemplo 2
nuevo_alimento2 = {
   "calories": 256,
    "proteins": 2.7,
    "fats":0.6,
    "carbohydrates": 63.2,
    "category": "frutos secos"
}

X_new2 = [[nuevo_alimento2["calories"], nuevo_alimento2["proteins"], nuevo_alimento2["fats"], nuevo_alimento2["carbohydrates"]]]
X_new2_scaled = scaler.transform(X_new2)

# Hacer la predicción
prediccion_momento2 = modelo_momento.predict(X_new2_scaled)

# Decodificar la predicción
momento_predicho2 = le_momento.inverse_transform(prediccion_momento2)

print(f"El alimento con categoría '{nuevo_alimento2['category']}' debe consumirse en el momento: {momento_predicho2[0]}")
